# Sistema de Seguimiento de Horas - Equipo INFRA

Esta aplicación permite realizar un seguimiento detallado de las horas trabajadas por técnicos en diferentes clientes y tipos de tareas. Proporciona una interfaz web para cargar datos desde archivos Excel, visualizar registros y generar análisis y métricas.

## Características

- **Carga de Datos**: Importación de registros desde archivos Excel
- **Visualización de Registros**: Vista detallada de todos los registros con opciones de filtrado
- **Análisis y Métricas**: Gráficos y resúmenes estadísticos por técnico, cliente, tipo de tarea y mes
- **Base de Datos**: Almacenamiento persistente en SQLite

## Requisitos Previos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar o descargar este repositorio

```bash
git clone <url-del-repositorio>
cd horas-sc
```

### 2. Crear y activar un entorno virtual (opcional pero recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Configuración de la Base de Datos

La aplicación crea automáticamente la base de datos SQLite al iniciar. Si necesitas inicializar manualmente la base de datos, puedes ejecutar:

```bash
python init_db.py
```

## Estructura del Proyecto

- `app.py`: Aplicación principal de Streamlit
- `backend.py`: Lógica de negocio y procesamiento de datos
- `database.py`: Funciones para interactuar con la base de datos SQLite
- `utils.py`: Funciones de utilidad para procesamiento de datos
- `init_db.py`: Script para inicializar la base de datos manualmente
- `seguimiento_horas.db`: Archivo de base de datos SQLite

## Ejecución de la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web predeterminado. Si no se abre automáticamente, puedes acceder a ella en: http://localhost:8501

## Uso de la Aplicación

### Cargar Datos

1. Selecciona "Cargar Datos" en el menú lateral
2. Haz clic en "Browse files" para seleccionar un archivo Excel
3. Verifica la vista previa de los datos
4. Haz clic en "Procesar y Cargar Datos" para guardar los registros en la base de datos

### Ver Registros

1. Selecciona "Ver Registros" en el menú lateral
2. Utiliza los filtros para buscar registros específicos por técnico, cliente, tipo de tarea o mes

### Análisis y Métricas

1. Selecciona "Análisis y Métricas" en el menú lateral
2. Explora los diferentes gráficos y resúmenes estadísticos

## Formato del Archivo Excel

El archivo Excel debe contener las siguientes columnas:

- `Fecha`: Fecha del registro (formato fecha)
- `Técnico`: Nombre del técnico
- `Cliente`: Nombre del cliente
- `Tipo tarea`: Categoría de la tarea realizada
- `Tarea Realizada de manera:`: Método de realización (ej. Remoto, Presencial)
- `N° de Ticket`: Número de ticket o referencia
- `Tiempo:`: Horas dedicadas (formato numérico)
- `Breve Descripción`: Descripción de la tarea
- `Mes`: Número del mes (1-12)

## Solución de Problemas

### Error al cargar el archivo Excel

- Verifica que el formato del archivo Excel sea correcto y contenga todas las columnas requeridas
- Asegúrate de que los datos de fecha y tiempo estén en formatos reconocibles

### Error de conexión a la base de datos

- Verifica que tengas permisos de escritura en el directorio del proyecto
- Intenta inicializar manualmente la base de datos con `python init_db.py`

## Licencia

[Especificar la licencia del proyecto]