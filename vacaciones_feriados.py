# vacaciones_feriados.py 
import streamlit as st
import pandas as pd
from datetime import datetime, date
from io import BytesIO
import base64
import os
import sqlite3

# =========================
# CONFIGURACIÓN ENCABEZADO
# =========================
COLOR_FONDO = "#0F69B4"
IMAGEN_LOCAL = "LOGO-PROPIO-ISL-2023-CMYK-01.png"
TITULO = "VACACIONES Y PERMISOS"
SUBTITULO = "Sección de Coordinación Territorial"
DB_FILE = "vacaciones_permisos.db"

def image_to_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

img_base64 = image_to_base64(IMAGEN_LOCAL)
img_src = f"data:image/png;base64,{img_base64}"

# =========================
# ESTILOS GLOBALES COMPACTOS
# =========================
st.set_page_config(page_title="VACACIONES Y PERMISOS",
                   page_icon="📅", layout="wide", initial_sidebar_state="collapsed")

st.markdown(f"""
    <style>
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: {COLOR_FONDO};
            height: 75px;
            width: 100%;
            color: white;
            position: relative;
        }}
        .header-logo {{
            position: absolute;
            left: 15px;
            top: 5px;
        }}
        .header-logo img {{
            height: 50px;
        }}
        .header-subtitle {{
            position: absolute;
            bottom: 5px;
            left: 20px;
            font-size: 11px;
        }}
        .header-title {{
            font-size: 18px;
            font-weight: bold;
        }}
        .header-spacer {{
            height: 15px;
            width: 100%;
        }}
        html, body, [class*="css"] {{
            font-size: 13px !important;
        }}
        .stTextInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] > div {{
            font-size: 13px !important;
            padding: 2px 6px !important;
            height: 34px !important;
        }}
        div.stButton > button, div.stDownloadButton > button {{
            font-size: 13px !important;
            padding: 4px 10px !important;
            height: 32px !important;
            border-radius: 6px;
        }}
        .stDataFrame table, .stTable table {{
            font-size: 12px !important;
        }}
        .stDataFrame table td, .stTable table td {{
            padding: 3px 6px !important;
        }}
        .stDataFrame table th, .stTable table th {{
            padding: 3px 6px !important;
            font-size: 12px !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 0.4rem;
            margin-bottom: 0.4rem;
        }}
        .element-container, div[data-testid="stVerticalBlock"] > div {{
            margin: 0 !important;
            padding: 0 !important;
        }}
        .calendario-container {{
            max-height: 600px;
            overflow-y: auto;
        }}
        .vacaciones-cell {{
            color: transparent !important;
            font-size: 0px !important;
        }}
        .stSelectbox, .stDateInput {{
            background-color: white;
        }}
        .column-header {{
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #0F69B4;
        }}
        .stSelectbox, .stDateInput, .stButton {{
            margin-bottom: 10px;
        }}
        .section-spacing {{
            margin-top: 20px;
        }}
        .fixed-height-container {{
            height: 400px;
            overflow-y: auto;
        }}
    </style>
    <div class="header-container">
        <div class="header-logo"><img src="{img_src}" alt="Logo"></div>
        <div class="header-subtitle">{SUBTITULO}</div>
        <div class="header-title">{TITULO}</div>
    </div>
    <div class="header-spacer"></div>
""", unsafe_allow_html=True)

# =========================
# BASE DE DATOS (SQLite)
# =========================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jefatura_regional TEXT,
            tipo TEXT,
            fecha_inicio TEXT,
            fecha_termino TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def cargar_desde_db():
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query("SELECT * FROM vacaciones", conn)
    except Exception as e:
        st.error(f"Error al cargar desde la base de datos: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()

    if df.empty:
        return pd.DataFrame(columns=[
            'Seleccionar', 'Jefatura Regional', 'Director Regional/Subrogante', 'Fecha Inicio', 'Fecha Término'
        ])

    df = df.drop(columns=["id"], errors="ignore")
    df.rename(columns={
        "jefatura_regional": "Jefatura Regional",
        "tipo": "Director Regional/Subrogante",
        "fecha_inicio": "Fecha Inicio",
        "fecha_termino": "Fecha Término"
    }, inplace=True)
    
    df.insert(0, "Seleccionar", False)

    for col in ['Fecha Inicio', 'Fecha Término']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').apply(
                lambda x: x.date() if not pd.isna(x) else None
            )
    
    return df

