import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
import base64
import os

# =========================
# CONFIGURACIÓN
# =========================
COLOR_FONDO = "#0F69B4"
IMAGEN_LOCAL = "LOGO-PROPIO-ISL-2023-CMYK-01.png"
TITULO = "DIRECTORIO DE CONTACTOS"
SUBTITULO = "Sección de Coordinación Territorial"

TAMANO_TEXTO_INPUT = "12px"
TAMANO_TEXTO_DROPDOWN = "12px"  # Modificado a 16px
TAMANO_TEXTO_BOTONES = "12px"
COLOR_BOTONES = "#0F69B4"
COLOR_BOTONES_HOVER = "#DDEFFB"
COLOR_BOTONES_SECUNDARIO = "#6c757d"
COLOR_BOTONES_SECUNDARIO_HOVER = "#5a6268"

# =========================
# COLUMNAS Y MAPEO
# =========================
COLUMNAS_UI = [
    'Nombre', 'Cargo', 'Dpto./Región',
    'Teléfono Directo/Anexo', 'Celular Institucional',
    'Celular Particular', 'Correo'
]

MAPEO_UI_BD = {
    'Nombre': 'Nombre',
    'Cargo': 'Cargo',
    'Dpto./Región': 'Dpto_Region',
    'Teléfono Directo/Anexo': 'Telefono',
    'Celular Institucional': 'CelularInst',
    'Celular Particular': 'CelularPart',
    'Correo': 'Correo'
}
MAPEO_BD_UI = {v: k for k, v in MAPEO_UI_BD.items()}

# =========================
# LISTAS DE OPCIONES
# =========================
OPCIONES_CARGO = [
    "DIRECTOR/A NACIONAL", "DIRECTOR/A NACIONAL(S)", "JEFA/E GABINETE", "JEFA/E GABINETE(S)", "JEFA/E COORDINACIÓN TERRITORIAL",
    "JEFA/E COORDINACIÓN TERRITORIAL(S)", "JEFA/E DPTO. ATENCIÓN DE USUARIOS", "JEFA/E DPTO. ATENCIÓN DE USUARIOS(S)","JEFA/E DEPARTAMENTO JURÍDICO",
    "JEFA/E DEPARTAMENTO JURÍDICO(S)", "JEFA/E DIVISIÓN FINANZAS Y ADMINISTRACIÓN", "JEFA/E DIVISIÓN FINANZAS Y ADMINISTRACIÓN(S)", "JEFA/E DIVISIÓN OPERACIONES",
    "JEFA/E DIVISIÓN OPERACIONES(S)", "JEFA/E DEPARTAMENTO DE TECNOLOGÍA DE LA INFORMACIÓN", "JEFA/E DEPARTAMENTO DE TECNOLOGÍA DE LA INFORMACIÓN(S)",
    "JEFA/E DEPTO. PREVENCIÓN DE RIESGOS LABORALES", "JEFA/E DEPTO. PREVENCIÓN DE RIESGOS LABORALES(S)", "JEFA/E DEPARTAMENTO DE GESTIÓN DE PERSONAS",
    "JEFA/E DEPARTAMENTO DE GESTIÓN DE PERSONAS(S)", "JEFA/E UNIDAD DE AUDITORÍA", "JEFA/E UNIDAD DE AUDITORÍA(S)",
    "JEFA/E DEPTO. DE ESTUDIOS Y GESTIÓN ESTRATÉGICA", "JEFA/E DEPTO. DE ESTUDIOS Y GESTIÓN ESTRATÉGICA(S)", "JEFA/E DPTO. DE ESTUDIOS", "JEFA/E DPTO. DE ESTUDIOS(S)",
    "JEFA/E DEPARTAMENTO DE COMUNICACIONES",
    "JEFA/E DEPARTAMENTO DE COMUNICACIONES(S)", "DIRECTOR/A REGIONAL", "DIRECTOR/A REGIONAL(S)"
]

OPCIONES_DEPTO = [
    "DIRECCIÓN NACIONAL", "GABINETE", "COORDINACIÓN TERRITORIAL", 
    "DAU", "DAF", "DIVOP", "DTI", "DEGE", "DGDP", "DAI", "DJU", "DCOM", 
    "DSALUD", "DPREV", "DEST", "ANTOFAGASTA", "TARAPACÁ", "ATACAMA", 
    "COQUIMBO", "VALPARAÍSO", "O'HIGGINS", "MAULE", "BIOBIO", "ARAUCANÍA",
    "LOS LAGOS", "AYSÉN", "MAGALLANES", "E.METROPOLITANA", "LOS RÍOS", 
    "ARICA Y PARINACOTA", "ÑUBLE"
]

# =========================
# FUNCIONES AUXILIARES
# =========================
def image_to_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

