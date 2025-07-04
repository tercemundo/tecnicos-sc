# backend.py
import pandas as pd
import database as db
import utils
import streamlit as st

@st.cache_data # Cachear los datos cargados para mejorar el rendimiento
def load_and_process_excel(uploaded_file):
    """Carga el archivo Excel, lo preprocesa y lo guarda en la base de datos."""
    try:
        df = pd.read_excel(uploaded_file)
        df_processed = utils.preprocess_data(df)

        conn = db.create_connection()
        if not conn:
            st.error("No se pudo conectar a la base de datos.")
            return pd.DataFrame() # Devolver un DataFrame vacío en caso de error

        # Insertar datos en la base de datos
        inserted_count = 0
        for index, row in df_processed.iterrows():
            tecnico_id = db.add_or_get_id(conn, 'tecnicos', row['tecnico'])
            cliente_id = db.add_or_get_id(conn, 'clientes', row['cliente'])
            tipo_tarea_id = db.add_or_get_id(conn, 'tipos_tarea', row['tipo_tarea'])

            registro_data = (
                row['fecha'].strftime('%Y-%m-%d'), # Formato YYYY-MM-DD para SQLite DATE
                tecnico_id,
                cliente_id,
                tipo_tarea_id,
                row['tarea_realizada_manera'],
                row['n_ticket'],
                row['tiempo'],
                row['descripcion'],
                row['mes']
            )
            if db.add_registro(conn, registro_data):
                inserted_count += 1

        db.close_connection(conn)
        st.success(f"Se cargaron {inserted_count} registros exitosamente.")
        return df_processed # Devolver los datos procesados para visualización inmediata

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return pd.DataFrame()

def get_all_data_from_db():
    """Obtiene todos los registros de la base de datos."""
    conn = db.create_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos.")
        return pd.DataFrame()
    df = db.get_all_registros_df(conn)
    db.close_connection(conn)
    return df

def get_summary_by_technician(df):
    """Calcula el resumen de horas por técnico."""
    if df.empty:
        return pd.DataFrame()
    summary = df.groupby('tecnico')['tiempo'].sum().reset_index()
    summary.columns = ['Técnico', 'Total Horas']
    return summary

def get_summary_by_client(df):
    """Calcula el resumen de horas por cliente."""
    if df.empty:
        return pd.DataFrame()
    summary = df.groupby('cliente')['tiempo'].sum().reset_index()
    summary.columns = ['Cliente', 'Total Horas']
    return summary

def get_summary_by_task_type(df):
    """Calcula el resumen de horas por tipo de tarea."""
    if df.empty:
        return pd.DataFrame()
    summary = df.groupby('tipo_tarea')['tiempo'].sum().reset_index()
    summary.columns = ['Tipo de Tarea', 'Total Horas']
    return summary

def get_summary_by_month(df):
    """Calcula el resumen de horas por mes."""
    if df.empty:
        return pd.DataFrame()
    summary = df.groupby('mes')['tiempo'].sum().reset_index()
    summary.columns = ['Mes', 'Total Horas']
    # Convertir número de mes a nombre para mejor visualización
    month_map = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    summary['Mes'] = summary['Mes'].map(month_map)
    return summary