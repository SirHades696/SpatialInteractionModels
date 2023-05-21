from qgis.core import *
import unittest
from qgis.core import QgsVectorLayer, QgsFeatureRequest

class TestVectorLayer(unittest.TestCase):
    def test_print_attribute_values(self):
        shapefile_path = "/home/hades/Documentos/Datos 2SFCA/UTM/Manzanas_UTM.shp"
        layer_name = "Manzanas_UTM"
        attribute_name = "POB65_MAS"

        layer = QgsVectorLayer(shapefile_path, layer_name, "ogr")
        self.assertTrue(layer.isValid(), "La capa no es válida")

        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        features = list(layer.getFeatures(request))
        self.assertGreater(len(features), 0, "No se encontraron características en la capa")

        for feature in features:
            attribute_value = feature[attribute_name]
            self.assertIsNotNone(attribute_value, "El valor del atributo es nulo")
            #print(attribute_value)

if __name__ == '__main__':
    qgs = QgsApplication([], False)
    QgsApplication.initQgis()
    unittest.main()

