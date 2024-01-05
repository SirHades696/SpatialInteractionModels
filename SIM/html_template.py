html_RO = '''<!doctype html>
<html>
    <link rel="icon" href="{path}/test1.png" type="image/x-icon" />
    <head>
        <title>Reporte - Modelos de Interacción Espacial</title>
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

        .overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1;
        }}

        .popup {{
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            z-index: 2;
            border-radius: 10px;
        }}

        .close-button {{
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 20px;
            cursor: pointer;
        }}
        
        .text-popup {{
            margin:0;
        }}
        
        tbody[class^="grupo"] {{
            cursor: pointer;
        }}
        
    </style>
    </head>
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
            <p align="left"><b>Ruta de almacenamiento: </b><a href="file://{output}" target="_blank">{output}</a></p>
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
                <td>Accesibilidad (Desviación estándar)</td>
                </tr>
                <tr>
                <th>ACC_IND</th>
                <td>Accesibilidad Individual (Por unidad)</td>
                <th>TOT_DEST</th>
                <td>Total de destinos</td>
                </tr>
                <tr>
                <th>ACC_TOT</th>
                <td>Accesibilidad Total (Suma de todas las unidades)</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                </tr>
                </tbody>
            </table>
        </div>
        <div>
        {table}
        </div>
        <div class="overlay" id="overlay"></div>
        <div class="popup" id="popup">
        <span class="close-button" onclick="closePopup()">&times;</span>
        <h2>Información importante</h2>
        <p class="text-popup">Puedes dar clic sobre cada registro CVE_ORI de la tabla para desglosar la información</p>
        </div>
        <script>

            window.onload = function() {{
                var overlay = document.getElementById("overlay");
                var popup = document.getElementById("popup");
                overlay.style.display = "block";
                popup.style.display = "block";
            }};


            function closePopup() {{
                var overlay = document.getElementById("overlay");
                var popup = document.getElementById("popup");
                overlay.style.display = "none";
                popup.style.display = "none";
            }}
            
            var grupos = document.querySelectorAll("#tabla tbody");
            for (var i = 0; i < grupos.length; i++) {{
                grupos[i].addEventListener("click", function() {{
                    var filasOcultas = this.querySelectorAll(".oculto");
                    var filaSeleccionada = event.target.parentNode;
                    var grupoSeleccionado = filaSeleccionada.parentNode;
                    console.log(grupoSeleccionado)
                    for (var j = 0; j < filasOcultas.length; j++) {{
                        if (filasOcultas[j].style.display === "none") {{
                            filasOcultas[j].style.display = "table-row";
                            filasOcultas[j].style.background = "#e0fffc"
                            grupoSeleccionado.style.background = "#e0fffc"
                            filaSeleccionada.style.fontWeight = "bold"

                        }} else {{
                            filasOcultas[j].style.display = "none";
                            filasOcultas[j].style.background = "none"
                            grupoSeleccionado.style.background = "none"
                            filaSeleccionada.style.fontWeight = "normal"
                        }}
                    }}
                }});
            }}
    </script>
    </body>
</html>'''

