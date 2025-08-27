import streamlit as st
import pandas as pd
import sqlite3
import base64
from io import BytesIO

# =========================
# CONFIGURACIÓN DEL ENCABEZADO
# =========================
COLOR_FONDO = "#0F69B4"
IMAGEN_LOCAL = "LOGO-PROPIO-ISL-2023-CMYK-01.png"
TITULO = "CONTROL CONTINUIDAD OPERACIONAL - MOVILIZACIONES"
SUBTITULO = "Sección de Coordinación Territorial"

# =========================
# FUNCIÓN PARA CONVERTIR IMAGEN A BASE64
# =========================
def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = image_to_base64(IMAGEN_LOCAL)
img_src = f"data:image/png;base64,{img_base64}"

# =========================
# CONFIGURACIÓN DE LA PÁGINA
# =========================
st.set_page_config(page_title="Registro Emergencias", layout="wide", page_icon="📊")

# =========================
# CSS Y HTML DEL ENCABEZADO
# =========================
st.markdown(f"""
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
    display: flex;
    flex-direction: column;
    align-items: flex-start;
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
.subtitulo-tabla {{
    margin-top: 20px;
    font-size: 16px;
    font-weight: normal;
    color: #000000;
}}
/* Encabezado de tabla */
.stDataFrame thead th {{
    background-color: #0F69B4 !important;
    color: #ffffff !important;
    font-weight: bold !important;
}}
/* Ajustes de celdas: multilínea, pequeño y centrado */
.stDataFrame td, .stDataFrame th {{
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
    font-size: 12px !important;
    text-align: center !important;
    vertical-align: middle !important;
    padding: 4px 6px !important;
    line-height: 1.2em !important;
}}
.table-legend {{
    font-size: 12px;
    color: #000000;
    margin-top: 1px;
    margin-bottom: 15px;
}}
</style>

<div class="header-container">
    <div class="header-logo">
        <img src="{img_src}" alt="Logo">
    </div>
    <div class="header-subtitle">{SUBTITULO}</div>
    <div class="header-title">{TITULO}</div>
</div>

<div class="subtitulo-tabla">Tabla Situación de Emergencias Regionales.</div>
""", unsafe_allow_html=True)

# =========================
# CREACIÓN DEL DATAFRAME BASE
# =========================
regiones = [
    'Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama', 'Coquimbo',
    'Valparaíso', 'Metropolitana', "O'Higgins", 'Maule', 'Ñuble',
    'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos', 'Aysén', 'Magallanes'
]

def crear_df_base():
    return pd.DataFrame({
        'Selecc': [False] * len(regiones),
        'Región': regiones,
        'Agua': [''] * len(regiones),
        'Electricidad': [''] * len(regiones),
        'Internet': [''] * len(regiones),
        'Acceso a Sistemas (Si/No)': [''] * len(regiones),
        'Reporte de TI (Si/No)': [''] * len(regiones),
        'Sistemas NO operativos (Cuáles?))': [''] * len(regiones),
        'Sucursales NO operativas': [''] * len(regiones),
        'Cuenta con VPN': [''] * len(regiones),
        'Atención recibida (Si/No)': [''] * len(regiones),
        'Funcionarios afectados': [''] * len(regiones),
        'Instrucciones SEREMI (Si/No)': [''] * len(regiones),
        'Instrucciones SEREMI(Cuáles?)': [''] * len(regiones),
        'Observ/Propuesta DR': [''] * len(regiones),
    })

