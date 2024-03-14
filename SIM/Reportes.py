import subprocess
import webbrowser
import os
import numpy as np
from collections import OrderedDict

from html_template import *

try:
    import pandas as pd
    from pyexcel_ods3 import save_data
    from bs4 import BeautifulSoup
    import plotly.express as px
except:
    subprocess.call(["pip", "install", "pandas"])
    subprocess.call(["pip", "install", "pyexcel-ods3"])
    subprocess.call(["pip", "install", "beautifulsoup4"])
    subprocess.call(["pip", "install", "plotly"])
    import pandas as pd
    from pyexcel_ods3 import save_data
    from bs4 import BeautifulSoup
    import plotly.express as px
    
class Reportes:

    def __init__(self, IDs:dict, values:dict, params:dict) -> None:
        self.params = params
        
        if self.params["RESTR"] == 0:
            df = pd.DataFrame.from_dict(IDs, orient='index')
            df_DEST = df.explode('ORI')
            new_df = pd.DataFrame.from_dict(values, orient='index')
            new_df_OI = new_df.explode('OI')
            new_df_OI['ACC_PROM'] = new_df.apply(lambda row: row['OI_SUM']/len(row['OI']), axis=1)
            new_df_OI['ACC_STD'] = new_df['OI'].apply(lambda x: np.std(x))
            self.df = pd.concat([df_DEST.reset_index(drop=True), new_df_OI.reset_index(drop=True)], axis=1)
            self.df['TOT_DEST'] = self.df.groupby('DEST')['ORI'].transform('count')
            self.df.rename(columns={'ORI': 'CVE_ORI',
                            'DEST': 'CVE_DEST',
                            'OI':'ACC_IND',
                            'OI_SUM':'ACC_TOT'}, inplace=True)
            self.df['CVE_ORI'] = self.df['CVE_ORI'].astype(str)
            self.df['CVE_DEST'] = self.df['CVE_DEST'].astype(str)
            self.df['ACC_IND'] = self.df['ACC_IND'].astype(float).round(4)
            self.df['ACC_TOT'] = self.df['ACC_TOT'].astype(float).round(4)
            self.df['ACC_PROM'] = self.df['ACC_PROM'].astype(float).round(4)
            self.df['ACC_STD'] = self.df['ACC_STD'].astype(float).round(4)
            pd.set_option('colheader_justify', 'center')
            
        elif self.params["RESTR"] == 1:
            if self.params["REPORTS"][0] == True:
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
                self.df['CVE_ORI'] = self.df['CVE_ORI'].astype(str)
                self.df['CVE_DEST'] = self.df['CVE_DEST'].astype(str)
                self.df['FLUJ_IND'] = self.df['FLUJ_IND'].astype(float).round(4)
                self.df['FLUJ_TOT'] = self.df['FLUJ_TOT'].astype(int)
                self.df['FLUJ_PROM'] = self.df['FLUJ_PROM'].astype(float).round(4)
                self.df['FLUJ_STD'] = self.df['FLUJ_STD'].astype(float).round(4)
                
            if self.params["REPORTS"][1] == True:
                aux = [int(v['DJ_SUM']) for v in values.values()]
                ceros = [aux for val in aux if val == 0]
                self.c_ceros = len(ceros)
                self.valores_dj =  [val for val in aux if val != 0]
                serie = pd.Series(self.valores_dj)
                conteo = serie.value_counts()
                self.s_prom = round(serie.mean(),4)
                self.s_mediana = round(serie.median(),4)
                self.s_std = round(serie.std(),4)
                s_moda = serie.mode()
                self.s_moda = ', '.join(map(str, s_moda))
                self.df2 = pd.DataFrame(conteo).reset_index()
                self.df2.columns = ['Flujos', 'Total']
            
        self.report_HTML()
        self.save_calcs()

    def report_HTML(self) -> None:
        path_file = os.path.dirname(os.path.abspath(__file__))
        path_icon = path_file.split("SIM")[0]
        unit, tipo_rest, tipo_filt, values_r = self.__aux_report()
        
        path_reports = self.params["OUTPUT"] + "Reportes/"
        if not os.path.exists(path_reports):
            os.makedirs(path_reports)
            os.chmod(path_reports, 0o777)
        
        if self.params["RESTR"] == 0:
            path = path_reports + self.params["PREFIJO"] + '_ReporteMIE_RO.html'
            html = self.df.to_html(classes='content-table" id="tabla',index=False)
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table')
            df = pd.read_html(str(table))[0]
            table = soup.find('table')
            df = pd.read_html(str(table))[0]
            grouped = df.groupby('CVE_DEST')
            new_html = ""
            for i, (name, group) in enumerate(grouped):
                tbody = soup.new_tag('tbody', **{'class': f'grupo{i+1}'})
                for j, row in group.iterrows():
                    tr = soup.new_tag('tr')
                    if j != group.first_valid_index():
                        tr['class'] = 'oculto'
                    for cell in row:
                        td = soup.new_tag('td')
                        td.string = str(cell)
                        tr.append(td)
                    tbody.append(tr)
                new_html += str(tbody)
            table.tbody.replace_with(BeautifulSoup(new_html, 'html.parser'))
            html = table.prettify()
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

            if os.path.isfile(path):
                webbrowser.open_new_tab(path)

            headers = self.df.columns.tolist()
            dp_hd = [h for h in headers if h not in ['CVE_DEST', 'ACC_TOT']]
            df = self.df.drop(columns=dp_hd)
            df_gp = df.groupby('CVE_DEST').first().reset_index() 
            df_filt = df_gp.loc[df_gp['ACC_TOT'] != 0]
            bp_path = self.boxplot(df_filt,
                        "ACC_TOT",
                        "Accesibilidad en el Origen",
                        df_filt.columns,
                        "RO")
            
            if os.path.isfile(bp_path):
                webbrowser.open_new_tab(bp_path)
                
        elif self.params["RESTR"] == 1:
            if self.params["REPORTS"][0] == True:
                path = path_reports + self.params["PREFIJO"] + '_ReporteMIE_RD.html'
                html = self.df.to_html(classes='content-table" id="tabla',index=False)
                soup = BeautifulSoup(html, 'html.parser')
                
                table = soup.find('table')
                df = pd.read_html(str(table))[0]
                table = soup.find('table')
                df = pd.read_html(str(table))[0]
                grouped = df.groupby('CVE_DEST')
                new_html = ""
                for i, (name, group) in enumerate(grouped):
                    tbody = soup.new_tag('tbody', **{'class': f'grupo{i+1}'})
                    for j, row in group.iterrows():
                        tr = soup.new_tag('tr')
                        if j != group.first_valid_index():
                            tr['class'] = 'oculto'
                        for cell in row:
                            td = soup.new_tag('td')
                            td.string = str(cell)
                            tr.append(td)
                        tbody.append(tr)
                    new_html += str(tbody)
                table.tbody.replace_with(BeautifulSoup(new_html, 'html.parser'))
                html = table.prettify()
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
                
                headers = self.df.columns.tolist()
                dp_hd = [h for h in headers if h not in ['CVE_DEST', 'FLUJ_TOT']]
                df = self.df.drop(columns=dp_hd)
                df_gp = df.groupby('CVE_DEST').first().reset_index() 
                df_filt = df_gp.loc[df_gp['FLUJ_TOT'] != 0]
                bp_path = self.boxplot(df_filt,
                            "FLUJ_TOT",
                            "Distribución de Flujos en el Destino",
                            df_filt.columns,
                            "RD")
                
                if os.path.isfile(bp_path):
                    webbrowser.open_new_tab(bp_path)
            
            if self.params["REPORTS"][1] == True:
                path = path_reports + self.params["PREFIJO"] + '_ReporteMIE_RDGeneral.html'
                html = self.df2.to_html(classes='content-table" id="tabla',index=False)
                soup = BeautifulSoup(html, 'html.parser')
                
                rows = soup.find_all('tr')
                for row in rows:
                    if 'style' in row.attrs:
                        del row['style']
                    row['style'] = 'text-align:center;'
                html = soup.prettify()

                with open(path,'w') as f:
                    f.write(html_RD_S.format(
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
                        values=values_r,
                        s_prom = self.s_prom,
                        s_mediana = self.s_mediana,
                        s_std = self.s_std,
                        s_moda = self.s_moda,
                        c_ceros = self.c_ceros))

                if os.path.isfile(path):
                    webbrowser.open_new_tab(path)
                df = pd.DataFrame(self.valores_dj, columns=["Flujos"])
                bp_path = self.boxplot(df,
                            "Flujos",
                            "Distribución de Flujos en el Destino (General)",
                            None,
                            "RDGeneral")
                
                if os.path.isfile(bp_path):
                    webbrowser.open_new_tab(bp_path)
                    
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

    def save_calcs(self) -> None:
        if any(self.params["SAVE"][ext] for ext in ["XLS", "ODS", "CSV"]):
            path_calcs = os.path.join(self.params["OUTPUT"], "Estadisticas")
            if not os.path.exists(path_calcs):
                os.makedirs(path_calcs)
                os.chmod(path_calcs, 0o777)
            
        if self.params["SAVE"]["XLS"] == True:
            path_xls = path_calcs + self.params["PREFIJO"] + '_ReporteMIE.xls'
            chunk_size = 65500
            chunks = [self.df[i:i+chunk_size] for i in range(0, self.df.shape[0], chunk_size)]
            with pd.ExcelWriter(path_xls) as writer: #type:ignore
                for i, chunk in enumerate(chunks):
                    chunk.to_excel(writer, sheet_name='Resultados'+str(i), index=False)

        if self.params["SAVE"]["ODS"] == True:
            path_ods = path_calcs + self.params["PREFIJO"] +'_ReporteMIE.ods'
            df = self.df.astype(str)
            headers = list(df.columns)
            data = OrderedDict()
            chunks = [df[i:i+65500] for i in range(0, df.shape[0], 65500)]
            for i, chunk in enumerate(chunks):
                data.update({f"Resultados_{i+1}": [headers] + chunk.values.tolist()})
            save_data(path_ods, data)

        if self.params["SAVE"]["CSV"] == True:
            path_csv = path_calcs + self.params["PREFIJO"] + '_ReporteMIE.csv'
            self.df.to_csv(path_csv, index=False)
            
    def boxplot(self, data:pd.DataFrame, column:str, plot_title:str, hv_dt:pd.DataFrame.columns, tr:str) -> str:
        path_plots = self.params["OUTPUT"] + "Graficas/"
        if not os.path.exists(path_plots):
            os.makedirs(path_plots)
            os.chmod(path_plots, 0o777)
        fig = px.box(data,y=column, points="all", hover_data=hv_dt, title=plot_title, notched=True)
        path = path_plots + self.params["PREFIJO"] + "_BoxPlot_" + tr + ".html"
        fig.write_html(path)
        return path