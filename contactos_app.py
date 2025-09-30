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
TAMANO_TEXTO_DROPDOWN = "12px"
TAMANO_TEXTO_BOTONES = "8px"
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
    "JEFA/E DEPTO. PREVENCIÓN DE RIESGOS LABORALES", "JEFA/E DEPTO. PREVENCIÓN RIESGOS LABORALES(S)", "JEFA/E DEPARTAMENTO DE GESTIÓN DE PERSONAS",
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
    "LOS LAGOS", "AYSEN", "MAGALLANES", "E.METROPOLITANA", "LOS RÍOS", 
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
        # eliminar columna id y renombrar a UI
        if "id" in df.columns:
            df = df.drop(columns=["id"])
        df = df.rename(columns=MAPEO_BD_UI)
    else:
        df = pd.DataFrame(columns=COLUMNAS_UI)
    return df

def guardar_en_bd(df_ui):
    # df_ui: DataFrame con nombres UI (COLUMNAS_UI)
    df_bd = df_ui.rename(columns=MAPEO_UI_BD)
    conn = sqlite3.connect(DB_FILE, timeout=10, check_same_thread=False)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contactos")
        conn.commit()
        # Insertar fila por fila (mantener orden y compatibilidad)
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
/* Eliminar scroll de la página principal */
.main .block-container {{
    overflow: hidden !important;
}}
/* Scroll solo para la tabla */
.element-container:has(.stDataEditor) {{
    overflow: auto !important;
    max-height: 400px !important;
}}

/* Minimizar espacios en contenedores */
.stTextInput, .stSelectbox, .stButton {{
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}}

/* Contenedores de columnas con mínimo espacio */
div[data-testid="column"] {{
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    padding-top: 2px !important;
    padding-bottom: 2px !important;
}}

/* Inputs con mínimo espacio */
.stTextInput > div > div > input {{ 
    font-size: {TAMANO_TEXTO_INPUT} !important; 
    height: 35px !important;
    padding: 6px 10px !important;
    margin: 1px 0px !important;
}}

/* Dropdowns con mínimo espacio */
.stSelectbox > div > div > select {{ 
    font-size: {TAMANO_TEXTO_DROPDOWN} !important; 
    height: 35px !important;
    padding: 6px !important;
    margin: 1px 0px !important;
}}

div[data-baseweb="select"] > div {{ 
    font-size: {TAMANO_TEXTO_DROPDOWN} !important; 
}}

/* Botones con mínimo espacio */
.stButton > button {{
    font-size: {TAMANO_TEXTO_BOTONES} !important;
    background-color: {COLOR_BOTONES} !important;
    color: white !important;
    border: none !important;
    width: 100% !important;
    min-width: 100% !important;
    height: 32px !important;
    padding: 0px 6px !important;
    margin: 1px 0px !important;
}}
.stButton > button:hover {{ background-color: {COLOR_BOTONES_HOVER} !important; }}

/* Botones de descarga */
.stDownloadButton > button {{
    font-size: {TAMANO_TEXTO_BOTONES} !important;
    background-color: {COLOR_BOTONES} !important;
    color: white !important;
    border: none !important;
    width: 100% !important;
    min-width: 100% !important;
    height: 32px !important;
    padding: 0px 6px !important;
    margin: 1px 0px !important;
}}
.stDownloadButton > button:hover {{ background-color: {COLOR_BOTONES_HOVER} !important; }}

/* Subheaders con mínimo espacio */
h3 {{
    font-size: 16px !important;
    margin-bottom: 0.2rem !important;
    margin-top: 0.2rem !important;
    color: #0F69B4 !important;
    font-weight: bold !important;
}}

/* Línea divisoria gris con menos espacio */
.divider {{
    border-top: 1px solid #ccc;
    margin: 0.5rem 0 !important;
    width: 100%;
}}

/* Header con menos margen inferior */
.header-container {{
    display: flex; align-items: center; justify-content: center;
    background-color: {COLOR_FONDO}; height: 85px; width: 100%;
    color: white; position: relative; margin: -1rem -1rem 0.5rem -1rem !important;
}}
.header-logo {{ position: absolute; left: 20px; top: 5px; }}
.header-logo img {{ height: 60px; }}
.header-subtitle {{ position: absolute; bottom: 5px; left: 20px; font-size: 10px; }}
.header-title {{ font-size: 20px; font-weight: bold; }}

/* Reducir espacio entre elementos de formulario */
div.row-widget.stButton {{
    margin: 1px 0px !important;
    padding: 0px !important;
}}

/* Reducir espacio en contenedores internos */
div[data-testid="stVerticalBlock"] > div {{
    margin: 0px !important;
    padding: 0px !important;
}}
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
# FORMULARIO (inputs)
# =========================
st.subheader("Agregar / Modificar Contacto")

# Mantener layout original para inputs (2.5, 0.6, 1, 1)
col_inputs, col_botones_placeholder, col_vacio1, col_vacio2 = st.columns([2.5, 0.6, 1, 1])

