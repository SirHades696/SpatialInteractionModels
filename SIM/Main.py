import tempfile
from datetime import datetime

from Capas import Capas
from Estadisticas import Estadisticas
from GestorArchivos import GestorArchivos
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import iface
from Reportes import Reportes

import numpy as np


class Main:
    def __init__(self, params:dict) -> None:
        """
        Metodo constructor que se encarga de recibir los los parametros necesarios para ejecutar los SIM (MIE).

        :param params: Recibe un dicccionario que contiene las variables necesarias para la ejecución del modelo
        La estructura es la siguiente:
        {
        "ORIGIN": - Hace referencia al archivo vectorial de origenes (poligonos)
        "ID_ORI": - Hace referencia al ID o identificador unico del archivo de origenes
        "VAR_ORI": - Hace referencia al atributo del archivo de origenes que identifica a la demanda
        "DEST": - Hace referencia al archivo vectorial de destinos (puntons)
        "ID_DEST": - Hace referrencia al ID o identificador unico del archivo de destino
        "VAR_DEST": - Hace referencia al atributo del archivo de destinos que identifica la oferta
        "UNIT": - Unidades de distancia en las que se evaluara la matriz de distancias: 0 - metros, 1 - kilometros, 2 - millas, 3 - pies, 4 - yardas
        "RESTR" - Identifica la restricción que se va a utilizar: 0 - Restriccion en el origen, 1 - restriccion en el destino, 2 - Doblemente Restr
        "VAL_REST": { - Hace referencia a los parametros necesarios para cada restriccion
            "R_ORIG": { - Hace referencia a la restriccion en el origen
                "OPTION": - Filtro para la restriccion, 0 - Mayor que, 1 - Menor que, 2 - Rango
                "VALUE": [] - Valor o valores de restriccion para el origen en forma de lista, son distancias
            },
            "R_DEST": { - Hace referencia a la restriccion en el destino
                "OPTION": Filtro para la restriccion, 0 - Mayor que, 1 - Menor que, 2 - Rango
                "VALUE": [] - Valor o valores de restriccion para el destino en forma de lista, son flujos
                }- Valor de retriccion para el destino, son flujos
            "D_REST":{ - Hace referencia a los doblemente restrictivos
                "RORIG": {
                    "OPTION": Filtro para la restriccion, 0 - Mayor que, 1 - Menor que, 2 - Rango
                    "VALUE": [] - Valor o valores de restriccion para el origen en forma de lista, son distancias
                    }
                "RDEST": {
                    "OPTION": Filtro para la restriccion, 0 - Mayor que, 1 - Menor que, 2 - Rango
                    "VALUE": [] - Valor o valores de restriccion para el destino en forma de lista, son flujos
                    }
                }
            },
        "FRICTION_DISTANCE": - Hace referencia al parametro fricción de la distancia
        "OUTPUT": - Hace referencia a la ruta de almacenamiento
        "EXPORTS": { - Permite guardar las capas en diferentes formatos, con las opciones de solo guardar o guardar y cargar automaticamente
                "GeoJSON": {"SAVE":False, "OPEN":False},
                "HD": {"SAVE":False, "OPEN":False},
                "Spatialite": {"SAVE":False, "OPEN":False},
                "Memory": True
                },
        "SAVE": { - Guarda las estadistiscas en hojas de calculo con extension XLS u ODS
            "XLS":False,
            "ODS":False
            }
        }
        """
        self.params = params
        self.origin = params["ORIGIN"]
        self.id_origin = params["ID_ORI"]
        self.destination = params["DEST"]
        self.var_origin = params["VAR_ORI"]
        self.id_dest = params["ID_DEST"]
        self.var_dest = params["VAR_DEST"]
        self.unit = params["UNIT"]
        self.val_rest = params["VAL_REST"]
        self.friction_distance = params["FRICTION_DISTANCE"]
        self.output = params["OUTPUT"]

    def run(self):
        if self.params["PREFIJO"]:
            aux_pref = self.params["PREFIJO"] + "_MIE"
        else:
            fecha = datetime.now()
            aux = fecha.strftime("%Y%m%d%H%M%S")
            self.params["PREFIJO"] = aux
            aux_pref = "MIE_" + self.params["PREFIJO"]
            
        gestor = GestorArchivos()
        capas = Capas()
        estadisticas = Estadisticas()
        # Messager Bar
        messageBar = iface.messageBar()
        messageBar.clearWidgets()
        progressBar = QProgressBar()
        progressBar.setMaximum(100)
        
        # adding widget
        messageBar.pushWidget(progressBar, Qgis.Info) #type:ignore

        #Clonando los archivos de entrada
        origin_clone = gestor.clone_layer(self.origin)
        destination_clone = gestor.clone_layer(self.destination)
        destination_clone.setName(destination_clone.name()+"_RO")

        progressBar.setValue(10)
        #Validando que el origen cuente unicamente con valores mayores a 0
        lys = capas.layer_filter(origin_clone,self.var_origin)
        origin_clone = lys[0]
        origin_SinDemanda = lys[1]

        flag = False
        if origin_clone.geometryType() == 2: #Polygon
            # calcula los centroides del archivo de origen (poligonos)
            origin_centroids = capas.centroid(origin_clone)
            flag = True
        else:
            origin_centroids = origin_clone

        progressBar.setValue(20)

        #Calculando la matriz de distancia
        matrix = estadisticas.distanceMatrix(origin_centroids,destination_clone,self.unit)

        # Extracción de la oferta/demanda y los IDs
        origins = estadisticas.extract_data(origin_clone,self.var_origin)
        dests = estadisticas.extract_data(destination_clone,self.var_dest)
        id_origins = estadisticas.extract_data(origin_clone, self.id_origin)
        id_dests = estadisticas.extract_data(destination_clone, self.id_dest)
        
        

        progressBar.setValue(40)
        # Construcción del dict que contiene los valores extraídos de la oferta/demanda y IDs
        values_OD = {
                "ORIGIN": origins,
                "ID_ORI": id_origins,
                "DEST": dests,
                "ID_DEST": id_dests,
                "FD": self.friction_distance
                }

        # -------------------- General process finished
        if self.params["RESTR"] == 0:
            values, values_oi, oi, oi_n = estadisticas.origin_restriction(matrix,self.val_rest, values_OD)
            data_layers = {
                "ORIGIN":origin_centroids,
                "DEST":destination_clone
                }
            
            capas.add_index(destination_clone,oi, "OI_SUM")
            capas.add_index(destination_clone, oi_n, "OI_SUM_N")
            
            origin_n = estadisticas.normalize(np.array(origins))
            capas.add_index(origin_clone,origin_n,self.var_origin + "_N")
            
            progressBar.setValue(50)

            for_lines, or_list = capas.features_selector_OR(data_layers,values, self.id_origin, self.id_dest,0)
            layer_RO_p = capas.merge_layers(or_list, "Centroides_evaluados")
            
            thematic_layers = []
            if self.params["LINES"] is True:
                try: 
                    with tempfile.TemporaryDirectory() as dir:
                        temp_path = dir + "/"
                        layers = capas.create_lines_RO(for_lines, values_oi, self.id_origin, self.id_dest, temp_path,0)
                        layer_RO = capas.merge_layers(layers, "Lineas_conectividad")
                except Exception as e:
                    pass
                capas.thematic_lines(layer_RO, "OI_SUM_N")
                thematic_layers.append(layer_RO_p)
                thematic_layers.append(layer_RO)    
            
            capas.thematic_points(destination_clone,"",1,"OI_SUM_N")
            
            progressBar.setValue(80)

            progressBar.setValue(90)
            thematic_layers = [destination_clone] + thematic_layers + [origin_SinDemanda, origin_clone]
            if flag == False:
                capas.thematic_points(origin_clone, "ORI", 1, self.var_origin + "_N")
                capas.thematic_points(destination_clone,"",1 ,"OI_SUM_N")
                hmap = destination_clone.clone()
                hmap.setName(destination_clone.name()+"_hmap")
                capas.thematic_points(hmap,"",2,"OI_SUM_N")
                thematic_layers.append(hmap)
                capas.thematic_points(origin_SinDemanda,"SinDemanda",0,"")
            else:
                hmap = destination_clone.clone()
                hmap.setName(destination_clone.name()+"_hmap")
                capas.thematic_points(hmap,"",2,"OI_SUM_N")
                thematic_layers.append(hmap)
                capas.thematic_polygons(origin_SinDemanda,"",1)
                capas.thematic_polygons(origin_clone, self.var_origin + "_N",0)
                
            if self.params["EXPORTS"]["Memory"] == True:
                root = QgsProject.instance().layerTreeRoot()
                group = root.addGroup(aux_pref)
                for i, layer in enumerate(thematic_layers):
                    group.insertLayer(i,layer)

            gestor.save_Layers(thematic_layers,self.output,self.params["EXPORTS"], self.params["PREFIJO"])
            # instancia de los reportes
            Reportes(values, values_oi, self.params)
            if self.params["LINES"] is True:
                gestor.destroy_layers(layers)
            gestor.destroy_layers(or_list)
            
        #------ dest restriction
        elif self.params["RESTR"] == 1:
            progressBar.setValue(60)
            values, values_dj, dj = estadisticas.dest_restriction(matrix, self.val_rest, values_OD)
            capas.add_index(destination_clone,dj, "DJ_SUM")
            vlayer = destination_clone.clone()
            vlayer.setName(destination_clone.name()+"_hmap")
            QgsProject.instance().addMapLayer(vlayer,False)
            progressBar.setValue(70)
                
            layers = [origin_SinDemanda, origin_clone, destination_clone, vlayer]
            
            capas.thematic_points(destination_clone,"",1,"DJ_SUM")
            capas.thematic_points(vlayer,"",2,"DJ_SUM")
            
            if flag:
                capas.thematic_polygons(origin_clone,"",2)
                capas.thematic_polygons(origin_SinDemanda,"",1)
            else:
                capas.thematic_points(origin_clone,"ORI",1,self.var_origin)
                capas.thematic_points(origin_SinDemanda,"SinDemanda",0,"")
                
            if self.params["EXPORTS"]["Memory"] == True:
                root = QgsProject.instance().layerTreeRoot()
                group = root.addGroup(aux_pref)
                for i,layer in enumerate(layers):
                    group.insertLayer(i,layer)
                    
            gestor.save_Layers(layers,self.output,self.params["EXPORTS"], self.params["PREFIJO"])
            # instancia de los reportes   
            Reportes(values, values_dj, self.params)
        elif self.params["RESTR"] == 2:
            pass

        messageBar.clearWidgets()
        messageBar.pushMessage("Info","Se completo la ejecución...",level=Qgis.Success) #type:ignore