html_RD = '''<!doctype html>
<html>
    <link rel="icon" href="{path}/test1.png" type="image/x-icon" />
    <head>
        <title>Reporte - Modelos de Interacción Espacial</title>
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
        
        .overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1;
        }}

        .popup {{
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            z-index: 2;
            border-radius: 10px;
        }}

        .close-button {{
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 20px;
            cursor: pointer;
        }}
        
        .text-popup {{
            margin:0;
        }}
        
        tbody[class^="grupo"]  {{
            cursor: pointer;
        }}

    </style>
    </head>
    <body>
        <h1 align="center">Reporte de ejecución (Completo)</h1>
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
            <p align="left"><b>Ruta de almacenamiento: </b><a href="file://{output}" target="_blank">{output}</a></p>
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
                <td>Flujos (Desviación estándar)</td>
                </tr>
                <tr>
                <th>FLUJ_IND</th>
                <td>Flujo Individual (Por unidad)</td>
                <th>FLUJ_TOT</th>
                <td>Flujo total recibido</td>
                </tr>
                </tbody>
            </table>
        </div>
        <div>
        {table}
        </div>
        <div class="overlay" id="overlay"></div>
        <div class="popup" id="popup">
        <span class="close-button" onclick="closePopup()">&times;</span>
        <h2>Información importante</h2>
        <p class="text-popup">Puedes dar clic sobre cada registro CVE_DEST de la tabla para desglosar la información</p>
        </div>
    <script>
            window.onload = function() {{
                var overlay = document.getElementById("overlay");
                var popup = document.getElementById("popup");
                overlay.style.display = "block";
                popup.style.display = "block";
            }};


            function closePopup() {{
                var overlay = document.getElementById("overlay");
                var popup = document.getElementById("popup");
                overlay.style.display = "none";
                popup.style.display = "none";
            }}
            
            var grupos = document.querySelectorAll("#tabla tbody");
            for (var i = 0; i < grupos.length; i++) {{
                grupos[i].addEventListener("click", function() {{
                    var filasOcultas = this.querySelectorAll(".oculto");
                    var filaSeleccionada = event.target.parentNode;
                    var grupoSeleccionado = filaSeleccionada.parentNode;
                    console.log(grupoSeleccionado)
                    for (var j = 0; j < filasOcultas.length; j++) {{
                        if (filasOcultas[j].style.display === "none") {{
                            filasOcultas[j].style.display = "table-row";
                            filasOcultas[j].style.background = "#e0fffc"
                            grupoSeleccionado.style.background = "#e0fffc"
                            filaSeleccionada.style.fontWeight = "bold"

                        }} else {{
                            filasOcultas[j].style.display = "none";
                            filasOcultas[j].style.background = "none"
                            grupoSeleccionado.style.background = "none"
                            filaSeleccionada.style.fontWeight = "normal"
                        }}
                    }}
                }});
            }}
    </script>
    </body>
</html>'''

html_RD_S = '''<!doctype html>
<html>
    <link rel="icon" href="{path}/test1.png" type="image/x-icon" />
    <head>
        <title>Reporte - Modelos de Interacción Espacial</title>
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
    </head>
    <body>
        <h1 align="center">Reporte de ejecución (General)</h1>
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
            <p align="left"><b>Ruta de almacenamiento: </b><a href="file://{output}" target="_blank">{output}</a></p>
        </div>
        <div>
            <table border="1" class="dataframe content-table">
                <tbody>
                <tr>
                <th>FLUJ_PROM</th>
                <td>Flujo promedio</td>
                <th>FLUJ_MEDIANA</th>
                <td>Flujo (Mediana)</td>
                </tr>
                <tr>
                <th>FLUJ_STD</th>
                <td>Flujo (Desviación estándar)</td>
                <th>FLUJ_MODA</th>
                <td>Flujo(s) (Moda)</td>
                </tr>
                <tr>
                <th>T_CEROS</th>
                <td>Total de ceros</td>
                <th></th>
                <td></td>
                </tr>
                <tr>
                <th>Flujos</th>
                <td>Flujos obtenidos</td>
                <th>Total</th>
                <td>Total de flujos identificados</td>
                </tr>
                </tbody>
            </table>
        </div>
        <div>
            <table border="1" class="dataframe content-table" id="tabla">
                <thead>
                    <tr style="text-align: right;">
                    <th>FLUJ_PROM</th>
                    <th>FLUJ_MEDIANA</th>
                    <th>FLUJ_STD</th>
                    <th>FLUJ_MODA</th>
                    <th>T_CEROS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>{s_prom}</td>
                    <td>{s_mediana}</td>
                    <td>{s_std}</td>
                    <td>{s_moda}</td>
                    <td>{c_ceros}</td>
                    </tr>
                </tbody>
                </table>
        </div>
        <div>
        {table}
        </div>
    </body>
</html>'''
