import streamlit as st
import pandas as pd
from datetime import datetime, date
from io import BytesIO
import base64
import os

# =========================
# CONFIGURACIÓN ENCABEZADO
# =========================
COLOR_FONDO = "#0F69B4"
IMAGEN_LOCAL = "LOGO-PROPIO-ISL-2023-CMYK-01.png"
TITULO = "VACACIONES Y PERMISOS"
SUBTITULO = "Sección de Coordinación Territorial"

def image_to_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

img_base64 = image_to_base64(IMAGEN_LOCAL)
img_src = f"data:image/png;base64,{img_base64}"

# CSS
header_html = f"""
    <style>
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: {COLOR_FONDO};
            height: 85px;
            width: 100%;
            color: white;
            position: relative;
        }}
        .header-logo {{
            position: absolute;
            left: 20px;
            top: 5px;
        }}
        .header-logo img {{
            height: 60px;
        }}
        .header-subtitle {{
            position: absolute;
            bottom: 5px;
            left: 20px;
            font-size: 10px;
        }}
        .header-title {{
            font-size: 20px;
            font-weight: bold;
        }}
        .header-spacer {{
            height: 20px;
            width: 100%;
        }}
        .stApp {{ margin: 0 !important; padding: 0 !important; }}
        .element-container, div[data-testid="stVerticalBlock"] > div {{
            margin: 0 !important;
            padding: 0 !important;
        }}
        .stDataFrame {{ font-size: 10px; margin: 0 !important; }}
        div[data-testid="stDataFrameResizable"] {{ overflow-x: auto; margin: 0 !important; }}
        .column-header {{
            
            text-align: Left;
            
            
            font-size: 14px;
        }}
        .stTextInput, .stDateInput, .stButton {{ 
            margin: 0 !important; 
            font-size: 8px;
        }}
        .stButton button {{
            font-size: 8px;
            padding: 0.05rem 0.05rem;
        }}
        .css-1d391kg {{
            font-size: 10px;
        }}
    </style>
    <div class="header-container">
        <div class="header-logo"><img src="{img_src}" alt="Logo"></div>
        <div class="header-subtitle">{SUBTITULO}</div>
        <div class="header-title">{TITULO}</div>
    </div>
    <div class="header-spacer"></div>
"""
st.markdown(header_html, unsafe_allow_html=True)

st.set_page_config(page_title="VACACIONES Y PERMISOS",
                   page_icon="📅", layout="wide", initial_sidebar_state="collapsed")

# =========================
# LISTAS INICIALES
# =========================
DIRECTORES_INICIALES = [
    "Sergio Martínez (Tarapa)", "Marcela Osorio (Antofa)", "Paulina Urizar (Atacam)",
    "Andrés Vera (Coquim)", "Maycol Gómez (Valpar)", "Guillermo Acuña (O'Higg)",
    "Camilo Farías (Maule)", "Oscar Menares (Biobio)", "Minerva Castañeda (Arauca)",
    "Nestor Villarroel (Los La)", "Jessica Coronado (Aysén)", "Marilyn Cárdenas (Magall)",
    "Enrique Carrasco (R.Metro)", "Milena Barría (Los Rí)", "Roberto Lau (Arica)",
    "Carlos Quezada (Ñuble)"
]

SUBROGANTES_INICIALES = [
    "José Rivera (Tarapa)", "Soledad Latorre (Antofa)", "Patricio Caballero (Atacam)",
    "Paula Saavedra (Atacam)", "Marisol Villalobos (Coquim)", "Alejandra Navarrete (Valpar)",
    "Andrés Zúñiga (O'Higg)", "Sylvia Lagos (Maule)", "Evelyn Cartes (Maule)",
    "Ximena Fierro (Biobío)", "Sandra Moreno (Arauca)", "Claudia San Martín (Los La)",
    "Paola Almonacid (Aisén)", "Javier Mancilla (Magall)", "Pablo Román (R.Metro)",
    "Ema Jeréz (Los Rí)", "Elsa Vega (Arica)", "Diego Otto (Ñuble)"
]