def guardar_en_db(df):
    init_db()
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute("DELETE FROM vacaciones")
    
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO vacaciones 
            (jefatura_regional, tipo, fecha_inicio, fecha_termino)
            VALUES (?, ?, ?, ?)
        """, (
            row.get("Jefatura Regional", None),
            row.get("Director Regional/Subrogante", None),
            str(row.get("Fecha Inicio")) if pd.notna(row.get("Fecha Inicio")) else None,
            str(row.get("Fecha Término")) if pd.notna(row.get("Fecha Término")) else None,
        ))
    conn.commit()
    conn.close()

# Inicializar DB
init_db()

# =========================
# LISTAS INICIALES
# =========================
JEFATURAS_REGIONALES = [
    "SERGIO MARTINEZ", "Larry Alegría", "Jenny Toledo", "José Rivera",
    "MARCELA OSORIO", "Soledad Latorre", "Ruben Melo", "Paulina Villalobos",
    "PAULINA URIZAR", "Paula Saavedra", "Patricio Caballero", "Pedro Espinoza",
    "ANDRÉS VERA", "Marisol Villalobos", "Guillermo Hernandez", "Mauricio Vargas",
    "MAYCOL GOMÉZ", "Alejandra Navarrete", "Claudia Galdames", "Claudio Irarrazaval",
    "GUILLERMO ACUÑA", "Andres Zuñiga", "Fernanda León", "Simón Navias",
    "CAMILO FARÍAS", "Sylvia Lagos", "Evelyn Cortes", "Felipe Jara",
    "OSCAR MENARES", "Gisela Delgado", "Ximena Fierro", "Omar González",
    "MINERVA CASTAÑEDA", "Sandra Moreno", "Jaime Zurita", "Claudia Barrientos",
    "NESTOR VILLARROEL", "Claudia San Martin", "Ingrid Evens", "Erick Sánchez",
    "JESSICA CORONADO", "Mery Fontecha", "Paola Almonacid", "Gonzalo Soto",
    "MARILYN CÁRDENAS", "Alex Hernández", "Javier Mancilla", "Rubén Ojeda",
    "ENRIQUE CARRASCO", "Karla Leyton", "Pablo Román", "Patricio Arenas",
    "MILENA BARRIA", "Ema Jerez Poblete", "Verónica Cavieres", "Patricio Olivera",
    "ROBERTO LAU", "Elsa Vega", "Maricela Chávez", "Sergio Tello",
    "CARLOS QUEZADA", "Ingrid Reyes", "Diego Otto", "Ralf Burgos"
]

TIPOS = ["Director Regional", "Subrogante"]

NOMBRES_CALENDARIO = JEFATURAS_REGIONALES.copy()

if "jefaturas_lista" not in st.session_state:
    st.session_state.jefaturas_lista = JEFATURAS_REGIONALES.copy()
if "tipos_lista" not in st.session_state:
    st.session_state.tipos_lista = TIPOS.copy()

# =========================
# ESTADO DE DATOS
# =========================
if 'vacaciones_data' not in st.session_state:
    st.session_state.vacaciones_data = cargar_desde_db()

if 'calendario_data' not in st.session_state:
    year = datetime.now().year
    all_days = pd.date_range(start=date(year, 1, 1), end=date(year, 12, 31), freq='D')
    calendario_df = pd.DataFrame(index=NOMBRES_CALENDARIO, columns=all_days.strftime('%Y-%m-%d'))
    calendario_df.index.name = 'Nombre'
    st.session_state.calendario_data = calendario_df.fillna('')

# Estado para formulario de edición
if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'jefatura': "",
        'tipo': "",
        'fecha_inicio': None,
        'fecha_termino': None
    }
if 'widget_counter' not in st.session_state:
    st.session_state.widget_counter = 0

# =========================
# FUNCIONES AUXILIARES
# =========================
def estilo_calendario(val):
    if val == 'Vacaciones': 
        return 'background-color: #DDEFFB; color: transparent !important; font-size: 0px !important;'
    if val == 'Subrogante': 
        return 'background-color: #EA7A85; color: transparent !important; font-size: 0px !important;'
    return ''

def crear_dataframe_vacio(columnas):
    df_vacio = pd.DataFrame(columns=columnas)
    for i in range(12):
        df_vacio.loc[i] = [""] * len(columnas)
    return df_vacio

def convertir_fechas_a_string(df):
    df_copy = df.copy()
    for col in ['Fecha Inicio', 'Fecha Término']:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else "")
    return df_copy

def convertir_string_a_fecha(valor):
    if pd.isna(valor) or valor == "" or valor is None:
        return None
    elif isinstance(valor, str):
        try:
            if len(valor) == 10 and valor.count('-') == 2:
                return pd.to_datetime(valor).date()
            elif len(valor) == 10 and valor.count('/') == 2:
                return pd.to_datetime(valor, format='%Y/%m/%d').date()
            else:
                return None
        except:
            return None
    elif isinstance(valor, date):
        return valor
    elif isinstance(valor, pd.Timestamp):
        return valor.date()
    return None

def limpiar_datos():
    if not st.session_state.vacaciones_data.empty:
        date_columns = ['Fecha Inicio', 'Fecha Término']
        for col in date_columns:
            if col in st.session_state.vacaciones_data.columns:
                st.session_state.vacaciones_data[col] = st.session_state.vacaciones_data[col].apply(
                    lambda x: None if pd.isna(x) else x
                )

def importar_desde_excel():
    archivo_excel = "vacaciones_permisos.xlsx"
    if os.path.exists(archivo_excel):
        try:
            df_importado = pd.read_excel(archivo_excel)
            columnas_requeridas = st.session_state.vacaciones_data.columns
            for columna in columnas_requeridas:
                if columna not in df_importado.columns:
                    df_importado[columna] = None
            columnas_fecha = ['Fecha Inicio', 'Fecha Término']
            for col in columnas_fecha:
                if col in df_importado.columns:
                    df_importado[col] = pd.to_datetime(df_importado[col], errors="coerce").dt.date
            st.session_state.vacaciones_data = df_importado[columnas_requeridas]
            guardar_en_db(st.session_state.vacaciones_data)
        except Exception:
            pass

def guardar_registro():
    # Obtener valores actuales de los widgets usando sus claves únicas
    jefatura_key = f"jefatura_input_{st.session_state.widget_counter}"
    tipo_key = f"tipo_input_{st.session_state.widget_counter}"
    fecha_inicio_key = f"fecha_inicio_{st.session_state.widget_counter}"
    fecha_termino_key = f"fecha_termino_{st.session_state.widget_counter}"
    
    jefatura_input = st.session_state.get(jefatura_key, "")
    tipo_input = st.session_state.get(tipo_key, "")
    fecha_inicio = st.session_state.get(fecha_inicio_key, None)
    fecha_termino = st.session_state.get(fecha_termino_key, None)
    
    if jefatura_input and tipo_input:
        if jefatura_input not in st.session_state.jefaturas_lista:
            st.session_state.jefaturas_lista.append(jefatura_input)
        fecha_inicio = convertir_string_a_fecha(fecha_inicio)
        fecha_termino = convertir_string_a_fecha(fecha_termino)
        
        # Si estamos editando un registro existente, modificarlo
        if st.session_state.editing_index is not None:
            idx = st.session_state.editing_index
            st.session_state.vacaciones_data.at[idx, 'Jefatura Regional'] = jefatura_input
            st.session_state.vacaciones_data.at[idx, 'Director Regional/Subrogante'] = tipo_input
            st.session_state.vacaciones_data.at[idx, 'Fecha Inicio'] = fecha_inicio
            st.session_state.vacaciones_data.at[idx, 'Fecha Término'] = fecha_termino
            st.session_state.vacaciones_data.at[idx, 'Seleccionar'] = False
        else:
            # Si no estamos editando, crear un nuevo registro
            nuevo_registro = {
                'Seleccionar': False,
                'Jefatura Regional': jefatura_input,
                'Director Regional/Subrogante': tipo_input,
                'Fecha Inicio': fecha_inicio,
                'Fecha Término': fecha_termino
            }
            st.session_state.vacaciones_data = pd.concat([
                st.session_state.vacaciones_data, pd.DataFrame([nuevo_registro])
            ], ignore_index=True)
        
        guardar_en_db(st.session_state.vacaciones_data)
        # Limpiar formulario
        st.session_state.form_data = {
            'jefatura': "",
            'tipo': "",
            'fecha_inicio': None,
            'fecha_termino': None
        }
        st.session_state.editing_index = None
        # Incrementar contador para forzar nuevos widgets
        st.session_state.widget_counter += 1

def modificar_registro():
    # Esta función solo establece el modo de edición
    if not st.session_state.vacaciones_data.empty:
        selected_rows = st.session_state.vacaciones_data[st.session_state.vacaciones_data['Seleccionar'] == True]
        if len(selected_rows) == 1:
            idx = selected_rows.index[0]
            row = selected_rows.iloc[0]
            st.session_state.editing_index = idx
            st.session_state.form_data = {
                'jefatura': row['Jefatura Regional'],
                'tipo': row['Director Regional/Subrogante'],
                'fecha_inicio': row['Fecha Inicio'],
                'fecha_termino': row['Fecha Término']
            }
            # Incrementar contador para forzar nuevos widgets con los datos cargados
            st.session_state.widget_counter += 1
        else:
            st.warning("Seleccione exactamente un registro para modificar")

def eliminar_registros_seleccionados():
    if not st.session_state.vacaciones_data.empty:
        # Eliminar filas seleccionadas
        indices_a_eliminar = st.session_state.vacaciones_data[st.session_state.vacaciones_data['Seleccionar'] == True].index
        st.session_state.vacaciones_data = st.session_state.vacaciones_data.drop(indices_a_eliminar).reset_index(drop=True)
        
        # Limpiar selección si estaba editando una fila eliminada
        if st.session_state.editing_index in indices_a_eliminar:
            st.session_state.editing_index = None
            st.session_state.form_data = {
                'jefatura': "",
                'tipo': "",
                'fecha_inicio': None,
                'fecha_termino': None
            }
        
        guardar_en_db(st.session_state.vacaciones_data)

def actualizar_calendario():
    year = datetime.now().year
    all_days = pd.date_range(start=date(year, 1, 1), end=date(year, 12, 31), freq='D')
    calendario_df = pd.DataFrame(index=NOMBRES_CALENDARIO, columns=all_days.strftime('%Y-%m-%d'))
    calendario_df.index.name = 'Nombre'
    for _, row in st.session_state.vacaciones_data.iterrows():
        jefatura = row['Jefatura Regional']
        tipo = row['Director Regional/Subrogante']
        if pd.notna(row['Fecha Inicio']) and pd.notna(row['Fecha Término']):
            try:
                fecha_inicio = pd.to_datetime(row['Fecha Inicio'])
                fecha_termino = pd.to_datetime(row['Fecha Término'])
                nombre_en_calendario = None
                for nombre_cal in calendario_df.index:
                    if (jefatura.upper() in nombre_cal.upper() or nombre_cal.upper() in jefatura.upper()):
                        nombre_en_calendario = nombre_cal
                        break
                if nombre_en_calendario:
                    for dia in pd.date_range(start=fecha_inicio, end=fecha_termino):
                        if dia.year == year:
                            dia_str = dia.strftime('%Y-%m-%d')
                            if dia_str in calendario_df.columns:
                                if tipo == "Director Regional":
                                    calendario_df.at[nombre_en_calendario, dia_str] = 'Vacaciones'
                                elif tipo == "Subrogante":
                                    calendario_df.at[nombre_en_calendario, dia_str] = 'Subrogante'
            except:
                continue
    st.session_state.calendario_data = calendario_df.fillna('')

def exportar_a_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.vacaciones_data.to_excel(writer, sheet_name='Registros', index=False)
        calendario_export = st.session_state.calendario_data.copy()
        calendario_export.reset_index(inplace=True)
        calendario_export.to_excel(writer, sheet_name='Calendario', index=False)
    output.seek(0)
    return output

# =========================
# LIMPIEZA Y CALENDARIO
# =========================
limpiar_datos()
actualizar_calendario()

# =========================
# INTERFAZ
# =========================
col_form, col_tabla, col_calendario = st.columns([1.5, 2, 2.5], gap="medium")

with col_form:
    st.markdown("### Formulario de Registro")
    st.markdown('<div class="column-header">Jefatura Regional</div>', unsafe_allow_html=True)
    
    # Usar el valor del form_data para inicializar el widget con clave única
    jefatura_index = 0
    if st.session_state.form_data['jefatura']:
        try:
            jefatura_index = st.session_state.jefaturas_lista.index(st.session_state.form_data['jefatura']) + 1
        except ValueError:
            jefatura_index = 0
    
    st.selectbox("Jefatura Regional", options=[""] + st.session_state.jefaturas_lista,
                 index=jefatura_index, key=f"jefatura_input_{st.session_state.widget_counter}", label_visibility="collapsed")
    
    st.markdown('<div class="column-header">Director Regional/Subrogante</div>', unsafe_allow_html=True)
    
    # Usar el valor del form_data para inicializar el widget con clave única
    tipo_index = 0
    if st.session_state.form_data['tipo']:
        try:
            tipo_index = st.session_state.tipos_lista.index(st.session_state.form_data['tipo']) + 1
        except ValueError:
            tipo_index = 0
    
    st.selectbox("Tipo", options=[""] + st.session_state.tipos_lista,
                 index=tipo_index, key=f"tipo_input_{st.session_state.widget_counter}", label_visibility="collapsed")
    
    col_fecha1, col_fecha2 = st.columns(2)
    with col_fecha1:
        st.markdown('<div class="column-header">Fecha Inicio</div>', unsafe_allow_html=True)
        st.date_input("Fecha Inicio", 
                     value=st.session_state.form_data['fecha_inicio'],
                     key=f"fecha_inicio_{st.session_state.widget_counter}", label_visibility="collapsed")
    with col_fecha2:
        st.markdown('<div class="column-header">Fecha Término</div>', unsafe_allow_html=True)
        st.date_input("Fecha Término", 
                     value=st.session_state.form_data['fecha_termino'],
                     key=f"fecha_termino_{st.session_state.widget_counter}", label_visibility="collapsed")

    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
    col_btn1.button("Guardar", on_click=guardar_registro, use_container_width=True)
    col_btn2.button("Modificar", on_click=modificar_registro, use_container_width=True)
    col_btn3.button("Eliminar", on_click=eliminar_registros_seleccionados, use_container_width=True)
    col_btn4.button("Importar", on_click=importar_desde_excel, use_container_width=True)
    with col_btn5:
        if not st.session_state.vacaciones_data.empty:
            excel_data = exportar_a_excel()
            st.download_button(
                "Exportar",
                data=excel_data,
                file_name="vacaciones_permisos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("Exportar", disabled=True, use_container_width=True)

with col_tabla:
    st.markdown("### Registros de Vacaciones")
    display_df = st.session_state.vacaciones_data.copy()
    
    if display_df.empty:
        display_df = crear_dataframe_vacio(['Seleccionar', 'Jefatura Regional', 'Director Regional/Subrogante', 'Fecha Inicio', 'Fecha Término'])
    else:
        # Convertir fechas a string para mostrar
        display_df = convertir_fechas_a_string(display_df)
    
    # Mostrar el dataframe con checkboxes editables
    edited_df = st.data_editor(
        display_df,
        use_container_width=True,
        height=550,
        key="vacaciones_data_editor",
        disabled=["Jefatura Regional", "Director Regional/Subrogante", 'Fecha Inicio', 'Fecha Término']
    )
    
    # Actualizar los checkboxes en el dataframe principal
    if not st.session_state.vacaciones_data.empty:
        st.session_state.vacaciones_data['Seleccionar'] = edited_df['Seleccionar']

with col_calendario:
    st.markdown("### Calendario de Vacaciones")
    calendario_con_estilo = st.session_state.calendario_data.style.map(estilo_calendario)
    st.dataframe(calendario_con_estilo, use_container_width=True, height=550)

st.markdown("---")
st.caption("Sistema de Gestión de Vacaciones y Permisos - Directores Regionales y Subrogantes")
