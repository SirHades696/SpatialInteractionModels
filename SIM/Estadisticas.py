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
        # distance filter step 1 and step 2, 1/dji^fd
        if val_rest['R_ORIG']['OPTION'] == 0:
            matrix = np.where(matrix >= val_rest['R_ORIG']['VALUE'][0],1/(matrix**values_OD["FD"]),0)
        elif val_rest['R_ORIG']['OPTION'] == 1:
            matrix = np.where(matrix <= val_rest['R_ORIG']['VALUE'][0],1/(matrix**values_OD["FD"]),0)
        elif val_rest['R_ORIG']['OPTION'] == 2:
            matrix = np.where((matrix >= val_rest['R_ORIG']['VALUE'][0]) & (matrix <= val_rest['R_ORIG']['VALUE'][1]),1/(matrix**values_OD["FD"]),0)
            
        # Wj * 1/dji^fd
        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] = matrix[i,j] * values_OD["DEST"][j]
        
        # ai = 1/sum(wj/dij^fd)
        suma = np.sum(matrix, axis=1)
        pre_ai = 1/suma
        # naN & Inf = 0
        ai = np.nan_to_num(pre_ai, nan=0.0, posinf=0.0, neginf=0.0)
        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] *=  values_OD["ORIGIN"][i] * ai[i]
        # oi
        sum_oi = np.sum(matrix,axis=0)
        oi = np.nan_to_num(sum_oi, nan=0.0,posinf=0.0, neginf=0.0)
        oi_n = self.normalize(oi)

        matrix_T = matrix.T
        values = {} #IDs
        values_oi = {} #Values of OI, total and individual
        
        count = 0
        for i in range(0, len(values_OD["DEST"])):
            aux = []
            aux_v = []
            for j in range(0, len(values_OD["ORIGIN"])):
                if matrix_T[i,j] > 0:
                    aux.append(values_OD["ID_ORI"][j])
                    aux_v.append(float(matrix_T[i,j]))
            if len(aux) != 0 and len(aux_v) != 0:
                values[str(count)] = {"DEST": values_OD["ID_DEST"][i], "ORI": aux}
                values_oi[str(count)] = {"OI": aux_v , "OI_SUM": round(oi[i]), "OI_SUM_N": oi_n[i]}
                count += 1
        
        return values, values_oi, oi.tolist(), oi_n, matrix

    def dest_restriction(self, matrix:np.ndarray, val_rest:dict, values_OD:dict) -> tuple:
        #----- first step
        matrix = np.power(matrix, values_OD["FD"])
        matrix = 1/matrix
        
        #---- second step
        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] = matrix[i,j] * values_OD["ORIGIN"][i]
        suma = np.sum(matrix, axis = 0)
        pre_bj = 1/suma
        # convirtiendo los naN e Inf en 0
        bj = np.nan_to_num(pre_bj, nan=0.0, posinf=0.0, neginf=0.0)
        #------------- third step
        for i in range(0, len(values_OD["ORIGIN"])):
            for j in range(0, len(values_OD["DEST"])):
                matrix[i,j] = matrix[i,j] * values_OD["DEST"][j] * bj[j]
        
        suma = np.sum(matrix,axis=1)
        suma_final = np.round(suma)

        if val_rest['R_DEST']['OPTION'] == 0:
            suma_final = np.where(suma_final >= val_rest['R_DEST']['VALUE'][0],suma_final,0)
        elif val_rest['R_DEST']['OPTION'] == 1:
            suma_final = np.where(suma_final <= val_rest['R_DEST']['VALUE'][0],suma_final,0)
        elif val_rest['R_DEST']['OPTION'] == 2:
            suma_final = np.where((suma_final >= val_rest['R_DEST']['VALUE'][0]) & (suma_final <= val_rest['R_DEST']['VALUE'][1]), suma_final,0)
        
        dj = suma_final.tolist()
        dj_n = self.normalize(suma_final)
        indexes = np.where(suma_final == 0)
        for index in indexes[0].tolist():
            matrix[index,:] = 0
            
        values = {}
        values_dj = {}
        for i in range(0, len(values_OD["ORIGIN"])):
            values[str(i)] = {"ORI": values_OD["ID_ORI"][i], "DEST":values_OD["ID_DEST"]}
            values_dj[str(i)] = {"DJ":matrix[i,:], "DJ_SUM":dj[i]}
        return values, values_dj, dj, dj_n, matrix

    def doubly_restriction(self, matrix:np.ndarray, val_rest:dict, values_OD:dict) -> None:
        if val_rest["REST"][0]['R_ORIG']['OPTION'] == 0:
            matrix = np.where(matrix >= val_rest["REST"][0]['R_ORIG']['VALUE'][0],1/(matrix**values_OD["FD"]),0)
        elif val_rest["REST"][0]['R_ORIG']['OPTION'] == 1:
            matrix = np.where(matrix <= val_rest["REST"][0]['R_ORIG']['VALUE'][0],1/(matrix**values_OD["FD"]),0)
        elif val_rest["REST"][0]['R_ORIG']['OPTION'] == 2:
            matrix = np.where((matrix >= val_rest["REST"][0]['R_ORIG']['VALUE'][0]) & (matrix <= val_rest["REST"][0]['R_ORIG']['VALUE'][1]),1/(matrix**values_OD["FD"]),0)
            
        ai = np.ones(len(values_OD["ORIGIN"]))
        bj = np.ones(len(values_OD["DEST"]))
        filas, columnas = matrix.shape
        error_oi_old = np.inf
        error_dj_old = np.inf
        its = 0
        c = 0
        while True:
            matrix_orig = matrix.copy()
            matrix_dest = matrix.copy()
            matrix_error = matrix.copy()
            error_oi_sum = np.sum(error_oi_old)
            error_dj_sum = np.sum(error_dj_old)
            its += 1
            
            # ------ ORIG
            for i in range(filas):
                for j in range(columnas):
                    matrix_orig[i, j] *= bj[j] * values_OD["DEST"][j]
            sum_orig = np.sum(matrix_orig, axis=1)
            pre_ai = 1 / sum_orig
            ai = np.nan_to_num(pre_ai, nan=0.0, posinf=0.0, neginf=0.0)
            
            # ---- DEST
            for i in range(filas):
                for j in range(columnas):
                    matrix_dest[i, j] *= ai[i] * values_OD["ORIGIN"][i]

            sum_dest = np.sum(matrix_dest, axis=0)
            pre_bj = 1 / sum_dest
            bj = np.nan_to_num(pre_bj, nan=0.0, posinf=0.0, neginf=0.0)
            
            for i in range(filas):
                for j in range(columnas):
                    matrix_error[i,j] *= ai[i]*bj[j]*values_OD["ORIGIN"][i]*values_OD["DEST"][j]

            n_oi = np.sum(matrix_error, axis=1)
            n_dj = np.sum(matrix_error, axis=0)

            error_oi = np.zeros(filas)
            for i in range(filas):
                error_oi[i] = abs(values_OD["ORIGIN"][i] - n_oi[i])

            error_dj = np.zeros(columnas)
            for j in range(columnas):
                error_dj[j] = abs(values_OD["DEST"][j] - n_dj[j])
                
            error_dj_sum = np.sum(error_dj)
            error_oi_sum = np.sum(error_oi)
            #print(its, c,error_oi_sum, error_dj_sum)
            if error_oi_sum == 0 and error_dj_sum == 0:
                break
            else:
                if error_dj_sum == error_dj_old and error_oi_sum == error_oi_old:
                    c +=1
                    if c == 10:
                        break
            error_dj_old = error_dj_sum
            error_oi_old = error_oi_sum
    
        for i in range(filas):
            for j in range(columnas):
                matrix[i, j] *= ai[i] * bj[j] * values_OD["ORIGIN"][i] * values_OD["DEST"][j]
        
        suma = np.sum(matrix,axis=1)
        suma_final = np.round(suma)

        if val_rest["REST"][1]['R_DEST']['OPTION'] == 0:
            suma_final = np.where(suma_final >= val_rest["REST"][1]['R_DEST']['VALUE'][0],suma_final,0)
        elif val_rest["REST"][1]['R_DEST']['OPTION'] == 1:
            suma_final = np.where(suma_final <= val_rest["REST"][1]['R_DEST']['VALUE'][0],suma_final,0)
        elif val_rest["REST"][1]['R_DEST']['OPTION'] == 2:
            suma_final = np.where((suma_final >= val_rest["REST"][1]['R_DEST']['VALUE'][0]) & (suma_final <= val_rest["REST"][1]['R_DEST']['VALUE'][1]), suma_final,0)
            
        indexes = np.where(suma_final == 0)
        for index in indexes[0].tolist():
            matrix[index,:] = 0

        # --------------- AI
        sum_ai = np.sum(matrix,axis=0)
        ai = np.nan_to_num(sum_ai, nan=0.0,posinf=0.0, neginf=0.0)
        ai_n = self.normalize(ai)
        matrix_T = matrix.T
        valuesAI = {} #IDs
        values_ai = {} #Values of AI, total and individual
        
        count = 0
        for i in range(0, len(values_OD["DEST"])):
            aux = []
            aux_v = []
            for j in range(0, len(values_OD["ORIGIN"])):
                if matrix_T[i,j] > 0:
                    aux.append(values_OD["ID_ORI"][j])
                    aux_v.append(float(matrix_T[i,j]))
            if len(aux) != 0 and len(aux_v) != 0:
                valuesAI[str(count)] = {"DEST": values_OD["ID_DEST"][i], "ORI": aux}
                values_ai[str(count)] = {"AI": aux_v , "AI_SUM": round(ai[i]), "AI_SUM_N":ai_n[i]}
                count += 1
        
        # ------------------- BJ
        sum_bj = np.sum(matrix,axis=1)
        suma_final = np.round(suma)
        bj = np.nan_to_num(suma_final.tolist(), nan=0.0,posinf=0.0, neginf=0.0)
        bj_n = self.normalize(bj)
        
        valuesBJ = {}
        values_bj = {}
        count = 0
        for i in range(0, len(values_OD["ORIGIN"])):
            aux = []
            aux_v = []
            for j in range(0, len(values_OD["DEST"])):
                if matrix[i,j] > 0:
                    aux.append(values_OD["ID_DEST"][j])
                    aux_v.append(float(matrix[i,j]))
            if len(aux) != 0 and len(aux_v) != 0:      
                valuesBJ[str(count)] = {"ORI": values_OD["ID_ORI"][i], "DEST": aux}
                values_bj[str(count)] = {"BJ": aux_v, "BJ_SUM":round(bj[i]), "BJ_SUM_N":bj_n[i]}
                count += 1
                        
        return matrix, valuesAI, values_ai, ai.tolist(), valuesBJ, values_bj, bj.tolist()
        
    def extract_data(self, layer:QgsVectorLayer, name_attr: str) -> list:
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry) # type:ignore
        values = []
        for feature in layer.getFeatures(request):
            attribute_value = feature[name_attr]
            values.append(attribute_value)
        return values
    
    def normalize(self, data:np.ndarray) -> list:
        norm = (data - np.min(data)) / (np.max(data) - np.min(data))
        return norm.tolist()