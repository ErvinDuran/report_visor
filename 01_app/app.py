import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
from shiny import App, render, ui, reactive
from shinywidgets import output_widget, render_widget

from connection import *

df = get_data()
total = str(df.shape[0])
departamentos = sorted(df['departamento'].unique().tolist())
categorias = sorted(df['circ_descripcion'].unique().tolist())

# Interfaz de usuario
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_dark_mode(),
        ui.h6('En este dashboard se representan los datos registrados hasta la fecha actual'),
        ui.input_action_button('action','Todos'),
        ui.input_select('departamento','Selecciona un departamento:',departamentos),
        ui.input_select('municipio','Seleccione un municipio',['m1','m2'])
    ),
    ui.layout_column_wrap(
        ui.value_box(
            'Total de registros',
            ui.tags.div(
                ui.output_text('count'),
                style='font-size: 90px; font-weight: bold;'
            ),
            theme='orange',
            full_screen = False
            ),
            
        ui.value_box(
            'Registros categoría 1y2',
            'valor intermedio o cuerpo',
            'nota',
            theme='blue',
            full_screen = False
            ),
            
        ui.value_box(
            'Registros categoría 3',
            'valor intermedio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
        
        ui.value_box(
            'Registros categoría 4',
            'valor intermedio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
        
        fill = False     
    ),
        ui.layout_columns(
        ui.card(
            ui.card_header("U.I. Por departamentos"),
            output_widget('grafica'),
            full_screen=False,
        ),
        ui.card(
            ui.card_header("Detalle de datos registrados"),
            ui.output_data_frame("datos"),
            full_screen=True,
        ),
    ),
    title = 'Industrias registradas en SIAI'
)
# Servidor
def server(input, output, session):

    @reactive.calc
    def filtrado_dep():
        filt_df = df[df['departamento'].isin([input.departamento()])]
        return filt_df
    
    @render.text
    def count():
        return filtrado_dep().shape[0]

    @render.data_frame
    def datos():
        cols = [
            'industrias_id',
            'fecha_reg',
            'departamento',
            'municipio',
            'cod_reg',
            'caeb',
            'circ_descripcion'
        ]
        return render.DataGrid(filtrado_dep()[cols], filters=True)
    
    @render_widget
    def grafica():
        filt_df = df[df['departamento'].isin([input.departamento()])]
        filt_df['fecha_reg'] = pd.to_datetime(filt_df['fecha_reg'])
        filt_df['mes_anio'] = filt_df['fecha_reg'].dt.to_period('M')
        conteo = filt_df['mes_anio'].value_counts().sort_index().reset_index()
        conteo.columns = ['mes_anio', 'conteo']
        conteo = filt_df['mes_anio'].value_counts().sort_index().reset_index()
        conteo.columns = ['mes_anio', 'conteo']
        # Convertir la columna 'mes_anio' a formato string
        conteo['mes_anio'] = conteo['mes_anio'].astype(str)

        # Visualización con Plotly
        fig = px.bar(conteo, x='mes_anio', y='conteo', title='Registros por Mes y Año',
                    labels={'mes_anio': 'Mes y Año', 'conteo': 'Número de Registros'})
        return fig

# Crear la aplicación
app = App(app_ui, server)