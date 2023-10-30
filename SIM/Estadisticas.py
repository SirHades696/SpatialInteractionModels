
from qgis.core import *
import numpy as np

class Estadisticas:

    def distanceMatrix(self, origin:QgsVectorLayer, destination:QgsVectorLayer, unit:int) -> np.ndarray:
        distance = QgsDistanceArea()
        distance.setSourceCrs(origin.crs(), QgsProject.instance().transformContext())
        ellip = QgsProject.instance().ellipsoid()
        if int(ellip.split(":")[1]) != 7030:
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
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceMeters) # type:ignore
                elif unit == 1:
                    d_aux = distance.measureLine(punto1, punto2)#/1000
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceKilometers) # type:ignore
                elif unit == 2:
                    d_aux = distance.measureLine(punto1, punto2)#/1609.344
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceMiles) # type:ignore
                elif unit == 3:
                    d_aux = distance.measureLine(punto1, punto2)#*3.28084
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.DistanceFeet) # type:ignore
                elif unit == 4:
                    d_aux = distance.measureLine(punto1, punto2)#/0.9144
                    d = distance.convertLengthMeasurement(d_aux, QgsUnitTypes.Yards) # type:ignore
                matrix[i,j] = d
                j += 1
            i += 1
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

        values = {} #IDs
        values_oi = {} #Values of OI, total and individual
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

    def dest_restriction(self, matrix:np.ndarray, val_rest:dict, values_OD:dict) -> tuple:
        #----- first step
        matrix = np.power(matrix, values_OD["FD"])
        matrix = 1/matrix
        #---- second step
        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] = matrix[i,j] * values_OD["DEST"][j]
        suma = np.sum(matrix, axis = 0)
        pre_bj = 1/suma
        # convirtiendo los naN e Inf en 0
        bj = np.nan_to_num(pre_bj, nan=0.0, posinf=0.0, neginf=0.0)
        #------------- third step
        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] = matrix[i,j] * values_OD["ORIGIN"][i] * bj[j]
        suma = np.sum(matrix,axis=0)
        suma_final = np.round(suma)

        if val_rest['R_DEST']['OPTION'] == 0:
            suma_final = np.where(suma_final >= val_rest['R_DEST']['VALUE'][0],suma_final,0)
        elif val_rest['R_DEST']['OPTION'] == 1:
            suma_final = np.where(suma_final <= val_rest['R_DEST']['VALUE'][0],suma_final,0)
        elif val_rest['R_DEST']['OPTION'] == 2:
            suma_final = np.where((suma_final >= val_rest['R_DEST']['VALUE'][0]) & (suma_final <= val_rest['R_DEST']['VALUE'][1]), suma_final,0)

        dj = suma_final.tolist()
        indexes = np.where(suma_final == 0)
        for index in indexes[0].tolist():
            matrix[:,index] = 0 
        values = {}
        values_dj = {}
        for i in range(0, len(values_OD["DEST"])):
            values[str(i)] = {"DEST": values_OD["ID_DEST"][i], "ORI":values_OD["ID_ORI"]}
            values_dj[str(i)] = {"DJ":matrix[:,i], "DJ_SUM":dj[i]}
        return values, values_dj, dj

    def extract_data(self, layer:QgsVectorLayer, name_attr: str) -> list:
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry) # type:ignore
        values = []
        for feature in layer.getFeatures(request):
            attribute_value = feature[name_attr]
            values.append(attribute_value)
        return values