def limpiar_datos(df):
    df_limpio = df.copy()
    for columna in df_limpio.columns:
        df_limpio[columna] = df_limpio[columna].astype(str).replace('nan','').replace('None','')
    return df_limpio

def _normaliza_numero_texto(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip()
    if s.lower() in ("nan", "none"):
        return ""
    if s.endswith(".0") and s[:-2].isdigit():
        return s[:-2]
    return s

# =========================
# BASE DE DATOS (SQLite)
# =========================
DB_FILE = "contactos.db"

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10, check_same_thread=False)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre TEXT,
                Cargo TEXT,
                Dpto_Region TEXT,
                Telefono TEXT,
                CelularInst TEXT,
                CelularPart TEXT,
                Correo TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()

def cargar_desde_bd():
    conn = sqlite3.connect(DB_FILE, timeout=10, check_same_thread=False)
    try:
        df = pd.read_sql_query("SELECT * FROM contactos", conn)
    finally:
        conn.close()
    if not df.empty:
        df = df.drop(columns=["id"])
        df = df.rename(columns=MAPEO_BD_UI)
    else:
        df = pd.DataFrame(columns=COLUMNAS_UI)
    return df

def guardar_en_bd(df_ui):
    df_bd = df_ui.rename(columns=MAPEO_UI_BD)
    conn = sqlite3.connect(DB_FILE, timeout=10, check_same_thread=False)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contactos")
        conn.commit()
        for _, row in df_bd.iterrows():
            cursor.execute("""
                INSERT INTO contactos (Nombre, Cargo, Dpto_Region,
                                       Telefono, CelularInst,
                                       CelularPart, Correo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(row))
        conn.commit()
    finally:
        conn.close()

# =========================
# EXCEL
# =========================
def exportar_excel(df_ui):
    buffer = BytesIO()
    df_ui.to_excel(buffer, index=False, sheet_name="Contactos")
    buffer.seek(0)
    return buffer

def importar_excel_automatico():
    archivo_excel = "contactos.xlsx"
    if os.path.exists(archivo_excel):
        try:
            df_importado = pd.read_excel(archivo_excel, dtype=str, keep_default_na=False)

            for columna in COLUMNAS_UI:
                if columna not in df_importado.columns:
                    df_importado[columna] = ""

            df_importado = df_importado[COLUMNAS_UI]

            for c in ['Teléfono Directo/Anexo', 'Celular Institucional', 'Celular Particular']:
                df_importado[c] = df_importado[c].apply(_normaliza_numero_texto)

            df_importado = limpiar_datos(df_importado)

            guardar_en_bd(df_importado)
            st.session_state.contactos = df_importado
        except Exception as e:
            st.error(f"❌ Error al importar el archivo: {e}")
    else:
        st.warning("⚠️ No se encontró el archivo 'contactos.xlsx'")

# =========================
# INICIALIZACIÓN
# =========================
st.set_page_config(page_title="Directorio de Contactos", layout="wide", initial_sidebar_state="collapsed")

# estilos y header
img_src = f"data:image/png;base64,{image_to_base64(IMAGEN_LOCAL)}"
st.markdown(f"""
<style>
.stTextInput > div > div > input {{ font-size: {TAMANO_TEXTO_INPUT} !important; }}
.stSelectbox > div > div > select {{ 
    font-size: {TAMANO_TEXTO_DROPDOWN} !important; 
    height: auto !important;
    padding: 8px !important;
}}
div[data-baseweb="select"] > div {{ 
    font-size: {TAMANO_TEXTO_DROPDOWN} !important; 
}}
.stButton > button {{
    font-size: {TAMANO_TEXTO_BOTONES} !important;
    background-color: {COLOR_BOTONES} !important;
    color: white !important;
    border: none !important;
    width: 100%;
}}
.stButton > button:hover {{ background-color: {COLOR_BOTONES_HOVER} !important; }}

/* Nuevo estilo para subheaders */
h3 {{
    font-size: 16px !important;
    margin-bottom: 0.5rem !important;
    margin-top: 0.5rem !important;
    color: #0F69B4 !important;
    font-weight: bold !important;
}}

/* Línea divisoria gris */
.divider {{
    border-top: 1px solid #ccc;
    margin: 2rem 0;
    width: 100%;
}}

.header-container {{
    display: flex; align-items: center; justify-content: center;
    background-color: {COLOR_FONDO}; height: 85px; width: 100%;
    color: white; position: relative; margin: -1rem -1rem 1.2rem -1rem;
}}
.header-logo {{ position: absolute; left: 20px; top: 5px; }}
.header-logo img {{ height: 60px; }}
.header-subtitle {{ position: absolute; bottom: 5px; left: 20px; font-size: 10px; }}
.header-title {{ font-size: 20px; font-weight: bold; }}
</style>
<div class="header-container">
    <div class="header-logo"><img src="{img_src}" alt="Logo"></div>
    <div class="header-subtitle">{SUBTITULO}</div>
    <div class="header-title">{TITULO}</div>
</div>
""", unsafe_allow_html=True)

# datos iniciales
init_db()
if "contactos" not in st.session_state:
    st.session_state.contactos = cargar_desde_bd()
if "registro_modificar" not in st.session_state:
    st.session_state.registro_modificar = None

# =========================
# FORMULARIO + BOTONES
# =========================
st.subheader("Agregar / Modificar Contacto")

# Modificado: Ahora tenemos 3 columnas en lugar de 2
col_inputs, col_botones, col_vacio = st.columns([4, 2, 2])  # Contenedor vacío añadido

with col_inputs:
    contacto_actual = {col:"" for col in COLUMNAS_UI}
    if st.session_state.registro_modificar is not None:
        contacto_actual = st.session_state.contactos.loc[st.session_state.registro_modificar]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nombre = st.text_input("Nombre", value=contacto_actual['Nombre'])
    with col2:
        cargo_idx = OPCIONES_CARGO.index(contacto_actual['Cargo']) if contacto_actual['Cargo'] in OPCIONES_CARGO else 0
        cargo = st.selectbox("Cargo", OPCIONES_CARGO, index=cargo_idx)
        depto_idx = OPCIONES_DEPTO.index(contacto_actual['Dpto./Región']) if contacto_actual['Dpto./Región'] in OPCIONES_DEPTO else 0
        departamento = st.selectbox("Dpto./Región", OPCIONES_DEPTO, index=depto_idx)
    with col3:
        telefono = st.text_input("Teléfono Directo/Anexo", value=contacto_actual['Teléfono Directo/Anexo'])
        celular_inst = st.text_input("Celular Institucional", value=contacto_actual['Celular Institucional'])
    with col4:
        celular_part = st.text_input("Celular Particular", value=contacto_actual['Celular Particular'])
        correo = st.text_input("Correo", value=contacto_actual['Correo'])

with col_botones:
    col_acciones, col_opciones = st.columns(2)

    with col_acciones:
        if st.button("Guardar"):
            nuevo = {
                "Nombre": nombre, "Cargo": cargo, "Dpto./Región": departamento,
                "Teléfono Directo/Anexo": telefono, "Celular Institucional": celular_inst,
                "Celular Particular": celular_part, "Correo": correo
            }
            if st.session_state.registro_modificar is not None:
                st.session_state.contactos.loc[st.session_state.registro_modificar] = nuevo
                st.session_state.registro_modificar = None
            else:
                st.session_state.contactos = pd.concat(
                    [st.session_state.contactos, pd.DataFrame([nuevo])],
                    ignore_index=True
                )
            guardar_en_bd(st.session_state.contactos)

        if st.button("Modificar"):
            if st.session_state.registro_modificar is None:
                st.warning("⚠️ Debes seleccionar un contacto para modificar.")

        if st.button("Cancelar"):
            st.session_state.registro_modificar = None

        if st.button("Eliminar"):
            if st.session_state.registro_modificar is not None:
                st.session_state.contactos = st.session_state.contactos.drop(
                    index=st.session_state.registro_modificar
                ).reset_index(drop=True)
                st.session_state.registro_modificar = None
                guardar_en_bd(st.session_state.contactos)

    with col_opciones:
        if st.button("📥 Exportar Excel"):
            buffer = exportar_excel(st.session_state.contactos)
            st.download_button("Descargar archivo", data=buffer, file_name="contactos.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        if st.button("📥 Importar Excel"):
            importar_excel_automatico()

# Contenedor vacío al lado derecho
with col_vacio:
    pass  # Este contenedor está vacío

# =========================
# LÍNEA DIVISORIA GRIS
# =========================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# TABLA
# =========================
st.subheader("Contactos Registrados")
tabla = st.session_state.contactos.copy()
if tabla.empty:
    tabla = pd.DataFrame(columns=COLUMNAS_UI)

if "Seleccionar" not in tabla.columns:
    tabla.insert(0, "Seleccionar", False)

edited = st.data_editor(
    tabla,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Seleccionar": st.column_config.CheckboxColumn("Seleccionar", help="Selecciona un contacto", default=False)
    }
)

seleccionados = edited[edited["Seleccionar"] == True]
if not seleccionados.empty:
    idx = seleccionados.index[0]
    edited.loc[edited.index != idx, "Seleccionar"] = False
    st.session_state.registro_modificar = idx
else:
    st.session_state.registro_modificar = None

st.session_state.contactos = edited.drop(columns=["Seleccionar"])
if not st.session_state.contactos.empty:
    guardar_en_bd(st.session_state.contactos)