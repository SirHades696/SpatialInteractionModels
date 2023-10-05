import subprocess
import webbrowser
import os
import numpy as np
from collections import OrderedDict

from html_template import *

try:
    import pandas as pd
    from pyexcel_ods3 import save_data
except:
    subprocess.call(["pip", "install", "pandas"])
    subprocess.call(["pip", "install", "xlwt"])
    subprocess.call(["pip", "install", "pyexcel-ods3"])
    import pandas as pd
    from pyexcel_ods3 import save_data

class Reportes:

    def __init__(self, IDs:dict, values:dict, params:dict) -> None:
        self.params = params
        
        if self.params["RESTR"] == 0:
            df = pd.DataFrame.from_dict(IDs, orient='index')
            df_DEST = df.explode('DEST')
            new_df = pd.DataFrame.from_dict(values, orient='index')
            new_df_OI = new_df.explode('OI')
            new_df_OI['ACC_PROM'] = new_df.apply(lambda row: row['OI_SUM']/len(row['OI']), axis=1)
            new_df_OI['ACC_STD'] = new_df['OI'].apply(lambda x: np.std(x))
            self.df = pd.concat([df_DEST.reset_index(drop=True), new_df_OI.reset_index(drop=True)], axis=1)
            self.df['TOT_DEST'] = self.df.groupby('ORI')['DEST'].transform('count')
            self.df.rename(columns={'ORI': 'CVE_ORI',
                            'DEST': 'CVE_DEST',
                            'OI':'ACC_IND',
                            'OI_SUM':'ACC_TOT'}, inplace=True)
            
            pd.set_option('colheader_justify', 'center')
        elif self.params["RESTR"] == 1:
            df = pd.DataFrame.from_dict(IDs, orient='index')
            df_ORI = df.explode('ORI')
            new_df = pd.DataFrame.from_dict(values, orient='index')
            new_df_OI = new_df.explode('DJ')
            new_df_OI['FLUJ_PROM'] = new_df.apply(lambda row: row['DJ_SUM']/len(row['DJ']), axis=1)
            new_df_OI['FLUJ_STD'] = new_df['DJ'].apply(lambda x: np.std(x))
            self.df = pd.concat([df_ORI.reset_index(drop=True), new_df_OI.reset_index(drop=True)], axis=1)
            self.df.rename(columns={'DEST': 'CVE_DEST',
                            'ORI': 'CVE_ORI',
                            'DJ':'FLUJ_IND',
                            'DJ_SUM':'FLUJ_TOT'}, inplace=True)
            pd.set_option('colheader_justify', 'center')
        self.report_HTML()
        self.save_calcs()

    def report_HTML(self) -> None:
        path_file = os.path.dirname(os.path.abspath(__file__))
        path_icon = path_file.split("SIM")[0]

        path = self.params["OUTPUT"] + 'ReporteMIE.html'
        html = self.df.to_html(classes='content-table',index=False)

        unit, tipo_rest, tipo_filt, values_r = self.__aux_report()
        
        if self.params["RESTR"] == 0:
            with open(path,'w') as f:
                f.write(html_RO.format(
                    path=path_icon,
                    table=html,
                    origin=self.params["ORIGIN"].source(),
                    id_ori=self.params["ID_ORI"],
                    var_ori=self.params["VAR_ORI"],
                    dest=self.params["DEST"].source(),
                    id_dest=self.params["ID_DEST"],
                    var_dest=self.params["VAR_DEST"],
                    friction_distance=self.params["FRICTION_DISTANCE"],
                    output=self.params["OUTPUT"],
                    unit=unit,
                    tipo_rest=tipo_rest,
                    tipo_filt=tipo_filt,
                    values=values_r))
        elif self.params["RESTR"] == 1:
            with open(path,'w') as f:
                f.write(html_RD.format(
                    path=path_icon,
                    table=html,
                    origin=self.params["ORIGIN"].source(),
                    id_ori=self.params["ID_ORI"],
                    var_ori=self.params["VAR_ORI"],
                    dest=self.params["DEST"].source(),
                    id_dest=self.params["ID_DEST"],
                    var_dest=self.params["VAR_DEST"],
                    friction_distance=self.params["FRICTION_DISTANCE"],
                    output=self.params["OUTPUT"],
                    unit=unit,
                    tipo_rest=tipo_rest,
                    tipo_filt=tipo_filt,
                    values=values_r))

        if os.path.isfile(path):
            webbrowser.open_new_tab(path)

    def __aux_report(self) -> tuple:
        if self.params["UNIT"] == 0:
            unit = "Metros"
        elif self.params["UNIT"] == 1:
            unit = "Kilómetros"
        elif self.params["UNIT"] == 2:
            unit = "Millas"
        elif self.params["UNIT"] == 3:
            unit = "Pies"
        else:
            unit = "Yardas"

        tipo_rest, tipo_filt, values_r = "","",""
        if self.params["RESTR"] == 0:
            tipo_rest = "Restricción en el orígen"
            if self.params["VAL_REST"]["R_ORIG"]["OPTION"] == 0:
                tipo_filt = "Mayor que..."
                values_r = str(self.params["VAL_REST"]["R_ORIG"]["VALUE"][0])
            elif self.params["VAL_REST"]["R_ORIG"]["OPTION"] == 1:
                tipo_filt = "Menor que..."
                values_r = str(self.params["VAL_REST"]["R_ORIG"]["VALUE"][0])
            else:
                tipo_filt = "Rango"
                values_r = "Entre " + str(self.params["VAL_REST"]["R_ORIG"]["VALUE"][0]) + " y " + str(self.params["VAL_REST"]["R_ORIG"]["VALUE"][1])

        elif self.params["RESTR"] == 1:
            tipo_rest = "Restricción en el destino"
            if self.params["VAL_REST"]["R_DEST"]["OPTION"] == 0:
                tipo_filt = "Mayor que..."
                values_r = str(self.params["VAL_REST"]["R_DEST"]["VALUE"][0])
            elif self.params["VAL_REST"]["R_DEST"]["OPTION"] == 1:
                tipo_filt = "Menor que..."
                values_r = str(self.params["VAL_REST"]["R_DEST"]["VALUE"][0])
            else:
                tipo_filt = "Rango"
                values_r = "Entre " + str(self.params["VAL_REST"]["R_DEST"]["VALUE"][0]) + " y " + str(self.params["VAL_REST"]["R_DEST"]["VALUE"][1])
        else:
            tipo_rest = "Doblemente restrictivo"
            #Pendiente
            #Agregar cada unas de las  caracteristicas de los modelos doblemente restrictivos
        return unit, tipo_rest, tipo_filt, values_r

    def save_calcs(self):
        if self.params["SAVE"]["XLS"] == True:
            path_xls = self.params["OUTPUT"] + 'ReporteMIE.xls'
            chunk_size = 65500
            chunks = [self.df[i:i+chunk_size] for i in range(0, self.df.shape[0], chunk_size)]
            with pd.ExcelWriter(path_xls) as writer: #type:ignore
                for i, chunk in enumerate(chunks):
                    chunk.to_excel(writer, sheet_name='Resultados'+str(i), index=False)

        if self.params["SAVE"]["ODS"] == True:
            path_ods = self.params["OUTPUT"] + 'ReporteMIE.ods'
            df = self.df.astype(str)
            headers = list(df.columns)
            data = OrderedDict()
            chunks = [df[i:i+65500] for i in range(0, df.shape[0], 65500)]
            for i, chunk in enumerate(chunks):
                data.update({f"Resultados_{i+1}": [headers] + chunk.values.tolist()})
            save_data(path_ods, data)

        if self.params["SAVE"]["CSV"] == True:
            path_csv = self.params["OUTPUT"] + 'ReporteMIE.csv'
            self.df.to_csv(path_csv, index=False)

