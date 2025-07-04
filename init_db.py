# init_db.py
# Script para inicializar la base de datos

from database import initialize_database

if __name__ == "__main__":
    print("Inicializando la base de datos...")
    success = initialize_database()
    if success:
        print("Base de datos inicializada correctamente.")
    else:
        print("Error al inicializar la base de datos.")