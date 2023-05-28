import sys
from qgis.core import *
# Librerias adicionales
sys.path.append('/home/hades/Documentos/projects/SpatialInteractionModels/SIM/')
from Main import Main

capa1 = r"/home/hades/Documentos/Datos 2SFCA/UTM/Manzanas_UTM_Corto.shp"
capa2 = r"/home/hades/Documentos/Datos 2SFCA/UTM/Farmacias_UTM_Corto.shp"

origin = QgsVectorLayer(capa1,"Manzanas","ogr")
destination = QgsVectorLayer(capa2,"Farmacias","ogr")

params = {
        "ORIGIN": origin,
        "ID_ORI": "clavegeo",
        "VAR_ORI": "POB65_MAS",
        "DEST": destination,
        "ID_DEST": "id",
        "VAR_DEST": "peso",
        "UNIT": 0,
        "RESTR": 0,
        "VAL_REST": {
            "R_ORIG": {
                "OPTION": 1,
                "VALUE": [500],
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
