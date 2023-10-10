html_RO = '''<!doctype html>
<html>
    <link rel="icon" href="{path}/test1.png" type="image/x-icon" />
    <head>
        <title>Reporte - Modelos de Interacción Espacial</title>
    </head>
    <style>

        * {{
            font-family: sans-serif;
        }}
        .content-table {{
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            min-width: 400px;
            border-radius: 5px 5px 0 0;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            border:none;
        }}

        .dataframe {{
            margin-left:auto;
            margin-right:auto;
            }}

        .content-table thead tr {{
            background-color: #0074cc;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
        }}

        .content-table th,
        .content-table td {{
            padding: 12px 15px;
            border:none;
        }}

        .content-table tbody tr {{
            border-bottom: 1px solid #dddddd;
        }}

        .content-table tbody tr:nth-of-type(even) {{
            background-color: #f3f3f3;
        }}

        .content-table tbody tr:last-of-type {{
            border-bottom: 2px solid #0074cc;
        }}

        .content-table tbody tr.active-row {{
            font-weight: bold;
            color: #0074cc;
        }}

        p {{
            margin-left: 5%;
            margin-top: 3px;
            margin-bottom: 3px;
        }}

    </style>
    <body>
        <h1 align="center">Reporte de ejecución</h1>
        <div>
            <p align="left"><b>Archivo de Orígen:</b> {origin}</p>
            <p align="left"><b>ID de orígen: </b>{id_ori}</p>
            <p align="left"><b>Campo de orígen: </b>{var_ori}</p>
            <p align="left"><b>Archivo de Destino: </b>{dest}</p>
            <p align="left"><b>ID de destino: </b>{id_dest}</p>
            <p align="left"><b>Campo de destino: </b>{var_dest}</p>
            <p align="left"><b>Fricción de distancia: </b>{friction_distance}</p>
            <p align="left"><b>Tipo de restricción: </b>{tipo_rest}</p>
            <p align="left"><b>Unidades de medida: </b>{unit}</p>
            <p align="left"><b>Tipo de filtro: </b>{tipo_filt}</p>
            <p align="left"><b>Valor(es): </b>{values}</p>
            <p align="left"><b>Ruta de almacenamiento: </b>{output}</p>
        </div>
        <div>
            <table border="1" class="dataframe content-table">
                <tbody>
                <tr>
                <th>CVE_ORI</th>
                <td>Clave de Orígen</td>
                <th>ACC_PROM</th>
                <td>Accesibilidad promedio</td>
                </tr>
                <tr>
                <th>CVE_DEST</th>
                <td>Clave de Destino</td>
                <th>ACC_STD</th>
                <td>Accesibilidad (Desviación Estándar)</td>
                </tr>
                <tr>
                <th>ACC_IND</th>
                <td>Accesibilidad Individual (por unidad)</td>
                <th>TOT_DEST</th>
                <td>Total de destinos</td>
                </tr>
                <tr>
                <th>ACC_TOT</th>
                <td>Accesibilidad Total (suma de todas las unidades)</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                </tr>
                </tbody>
            </table>
        </div>
        <div>
        {table}
        </div>
    </body>
</html>'''

html_RD = '''<!doctype html>
<html>
    <link rel="icon" href="{path}/test1.png" type="image/x-icon" />
    <head>
        <title>Reporte - Modelos de Interacción Espacial</title>
    </head>
    <style>

        * {{
            font-family: sans-serif;
        }}
        .content-table {{
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            min-width: 400px;
            border-radius: 5px 5px 0 0;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            border:none;
        }}

        .dataframe {{
            margin-left:auto;
            margin-right:auto;
            }}

        .content-table thead tr {{
            background-color: #0074cc;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
        }}

        .content-table th,
        .content-table td {{
            padding: 12px 15px;
            border:none;
        }}

        .content-table tbody tr {{
            border-bottom: 1px solid #dddddd;
        }}

        .content-table tbody tr:nth-of-type(even) {{
            background-color: #f3f3f3;
        }}

        .content-table tbody tr:last-of-type {{
            border-bottom: 2px solid #0074cc;
        }}

        .content-table tbody tr.active-row {{
            font-weight: bold;
            color: #0074cc;
        }}

        p {{
            margin-left: 5%;
            margin-top: 3px;
            margin-bottom: 3px;
        }}
        
        .oculto {{
        display: none;
            }}
            
    </style>
    <body>
        <h1 align="center">Reporte de ejecución</h1>
        <div>
            <p align="left"><b>Archivo de Orígen:</b> {origin}</p>
            <p align="left"><b>ID de orígen: </b>{id_ori}</p>
            <p align="left"><b>Campo de orígen: </b>{var_ori}</p>
            <p align="left"><b>Archivo de Destino: </b>{dest}</p>
            <p align="left"><b>ID de destino: </b>{id_dest}</p>
            <p align="left"><b>Campo de destino: </b>{var_dest}</p>
            <p align="left"><b>Fricción de distancia: </b>{friction_distance}</p>
            <p align="left"><b>Tipo de restricción: </b>{tipo_rest}</p>
            <p align="left"><b>Unidades de medida: </b>{unit}</p>
            <p align="left"><b>Tipo de filtro: </b>{tipo_filt}</p>
            <p align="left"><b>Valor(es): </b>{values}</p>
            <p align="left"><b>Ruta de almacenamiento: </b>{output}</p>
        </div>
        <div>
            <table border="1" class="dataframe content-table">
                <tbody>
                <tr>
                <th>CVE_DEST</th>
                <td>Clave de Destino</td>
                <th>FLUJ_PROM</th>
                <td>Flujo promedio</td>
                </tr>
                <tr>
                <th>CVE_ORI</th>
                <td>Clave de Orígen</td>
                <th>FLUJ_STD</th>
                <td>Flujos (Desviación Estándar)</td>
                </tr>
                <tr>
                <th>FLUJ_IND</th>
                <td>Flujo Individual (por unidad)</td>
                <th>FLUJ_TOT</th>
                <td>Flujo total recibido</td>
                </tr>
                </tbody>
            </table>
        </div>
        <div>
        {table}
        </div>
    </body>
    <script>
    var grupos = document.querySelectorAll("#tabla tbody");
    for (var i = 0; i < grupos.length; i++) {{
        grupos[i].addEventListener("click", function() {{
            var filasOcultas = this.querySelectorAll(".oculto");
            for (var j = 0; j < filasOcultas.length; j++) {{
                if (filasOcultas[j].style.display === "none") {{
                    filasOcultas[j].style.display = "table-row";
                }} else {{
                    filasOcultas[j].style.display = "none";
                }}
            }}
        }});
    }}
    </script>
</html>'''
