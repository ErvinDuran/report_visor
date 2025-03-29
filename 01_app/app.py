import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

from shiny import App, render, ui, reactive
from shinywidgets import output_widget, render_widget
from connection import *

df = get_data()
total = str(df.shape[0])

# PREPARACIÓN DE DATOS DE CONSULTA Y FILTRO
departamentos = sorted(df['departamento'].unique().tolist())
departamentos.insert(0, 'TODOS')

def get_municipios(departamento):
    if departamento == 'TODOS':
        municipios = sorted(df['municipio'].unique().tolist())
    else:
        municipios = sorted(df[df['departamento'] == departamento]['municipio'].unique().tolist())
    municipios.insert(0, 'TODOS')
    return municipios

# Interfaz de usuario
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_dark_mode(),
        ui.input_select('departamento', 'Selecciona un departamento:', departamentos),
        ui.input_select('municipio', 'Seleccione un municipio:', get_municipios('TODOS'))
    ),
    ui.layout_column_wrap(
        ui.value_box(
            'Total de registros',
            ui.tags.div(
                ui.output_text('count'),
                style='font-size: 90px; font-weight: bold;'
            ),
            theme='bg-gradient-orange-red',
            full_screen=False
        ),
        fill=False
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
    title='Industrias registradas en SIAI'
)

# Servidor
def server(input, output, session):
    @reactive.calc
    def municipios_disponibles():
        return get_municipios(input.departamento())

    @reactive.effect
    def _():
        ui.update_select("municipio", choices=municipios_disponibles())

    @reactive.calc
    def filtrado_dep_mun():
        filt_df = df.copy()
        
        if input.departamento() != 'TODOS':
            filt_df = filt_df[filt_df['departamento'] == input.departamento()]
        
        if input.municipio() != 'TODOS':
            filt_df = filt_df[filt_df['municipio'] == input.municipio()]
        
        return filt_df

    @render.text
    def count():
        return filtrado_dep_mun().shape[0]

    @render.data_frame
    def datos():
        cols = ['industrias_id', 'fecha_reg', 'departamento', 'municipio', 'cod_reg', 'caeb', 'circ_descripcion']
        return render.DataGrid(filtrado_dep_mun()[cols], filters=True)

    @render_widget
    def grafica():
        filt_df = filtrado_dep_mun().copy()
        filt_df['fecha_reg'] = pd.to_datetime(filt_df['fecha_reg'])
        filt_df['anio'] = filt_df['fecha_reg'].dt.to_period('Y')
        conteo = filt_df['anio'].value_counts().sort_index().reset_index()
        conteo.columns = ['anio', 'conteo']
        conteo['anio'] = conteo['anio'].astype(str)
        
        fig = px.bar(conteo, x='anio', y='conteo', title='Registros por Año',
                     labels={'anio': 'Año', 'conteo': 'Número de Registros'})

        fig.update_layout(width=750, height=500)
        return fig

# Crear la aplicación
app = App(app_ui, server)
