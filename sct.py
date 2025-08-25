import streamlit as st 
from pathlib import Path
import base64

# =========================
# CONFIGURACIÓN DEL ENCABEZADO
# =========================
COLOR_FONDO = "#0F69B4"  # Azul
IMAGEN_LOCAL = "LOGO-PROPIO-ISL-2023-CMYK-01.png"
TITULO = "SECCIÓN DE COORDINACIÓN TERRITORIAL"
SUBTITULO = "Sección de Coordinación Territorial"

# =========================
# CONVERTIR IMAGEN LOCAL A BASE64
# =========================
def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Cargar imagen del encabezado
try:
    img_base64 = image_to_base64(IMAGEN_LOCAL)
    img_src = f"data:image/png;base64,{img_base64}"
except:
    img_src = ""

# =========================
# CSS + HTML DEL ENCABEZADO Y NUEVO CONTENEDOR
# =========================
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
            margin: -1rem -1rem 1.2rem -1rem;
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

        /* Nuevo contenedor "Quienes somos" */
        .quienes-somos {{
            background-color: #ffffff;
            width: 100%;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: #333;
            margin-bottom: 30px;
        }}
        /* Línea separadora */
        .separador {{
            width: 100%;
            border: 0;
            height: 2px;
            background-color: #ccc;
            margin-bottom: 30px;
        }}
    </style>

    <!-- Encabezado -->
    <div class="header-container">
        <div class="header-logo">
            <img src="{img_src}" alt="Logo">
        </div>
        <div class="header-subtitle">{SUBTITULO}</div>
        <div class="header-title">{TITULO}</div>
    </div>

    <!-- Nuevo contenedor -->
    <div class="quienes-somos">
        La Sección de Coordinación Territorial (SCT) tiene como función la supervisión funcional <br> de las Direcciones Regionales del ISL,
        coordinando acciones con diferentes áreas a nivel central y <br> regional para el cumplimiento de objetivos y metas del Servicio.
    </div>

    <!-- Línea separadora -->
    <hr class="separador">
"""
# =========================
# CONFIGURACIÓN DE LA PÁGINA PRINCIPAL
# =========================
st.set_page_config(
    page_title="Menú principal", 
    layout="wide",  
    initial_sidebar_state="collapsed"
)

# Ocultar la barra lateral
st.markdown(
    """
    <style>
    .css-1d391kg {display: none}
    section[data-testid="stSidebar"] {display: none !important;}
    button[data-testid="baseButton-header"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

# Renderizar encabezado
st.markdown(header_html, unsafe_allow_html=True)

# =========================
# FUNCIÓN PARA IMÁGENES DE BOTONES
# =========================
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# =========================
# BOTONES/IMÁGENES PRINCIPALES
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    try:
        img_bytes = img_to_bytes("Gestión_Archivos.png")
        st.markdown(
            f'<div style="text-align: center;">'
            f'<a href="https://gestor-tareas-isl-oct.streamlit.app" target="_blank">'
            f'<img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px; '
            f'border-radius:8px; cursor:pointer; box-shadow:2px 2px 6px rgba(0,0,0,0.3);">'
            f'</a>'
            f'<div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Compromisos OCT</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    except:
        st.error("No se pudo cargar la imagen Gestión_Archivos.png")

with col2:
    try:
        img_bytes = img_to_bytes("Gestión_regional.png")
        st.markdown(
            f'<div style="text-align: center;">'
            f'<a href="https://cuadernoreunionesregionales-oct.streamlit.app/" target="_blank">'
            f'<img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px; '
            f'border-radius:8px; cursor:pointer; box-shadow:2px 2px 6px rgba(0,0,0,0.3);">'
            f'</a>'
            f'<div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Seguimiento Regional</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    except:
        st.error("No se pudo cargar la imagen Gestión_regional.png")

with col4:
    try:
        img_bytes = img_to_bytes("Contactos.png")
        contactos_url = "http://localhost:8502"
        st.markdown(
            f'<div style="text-align: center;">'
            f'<a href="{contactos_url}" target="_blank">'
            f'<img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px; '
            f'border-radius:8px; cursor:pointer; box-shadow:2px 2px 6px rgba(0,0,0,0.3);">'
            f'</a>'
            f'<div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Contactos</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    except:
        st.error("No se pudo cargar la imagen Contactos.png")

with col3:
    try:
        img_bytes = img_to_bytes("vacaciones_feriados.png")
        st.markdown(
            f'<div style="text-align: center;">'
            f'<a href="https://sct-vacaciones-feriados.streamlit.app/" target="_blank">'
            f'<img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px; '
            f'border-radius:8px; cursor:pointer; box-shadow:2px 2px 6px rgba(0,0,0,0.3);">'
            f'</a>'
            f'<div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Vacaciones</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    except:
        st.error("No se pudo cargar la imagen vacaciones.png")

# Espaciado adicional
st.markdown("<br><br>", unsafe_allow_html=True)



