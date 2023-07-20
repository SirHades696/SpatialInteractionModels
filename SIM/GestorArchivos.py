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

    def save_data(self, layers:list, path:str, data:dict) -> None:
        if data["GeoJSON"] == True:
            path_g = path + "GeoJSON/"
            if not os.path.exists(path_g):
                os.makedirs(path_g)
                os.chmod(path_g, 0o777)
            else:
                print("La carpeta ya existe")
            for layer in layers:
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                 path_g + layer.name()+".geojson",
                                                                 "UTF-8",
                                                                 layer.crs(),
                                                                 driverName="GeoJSON")
                if result[1] == "":
                    print(f"GEOJSON - La capa {layer.name()} exportada con éxito")
                else:
                    print("GEOJSON - Hubo un error al exportar la capa {layer.name()}: ", result[1])

        if data["Spatialite"] == True:
            path_s = path + "Spatialite/"
            if not os.path.exists(path_s):
                os.makedirs(path_s)
                os.chmod(path_s, 0o777)
            else:
                print("La carpeta ya existe")

            for layer in layers:
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                 path_s + layer.name()+".sqlite",
                                                                 "UTF-8",
                                                                 layer.crs(),
                                                                 driverName="SQLite",
                                                                 datasourceOptions=["SPATIALITE=YES"])
                if result[1] == "":
                    print(f"SPATIALITE - La capa {layer.name()} exportada con éxito")
                else:
                    print("SPATIALITE - Hubo un error al exportar la capa {layer.name()}: ", result[1])

        if data["HD"] == True:
            path_hd = path + "Shapefiles/"
            if not os.path.exists(path_hd):
                os.makedirs(path_hd)
                os.chmod(path_hd, 0o777)
            else:
                print("La carpeta ya existe")

            for layer in layers:
                result = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                                 path_hd + layer.name() + ".shp",
                                                                 "UTF-8",
                                                                 layer.crs(),
                                                                 driverName="ESRI Shapefile")
                layer.saveNamedStyle(path_hd + layer.name() +".qml")
                if result[1] == "":
                    print(f"SHAPEFILE - La capa {layer.name()} exportada con éxito")
                else:
                    print("SHAPEFILE - Hubo un error al exportar la capa {layer.name()}: ", result[1])