if "directores_lista" not in st.session_state:
    st.session_state.directores_lista = DIRECTORES_INICIALES.copy()
if "subrogantes_lista" not in st.session_state:
    st.session_state.subrogantes_lista = SUBROGANTES_INICIALES.copy()

# =========================
# ESTADO DE DATOS
# =========================
if 'directores_data' not in st.session_state:
    st.session_state.directores_data = pd.DataFrame(columns=[
        'Director Regional', 'Teléfono Director', 'Fecha Inicio Director', 'Fecha Término Director',
        'Subrogante', 'Teléfono Subrogante', 'Fecha Inicio Subrogante', 'Fecha Término Subrogante'
    ])
if 'calendario_data' not in st.session_state:
    year = datetime.now().year
    all_days = pd.date_range(start=date(year, 1, 1), end=date(year, 12, 31), freq='D')
    st.session_state.calendario_data = pd.DataFrame(index=[], columns=all_days.strftime('%Y-%m-%d'))
    st.session_state.calendario_data.index.name = 'Nombre'
if 'selected_rows' not in st.session_state:
    st.session_state.selected_rows = []
if 'modo_edicion' not in st.session_state:
    st.session_state.modo_edicion = False
if 'indice_edicion' not in st.session_state:
    st.session_state.indice_edicion = None

# =========================
# FUNCIONES
# =========================
def estilo_calendario(val):
    if val == 'Vacaciones': return 'background-color: #DDEFFB;'
    if val == 'Subrogante': return 'background-color: #EA7A85;'
    return ''

def crear_dataframe_vacio(columnas):
    df_vacio = pd.DataFrame(columns=columnas)
    for i in range(12): df_vacio.loc[i] = [""] * len(columnas)
    return df_vacio

def convertir_fechas_a_string(df):
    """Convierte las columnas de fecha a strings para mostrar en la tabla"""
    df_copy = df.copy()
    columnas_fecha = ['Fecha Inicio Director', 'Fecha Término Director', 
                     'Fecha Inicio Subrogante', 'Fecha Término Subrogante']
    
    for col in columnas_fecha:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else "")
    
    return df_copy

def convertir_string_a_fecha(valor):
    """Convierte strings de fecha a objetos datetime.date"""
    if pd.isna(valor) or valor == "":
        return None
    elif isinstance(valor, str):
        try:
            return pd.to_datetime(valor).date()
        except:
            return None
    elif isinstance(valor, date):
        return valor
    return None

def convertir_a_string_telefono(valor):
    """Convierte números de teléfono a strings, eliminando decimales .0"""
    if pd.isna(valor) or valor == "":
        return ""
    elif isinstance(valor, (int, float)):
        # Convertir a string y eliminar .0 si es un número flotante
        return str(int(valor)) if valor == int(valor) else str(valor)
    elif isinstance(valor, str):
        return valor
    return str(valor)

def importar_desde_excel():
    archivo_excel = "vacaciones_permisos.xlsx"
    if os.path.exists(archivo_excel):
        try:
            df_importado = pd.read_excel(archivo_excel)
            columnas_requeridas = st.session_state.directores_data.columns
            for columna in columnas_requeridas:
                if columna not in df_importado.columns:
                    df_importado[columna] = None
            
            # Convertir columnas de fecha si es necesario
            columnas_fecha = ['Fecha Inicio Director', 'Fecha Término Director', 
                             'Fecha Inicio Subrogante', 'Fecha Término Subrogante']
            for col in columnas_fecha:
                if col in df_importado.columns:
                    df_importado[col] = pd.to_datetime(df_importado[col]).dt.date
            
            # Convertir números de teléfono a strings
            columnas_telefono = ['Teléfono Director', 'Teléfono Subrogante']
            for col in columnas_telefono:
                if col in df_importado.columns:
                    df_importado[col] = df_importado[col].apply(convertir_a_string_telefono)
            
            st.session_state.directores_data = df_importado[columnas_requeridas]
            actualizar_calendario()
        except:
            pass

