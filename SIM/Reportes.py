import subprocess
import sys
import webbrowser
import os
import numpy as np

from html_template import html_string

try:
    import pandas as pd
    from pyexcel_ods import save_data
    import xlwt
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyexcel-ods"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "xlwt"])
    import pandas as pd
    from pyexcel_ods import save_data
    import xlwt

class Reportes:

    def __init__(self, IDs:dict, values:dict, params:dict) -> None:
        self.params = params
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

    def report_HTML(self) -> None:
        path = self.params["OUTPUT"] + 'ReporteMIE.html'
        html = self.df.to_html(classes='content-table',index=False)

        unit, tipo_rest, tipo_filt, values_r = self.__aux_report()

        with open(path,'w') as f:
            f.write(html_string.format(
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
        return unit, tipo_rest, tipo_filt, values_r

    def report_XLS(self) -> None:
        path = self.params["OUTPUT"] + 'ReporteMIE.xls'
        with pd.ExcelWriter(path) as writer: #type: ignore
            self.df.to_excel(writer, index=False, sheet_name="Resultados")

    def report_ODS(self) -> None:
        path = self.params["OUTPUT"] + 'ReporteMIE.ods'
        headers = list(self.df.columns)
        save_data(path, {"Resultados": [headers] + self.df.values.tolist()})

