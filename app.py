# app.py
import streamlit as st
import pandas as pd
import backend as be
import database as db # Necesario para crear la base de datos inicialmente

# Configuración básica de la página
st.set_page_config(page_title="Seguimiento de Horas", layout="wide")

st.title("📊 Sistema de Seguimiento de Horas - Equipo INFRA")

# Crear la base de datos y tablas si no existen al iniciar la app
conn_init = db.create_connection()
if conn_init:
    db.create_tables(conn_init)
    db.close_connection(conn_init)

# --- Sidebar ---
st.sidebar.header("Opciones")
menu_option = st.sidebar.radio("Navegación", ["Cargar Datos", "Ver Registros", "Análisis y Métricas"])

# --- Contenido Principal ---
if menu_option == "Cargar Datos":
    st.header("Cargar Archivo Excel")
    st.write("Por favor, sube el archivo Excel con los registros de horas.")

    uploaded_file = st.file_uploader("Selecciona el archivo .xlsx", type=["xlsx"])

    if uploaded_file is not None:
        # Mostrar una vista previa del archivo cargado
        try:
            df_preview = pd.read_excel(uploaded_file)
            st.subheader("Vista Previa del Archivo")
            st.dataframe(df_preview.head())

            if st.button("Procesar y Cargar Datos"):
                # Limpiar y procesar datos, y guardarlos en la BD
                processed_df = be.load_and_process_excel(uploaded_file)
                if not processed_df.empty:
                    st.success("Datos cargados exitosamente en la base de datos. Puedes verlos en la sección 'Ver Registros' o 'Análisis'.")
                    # Opcional: Actualizar la caché de datos si se desea mostrar inmediatamente
                    st.experimental_rerun()
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

elif menu_option == "Ver Registros":
    st.header("Todos los Registros")
    all_records_df = be.get_all_data_from_db()

    if not all_records_df.empty:
        st.write("Aquí se muestran todos los registros almacenados en la base de datos.")
        st.dataframe(all_records_df)

        # Opciones de filtrado
        st.subheader("Filtrar Registros")
        # Obtener listas únicas para los filtros
        tecnicos_unicos = ['Todos'] + sorted(all_records_df['tecnico'].unique().tolist())
        clientes_unicos = ['Todos'] + sorted(all_records_df['cliente'].unique().tolist())
        tipos_tarea_unicos = ['Todos'] + sorted(all_records_df['tipo_tarea'].unique().tolist())
        meses_unicos = ['Todos'] + sorted(all_records_df['mes'].unique().tolist())

        filtro_tecnico = st.selectbox("Filtrar por Técnico", tecnicos_unicos)
        filtro_cliente = st.selectbox("Filtrar por Cliente", clientes_unicos)
        filtro_tipo_tarea = st.selectbox("Filtrar por Tipo de Tarea", tipos_tarea_unicos)
        filtro_mes = st.selectbox("Filtrar por Mes", meses_unicos)

        # Aplicar filtros
        df_filtrado = all_records_df.copy()
        if filtro_tecnico != "Todos":
            df_filtrado = df_filtrado[df_filtrado['tecnico'] == filtro_tecnico]
        if filtro_cliente != "Todos":
            df_filtrado = df_filtrado[df_filtrado['cliente'] == filtro_cliente]
        if filtro_tipo_tarea != "Todos":
            df_filtrado = df_filtrado[df_filtrado['tipo_tarea'] == filtro_tipo_tarea]
        if filtro_mes != "Todos":
            df_filtrado = df_filtrado[df_filtrado['mes'] == filtro_mes]

        st.subheader("Registros Filtrados")
        st.dataframe(df_filtrado)
    else:
        st.info("No hay registros en la base de datos. Por favor, carga el archivo Excel.")

elif menu_option == "Análisis y Métricas":
    st.header("Análisis y Métricas de Horas")
    all_records_df = be.get_all_data_from_db()

    if not all_records_df.empty:
        # --- Resumen por Técnico ---
        st.subheader("Horas Totales por Técnico")
        summary_tecnico = be.get_summary_by_technician(all_records_df)
        st.dataframe(summary_tecnico)
        # Gráfico de barras para horas por técnico
        if not summary_tecnico.empty:
            st.bar_chart(summary_tecnico.set_index('Técnico')['Total Horas'])

        # --- Resumen por Cliente ---
        st.subheader("Horas Totales por Cliente")
        summary_cliente = be.get_summary_by_client(all_records_df)
        st.dataframe(summary_cliente)
        # Gráfico de barras para horas por cliente
        if not summary_cliente.empty:
            st.bar_chart(summary_cliente.set_index('Cliente')['Total Horas'])

        # --- Resumen por Tipo de Tarea ---
        st.subheader("Horas Totales por Tipo de Tarea")
        summary_tipo_tarea = be.get_summary_by_task_type(all_records_df)
        st.dataframe(summary_tipo_tarea)
        # Gráfico de pastel para tipos de tarea
        if not summary_tipo_tarea.empty:
            st.write("Distribución de Horas por Tipo de Tarea")
            import altair as alt
            
            # Crear un gráfico de pastel con Altair
            pie_chart = alt.Chart(summary_tipo_tarea).mark_arc().encode(
                theta=alt.Theta(field="Total Horas", type="quantitative"),
                color=alt.Color(field="Tipo de Tarea", type="nominal"),
                tooltip=['Tipo de Tarea', 'Total Horas']
            ).properties(
                title='Distribución de Horas por Tipo de Tarea'
            )
            
            st.altair_chart(pie_chart, use_container_width=True)

        # --- Resumen por Mes ---
        st.subheader("Horas Totales por Mes")
        summary_mes = be.get_summary_by_month(all_records_df)
        st.dataframe(summary_mes)
        # Gráfico de línea para horas por mes
        if not summary_mes.empty:
            st.write("Evolución de Horas Mensuales")
            st.line_chart(summary_mes.set_index('Mes')['Total Horas'])

        # --- Top 5 Técnicos con Desglose por Cliente ---
        st.subheader("Top 5 Técnicos con Desglose por Cliente")
        if st.button("Mostrar Top 5 Técnicos y Desglose por Cliente"):
            top_tecnicos, desglose_clientes = be.get_top_technicians_with_client_breakdown(all_records_df)
            
            if not top_tecnicos.empty:
                st.write("### Top 5 Técnicos con Más Horas Trabajadas")
                st.dataframe(top_tecnicos)
                
                # Gráfico de barras para los top 5 técnicos
                st.bar_chart(top_tecnicos.set_index('Técnico')['Total Horas'])
                
                st.write("### Desglose de Horas por Cliente para cada Técnico")
                # Mostrar desglose por cliente para cada técnico
                for tecnico in top_tecnicos['Técnico']:
                    st.write(f"**{tecnico}**")
                    desglose_tecnico = desglose_clientes[desglose_clientes['Técnico'] == tecnico]
                    st.dataframe(desglose_tecnico[['Cliente', 'Horas']])
                    
                    # Gráfico de barras para el desglose por cliente
                    st.bar_chart(desglose_tecnico.set_index('Cliente')['Horas'])

    else:
        st.info("No hay registros para analizar. Por favor, carga el archivo Excel.")