def guardar_registro():
    director_input = st.session_state.get('director_input_widget', "")
    telefono_dir_input = st.session_state.get('telefono_dir_input_widget', "")
    fecha_inicio_dir = st.session_state.get('fecha_inicio_dir_widget', None)
    fecha_termino_dir = st.session_state.get('fecha_termino_dir_widget', None)
    subrogante_input = st.session_state.get('subrogante_input_widget', "")
    telefono_sub_input = st.session_state.get('telefono_sub_input_widget', "")
    fecha_inicio_sub = st.session_state.get('fecha_inicio_sub_widget', None)
    fecha_termino_sub = st.session_state.get('fecha_termino_sub_widget', None)
    
    if director_input:
        if director_input not in st.session_state.directores_lista:
            st.session_state.directores_lista.append(director_input)
        if subrogante_input and subrogante_input not in st.session_state.subrogantes_lista:
            st.session_state.subrogantes_lista.append(subrogante_input)

        # Asegurar que las fechas sean objetos date y teléfonos sean strings
        fecha_inicio_dir = convertir_string_a_fecha(fecha_inicio_dir)
        fecha_termino_dir = convertir_string_a_fecha(fecha_termino_dir)
        fecha_inicio_sub = convertir_string_a_fecha(fecha_inicio_sub)
        fecha_termino_sub = convertir_string_a_fecha(fecha_termino_sub)
        telefono_dir_input = convertir_a_string_telefono(telefono_dir_input)
        telefono_sub_input = convertir_a_string_telefono(telefono_sub_input)

        nuevo_registro = {
            'Director Regional': director_input,
            'Teléfono Director': telefono_dir_input,
            'Fecha Inicio Director': fecha_inicio_dir,
            'Fecha Término Director': fecha_termino_dir,
            'Subrogante': subrogante_input,
            'Teléfono Subrogante': telefono_sub_input,
            'Fecha Inicio Subrogante': fecha_inicio_sub,
            'Fecha Término Subrogante': fecha_termino_sub
        }

        if st.session_state.modo_edicion and st.session_state.indice_edicion is not None:
            # 🔹 Modificar registro existente - asegurar tipos de datos correctos
            for col, value in nuevo_registro.items():
                # Convertir a tipo de dato compatible con la columna existente
                if col in ['Teléfono Director', 'Teléfono Subrogante']:
                    # Asegurar que los teléfonos sean strings
                    st.session_state.directores_data.loc[st.session_state.indice_edicion, col] = str(value) if value is not None else ""
                elif col in ['Fecha Inicio Director', 'Fecha Término Director', 
                           'Fecha Inicio Subrogante', 'Fecha Término Subrogante']:
                    # Asegurar que las fechas sean objetos date
                    st.session_state.directores_data.loc[st.session_state.indice_edicion, col] = value
                else:
                    st.session_state.directores_data.loc[st.session_state.indice_edicion, col] = value
            st.session_state.modo_edicion = False
            st.session_state.indice_edicion = None
        else:
            # 🔹 Crear nuevo registro
            st.session_state.directores_data = pd.concat([
                st.session_state.directores_data, pd.DataFrame([nuevo_registro])
            ], ignore_index=True)

        actualizar_calendario()

        # Reset widgets usando callbacks
        st.session_state.director_input_widget = ""
        st.session_state.telefono_dir_input_widget = ""
        st.session_state.fecha_inicio_dir_widget = None
        st.session_state.fecha_termino_dir_widget = None
        st.session_state.subrogante_input_widget = ""
        st.session_state.telefono_sub_input_widget = ""
        st.session_state.fecha_inicio_sub_widget = None
        st.session_state.fecha_termino_sub_widget = None