# =========================
# CONEXIÓN A BASE DE DATOS
# =========================
conn = sqlite3.connect("emergencias.db", check_same_thread=False)
c = conn.cursor()
# Crear tabla si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS emergencias (
    Region TEXT PRIMARY KEY,
    Selecc INTEGER,
    Agua TEXT,
    Electricidad TEXT,
    Internet TEXT,
    AccesoSistemas TEXT,
    InfoTI TEXT,
    SistemasNoOperativos TEXT,
    SucursalesNoOperativas TEXT,
    VPN TEXT,
    Atenciones TEXT,
    FuncionariosAfectados TEXT,
    InstruccionesSEREMI TEXT,
    CualInstruccionSEREMI TEXT,
    Observaciones TEXT
)
""")
conn.commit()

# =========================
# CARGAR DATOS DE LA DB O CREAR BASE
# =========================
def cargar_datos():
    df_db = pd.read_sql("SELECT * FROM emergencias", conn)
    if df_db.empty:
        return crear_df_base()
    else:
        df_db = df_db.rename(columns={
            'Region': 'Región',
            'Selecc': 'Selecc',
            'AccesoSistemas': 'Acceso a Sistemas (Si/No)',
            'InfoTI': 'Reporte de TI (Si/No)',
            'SistemasNoOperativos': 'Sistemas NO operativos (Cuáles?))',
            'SucursalesNoOperativas': 'Sucursales NO operativas',
            'VPN': 'Cuenta con VPN',
            'Atenciones': 'Atención recibida (Si/No)',
            'FuncionariosAfectados': 'Funcionarios afectados',
            'InstruccionesSEREMI': 'Instrucciones SEREMI (Si/No)',
            'CualInstruccionSEREMI': 'Instrucciones SEREMI(Cuáles?)',
            'Observaciones': 'Observ/Propuesta DR'
        })
        return df_db

if "df_emergencias" not in st.session_state:
    st.session_state.df_emergencias = cargar_datos()

# =========================
# CONFIGURACIÓN DE COLUMNAS
# =========================
column_config = {
    "Selecc": st.column_config.CheckboxColumn("Selecc", width=80),
    "Región": st.column_config.TextColumn("Región", width=120, disabled=True),
    "Agua": st.column_config.TextColumn("Agua", width=80),
    "Electricidad": st.column_config.TextColumn("Electricidad", width=110),
    "Internet": st.column_config.TextColumn("Internet", width=100),
    "Acceso a Sistemas (Si/No)": st.column_config.TextColumn("Acceso a Sistemas (Si/No)", width=190),
    "Reporte de TI (Si/No)": st.column_config.TextColumn("Reporte de TI (Si/No)", width=170),
    "Sistemas NO operativos (Cuáles?))": st.column_config.TextColumn("Sistemas NO operativos (Cuáles?))", width=240),
    "Sucursales NO operativas": st.column_config.TextColumn("Sucursales NO operativas", width=190),
    "Cuenta con VPN": st.column_config.TextColumn("Cuenta con VPN", width=130),
    "Atención recibida (Si/No)": st.column_config.TextColumn("Atención recibida (Si/No)", width=180),
    "Funcionarios afectados": st.column_config.TextColumn("Funcionarios afectados", width=180),
    "Instrucciones SEREMI (Si/No)": st.column_config.TextColumn("Instrucciones SEREMI (Si/No)", width=210),
    "Instrucciones SEREMI(Cuáles?)": st.column_config.TextColumn("Instrucciones SEREMI(Cuáles?)", width=230),
    "Observ/Propuesta DR": st.column_config.TextColumn("Observ/Propuesta DR", width=250),
}

# =========================
# TABLA EDITABLE
# =========================
edited_df = st.data_editor(
    st.session_state.df_emergencias,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    column_config=column_config
)

# =========================
# BOTONES DE ACCIÓN
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 Guardar Datos", use_container_width=True):
        df_guardar = edited_df.copy()
        df_guardar_db = df_guardar.rename(columns={
            'Región':'Region',
            'Selecc':'Selecc',
            'Acceso a Sistemas (Si/No)':'AccesoSistemas',
            'Reporte de TI (Si/No)':'InfoTI',
            'Sistemas NO operativos (Cuáles?))':'SistemasNoOperativos',
            'Sucursales NO operativas':'SucursalesNoOperativas',
            'Cuenta con VPN':'VPN',
            'Atención recibida (Si/No)':'Atenciones',
            'Funcionarios afectados':'FuncionariosAfectados',
            'Instrucciones SEREMI (Si/No)':'InstruccionesSEREMI',
            'Instrucciones SEREMI(Cuáles?)':'CualInstruccionSEREMI',
            'Observ/Propuesta DR':'Observaciones'
        })
        for _, row in df_guardar_db.iterrows():
            c.execute("""
            INSERT OR REPLACE INTO emergencias
            (Region, Selecc, Agua, Electricidad, Internet, AccesoSistemas, InfoTI, SistemasNoOperativos,
            SucursalesNoOperativas, VPN, Atenciones, FuncionariosAfectados, InstruccionesSEREMI, CualInstruccionSEREMI, Observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(row))
        conn.commit()
        st.session_state.df_emergencias = df_guardar.copy()

with col2:
    if st.button("🔄 Limpiar Tabla", use_container_width=True):
        st.session_state.df_emergencias = crear_df_base()

with col3:
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    excel_data = to_excel(edited_df)
    st.download_button(
        label="📥 Exportar a Excel",
        data=excel_data,
        file_name="registro_emergencias.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# =========================
# NOTA EXPLICATIVA
# =========================
st.info("""
**Instrucciones:** 
- Complete directamente los datos en la tabla
- La primera columna es un checkbox de selección
- Indique SI/NO o texto en Agua, Electricidad, Internet, VPN, etc.
- Todo el texto se ajusta en varias líneas, con letra más pequeña y centrado
- Use la columna de observaciones para notas adicionales
""")

