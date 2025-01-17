from qgis.core import * #type:ignore
import numpy as np
import os
import processing #type:ignore
from osgeo import ogr

class GestorArchivos:

    def clone_layer(self, layer:QgsVectorLayer) -> QgsVectorLayer:
        feats = [feat for feat in layer.getFeatures()] # all feats
        espg = layer.crs().authid() #ESPG:4326 for example
        geometry = QgsWkbTypes.displayString(layer.wkbType()) # for example Polygon, Point, MultiPolygon
        mem_layer = QgsVectorLayer(geometry+"?crs=" + espg, layer.name(), "memory")
        mem_layer_data = mem_layer.dataProvider()
        attr = layer.dataProvider().fields().toList()
        mem_layer_data.addAttributes(attr)
        mem_layer.updateFields()
        mem_layer_data.addFeatures(feats)

        return mem_layer

    def destroy_layers(self, layers:list) -> None:
        for layer in layers:
            QgsProject.instance().removeMapLayer(layer)

    def read_csv_matrix(self, path:str) -> np.ndarray:
        matrix = np.loadtxt(path, delimiter=",", dtype=float)
        return matrix

    def save_Layers(self, layers:list, path:str, data:dict, prefix:str) -> None:
        root = QgsProject.instance().layerTreeRoot()
        if data["GeoJSON"]["SAVE"] == True:
            path_g = path + "GeoJSON/" 
            if not os.path.exists(path_g):
                os.makedirs(path_g)
                os.chmod(path_g, 0o777)
            else:
                print("La carpeta ya existe")
            ly_path = []
            for layer in layers:
                output = path_g + prefix + "_" + layer.name()+".geojson"
                ly_path.append(output)
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                output,
                                                                "UTF-8",
                                                                layer.crs(),
                                                                driverName="GeoJSON")
                if result[1] == "":
                    print(f"GEOJSON - La capa {layer.name()} exportada con éxito")
                else:
                    print("GEOJSON - Hubo un error al exportar la capa {layer.name()}: ", result[1])
            
            if data["GeoJSON"]["OPEN"] == True:
                group = root.addGroup("MIE_" + prefix + "_GeoJSON")
                for layer in ly_path:
                    name = layer.split("/")[-1].split(".geojson")[0]
                    lyr = QgsVectorLayer(layer,name,"ogr")
                    QgsProject.instance().addMapLayer(lyr,False)
                    group.addLayer(lyr)

        if data["Spatialite"]["SAVE"] == True:
            path_s = path + "Spatialite/"
            if not os.path.exists(path_s):
                os.makedirs(path_s)
                os.chmod(path_s, 0o777)
            else:
                print("La carpeta ya existe")

            ly_path = []
            for layer in layers:
                output = path_s + prefix + "_" + layer.name()+".sqlite"
                ly_path.append(output)
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                output,
                                                                "UTF-8",
                                                                layer.crs(),
                                                                driverName="SQLite",
                                                                datasourceOptions=["SPATIALITE=YES"])
                if result[1] == "":
                    print(f"SPATIALITE - La capa {layer.name()} exportada con éxito")
                else:
                    print("SPATIALITE - Hubo un error al exportar la capa {layer.name()}: ", result[1])
            
            if data["Spatialite"]["OPEN"] == True:
                group = root.addGroup("MIE_" + prefix + "_Spatialite")
                for layer in ly_path:
                    name = layer.split("/")[-1].split(".sqlite")[0]
                    lyr = QgsVectorLayer(layer, name,"ogr")
                    QgsProject.instance().addMapLayer(lyr, False)
                    group.addLayer(lyr)

        if data["HD"]["SAVE"] == True:
            path_hd = path + "Shapefiles/"
            if not os.path.exists(path_hd):
                os.makedirs(path_hd)
                os.chmod(path_hd, 0o777)
            else:
                print("La carpeta ya existe")
            ly_path = []
            for layer in layers:
                output = path_hd + prefix + "_" + layer.name() + ".shp"
                ly_path.append(output)
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                output,
                                                                "UTF-8",
                                                                layer.crs(),
                                                                driverName="ESRI Shapefile")
                layer.saveNamedStyle(path_hd + prefix + "_" + layer.name() +".qml")
                if result[1] == "":
                    print(f"SHAPEFILE - La capa {layer.name()} exportada con éxito")
                else:
                    print("SHAPEFILE - Hubo un error al exportar la capa {layer.name()}: ", result[1])
            
            if data["HD"]["OPEN"] == True:
                group = root.addGroup("MIE_" + prefix + "_SHP")
                for layer in ly_path:
                    name = layer.split("/")[-1].split(".shp")[0]
                    lyr = QgsVectorLayer(layer, name,"ogr")
                    QgsProject.instance().addMapLayer(lyr, False)
                    group.addLayer(lyr)
                    
        if data["Memory"] == False:
            self.destroy_layers(layers)

        if data["Geopackage"]["SAVE"] == True:
            path_gp = path + "Geopackage/"
            if not os.path.exists(path_gp):
                os.makedirs(path_gp)
                os.chmod(path_gp, 0o777)

            aux = {
                    "LAYERS":layers,
                    "OUTPUT":path_gp + prefix + "_" + "MIE.gpkg",
                    "OVERWRITE":False,
                    "SAVE_STYLES":True,
                    "SAVE_METADATA":True,
                    "SELECTED_FEATURES_ONLY":False
                    }
            out = processing.run("native:package",aux)

            if data["Geopackage"]["OPEN"] == True:
                conn = ogr.Open(out["OUTPUT"])
                group = root.addGroup("MIE_" + prefix + "_Geopkg")
                for i in conn:
                    ly = QgsVectorLayer(f"{out['OUTPUT']}|layername={i.GetName()}", i.GetName(), 'ogr')
                    QgsProject.instance().addMapLayer(ly, False)
                    group.addLayer(ly)

    def delete_dup(self, layer:QgsVectorLayer, field:str):
        if not layer.isEditable():
            layer.startEditing()
        atributos_vistos = set()
        duplicados = []
        for feature in layer.getFeatures():
            atributos = tuple(feature[field])
            if atributos in atributos_vistos:
                duplicados.append(feature.id())
            else:
                atributos_vistos.add(atributos)
        if duplicados:
            layer.deleteFeatures(duplicados)
        layer.commitChanges()