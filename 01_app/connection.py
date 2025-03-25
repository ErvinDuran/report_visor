import sqlite3
import pandas as pd

def get_data():
    DB_NAME = 'data.db'
    QUERY = """
            SELECT
                i.id AS industrias_id,
                d.departamento AS departamento,
                i.municipio,
                i.cod_reg,
                i.fecha_reg,
                i.caeb,
                c.circ AS circ_descripcion,
                i.nom_unidad,
                i.razon_social,
                i.rep_legal,
                i.latitud,
                i.longitud
            FROM 
                industrias i
            JOIN 
                departamentos d ON i.departamento = d.cod_depto
            JOIN 
                circ_std c ON i.circ = c.id;
            """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(QUERY,conn)
    return df