def modificar_registro():
    if st.session_state.selected_rows and len(st.session_state.selected_rows) == 1:
        idx = st.session_state.selected_rows[0]
        registro = st.session_state.directores_data.loc[idx]

        # Cargar valores a los widgets
        st.session_state.director_input_widget = registro['Director Regional']
        st.session_state.telefono_dir_input_widget = convertir_a_string_telefono(registro['Teléfono Director'])
        st.session_state.fecha_inicio_dir_widget = registro['Fecha Inicio Director']
        st.session_state.fecha_termino_dir_widget = registro['Fecha Término Director']
        st.session_state.subrogante_input_widget = registro['Subrogante'] if pd.notna(registro['Subrogante']) else ""
        st.session_state.telefono_sub_input_widget = convertir_a_string_telefono(registro['Teléfono Subrogante'])
        st.session_state.fecha_inicio_sub_widget = registro['Fecha Inicio Subrogante']
        st.session_state.fecha_termino_sub_widget = registro['Fecha Término Subrogante']

        st.session_state.modo_edicion = True
        st.session_state.indice_edicion = idx

def eliminar_registros_seleccionados():
    if st.session_state.selected_rows:
        st.session_state.directores_data = st.session_state.directores_data.drop(
            st.session_state.selected_rows
        ).reset_index(drop=True)
        actualizar_calendario()
        st.session_state.selected_rows = []

def actualizar_calendario():
    year = datetime.now().year
    all_days = pd.date_range(start=date(year, 1, 1), end=date(year, 12, 31), freq='D')
    calendario_df = pd.DataFrame(index=[], columns=all_days.strftime('%Y-%m-%d'))
    calendario_df.index.name = 'Nombre'

    for _, row in st.session_state.directores_data.iterrows():
        director = row['Director Regional']
        subrogante = row['Subrogante']

        if pd.notna(row['Fecha Inicio Director']) and pd.notna(row['Fecha Término Director']):
            for dia in pd.date_range(start=row['Fecha Inicio Director'], end=row['Fecha Término Director']):
                if dia.year == year:
                    if director not in calendario_df.index:
                        calendario_df.loc[director] = [''] * len(calendario_df.columns)
                    calendario_df.at[director, dia.strftime('%Y-%m-%d')] = 'Vacaciones'

        if subrogante and pd.notna(row['Fecha Inicio Subrogante']) and pd.notna(row['Fecha Término Subrogante']):
            for dia in pd.date_range(start=row['Fecha Inicio Subrogante'], end=row['Fecha Término Subrogante']):
                if dia.year == year:
                    if subrogante not in calendario_df.index:
                        calendario_df.loc[subrogante] = [''] * len(calendario_df.columns)
                    calendario_df.at[subrogante, dia.strftime('%Y-%m-%d')] = 'Subrogante'

    st.session_state.calendario_data = calendario_df.fillna('')

def exportar_a_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.directores_data.to_excel(writer, sheet_name='Registros', index=False)
        calendario_export = st.session_state.calendario_data.copy()
        calendario_export.reset_index(inplace=True)
        calendario_export.to_excel(writer, sheet_name='Calendario', index=False)
    output.seek(0)
    return output

# =========================
# INTERFAZ
# =========================
col_form, col_table = st.columns([1, 2], gap="small")

