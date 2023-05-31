import sys
from qgis.core import *
# Librerias adicionales
sys.path.append('/home/hades/Documentos/projects/SpatialInteractionModels/SIM/')
from Main import Main

capa1 = r"/home/hades/Documentos/Datos_EDOMEX/Localidades_ZMT_pob_repro/L_ZMT_pob.shp"
capa2 = r"/home/hades/Documentos/Datos_EDOMEX/CLUES_repro/CLUES.shp"

origin = QgsVectorLayer(capa1,"ZMT","ogr")
destination = QgsVectorLayer(capa2,"CLUES","ogr")

params = {
        "ORIGIN": origin,
        "ID_ORI": "CVEGEO",
        "VAR_ORI": "POB1",
        "DEST": destination,
        "ID_DEST": "CLUES",
        "VAR_DEST": "C1301",
        "UNIT": 0,
        "RESTR": 0,
        "VAL_REST": {
            "R_ORIG": {
                "OPTION": 2,
                "VALUE": [1000,2500],
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
        "OUTPUT":"/home/hades/Documentos/projects/SpatialInteractionModels/"
        }

run = Main(params)
run.run()