with col_inputs:
    contacto_actual = {col:"" for col in COLUMNAS_UI}
    if st.session_state.registro_modificar is not None and not st.session_state.contactos.empty:
        try:
            contacto_actual = st.session_state.contactos.loc[st.session_state.registro_modificar]
        except Exception:
            # si el índice no existe, mantener vacío
            contacto_actual = {col:"" for col in COLUMNAS_UI}

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nombre = st.text_input("Nombre", value=contacto_actual.get('Nombre', ''))
    with col2:
        cargo_val = contacto_actual.get('Cargo', '')
        cargo_idx = OPCIONES_CARGO.index(cargo_val) if cargo_val in OPCIONES_CARGO else 0
        cargo = st.selectbox("Cargo", OPCIONES_CARGO, index=cargo_idx)
        depto_val = contacto_actual.get('Dpto./Región', '')
        depto_idx = OPCIONES_DEPTO.index(depto_val) if depto_val in OPCIONES_DEPTO else 0
        departamento = st.selectbox("Dpto./Región", OPCIONES_DEPTO, index=depto_idx)
    with col3:
        telefono = st.text_input("Teléfono Directo/Anexo", value=contacto_actual.get('Teléfono Directo/Anexo', ''))
        celular_inst = st.text_input("Celular Institucional", value=contacto_actual.get('Celular Institucional', ''))
    with col4:
        celular_part = st.text_input("Celular Particular", value=contacto_actual.get('Celular Particular', ''))
        correo = st.text_input("Correo", value=contacto_actual.get('Correo', ''))

# dejamos los placeholders vacíos para preservar diseño original
with col_botones_placeholder:
    pass
with col_vacio1:
    pass
with col_vacio2:
    pass

# =========================
# FILA DE BOTONES (4 columnas: 2.5, 0.6, 1, 1)
# En la PRIMERA columna colocamos TODOS los botones uno al lado del otro
# =========================
fila_btns = st.columns([0.5, 2, 1, 1, 1])

with fila_btns[0]:
    pass


# primera columna: botones horizontales
with fila_btns[1]:
    b1, b2, b3, b4, b5, b6 = st.columns([1,1,1,1,1,1])

    with b1:
        if st.button("Guardar", use_container_width=True, key="btn_guardar"):
            nuevo = {
                "Nombre": nombre, "Cargo": cargo, "Dpto./Región": departamento,
                "Teléfono Directo/Anexo": telefono, "Celular Institucional": celular_inst,
                "Celular Particular": celular_part, "Correo": correo
            }
            if st.session_state.registro_modificar is not None:
                try:
                    st.session_state.contactos.loc[st.session_state.registro_modificar] = nuevo
                except Exception:
                    # si falla por índice, concatenar como nuevo
                    st.session_state.contactos = pd.concat(
                        [st.session_state.contactos, pd.DataFrame([nuevo])],
                        ignore_index=True
                    )
                st.session_state.registro_modificar = None
            else:
                st.session_state.contactos = pd.concat(
                    [st.session_state.contactos, pd.DataFrame([nuevo])],
                    ignore_index=True
                )
            guardar_en_bd(st.session_state.contactos)

    with b2:
        if st.button("Modificar", use_container_width=True, key="btn_modificar"):
            if st.session_state.registro_modificar is None:
                st.warning("⚠️ Debes seleccionar un contacto para modificar.")

    with b3:
        if st.button("Cancelar", use_container_width=True, key="btn_cancelar"):
            st.session_state.registro_modificar = None

    with b4:
        if st.button("Eliminar", use_container_width=True, key="btn_eliminar"):
            if st.session_state.registro_modificar is not None:
                try:
                    st.session_state.contactos = st.session_state.contactos.drop(
                        index=st.session_state.registro_modificar
                    ).reset_index(drop=True)
                except Exception:
                    st.warning("No se pudo eliminar el registro seleccionado.")
                st.session_state.registro_modificar = None
                guardar_en_bd(st.session_state.contactos)

    with b5:
        if st.button("Exportar", use_container_width=True, key="btn_exportar"):
            buffer = exportar_excel(st.session_state.contactos)
            # Mostrar botón de descarga inmediatamente
            st.download_button("Descargar archivo", data=buffer, file_name="contactos.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)

    with b6:
        if st.button("Importar", use_container_width=True, key="btn_importar"):
            importar_excel_automatico()

# columnas vacías para mantener proporciones y diseño
with fila_btns[2]:
    pass
with fila_btns[3]:
    pass
with fila_btns[4]:
    pass

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
    # forzar único seleccionado
    edited.loc[edited.index != idx, "Seleccionar"] = False
    st.session_state.registro_modificar = idx
else:
    st.session_state.registro_modificar = None

st.session_state.contactos = edited.drop(columns=["Seleccionar"])
if not st.session_state.contactos.empty:
    guardar_en_bd(st.session_state.contactos)
if not st.session_state.contactos.empty:
    guardar_en_bd(st.session_state.contactos)

