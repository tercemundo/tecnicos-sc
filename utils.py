# utils.py
import pandas as pd
import re

def clean_time_string(time_str):
    """Limpia la cadena de tiempo para convertirla a float."""
    if isinstance(time_str, (int, float)):
        return float(time_str)
    if isinstance(time_str, str):
        # Reemplazar comas por puntos para decimales y eliminar caracteres no numéricos (excepto el punto)
        cleaned_str = time_str.replace(',', '.').strip()
        # Intentar eliminar cualquier cosa que no sea un dígito o un punto decimal
        numeric_part = re.findall(r'[\d.]+', cleaned_str)
        if numeric_part:
            return float(numeric_part[0])
    return 0.0 # Valor por defecto si no se puede parsear

def preprocess_data(df):
    """Limpia y preprocesa el DataFrame cargado del Excel."""
    # Asegurarse de que las columnas relevantes existan
    required_columns = ['Fecha', 'Técnico', 'Cliente', 'Tipo tarea', 'Tarea Realizada de manera:', 'N° de Ticket', 'Tiempo:', 'Breve Descripción', 'Mes']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"La columna requerida '{col}' no se encuentra en el archivo Excel.")

    # Renombrar columnas para facilitar el acceso
    df = df.rename(columns={
        'Fecha': 'fecha',
        'Técnico': 'tecnico',
        'Cliente': 'cliente',
        'Tipo tarea': 'tipo_tarea',
        'Tarea Realizada de manera:': 'tarea_realizada_manera',
        'N° de Ticket': 'n_ticket',
        'Tiempo:': 'tiempo_str', # Mantener como string inicialmente para limpieza
        'Breve Descripción': 'descripcion',
        'Mes': 'mes'
    })

    # Limpiar y convertir la columna 'tiempo'
    df['tiempo'] = df['tiempo_str'].apply(clean_time_string)

    # Convertir 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Manejar valores nulos
    df = df.dropna(subset=['fecha', 'tecnico', 'cliente', 'tipo_tarea', 'tiempo']) # Eliminar filas con datos esenciales faltantes

    # Asegurar que el mes y tiempo sean numéricos
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce').fillna(0).astype(int)
    # 'tiempo' ya se procesó como float

    # Eliminar columnas temporales o innecesarias
    df = df.drop(columns=['tiempo_str'])

    return df