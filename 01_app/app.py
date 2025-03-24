import sqlite3
import pandas as pd
from shiny import App, render, ui

# Conectar a la base de datos SQLite
conn = sqlite3.connect('data.db')  # Asegúrate de que 'data.db' exista
cursor = conn.cursor()
cursor.execute("SELECT * FROM industrias")  # Reemplaza 'industrias' por tu tabla
resultados = cursor.fetchall()
columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
df = pd.DataFrame(resultados, columns=columnas)  # Crear DataFrame

# Definir estilos CSS personalizados
custom_styles = """
<style>
    .custom-table {
        background-color: #ccffcc; /* Verde claro */
        border-collapse: collapse;
        width: 100%;
    }
    .custom-table th {
        background-color: #006400; /* Verde oscuro */
        color: white; /* Texto en blanco */
        padding: 10px;
    }
    .custom-table td {
        padding: 10px;
        border: 1px solid #006400; /* Bordes verde oscuro */
    }
</style>
"""

# Interfaz de usuario
app_ui = ui.page_fluid(
    ui.HTML(custom_styles),  # Incluir los estilos CSS personalizados
    ui.panel_title("Tabla personalizada desde SQLite"),
    ui.output_ui("tabla")  # Cambiar a output_ui para HTML personalizado
)

# Servidor
def server(input, output, session):
    @output
    @render.ui
    def tabla():
        # Renderizar la tabla como HTML con clase CSS personalizada
        return ui.HTML(df.to_html(classes="custom-table", index=False))

# Crear la aplicación
app = App(app_ui, server)