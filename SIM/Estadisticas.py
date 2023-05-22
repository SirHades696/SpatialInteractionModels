
from qgis.core import *
import math

class Estadisticas:

    def distanceMatrix(self, origin:object, destination:object, unit:int) -> list:
        distance = QgsDistanceArea()
        distance.setSourceCrs(origin.crs(), QgsProject.instance().transformContext())
        ellip = QgsProject.instance().ellipsoid()
        if ellip.split(":")[1] != 7030:
            ellip = "EPSG:7030"
        distance.setEllipsoid(ellip)

        matrix = []
        for f1 in origin.getFeatures():
            row = []
            for f2 in destination.getFeatures():
                punto1 = f1.geometry().asPoint()
                punto2 = f2.geometry().asPoint()
                d = 0
                # 0 - metros, 1 - kilometros, 2 - millas, 3 - pies, 4 - yardas
                if unit == 0:
                    d = distance.measureLine(punto1, punto2)
                elif unit == 1:
                    d = distance.measureLine(punto1, punto2)/1000
                elif unit == 2:
                    d = distance.measureLine(punto1, punto2)/1609.344
                elif unit == 3:
                    d = distance.measureLine(punto1, punto2)*3.28084
                elif unit == 4:
                    d = distance.measureLine(punto1, punto2)/0.9144
                row.append(d)
            matrix.append(row)
        return matrix

    def origin_restriction(self, matrix:list, val_rest:dict, values_OD:dict ) -> tuple:
        # filters and first step of SIM
        if val_rest['R_ORIG']['OPTION'] == 0:
            for i in range(0, len(values_OD["ORIGIN"])):
                for j in range(0, len(values_OD["DEST"])):
                    if matrix[i][j] >= val_rest['R_ORIG']['VALUE'][0]: # >=
                        matrix[i][j] = 1/(math.pow(matrix[i][j],values_OD["FD"]))
                    else:
                        matrix[i][j] = 0
        elif val_rest['R_ORIG']['OPTION'] == 1:
            for i in range(0, len(values_OD["ORIGIN"])):
                for j in range(0, len(values_OD["DEST"])):
                    if matrix[i][j] <= val_rest['R_ORIG']['VALUE'][0]: # <=
                        matrix[i][j] = 1/(math.pow(matrix[i][j],values_OD["FD"]))
                    else:
                        matrix[i][j] = 0
        elif val_rest['R_ORIG']['OPTION'] == 2:
            for i in range(0, len(values_OD["ORIGIN"])):
                for j in range(0, len(values_OD["DEST"])):
                    if matrix[i][j] >= val_rest['R_ORIG']['VALUE'][0] and matrix[i][j] <= val_rest['R_ORIG']['VALUE'][1]: # Range
                        matrix[i][j] = 1/(math.pow(matrix[i][j],values_OD["FD"]))
                    else:
                        matrix[i][j] = 0

        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i][j] = matrix[i][j] * values_OD["DEST"][j]

        ai = []
        for i in range(0, len(values_OD["ORIGIN"])):
            suma = 0
            for j in range(0, len(values_OD["DEST"])):
                suma += matrix[i][j]
            if suma != 0:
                ai.append(1/suma)
            else:
                ai.append(0)

        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i][j] = matrix[i][j] * values_OD["ORIGIN"][i] * ai[i]

        oi = []
        for i in range(0, len(values_OD["ORIGIN"])):
            suma = 0
            for j in range(0, len(values_OD["DEST"])):
                suma += matrix[i][j]
            oi.append(suma)

        values = {}
        values_oi = {}
        count = 0
        for i in range(0, len(values_OD["ORIGIN"])):
            aux = []
            aux_v = []
            for j in range(0, len(values_OD["DEST"])):
                if matrix[i][j] > 0:
                    aux.append(values_OD["ID_DEST"][j])
                    aux_v.append(matrix[i][j])
            if len(aux) != 0 and len(aux_v) != 0:
                values[str(count)] = {"ORI": values_OD["ID_ORI"][i], "DEST": aux}
                values_oi[str(count)] = {"OI": aux_v , "OI_SUM": oi[i]}
                count += 1
        #print(values_oi)
        return values, values_oi

    def extract_data(self, layer:object, name_attr: str) -> list:
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        values = []
        for feature in layer.getFeatures(request):
            attribute_value = feature[name_attr]
            values.append(attribute_value)
        return values


