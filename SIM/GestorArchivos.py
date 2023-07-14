from qgis.core import *
import numpy as np

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
