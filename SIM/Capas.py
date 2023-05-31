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

    def centroid(self, layer:QgsVectorLayer) -> QgsVectorLayer:
        params = {
                "INPUT":layer,
                "ALL_PARTS": False,
                "OUTPUT": "memory:"
                }
        output_layer = processing.run("native:centroids", params)
        return output_layer['OUTPUT']

    def features_selector_OR(self, layers:dict, values:dict, id_ori: str, id_dest:str) -> tuple:
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
                    QgsProject.instance().addMapLayer(saved["OUTPUT"])

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
        return matrix_OD, origin_list

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
        return lines_layers_name

    def merge_layers(self, layers:list, name:str) -> QgsVectorLayer:
        if type(layers[0]) == str:
            crs = layers[0]
        else:
            crs = layers[0].crs().authid()
        data = {
                    "LAYERS":layers,
                    "CRS": crs,
                    "OUTPUT":"memory:" + name
                    }
        layer = processing.run("native:mergevectorlayers",data)
        QgsProject.instance().addMapLayer(layer["OUTPUT"])

        return layer['OUTPUT']

    def thematic_lines(self, layer:QgsVectorLayer, field_name:str) -> None:
        field = field_name
        values = layer.uniqueValues(layer.fields().indexFromName(field))
        min_v = min(values)
        max_v = max(values)
        random_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        line_symbol = QgsLineSymbol.createSimple({'color': random_color.name()})
        line_symbol.setOutputUnit(QgsUnitTypes.RenderMillimeters)
        renderer = QgsSingleSymbolRenderer(line_symbol)
        layer.setRenderer(renderer)
        exp = f'coalesce(scale_exp("{field}", {min_v}, {max_v}, 0.1, 2.5, 0.57), 0)'
        layer.renderer().symbol().symbolLayer(0).dataDefinedProperties().property(QgsSymbolLayer.PropertyStrokeWidth).setExpressionString(exp)
        layer.renderer().symbol().symbolLayer(0).dataDefinedProperties().property(QgsSymbolLayer.PropertyStrokeWidth).setActive(True)
        layer.triggerRepaint()
        QgsProject.instance().reloadAllLayers()

    def add_index(self, layer:QgsVectorLayer, values: list) -> None:
        with edit(layer):
            layer.addAttribute(QgsField("OI_SUM",QVariant.Double))
            layer.updateFields()
            features = layer.getFeatures()
            for i, feature in enumerate(features):
                feature["OI_SUM"] = values[i]
                layer.updateFeature(feature)
        QgsProject.instance().addMapLayer(layer)

    def thematic_polygons(self, layer:QgsVectorLayer, field_name:str) -> None:
        symbol = QgsFillSymbol()
        clasificacion = [QgsGraduatedSymbolRenderer.Quantile]
        style = QgsStyle().defaultStyle()
        color_ramp = style.colorRampNames()
        ramp = style.colorRamp(color_ramp[25]) #RdYlGn
        field = field_name
        renderer = QgsGraduatedSymbolRenderer.createRenderer(layer, field, 5, clasificacion[0], symbol, ramp)
        layer.setRenderer(renderer)
        QgsProject.instance().reloadAllLayers()


    def thematic_points(self, layer:QgsVectorLayer, l_type:str) -> None:
        if l_type == "ORI":
            color = '78,124,185,255'
            outline_color = '0,0,0,255'
            outline_width = '0.2'
            scale_method = 'area'
        else:
            color = '0,0,0,255'
            outline_color = '255,255,255,255'
            outline_width = '0.4'
            scale_method = 'diameter'

        data = {'angle': '0',
                'cap_style': 'square',
                'color': color,
                'horizontal_anchor_point':'1',
                'joinstyle': 'bevel',
                'name': 'circle',
                'offset': '0,0',
                'offset_map_unit_scale':'3x:0,0,0,0,0,0',
                'offset_unit': 'MM',
                'outline_color': outline_color,
                'outline_style': 'solid',
                'outline_width': outline_width,
                'outline_width_map_unit_scale': '3x:0,0,0,0,0,0',
                'outline_width_unit': 'MM',
                'scale_method': scale_method,
                'size': '3',
                'size_map_unit_scale': '3x:0,0,0,0,0,0',
                'size_unit': 'MM',
                'vertical_anchor_point': '1'}
        symbol = QgsMarkerSymbol.createSimple(data)
        layer.renderer().setSymbol(symbol)
        layer.triggerRepaint()
        QgsProject.instance().reloadAllLayers()

