import sys
from qgis.core import *
# Librerias adicionales
sys.path.append('/home/hades/Documentos/projects/SpatialInteractionModels/SIM/')
from Main import Main

capa1 = r"/home/hades/Documentos/Datos_EDOMEX/Localidades_ZMT_pob_repro/LZMT_C.shp"
#capa1 = r"/home/hades/Documentos/Datos_EDOMEX/Localidades_ZMT_pob_repro/LZMT_C_Puntos.shp"
capa2 = r"/home/hades/Documentos/Datos_EDOMEX/CLUES_repro/CLUES.shp"

origin = QgsVectorLayer(capa1,"ZMT","ogr")
destination = QgsVectorLayer(capa2,"CLUES","ogr")

params = {
        "ORIGIN": origin,
        "ID_ORI": "CVEGEO",
        "VAR_ORI": "POB65_MAS",
        "DEST": destination,
        "ID_DEST": "CLUES",
        "VAR_DEST": "C1301", #Medicina general
        "UNIT": 0, # 0 - metros
        "RESTR": 0,
        "VAL_REST": {
            "R_ORIG": {
                "OPTION": 2,
                "VALUE": [500,3000],
                       },
            "R_DEST": {
                "OPTION": 0,
                "VALUE": [5],
                },
            "D_REST":{
                "RORIG": {
                    "OPTION": 0,
                    "VALUE": [5],
                    },
                "RDEST": {
                    "OPTION": 0,
                    "VALUE": [5],
                    }
                }
            },
        "FRICTION_DISTANCE": 1.2,
        "OUTPUT":"/home/hades/Documentos/projects/SpatialInteractionModels/test/"
        }

run = Main(params)
run.run()
