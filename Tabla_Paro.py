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
/* Estilos tabla */
.stDataFrame thead th {{
    background-color: #0F69B4 !important;
    color: #ffffff !important;
    font-weight: bold !important;
}}
.stDataFrame table td {{
    white-space: normal;
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

<div class="subtitulo-tabla">Tabla Situación de Sucursales.</div>
""", unsafe_allow_html=True)

# =========================
# CONFIGURACIÓN DE LA PÁGINA
# =========================
st.set_page_config(page_title="Registro de Sucursales", layout="wide", page_icon="📊")

# =========================
# CREACIÓN DEL DATAFRAME BASE
# =========================
regiones = [
    'Arica', 'Tarapacá', 'Antofagasta', 'Atacama', 'Coquimbo', 
    'Valparaíso', 'R.Metropol.', "O'Higgins", 'Maule', 'Ñuble', 
    'Biobío', 'Araucanía', 'Los Ríos', 'Los Lagos', 'Aysén', 
    'Magallanes'
]

def crear_df_base():
    return pd.DataFrame({
        'Región': regiones,
        '% Adhesión': [''] * len(regiones),
        'T.E. Suc1': [''] * len(regiones),
        'T.E. Suc2': [''] * len(regiones),
        'T.E. Suc3': [''] * len(regiones),
        'T.E. Suc4': [''] * len(regiones),
        'T.E. Suc5': [''] * len(regiones),
        'T.E. Suc6': [''] * len(regiones),
        'Observaciones': [''] * len(regiones),
        'Suc. Cerr.1': [''] * len(regiones),
        'Suc. Cerr.2': [''] * len(regiones),
        'Suc. Cerr.3': [''] * len(regiones),
        'Suc. Cerr.4': [''] * len(regiones),
        'Suc. Cerr.5': [''] * len(regiones),
        'Suc. Cerr.6': [''] * len(regiones),
    })

# =========================
# CONEXIÓN A BASE DE DATOS
# =========================
conn = sqlite3.connect("sucursales.db", check_same_thread=False)
c = conn.cursor()
# Crear tabla si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS sucursales (
    Region TEXT PRIMARY KEY,
    Porc_Adhesion REAL,
    TE_Suc1 TEXT, TE_Suc2 TEXT, TE_Suc3 TEXT, TE_Suc4 TEXT, TE_Suc5 TEXT, TE_Suc6 TEXT,
    Observaciones TEXT,
    Suc_Cerr1 TEXT, Suc_Cerr2 TEXT, Suc_Cerr3 TEXT, Suc_Cerr4 TEXT, Suc_Cerr5 TEXT, Suc_Cerr6 TEXT
)
""")
conn.commit()

# =========================
# CARGAR DATOS DE LA DB O CREAR BASE
# =========================
def cargar_datos():
    df_db = pd.read_sql("SELECT * FROM sucursales", conn)
    if df_db.empty:
        return crear_df_base()
    else:
        # Ajustar nombres de columnas para coincidir con DataFrame editable
        df_db = df_db.rename(columns={
            'Region': 'Región',
            'Porc_Adhesion': '% Adhesión',
            'TE_Suc1':'T.E. Suc1','TE_Suc2':'T.E. Suc2','TE_Suc3':'T.E. Suc3','TE_Suc4':'T.E. Suc4','TE_Suc5':'T.E. Suc5','TE_Suc6':'T.E. Suc6',
            'Suc_Cerr1':'Suc. Cerr.1','Suc_Cerr2':'Suc. Cerr.2','Suc_Cerr3':'Suc. Cerr.3','Suc_Cerr4':'Suc. Cerr.4','Suc_Cerr5':'Suc. Cerr.5','Suc_Cerr6':'Suc. Cerr.6'
        })
        return df_db

# Inicializar session_state
if "df_sucursales" not in st.session_state:
    st.session_state.df_sucursales = cargar_datos()

# =========================
# CONFIGURACIÓN DE COLUMNAS
# =========================
column_config = {
    "Región": st.column_config.TextColumn("Región", width=80, disabled=True),
    "% Adhesión": st.column_config.NumberColumn("% Adhesión", format="%.2f%%", width=120),
    "T.E. Suc1": st.column_config.TextColumn("T.E. Suc1", width=100),
    "T.E. Suc2": st.column_config.TextColumn("T.E. Suc2", width=100),
    "T.E. Suc3": st.column_config.TextColumn("T.E. Suc3", width=100),
    "T.E. Suc4": st.column_config.TextColumn("T.E. Suc4", width=100),
    "T.E. Suc5": st.column_config.TextColumn("T.E. Suc5", width=100),
    "T.E. Suc6": st.column_config.TextColumn("T.E. Suc6", width=100),
    "Observaciones": st.column_config.TextColumn("Observaciones", width=250),
    "Suc. Cerr.1": st.column_config.TextColumn("Suc. Cerr.1", width=100),
    "Suc. Cerr.2": st.column_config.TextColumn("Suc. Cerr.2", width=100),
    "Suc. Cerr.3": st.column_config.TextColumn("Suc. Cerr.3", width=100),
    "Suc. Cerr.4": st.column_config.TextColumn("Suc. Cerr.4", width=100),
    "Suc. Cerr.5": st.column_config.TextColumn("Suc. Cerr.5", width=100),
    "Suc. Cerr.6": st.column_config.TextColumn("Suc. Cerr.6", width=100),
}

# =========================
# TABLA EDITABLE
# =========================
edited_df = st.data_editor(
    st.session_state.df_sucursales,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    column_config=column_config
)

# =========================
# LEYENDA
# =========================
st.markdown('<div class="table-legend">(*T.E= Turno ético , Suc. Cerr.= Sucursal Cerrada)</div>', unsafe_allow_html=True)

# =========================
# BOTONES DE ACCIÓN
# =========================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 Guardar Datos", use_container_width=True):
        df_guardar = edited_df.copy()
        # Convertir % Adhesión vacío a None
        df_guardar["% Adhesión"] = df_guardar["% Adhesión"].replace('', None)
        # Renombrar columnas a nombres DB
        df_guardar_db = df_guardar.rename(columns={
            'Región':'Region','% Adhesión':'Porc_Adhesion',
            'T.E. Suc1':'TE_Suc1','T.E. Suc2':'TE_Suc2','T.E. Suc3':'TE_Suc3','T.E. Suc4':'TE_Suc4','T.E. Suc5':'TE_Suc5','T.E. Suc6':'TE_Suc6',
            'Suc. Cerr.1':'Suc_Cerr1','Suc. Cerr.2':'Suc_Cerr2','Suc. Cerr.3':'Suc_Cerr3','Suc. Cerr.4':'Suc_Cerr4','Suc. Cerr.5':'Suc_Cerr5','Suc. Cerr.6':'Suc_Cerr6'
        })
        for _, row in df_guardar_db.iterrows():
            c.execute("""
            INSERT OR REPLACE INTO sucursales 
            (Region, Porc_Adhesion, TE_Suc1, TE_Suc2, TE_Suc3, TE_Suc4, TE_Suc5, TE_Suc6,
            Observaciones, Suc_Cerr1, Suc_Cerr2, Suc_Cerr3, Suc_Cerr4, Suc_Cerr5, Suc_Cerr6)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(row))
        conn.commit()
        # Actualizar session_state
        st.session_state.df_sucursales = df_guardar.copy()

with col2:
    if st.button("🔄 Limpiar Tabla", use_container_width=True):
        st.session_state.df_sucursales = crear_df_base()

with col3:
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        processed_data = output.getvalue()
        return processed_data

    excel_data = to_excel(edited_df)
    st.download_button(
        label="📥 Exportar a Excel",
        data=excel_data,
        file_name="registro_sucursales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# =========================
# NOTA EXPLICATIVA
# =========================
st.info("""
**Instrucciones:** 
- Complete directamente los datos en la tabla
- Columna '% Adhesión': ingrese porcentajes (ej: 85.50)
- Columnas de sucursales: ingrese cualquier texto relevante
- Use la columna Observaciones para notas adicionales
""")




