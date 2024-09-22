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
    def __init__(self):
        color1 = QColor("#7b7b7b")  # gray
        color2 = QColor("#b7b7b7")  # gray deg
        color3 = QColor("#f7f7f7")  # white
        color4 = QColor("#c2a5cf")  # purple deg
        color5 = QColor("#7b3294")  # purple

        style = QgsStyle().defaultStyle()
        ramp = QgsStyle().defaultStyle().colorRamp("GyWtPu")
        if ramp is None:
            ramp = QgsGradientColorRamp(color1, color5, False)
            stops = [
                QgsGradientStop(0.25, color2),
                QgsGradientStop(0.50, color3),
                QgsGradientStop(0.75, color4)
            ]
            ramp.setStops(stops)
            style.addColorRamp("GyWtPu", ramp)
    
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
            aux = "_Demanda" if i == 0 else "_SinDemanda"
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
            # ------ DEST
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
                        origin_list.append(saved["OUTPUT"])
                        
            # ORIGINs
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
                                "OUTPUT":"memory:"+str(values[str(i)]['ORI'][j])}
                        saved = processing.run("native:saveselectedfeatures",data2)
                        dest_list.append(saved["OUTPUT"])

            # Matrix with Origins and Dest (filters)
            matrix_OD = [list(par) for par in zip(origin_list, dest_list)]
            return matrix_OD, dest_list
        else:
            # Origin
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
                        dest_list.append(saved["OUTPUT"])

            # Dest
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
                                "OUTPUT":"memory:"+str(values[str(i)]['DEST'][j])}
                        saved = processing.run("native:saveselectedfeatures",data2)
                        origin_list.append(saved["OUTPUT"])
            # Matrix with Origins and Dest (filters)
            matrix_OD = [list(par) for par in zip(dest_list, origin_list)]
            return matrix_OD, origin_list
        
    def create_lines_RO(self,matrix_OD:list, values_oi:dict, id_ori: str, id_dest:str, temp_path:str, l_type:int) -> list:
        epsg = matrix_OD[0][0].crs().authid()
        lines_layers_name = []
        if l_type == 0:
            qf_id1 = "ID_ORI"
            qf_id2 = "ID_DEST"
            qf_var1 = "OI_RO"
            qf_var2 = "OI_SUM"
            qf_var3 = "OI_SUM_N"
            ly_nme = "RO"
            hd1 = "OI"
            hd2 = "OI_SUM"
            hd3 = "OI_SUM_N"
        elif l_type == 1:
            qf_id1 = "ID_ORI"
            qf_id2 = "ID_DEST"
            qf_var1 = "AI_DR"
            qf_var2 = "AI_SUM"
            qf_var3 = "AI_SUM_N"
            ly_nme = "DRO"
            hd1 = "AI"
            hd2 = "AI_SUM"
            hd3 = "AI_SUM_N"
            
        # Preparación fuera del bucle principal
        for i, (origin_layer, destination_layer) in enumerate(matrix_OD):
            origin_features = origin_layer.getFeatures()
            destination_features = destination_layer.getFeatures()
            index_O = origin_layer.fields().indexFromName(id_dest)
            index_D = destination_layer.fields().indexFromName(id_ori)
            
            # Crear capa de líneas una vez por iteración principal
            fields = QgsFields()
            fields.append(QgsField(qf_id1, QVariant.String))
            fields.append(QgsField(qf_id2, QVariant.String))
            fields.append(QgsField(qf_var1, QVariant.Double))
            fields.append(QgsField(qf_var2, QVariant.Double))
            fields.append(QgsField(qf_var3, QVariant.Double))
            
            layer_name = 'Lineas_' + ly_nme + f'_{i+1}'
            lines_layer = QgsVectorLayer(f'LineString?crs={epsg}', layer_name, 'memory')
            lines_layers_name.append(temp_path + layer_name + ".shp")
            lines_layer.dataProvider().addAttributes(fields)
            lines_layer.updateFields()
            
            # Crear lista para almacenar características antes de añadirlas en masa
            features_to_add = []

            for origin_feature in origin_features:
                origin_geometry = origin_feature.geometry()
                attr_valueO = origin_feature.attributes()[index_O]
                
                for column, destination_feature in enumerate(destination_features):
                    destination_geometry = destination_feature.geometry()
                    
                    # Crear geometría de la línea
                    line_geometry = QgsGeometry.fromPolylineXY([origin_geometry.asPoint(), destination_geometry.asPoint()])
                    
                    # Crear y configurar la característica de la línea
                    line_feature = QgsFeature()
                    line_feature.setGeometry(line_geometry)
                    attr_valueD = destination_feature.attributes()[index_D]
                    line_feature.setAttributes([
                        attr_valueO, attr_valueD, 
                        values_oi[str(i)][hd1][column], 
                        values_oi[str(i)][hd2], 
                        values_oi[str(i)][hd3]
                    ])
                    
                    # Añadir la característica a la lista
                    features_to_add.append(line_feature)
            
            # Añadir todas las características al proveedor de datos de la capa de una sola vez
            lines_layer.dataProvider().addFeatures(features_to_add)
            
            # Escribir la capa al archivo
            layer_path = temp_path + layer_name + ".shp"
            QgsVectorFileWriter.writeAsVectorFormat(lines_layer, layer_path, "UTF-8", lines_layer.crs(), "ESRI Shapefile")

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
        QgsProject.instance().addMapLayer(layer,False)
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
        QgsProject.instance().addMapLayer(layer,False)
        if p_type == 0:
            symbol = QgsFillSymbol()
            symbol.setOpacity(0.5)
            clasificacion = [QgsGraduatedSymbolRenderer.Jenks] #type:ignore
            style = QgsStyle().defaultStyle()
            color_ramp = style.colorRampNames()
            ind_c = color_ramp.index("RdYlGn")
            ramp = style.colorRamp(color_ramp[ind_c]) #RdYlGn
            ramp.invert()
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
        QgsProject.instance().addMapLayer(layer,False)
        if l_render == 0:
            if l_type == "ORI":
                color = '0,0,0,255'
                outline_color = '255,255,255,255'
                outline_width = '0.4'
                scale_method = 'diameter'
                size = '1.5'
                name = 'circle'
                angle = '0'
            elif l_type == "SinDemanda":
                color = '83,83,83,255'
                outline_color = '247,247,247,255'
                outline_width = '0.4'
                scale_method = 'diameter'
                size = '4'
                name = 'circle'
                angle = '0'
            data = {'angle': angle,
                    'cap_style': 'square',
                    'color': color,
                    'horizontal_anchor_point':'1',
                    'joinstyle': 'bevel',
                    'name': name,
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
            if l_type == "ORI":
                symbol_layer = QgsSimpleMarkerSymbolLayer()
                symbol_layer.setShape(QgsSimpleMarkerSymbolLayer.Diamond)
                symbol_layer.setSize(3)  
                symbol_layer.setColor(QColor(0, 0, 0))
                symbol_layer.setAngle(45)
                symbol_layer.setStrokeWidth(0)  
                symbol.changeSymbolLayer(0, symbol_layer)
            exp = f'coalesce(scale_linear("{field_name}", {min_v}, {max_v}, 1, 10), 0)'
            symbol.symbolLayer(0).setDataDefinedProperty(QgsSymbolLayer.PropertySize, QgsProperty.fromExpression(exp)) #type:ignore
            clasificacion = [QgsGraduatedSymbolRenderer.Jenks] #type:ignore
            style = QgsStyle().defaultStyle()
            color_ramp = style.colorRampNames()
            if l_type == "ORI":
                ind_c = color_ramp.index("RdYlGn")
            else:
                ind_c = color_ramp.index("GyWtPu")
            ramp = style.colorRamp(color_ramp[ind_c]) #Gray White Purple
            if l_type == "ORI":
                ramp.invert()
            renderer = QgsGraduatedSymbolRenderer.createRenderer(layer, field_name, 5, clasificacion[0], symbol, ramp)
            # pendiente para agregar el contorno blanco
            layer.setRenderer(renderer)
            layer.triggerRepaint()
            QgsProject.instance().reloadAllLayers()

        elif l_render == 2:
            values = layer.uniqueValues(layer.fields().indexFromName(field_name))
            max_v = max(values)
            heatmap = QgsHeatmapRenderer()
            ramp = QgsStyle().defaultStyle().colorRamp('GyWtPu')
            heatmap.setColorRamp(ramp)
            heatmap.setMaximumValue(max_v)
            heatmap.setWeightExpression(field_name)
            layer.setRenderer(heatmap)
            layer.triggerRepaint()
            QgsProject.instance().reloadAllLayers()