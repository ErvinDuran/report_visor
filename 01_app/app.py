import sqlite3
import pandas as pd
<<<<<<< HEAD
=======
import matplotlib.pyplot as plt
import numpy as np

>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060
from shiny import App, render, ui
from connection import *

df = get_data()
total = str(df.shape[0])
departamentos = sorted(df['departamento'].unique().tolist())
<<<<<<< HEAD
=======
categorias = sorted(df['circ_descripcion'].unique().tolist())
print(categorias)
>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060

# Interfaz de usuario
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_dark_mode(),
        ui.h6('En este dashboard se representan los datos registrados hasta la fecha actual'),
<<<<<<< HEAD
=======
        ui.input_action_button('action','Todos'),
>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060
        ui.input_select('departamento','Selecciona un departamento:',departamentos)
    ),
    ui.layout_column_wrap(
        ui.value_box(
<<<<<<< HEAD
            'Valor superior',
            'valor intermadio o cuerpo'
            ,'nota',
            theme='blue',
=======
            'Total de registros',
            'valor intermadio o cuerpo'
            ,'nota',
            theme='orange',
>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060
            full_screen = False
            ),
            
        ui.value_box(
<<<<<<< HEAD
            'Valor superior',
=======
            'Registros categoría 1y2',
>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060
            'valor intermedio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
            
        ui.value_box(
<<<<<<< HEAD
            'Valor superior',
=======
            'Registros categoría 3',
>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060
            'valor intermadio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
        
        ui.value_box(
<<<<<<< HEAD
            'Valor superior',
=======
            'Registros categoría 4',
>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060
            'valor intermadio o cuerpo'
            ,'nota',
            theme='blue',
            full_screen = False
            ),
        
        fill = False     
    ),
<<<<<<< HEAD
=======
        ui.layout_columns(
        ui.card(
            ui.card_header("U.I. Por departamentos"),
            ui.output_plot('grafica'),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Detalle de datos registrados"),
            ui.output_data_frame("datos"),
            full_screen=True,
        ),
    ),
>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060
    title = 'Industrias registradas en SIAI'
)
# Servidor
def server(input, output, session):
<<<<<<< HEAD
    pass
=======

    @render.data_frame
    def datos():
        cols = [
            'industrias_id',
            'departamento',
            'municipio',
            'cod_reg',
            'caeb',
            'circ_descripcion'
        ]
        return render.DataGrid(df[cols])
    
    @render.plot
    def grafica():
        # Agrupar datos por departamento y calcular la suma de cantidades
        agrupados = df.groupby("departamento")["industrias_id"].count()
        totales = agrupados.tolist()  # Convertir a lista de valores
        departamentos = agrupados.index.tolist()  # Nombres de departamentos como lista


        # Función para mostrar porcentaje y valores absolutos
        def func(pct, allvals):
            absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
            return f"{pct:.1f}%\n({absolute:d})"

        # Crear el gráfico de pastel
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
        wedges, texts, autotexts = ax.pie(
            totales,
            autopct=lambda pct: func(pct, totales),
            textprops=dict(color="w"),
            startangle=90
        )

        # Agregar leyenda
        ax.legend(
            wedges, departamentos,
            title="Departamentos",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        # Personalización del título
        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title("Distribución por Departamento")

        return fig

>>>>>>> e0d0914de5581ab3a195dab0c05909c5709bd060

# Crear la aplicación
app = App(app_ui, server)