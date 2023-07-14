
from qgis.core import *
import numpy as np

class Estadisticas:

    def distanceMatrix(self, origin:QgsVectorLayer, destination:QgsVectorLayer, unit:int) -> np.ndarray:
        distance = QgsDistanceArea()
        distance.setSourceCrs(origin.crs(), QgsProject.instance().transformContext())
        ellip = QgsProject.instance().ellipsoid()
        if ellip.split(":")[1] != 7030:
            ellip = "EPSG:7030"
        distance.setEllipsoid(ellip)

        f_origin = origin.getFeatures()
        f_dest = destination.getFeatures()
        rows = len(list(f_origin))
        columns = len(list(f_dest))
        matrix = np.zeros((rows,columns))
        i = 0
        for f1 in origin.getFeatures():
            j = 0
            for f2 in destination.getFeatures():
                punto1 = f1.geometry().asPoint()
                punto2 = f2.geometry().asPoint()
                d = 0
                # 0 - metros, 1 - kilometros, 2 - millas, 3 - pies, 4 - yardas
                if unit == 0:
                    d_aux = distance.measureLine(punto1, punto2)
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceMeters)
                elif unit == 1:
                    d_aux = distance.measureLine(punto1, punto2)#/1000
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceKilometers)
                elif unit == 2:
                    d_aux = distance.measureLine(punto1, punto2)#/1609.344
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceMiles)
                elif unit == 3:
                    d_aux = distance.measureLine(punto1, punto2)#*3.28084
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceFeet)
                elif unit == 4:
                    d_aux = distance.measureLine(punto1, punto2)#/0.9144
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.Yards)
                matrix[i,j] = d
                j += 1
            i += 1
        #np.savetxt("matrix.csv", matrix, delimiter=',')
        return matrix

    def origin_restriction(self, matrix:np.ndarray, val_rest:dict, values_OD:dict ) -> tuple:
        if val_rest['R_ORIG']['OPTION'] == 0:
            matrix = np.where(matrix >= val_rest['R_ORIG']['VALUE'][0],1/(matrix**values_OD["FD"]),0)
        elif val_rest['R_ORIG']['OPTION'] == 1:
            matrix = np.where(matrix <= val_rest['R_ORIG']['VALUE'][0],1/(matrix**values_OD["FD"]),0)
        elif val_rest['R_ORIG']['OPTION'] == 2:
            matrix = np.where((matrix >= val_rest['R_ORIG']['VALUE'][0]) & (matrix <= val_rest['R_ORIG']['VALUE'][1]),1/(matrix**values_OD["FD"]),0)

        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] = matrix[i,j] * values_OD["DEST"][j]

        ai = []
        for i in range(0, len(values_OD["ORIGIN"])):
            suma = 0
            for j in range(0, len(values_OD["DEST"])):
                suma += matrix[i,j]
            if suma != 0:
                ai.append(float(1/suma))
            else:
                ai.append(float(0))

        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] = matrix[i,j] * values_OD["ORIGIN"][i] * ai[i]

        oi = []
        for i in range(0, len(values_OD["ORIGIN"])):
            suma = 0
            for j in range(0, len(values_OD["DEST"])):
                suma += matrix[i,j]
            oi.append(float(suma))

        values = {}
        values_oi = {}
        count = 0
        for i in range(0, len(values_OD["ORIGIN"])):
            aux = []
            aux_v = []
            for j in range(0, len(values_OD["DEST"])):
                if matrix[i,j] > 0:
                    aux.append(values_OD["ID_DEST"][j])
                    aux_v.append(float(matrix[i,j]))
            if len(aux) != 0 and len(aux_v) != 0:
                values[str(count)] = {"ORI": values_OD["ID_ORI"][i], "DEST": aux}
                values_oi[str(count)] = {"OI": aux_v , "OI_SUM": float(oi[i])}
                count += 1
        return values, values_oi, oi

    def extract_data(self, layer:QgsVectorLayer, name_attr: str) -> list:
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        values = []
        for feature in layer.getFeatures(request):
            attribute_value = feature[name_attr]
            values.append(attribute_value)
        return values


