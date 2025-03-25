import sqlite3
import pandas as pd
from shiny import App, render, ui
from connection import *

df = get_data()
total = str(df.shape[0])
departamentos = sorted(df['departamento'].unique().tolist())

# Interfaz de usuario
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_dark_mode(),
        ui.h6('En este dashboard se representan los datos registrados hasta la fecha actual'),
        ui.input_select('departamento','Selecciona un departamento:',departamentos)
    ),
    ui.layout_column_wrap(
        ui.value_box(
            'Valor superior',
            'valor intermadio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
            
        ui.value_box(
            'Valor superior',
            'valor intermedio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
            
        ui.value_box(
            'Valor superior',
            'valor intermadio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
        
        ui.value_box(
            'Valor superior',
            'valor intermadio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
        
        fill = False     
    ),
    title = 'Industrias registradas en SIAI'
)
# Servidor
def server(input, output, session):
    pass

# Crear la aplicación
app = App(app_ui, server)