with col_form:
    col_nombre_dir, col_nombre_sub = st.columns(2)
    col_nombre_dir.markdown('<div class="column-header">Director/a Regional</div>', unsafe_allow_html=True)
    col_nombre_sub.markdown('<div class="column-header">Subrogante</div>', unsafe_allow_html=True)

    col_input_dir, col_input_sub = st.columns(2)
    with col_input_dir:
        st.selectbox("Nombre Director", options=[""] + st.session_state.directores_lista,
                     key="director_input_widget", label_visibility="collapsed")
    with col_input_sub:
        st.selectbox("Nombre Subrogante", options=[""] + st.session_state.subrogantes_lista,
                     key="subrogante_input_widget", label_visibility="collapsed")

    col_tel_dir, col_tel_sub = st.columns(2)
    col_tel_dir.text_input("Teléfono Whatsapp (1)", value="", key="telefono_dir_input_widget")
    col_tel_sub.text_input("Teléfono Whatsapp (2)", value="", key="telefono_sub_input_widget")

    col_fecha_dir1, col_fecha_sub1 = st.columns(2)
    col_fecha_dir1.date_input("Fecha Inicio (1)", value=None, key="fecha_inicio_dir_widget")
    col_fecha_sub1.date_input("Fecha Inicio (2)", value=None, key="fecha_inicio_sub_widget")

    col_fecha_dir2, col_fecha_sub2 = st.columns(2)
    col_fecha_dir2.date_input("Fecha Término (1)", value=None, key="fecha_termino_dir_widget")
    col_fecha_sub2.date_input("Fecha Término (2)", value=None, key="fecha_termino_sub_widget")

    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
    col_btn1.button("💾 Guardar", on_click=guardar_registro, use_container_width=True)
    col_btn2.button("✏️ Modificar", on_click=modificar_registro, use_container_width=True)
    col_btn3.button("🗑️ Eliminar", on_click=eliminar_registros_seleccionados, use_container_width=True)
    col_btn4.button("📥 Importar", on_click=importar_desde_excel, use_container_width=True)
    with col_btn5:
        if not st.session_state.directores_data.empty:
            excel_data = exportar_a_excel()
            st.download_button("📤 Exportar", data=excel_data,
                file_name="vacaciones_permisos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("📤 Exportar", disabled=True, use_container_width=True)

with col_table:
    columnas_tabla = ['Seleccionar','Director Regional','Teléfono Director','Fecha Inicio Director',
                      'Fecha Término Director','Subrogante','Teléfono Subrogante',
                      'Fecha Inicio Subrogante','Fecha Término Subrogante']

    if st.session_state.directores_data.empty:
        display_df = crear_dataframe_vacio(columnas_tabla[1:])
        display_df.insert(0,"Seleccionar",False)
    else:
        # Convertir fechas a strings para mostrar en la tabla
        display_df = convertir_fechas_a_string(st.session_state.directores_data.copy())
        display_df.insert(0,"Seleccionar",False)
        if len(display_df) < 12:
            for _ in range(12 - len(display_df)):
                display_df.loc[len(display_df)] = [False] + [""] * (len(columnas_tabla)-1)

    edited_df = st.data_editor(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Seleccionar": st.column_config.CheckboxColumn("Seleccionar", help="Seleccione registros para modificar o eliminar", default=False)
        },
        disabled=list(display_df.columns[1:]),
        num_rows="fixed"
    )
    if not st.session_state.directores_data.empty:
        selected_indices = []
        for idx, row in edited_df.iterrows():
            if idx < len(st.session_state.directores_data) and row["Seleccionar"]:
                selected_indices.append(idx)
        st.session_state.selected_rows = selected_indices

# Calendario
if st.session_state.calendario_data.empty:
    year = datetime.now().year
    all_days = pd.date_range(start=date(year, 1, 1), end=date(year, 12, 31), freq='D')
    calendario_vacio = pd.DataFrame(index=range(12), columns=all_days.strftime('%Y-%m-%d')).fillna('')
    st.dataframe(calendario_vacio.style.map(estilo_calendario), use_container_width=True, height=400)
else:
    st.dataframe(st.session_state.calendario_data.style.map(estilo_calendario),
                 use_container_width=True, height=400)

st.markdown("---")
st.caption("Sistema de Gestión de Vacaciones y Permisos - Directores Regionales y Subrogantes")