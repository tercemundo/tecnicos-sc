# database.py
import sqlite3
import pandas as pd

DATABASE_NAME = 'seguimiento_horas.db'

def create_connection():
    """Crea una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn

def create_tables(conn):
    """Crea las tablas necesarias en la base de datos."""
    cursor = conn.cursor()

    # Tabla de Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')

    # Tabla de Técnicos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')

    # Tabla de Tareas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipos_tarea (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')

    # Tabla principal de Registros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            tecnico_id INTEGER NOT NULL,
            cliente_id INTEGER NOT NULL,
            tipo_tarea_id INTEGER NOT NULL,
            tarea_realizada_manera TEXT,
            n_ticket TEXT,
            tiempo REAL NOT NULL,
            descripcion TEXT,
            mes INTEGER NOT NULL,
            FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (tipo_tarea_id) REFERENCES tipos_tarea(id)
        )
    ''')
    conn.commit()

def add_or_get_id(conn, table_name, name):
    """Añade un nombre a una tabla si no existe y devuelve su ID."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {table_name} WHERE nombre = ?", (name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(f"INSERT INTO {table_name} (nombre) VALUES (?)", (name,))
        conn.commit()
        return cursor.lastrowid

def add_registro(conn, registro_data):
    """Añade un registro a la tabla de registros."""
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO registros (fecha, tecnico_id, cliente_id, tipo_tarea_id, tarea_realizada_manera, n_ticket, tiempo, descripcion, mes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', registro_data)
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error de integridad al insertar registro: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error al insertar registro: {e}")
        return False

def get_all_registros_df(conn):
    """Obtiene todos los registros como un DataFrame de Pandas."""
    query = """
    SELECT
        r.id,
        r.fecha,
        t.nombre AS tecnico,
        c.nombre AS cliente,
        tt.nombre AS tipo_tarea,
        r.tarea_realizada_manera,
        r.n_ticket,
        r.tiempo,
        r.descripcion,
        r.mes
    FROM registros r
    JOIN tecnicos t ON r.tecnico_id = t.id
    JOIN clientes c ON r.cliente_id = c.id
    JOIN tipos_tarea tt ON r.tipo_tarea_id = tt.id
    """
    return pd.read_sql_query(query, conn)

def close_connection(conn):
    """Cierra la conexión a la base de datos."""
    if conn:
        conn.close()
        print("Conexión a la base de datos cerrada.")

# Función para inicializar la base de datos explícitamente
def initialize_database():
    """Inicializa la base de datos y crea las tablas si no existen."""
    conn = create_connection()
    if conn:
        create_tables(conn)
        print("Base de datos inicializada correctamente.")
        close_connection(conn)
        return True
    return False

# Inicializar la base de datos al importar este módulo
conn = create_connection()
if conn:
    create_tables(conn)
    close_connection(conn)