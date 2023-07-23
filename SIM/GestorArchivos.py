from qgis.core import *
import numpy as np
import os

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

    def save_Layers(self, layers:list, path:str, data:dict) -> None:
        if data["GeoJSON"]["SAVE"] == True:
            path_g = path + "GeoJSON/"
            if not os.path.exists(path_g):
                os.makedirs(path_g)
                os.chmod(path_g, 0o777)
            else:
                print("La carpeta ya existe")
            for layer in layers:
                output = path_g + layer.name()+".geojson"
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                 output,
                                                                 "UTF-8",
                                                                 layer.crs(),
                                                                 driverName="GeoJSON")
                if result[1] == "":
                    print(f"GEOJSON - La capa {layer.name()} exportada con éxito")
                    if data["GeoJSON"]["OPEN"] == True:
                        lyr = QgsVectorLayer(output,layer.name(),"ogr")
                        QgsProject.instance().addMapLayer(lyr)
                else:
                    print("GEOJSON - Hubo un error al exportar la capa {layer.name()}: ", result[1])

        if data["Spatialite"]["SAVE"] == True:
            path_s = path + "Spatialite/"
            if not os.path.exists(path_s):
                os.makedirs(path_s)
                os.chmod(path_s, 0o777)
            else:
                print("La carpeta ya existe")

            for layer in layers:
                output = path_s + layer.name()+".sqlite"
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                 output,
                                                                 "UTF-8",
                                                                 layer.crs(),
                                                                 driverName="SQLite",
                                                                 datasourceOptions=["SPATIALITE=YES"])
                if result[1] == "":
                    print(f"SPATIALITE - La capa {layer.name()} exportada con éxito")
                    if data["Spatialite"]["OPEN"] == True:
                        lyr = QgsVectorLayer(output,layer.name(),"ogr")
                        QgsProject.instance().addMapLayer(lyr)
                else:
                    print("SPATIALITE - Hubo un error al exportar la capa {layer.name()}: ", result[1])

        if data["HD"]["SAVE"] == True:
            path_hd = path + "Shapefiles/"
            if not os.path.exists(path_hd):
                os.makedirs(path_hd)
                os.chmod(path_hd, 0o777)
            else:
                print("La carpeta ya existe")

            for layer in layers:
                output = path_hd + layer.name() + ".shp"
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                 output,
                                                                 "UTF-8",
                                                                 layer.crs(),
                                                                 driverName="ESRI Shapefile")
                layer.saveNamedStyle(path_hd + layer.name() +".qml")
                if result[1] == "":
                    print(f"SHAPEFILE - La capa {layer.name()} exportada con éxito")
                    if data["HD"]["OPEN"] == True:
                        lyr = QgsVectorLayer(output,layer.name(),"ogr")
                        QgsProject.instance().addMapLayer(lyr)

                else:
                    print("SHAPEFILE - Hubo un error al exportar la capa {layer.name()}: ", result[1])

        if data["Memory"] == False:
            self.destroy_layers(layers)

