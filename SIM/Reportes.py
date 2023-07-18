import subprocess
import sys
import webbrowser
import os
import numpy as np
import re

from html_template import html_string

try:
    import pandas as pd
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

class Reportes:

    def report_html(self, IDs:dict, values:dict, params:dict) -> None:
        df = pd.DataFrame.from_dict(IDs, orient='index')
        df_DEST = df.explode('DEST')
        new_df = pd.DataFrame.from_dict(values, orient='index')
        new_df_OI = new_df.explode('OI')
        new_df_OI['ACC_PROM'] = new_df.apply(lambda row: row['OI_SUM']/len(row['OI']), axis=1)
        new_df_OI['ACC_STD'] = new_df['OI'].apply(lambda x: np.std(x))
        df = pd.concat([df_DEST.reset_index(drop=True), new_df_OI.reset_index(drop=True)], axis=1)
        df['TOT_DEST'] = df.groupby('ORI')['DEST'].transform('count')
        df.rename(columns={'ORI': 'CVE_ORI',
                           'DEST': 'CVE_DEST',
                           'OI':'ACC_IND',
                           'OI_SUM':'ACC_TOT'}, inplace=True)
        pd.set_option('colheader_justify', 'center')   # <th>

        path = params["OUTPUT"] + 'ReporteModelosInteraccionEspacial.html'

        if params["UNIT"] == 0:
            unit = "Metros"
        elif params["UNIT"] == 1:
            unit = "Kilómetros"
        elif params["UNIT"] == 2:
            unit = "Millas"
        elif params["UNIT"] == 3:
            unit = "Pies"
        else:
            unit = "Yardas"

        tipo_rest, tipo_filt, values_r = "","",""
        if params["RESTR"] == 0:
            tipo_rest = "Restricción en el orígen"
            if params["VAL_REST"]["R_ORIG"]["OPTION"] == 0:
                tipo_filt = "Mayor que..."
                values_r = str(params["VAL_REST"]["R_ORIG"]["VALUE"][0])
            elif params["VAL_REST"]["R_ORIG"]["OPTION"] == 1:
                tipo_filt = "Menor que..."
                values_r = str(params["VAL_REST"]["R_ORIG"]["VALUE"][0])
            else:
                tipo_filt = "Rango"
                values_r = "Entre " + str(params["VAL_REST"]["R_ORIG"]["VALUE"][0]) + " y " + str(params["VAL_REST"]["R_ORIG"]["VALUE"][1])

        elif params["RESTR"] == 1:
            tipo_rest = "Restricción en el destino"
            if params["VAL_REST"]["R_DEST"]["OPTION"] == 0:
                tipo_filt = "Mayor que..."
                values_r = str(params["VAL_REST"]["R_DEST"]["VALUE"][0])
            elif params["VAL_REST"]["R_DEST"]["OPTION"] == 1:
                tipo_filt = "Menor que..."
                values_r = str(params["VAL_REST"]["R_DEST"]["VALUE"][0])
            else:
                tipo_filt = "Rango"
                values_r = "Entre " + str(params["VAL_REST"]["R_DEST"]["VALUE"][0]) + " y " + str(params["VAL_REST"]["R_DEST"]["VALUE"][1])
        else:
            tipo_rest = "Doblemente restrictivo"
            #Pendiente

        html = df.to_html(classes='content-table',index=False)


        with open(path,'w') as f:
            f.write(html_string.format(
                table=html,
                origin=params["ORIGIN"].source(),
                id_ori=params["ID_ORI"],
                var_ori=params["VAR_ORI"],
                dest=params["DEST"].source(),
                id_dest=params["ID_DEST"],
                var_dest=params["VAR_DEST"],
                friction_distance=params["FRICTION_DISTANCE"],
                output=params["OUTPUT"],
                unit=unit,
                tipo_rest=tipo_rest,
                tipo_filt=tipo_filt,
                values=values_r))

        if os.path.isfile(path):
            webbrowser.open_new_tab(path)


