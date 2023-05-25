import processing
from qgis.core import *
import random
from PyQt5.QtGui import *

try:
    from qgis.core import QVariant
except ImportError:
    try:
        from PyQt5.QtCore import QVariant
    except ImportError:
        print("Error")

class Capas:

    def centroid(self, layer:object) -> object:
        params = {
                "INPUT":layer,
                "ALL_PARTS": True,
                "OUTPUT": "memory:"
                }
        output_layer = processing.run("native:centroids", params)
        return output_layer['OUTPUT']

    def features_selector_OR(self, layers:dict, values:dict, id_ori: str, id_dest:str) -> list:
        origin = layers['ORIGIN']
        dest = layers['DEST']

        origin_fields = origin.fields()
        dest_fields = dest.fields()

        origin_list = []
        dest_list = []
        # For origins
        for field in origin_fields:
            if field.name() == id_ori:
                for i in range(0,len(values)):
                    origin.removeSelection()
                    if field.type() == 7 or field.type() == 10: # for strings
                        expr = f"\"{id_ori}\"=\'{values[str(i)]['ORI']}\'"
                    else:
                        expr = f"\"{id_ori}\"={values[str(i)]['ORI']}"
                    data = {
                            "INPUT":origin,
                            "EXPRESSION":expr,
                            "METHOD":1
                            }
                    selected_features = processing.run("qgis:selectbyexpression",data)
                    data2 = {
                            "INPUT":selected_features["OUTPUT"],
                            "OUTPUT":"memory:"+str(values[str(i)]['ORI'])}
                    saved = processing.run("native:saveselectedfeatures",data2)
                    origin_list.append(saved["OUTPUT"])
                    #QgsProject.instance().addMapLayer(saved["OUTPUT"])

        # for destinations
        for field in dest_fields:
            if field.name() == id_dest:
                for i in range(0,len(values)):
                    dest.removeSelection()
                    selected_features = {}
                    for j in range(0, len(values[str(i)]["DEST"])):
                        if field.type() == 7 or field.type() == 10: # for strings
                            expr = f"\"{id_dest}\"=\'{values[str(i)]['DEST'][j]}\'"
                        else:
                            expr = f"\"{id_dest}\"={values[str(i)]['DEST'][j]}"
                        data = {
                                "INPUT":dest,
                                "EXPRESSION":expr,
                                "METHOD":1
                                }
                        selected_features = processing.run("qgis:selectbyexpression",data)
                    data2 = {
                            "INPUT":selected_features["OUTPUT"],
                            "OUTPUT":"memory:"+dest.name()+"_"+str(i+1)}
                    saved = processing.run("native:saveselectedfeatures",data2)
                    dest_list.append(saved["OUTPUT"])
                    #QgsProject.instance().addMapLayer(saved["OUTPUT"])

        # Matrix with Origins and Dest (filters)
        matrix_OD = [list(par) for par in zip(origin_list, dest_list)]
        return matrix_OD

    def create_lines_RO(self,matrix_OD:list, values_oi:dict, id_ori: str, id_dest:str) -> list:
        espg = matrix_OD[0][0].crs().authid()
        lines_layers_name = []
        for i in range(len(matrix_OD)):
            origin_features = matrix_OD[i][0].getFeatures()
            destination_features = matrix_OD[i][1].getFeatures()
            index_O = matrix_OD[i][0].fields().indexFromName(id_ori)
            index_D = matrix_OD[i][1].fields().indexFromName(id_dest)

            # Create a empty Linestring
            fields = QgsFields()
            fields.append(QgsField('ID_ORI', QVariant.String))
            fields.append(QgsField('ID_DEST', QVariant.String))
            fields.append(QgsField('OI_RO', QVariant.Double))
            fields.append(QgsField('OI_SUM', QVariant.Double))
            layer_name = 'Lineas_RO_' + str(i+1)
            lines_layer = QgsVectorLayer('LineString?crs='+espg, layer_name, 'memory')
            lines_layers_name.append(lines_layer.id())
            lines_layer.dataProvider().addAttributes(fields)
            lines_layer.updateFields()

            row = 0
            for origin_feature in origin_features:
                column = 0
                for destination_feature in destination_features:
                    # get a geometry
                    origin_geometry = origin_feature.geometry()
                    destination_geometry = destination_feature.geometry()

                    # create a line geometry
                    line_geometry = QgsGeometry.fromPolylineXY([origin_geometry.asPoint(), destination_geometry.asPoint()])

                    # adding feature by feature
                    line_feature = QgsFeature()
                    line_feature.setGeometry(line_geometry)
                    attr_valueO = origin_feature.attributes()[index_O]
                    attr_valueD = destination_feature.attributes()[index_D]
                    line_feature.setAttributes([attr_valueO, attr_valueD, values_oi[str(i)]["OI"][column], values_oi[str(i)]["OI_SUM"]])

                    # adding features
                    lines_layer.dataProvider().addFeatures([line_feature])

                    # Agregar la capa al proyecto
                    QgsProject.instance().addMapLayer(lines_layer)
                    column +=1
                row +=1
        return lines_layers_name

    def merger_points(self, matrix_OD:list) -> None:
        for i in range(0, len(matrix_OD)):
            data = {
                    "LAYERS":[matrix_OD[i][0],matrix_OD[i][1]],
                    "CRS": matrix_OD[i][0].crs().authid(),
                    "OUTPUT":"memory:Puntos_OR_"+ str(i+1)
                    }
            layer = processing.run("native:mergevectorlayers",data)
            QgsProject.instance().addMapLayer(layer["OUTPUT"])

    def thematic_lines(self, layers: list, field_name:str) -> None:
        all_layers = QgsProject.instance().mapLayers()
        for i in range(0, len(layers)):
            if all_layers[layers[i]]:
                layer = all_layers[layers[i]]
                field = field_name
                random_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                line_symbol = QgsLineSymbol.createSimple({'color': random_color.name()})
                line_symbol.setOutputUnit(QgsUnitTypes.RenderPixels)
                renderer = QgsSingleSymbolRenderer(line_symbol)
                layer.setRenderer(renderer)
                features = layer.getFeatures()
                for feature in features:
                    valor_ancho_linea = feature.attribute(field)
                    line_symbol.setWidth(valor_ancho_linea)
                    layer.triggerRepaint()

        QgsProject.instance().reloadAllLayers()

    def add_index(self, layer: object, values: list) -> None:
        with edit(layer):
            layer.addAttribute(QgsField("OI_SUM",QVariant.Double))
            layer.updateFields()
            features = layer.getFeatures()
            for i, feature in enumerate(features):
                feature["OI_SUM"] = values[i]
                layer.updateFeature(feature)
        QgsProject.instance().addMapLayer(layer)

    def thematic_polygons(self, layer:object, field_name:str) -> None:
        symbol = QgsFillSymbol()
        clasificacion = [QgsGraduatedSymbolRenderer.Quantile]
        style = QgsStyle().defaultStyle()
        color_ramp = style.colorRampNames()
        ramp = style.colorRamp(color_ramp[25]) #RdYlGn
        field = field_name
        renderer = QgsGraduatedSymbolRenderer.createRenderer(layer, field, 5, clasificacion[0], symbol, ramp)
        layer.setRenderer(renderer)

