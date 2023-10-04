import processing #type:ignore
from qgis.core import * #type:ignore
import random
from PyQt5.QtGui import * #type:ignore
from datetime import datetime

try:
    from qgis.core import QVariant #type:ignore
except ImportError:
    try:
        from PyQt5.QtCore import QVariant
    except ImportError:
        print("Error")

class Capas:
    def layer_filter(self, layer:QgsVectorLayer, field_name:str) -> list:
        exprs = [f'"{field_name}" > 0',f'"{field_name}" <= 0']
        layers = []
        for i,expr in enumerate(exprs):
            data_sl = {
                "INPUT":layer,
                "EXPRESSION":expr,
                "METHOD":0 #new selection
            }
            selection = processing.run("qgis:selectbyexpression",data_sl)["OUTPUT"]
            aux = "_VMC" if i == 0 else "_VMenC"
            data_sv = {
                "INPUT":selection,
                "OUTPUT":"memory:" + layer.name() + aux}
            saved = processing.run("native:saveselectedfeatures",data_sv)["OUTPUT"]
            layers.append(saved)
            QgsProject.instance().addMapLayer(saved,False)

        return layers


    def centroid(self, layer:QgsVectorLayer) -> QgsVectorLayer:
        params = {
                "INPUT":layer,
                "ALL_PARTS": False,
                "OUTPUT": "memory:"
                }
        output_layer = processing.run("native:centroids", params)
        return output_layer['OUTPUT']

    def features_selector_OR(self, layers:dict, values:dict, id_ori: str, id_dest:str, r_type:int) -> tuple:
        origin = layers['ORIGIN']
        dest = layers['DEST']

        origin_fields = origin.fields()
        dest_fields = dest.fields()

        origin_list = []
        dest_list = []
        if r_type == 0:
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

            # Matrix with Origins and Dest (filters)
            matrix_OD = [list(par) for par in zip(origin_list, dest_list)]
        else:
            # For dest
            for field in dest_fields:
                if field.name() == id_dest:
                    for i in range(0,len(values)):
                        dest.removeSelection()
                        if field.type() == 7 or field.type() == 10: # for strings
                            expr = f"\"{id_dest}\"=\'{values[str(i)]['DEST']}\'"
                        else:
                            expr = f"\"{id_dest}\"={values[str(i)]['DEST']}"
                        data = {
                                "INPUT":dest,
                                "EXPRESSION":expr,
                                "METHOD":1
                                }
                        selected_features = processing.run("qgis:selectbyexpression",data)
                        data2 = {
                                "INPUT":selected_features["OUTPUT"],
                                "OUTPUT":"memory:"+str(values[str(i)]['DEST'])}
                        saved = processing.run("native:saveselectedfeatures",data2)
                        dest_list.append(saved["OUTPUT"])

            # for origins
            for field in origin_fields:
                if field.name() == id_ori:
                    for i in range(0,len(values)):
                        origin.removeSelection()
                        selected_features = {}
                        for j in range(0, len(values[str(i)]["ORI"])):
                            if field.type() == 7 or field.type() == 10: # for strings
                                expr = f"\"{id_ori}\"=\'{values[str(i)]['ORI'][j]}\'"
                            else:
                                expr = f"\"{id_ori}\"={values[str(i)]['ORI'][j]}"
                            data = {
                                    "INPUT":origin,
                                    "EXPRESSION":expr,
                                    "METHOD":1
                                    }
                            selected_features = processing.run("qgis:selectbyexpression",data)
                        data2 = {
                                "INPUT":selected_features["OUTPUT"],
                                "OUTPUT":"memory:"+dest.name()+"_"+str(i+1)}
                        saved = processing.run("native:saveselectedfeatures",data2)
                        origin_list.append(saved["OUTPUT"])
            # Matrix with Origins and Dest (filters)
            matrix_OD = [list(par) for par in zip(dest_list, origin_list)]

        return matrix_OD, dest_list

    def create_lines_RO(self,matrix_OD:list, values_oi:dict, id_ori: str, id_dest:str, temp_path:str, l_type:int) -> list:
        epsg = matrix_OD[0][0].crs().authid()
        lines_layers_name = []
        if l_type == 0:
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
                lines_layer = QgsVectorLayer('LineString?crs='+epsg, layer_name, 'memory')
                #lines_layers_name.append(lines_layer.id())
                lines_layers_name.append(temp_path + layer_name + ".shp")
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
                        layer_path = temp_path + layer_name + ".shp"
                        QgsVectorFileWriter.writeAsVectorFormat(lines_layer, layer_path, "UTF-8", lines_layer.crs(), "ESRI Shapefile")
                        column +=1
        else:
            for i in range(len(matrix_OD)):
                destination_features = matrix_OD[i][0].getFeatures()
                origin_features = matrix_OD[i][1].getFeatures()
                index_D = matrix_OD[i][0].fields().indexFromName(id_dest)
                index_O = matrix_OD[i][1].fields().indexFromName(id_ori)
                # Create a empty Linestring
                fields = QgsFields()
                fields.append(QgsField('ID_DEST', QVariant.String))
                fields.append(QgsField('ID_ORI', QVariant.String))
                fields.append(QgsField('DJ_RD', QVariant.Double))
                fields.append(QgsField('DJ_SUM', QVariant.Int))
                layer_name = 'Lineas_RD_' + str(i+1)
                lines_layer = QgsVectorLayer('LineString?crs='+epsg, layer_name, 'memory')
                #lines_layers_name.append(lines_layer.id())
                lines_layers_name.append(temp_path + layer_name + ".shp")
                lines_layer.dataProvider().addAttributes(fields)
                lines_layer.updateFields()

                for destination_feature in destination_features:
                    column = 0
                    for origin_feature in origin_features:
                        # get a geometry
                        destination_geometry = destination_feature.geometry()
                        origin_geometry = origin_feature.geometry()

                        # create a line geometry
                        line_geometry = QgsGeometry.fromPolylineXY([destination_geometry.asPoint(), origin_geometry.asPoint()])

                        # adding feature by feature
                        line_feature = QgsFeature()
                        line_feature.setGeometry(line_geometry)
                        attr_valueD = destination_feature.attributes()[index_D]
                        attr_valueO = origin_feature.attributes()[index_O]
                        line_feature.setAttributes([attr_valueD, attr_valueO, float(values_oi[str(i)]["DJ"][column]), values_oi[str(i)]["DJ_SUM"]])

                        # adding features
                        lines_layer.dataProvider().addFeatures([line_feature])

                        # Agregar la capa al proyecto
                        layer_path = temp_path + layer_name + ".shp"
                        QgsVectorFileWriter.writeAsVectorFormat(lines_layer, layer_path, "UTF-8", lines_layer.crs(), "ESRI Shapefile")
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
        QgsProject.instance().addMapLayer(layer["OUTPUT"], False)

        return layer['OUTPUT']

    def thematic_lines(self, layer:QgsVectorLayer, field_name:str) -> None:
        field = field_name
        values = layer.uniqueValues(layer.fields().indexFromName(field))
        min_v = min(values)
        max_v = max(values)
        random_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        line_symbol = QgsLineSymbol.createSimple({'color': random_color.name()})
        line_symbol.setOutputUnit(QgsUnitTypes.RenderMillimeters) #type:ignore
        renderer = QgsSingleSymbolRenderer(line_symbol)
        layer.setRenderer(renderer)
        exp = f'coalesce(scale_exp("{field}", {min_v}, {max_v}, 0.1, 2.5, 0.57), 0)'
        layer.renderer().symbol().symbolLayer(0).dataDefinedProperties().property(QgsSymbolLayer.PropertyStrokeWidth).setExpressionString(exp) #type:ignore
        layer.renderer().symbol().symbolLayer(0).dataDefinedProperties().property(QgsSymbolLayer.PropertyStrokeWidth).setActive(True) #type:ignore
        layer.triggerRepaint()
        QgsProject.instance().reloadAllLayers()

    def add_index(self, layer:QgsVectorLayer, values: list, var:str) -> QgsVectorLayer:
        with edit(layer):
            if var == "DJ_SUM":
                layer.addAttribute(QgsField(var,QVariant.Int))
            else:
                layer.addAttribute(QgsField(var,QVariant.Double))
            layer.updateFields()
            features = layer.getFeatures()
            for i, feature in enumerate(features):
                feature[var] = values[i]
                layer.updateFeature(feature)
        QgsProject.instance().addMapLayer(layer, False)

    def thematic_polygons(self, layer:QgsVectorLayer, field_name:str, p_type:int) -> None:
        if p_type == 0:
            symbol = QgsFillSymbol()
            clasificacion = [QgsGraduatedSymbolRenderer.Jenks] #type:ignore
            style = QgsStyle().defaultStyle()
            color_ramp = style.colorRampNames()
            ind_c = color_ramp.index("RdYlGn")
            ramp = style.colorRamp(color_ramp[ind_c]) #RdYlGn
            field = field_name
            renderer = QgsGraduatedSymbolRenderer.createRenderer(layer, field, 5, clasificacion[0], symbol, ramp)
            layer.setRenderer(renderer)
            QgsProject.instance().reloadAllLayers()
        elif p_type == 1:
            data = {
            "border_width_map_unit_scale": "3x:0,0,0,0,0,0",
            "color": "150,150,150,255",
            "joinstyle":"bevel",
            "offset": "0,0",
            "offset_map_unit_scale": "3x:0,0,0,0,0,0",
            "offset_unit": "MM",
            "outline_color": "247,247,247,255",
            "outline_style": "solid",
            "outline_width": "0.26",
            "outline_width_unit": "MM",
            "style": "solid"
            }
            symbol = QgsFillSymbol.createSimple(data)
            renderer = QgsSingleSymbolRenderer(symbol)
            layer.setRenderer(renderer)
            layer.triggerRepaint()
            QgsProject.instance().reloadAllLayers()
        else:
            data = {
                'color':'255,255,255,0', 
                'outline_color':'255,255,255'
            }
            symbol = QgsFillSymbol.createSimple(data)
            renderer = QgsSingleSymbolRenderer(symbol)
            layer.setRenderer(renderer)
            layer.triggerRepaint()
            QgsProject.instance().reloadAllLayers()

    def thematic_points(self, layer:QgsVectorLayer, l_type:str, l_render:int,field_name:str) -> None:
        if l_render == 0:
            if l_type == "ORI":
                color = '1,200,255,255'
                outline_color = '0,0,0,255'
                outline_width = '0.2'
                scale_method = 'area'
                size = '3'
            elif l_type == "VMenC":
                color = '83,83,83,255'
                outline_color = '247,247,247,255'
                outline_width = '0.4'
                scale_method = 'diameter'
                size = '4'
            else:
                color = '0,0,0,255'
                outline_color = '255,255,255,255'
                outline_width = '0.4'
                scale_method = 'diameter'
                size = '3'

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
                    'size': size,
                    'size_map_unit_scale': '3x:0,0,0,0,0,0',
                    'size_unit': 'MM',
                    'vertical_anchor_point': '1'}
            symbol = QgsMarkerSymbol.createSimple(data)
            renderer = QgsSingleSymbolRenderer(symbol)
            layer.setRenderer(renderer)
            layer.triggerRepaint()
            QgsProject.instance().reloadAllLayers()
        elif l_render == 1:
            values = layer.uniqueValues(layer.fields().indexFromName(field_name))
            min_v = min(values)
            max_v = max(values)
            symbol = QgsMarkerSymbol()
            exp = f'coalesce(scale_linear("{field_name}", {min_v}, {max_v}, 1, 10), 0)'
            symbol.symbolLayer(0).setDataDefinedProperty(QgsSymbolLayer.PropertySize, QgsProperty.fromExpression(exp)) #type:ignore
            symbol.setOpacity(0.6)
            clasificacion = [QgsGraduatedSymbolRenderer.Jenks] #type:ignore
            style = QgsStyle().defaultStyle()
            color_ramp = style.colorRampNames()
            ramp = style.colorRamp(color_ramp[25]) #RdYlGn
            renderer = QgsGraduatedSymbolRenderer.createRenderer(layer, field_name, 5, clasificacion[0], symbol, ramp)
            # pendiente para agregar el contorno blanco
            layer.setRenderer(renderer)
            layer.triggerRepaint()
            QgsProject.instance().reloadAllLayers()

        elif l_render == 2:
            values = layer.uniqueValues(layer.fields().indexFromName(field_name))
            max_v = max(values)
            heatmap = QgsHeatmapRenderer()
            ramp = QgsStyle().defaultStyle().colorRamp('RdYlGn')
            heatmap.setColorRamp(ramp)
            heatmap.setMaximumValue(max_v)
            heatmap.setWeightExpression(field_name)
            layer.setRenderer(heatmap)
            layer.triggerRepaint()