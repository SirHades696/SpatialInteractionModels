
from Capas import Capas
from GestorArchivos import GestorArchivos
from Estadisticas import Estadisticas

from qgis.core import *

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
        "RESTR" - Identifica la restricción que se va a utilizar: 0 - Restriccion en el origen, 1 - restriccion en el destino, 3 - Doblemente Restr
        "VAL_REST": { - Hace referencia a los parametros necesarios para cada restriccion
            "R_ORIG": { - Hace referencia a la restriccion en el origen
                "OPTION": - Filtro para la restriccion, 0 - Mayor que, 1 - Menor que, 2 - Rango
                "VALUE": [] - Valor o valores de restriccion para el origen en forma de lista, son distancias
                 }
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
        }
        """
        self.origin = params["ORIGIN"]
        self.id_origin = params["ID_ORI"]
        self.destination = params["DEST"]
        self.var_origin = params["VAR_ORI"]
        self.id_dest = params["ID_DEST"]
        self.var_dest = params["VAR_DEST"]
        self.unit = params["UNIT"]
        self.val_rest = params["VAL_REST"]
        self.friction_distance = params["FRICTION_DISTANCE"]

    def run(self):
        gestor = GestorArchivos()
        capas = Capas()
        estadisticas = Estadisticas()

        #Clonando los archivos de entrada
        origin_clon = gestor.clone_layer(self.origin)
        destination_clon = gestor.clone_layer(self.destination)

        # calcula los centroides del archivo de origen (poligonos)
        origin_centroids = capas.centroid(origin_clon)

        #Calculando la matriz de distancia
        matrix = estadisticas.distanceMatrix(origin_centroids,destination_clon,self.unit)

        # Extracción de la oferta/demanda y los IDs
        origins = estadisticas.extract_data(origin_clon,self.var_origin)
        dests = estadisticas.extract_data(destination_clon,self.var_dest)
        id_origins = estadisticas.extract_data(origin_clon, self.id_origin)
        id_dests = estadisticas.extract_data(destination_clon, self.id_dest)

        # Construcción del dict que contiene los valores extraídos de la oferta/demanda y IDs
        values_OD = {
                "ORIGIN": origins,
                "ID_ORI": id_origins,
                "DEST": dests,
                "ID_DEST": id_dests,
                "FD": self.friction_distance
                }

        values, values_oi, oi = estadisticas.origin_restriction(matrix,self.val_rest, values_OD)

        data_layers = {
                "ORIGIN":origin_centroids,
                "DEST":destination_clon
                }

        capas.add_index(origin_clon,oi)
        capas.thematic_polygons(origin_clon,"OI_SUM")

        for_lines, or_list = capas.features_selector_OR(data_layers,values, self.id_origin, self.id_dest)
        layers = capas.create_lines_RO(for_lines, values_oi, self.id_origin, self.id_dest)

        layer_RO = capas.merge_layers(layers, "Lineas_RO")
        layer_RO_p = capas.merge_layers(or_list, "Puntos_RO")
        capas.thematic_lines(layer_RO, "OI_SUM")

        QgsProject.instance().addMapLayer(destination_clon)

        capas.thematic_points(layer_RO_p,"ORI")
        capas.thematic_points(destination_clon,"DEST")

        gestor.destroy_layers(layers)
        gestor.destroy_layers(or_list)






