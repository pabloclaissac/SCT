import streamlit as st 
from pathlib import Path
import base64
import os
import subprocess

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
        .quienes-somos {{
            background-color: #ffffff;
            width: 100%;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: #333;
            margin-bottom: 30px;
        }}
        .separador {{
            width: 100%;
            border: 0;
            height: 2px;
            background-color: #ccc;
            margin-bottom: 30px;
        }}
    </style>
    <div class="header-container">
        <div class="header-logo">
            <img src="{img_src}" alt="Logo">
        </div>
        <div class="header-subtitle">{SUBTITULO}</div>
        <div class="header-title">{TITULO}</div>
    </div>
    <div class="quienes-somos">
        <div style="margin-top:8px; font-size:18px; font-weight:500; color:#333;">La Sección de Coordinación Territorial (SCT) tiene como función la supervisión funcional de las Direcciones Regionales del ISL,
        coordinando acciones con diferentes áreas a nivel central y regional para el cumplimiento de objetivos y metas del Servicio.
    </div></div>
    <hr class="separador">
"""
st.set_page_config(page_title="Menú principal", layout="wide", initial_sidebar_state="collapsed")
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
col1, col2, col3, col4, col5 = st.columns(5)

# --- Columna 1
with col1:
    st.markdown("""<div style='text-align: center; font-size:18px; font-weight:bold; color:#0F69B4; margin-bottom:12px'>
                Coordinación Territorial
                </div>""", 
                unsafe_allow_html=True
                )
    try:
        img_bytes = img_to_bytes("Gestión_Archivos.png")
        st.markdown(f'<div style="text-align: center; margin-bottom: 15px;">'
                    f'<a href="https://gestor-tareas-isl-oct.streamlit.app" target="_blank">'
                    f'<img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px; '
                    f'border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);">'
                    f'</a>'
                    f'<div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Compromisos OCT</div>'
                    f'</div>', 
                    unsafe_allow_html=True
                    )
    except:
        st.error("No se pudo cargar la imagen Gestión_Archivos.png")

    try:
        img_bytes = img_to_bytes("Gestión_regional.png")
        st.markdown(f'<div style="text-align: center;"><a href="https://cuadernoreunionesregionales-oct.streamlit.app/" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Seguimiento Regional</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen Gestión_regional.png")

# --- Columna 2
with col2:
    st.markdown("""<div style='text-align: center; font-size:18px; font-weight:bold; color:#0F69B4; margin-bottom: 12px;'>Portales ISL</div>""", unsafe_allow_html=True)
    try:
        img_bytes = img_to_bytes("PortalGestiona.png")
        st.markdown(f'<div style="text-align: center; margin-bottom: 15px;"><a href="https://sites.google.com/isl.gob.cl/portalgestionadege/" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Portal Gestiona (DEGE)</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen PortalGestiona.png")

    try:
        img_bytes = img_to_bytes("controlygestionat.png")
        st.markdown(f'<div style="text-align: center;"><a href="https://sites.google.com/isl.gob.cl/seguimiento-at/inicio" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Control y Gestión AT</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen controlygestionat.png")

# --- Columna 3
with col3:
    st.markdown("""<div style='text-align: center; font-size:18px; font-weight:bold; color:#0F69B4; margin-bottom: 12px;'>Control de Indicadores</div>""", unsafe_allow_html=True)
    # Primer botón
    try:
        archivo_excel1 = r"C:\Users\pclaissacs\OneDrive - Instituto de Seguridad Laboral\2.- 2025\1.Coordinación Regional\Códigos-Aplicaciones\Ver Excel\CONTROL INDICADORES PREVENCIÓN 2025.xlsm"
        img_bytes = img_to_bytes("IndicadoresPrevencion.png")
        st.markdown(f"""<div style="text-align: center; margin-bottom: 15px;">
                <form action="" method="get">
                    <button type="submit" name="boton" value="abrir_excel1" style="border:none; background:none; padding:0; cursor:pointer;">
                        <img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);">
                    </button>
                </form>
                <div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Indicadores Prevención</div>
            </div>""", unsafe_allow_html=True)
        if st.query_params.get("boton") == "abrir_excel1":
            if os.path.exists(archivo_excel1):
                subprocess.Popen(["start", "excel", archivo_excel1], shell=True)
                st.query_params.clear()
    except Exception as e:
        st.error(f"No se pudo cargar el botón Indicadores Prevención: {e}")

    # Segundo botón (nuevo)
    try:
        archivo_excel2 = r"C:\Users\pclaissacs\OneDrive - Instituto de Seguridad Laboral\2.- 2025\1.Coordinación Regional\Códigos-Aplicaciones\Ver Excel\ACCIDENTES 2025.xlsm"
        img_bytes = img_to_bytes("EstadisticasAccidentes.png")
        st.markdown(f"""<div style="text-align: center;">
                <form action="" method="get">
                    <button type="submit" name="boton" value="abrir_excel2" style="border:none; background:none; padding:0; cursor:pointer;">
                        <img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);">
                    </button>
                </form>
                <div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Accidentes</div>
            </div>""", unsafe_allow_html=True)
        if st.query_params.get("boton") == "abrir_excel2":
            if os.path.exists(archivo_excel2):
                subprocess.Popen(["start", "excel", archivo_excel2], shell=True)
                st.query_params.clear()
    except Exception as e:
        st.error(f"No se pudo cargar el botón Otro Indicador: {e}")

# --- Columna 4
with col4:
    st.markdown("""<div style='text-align: center; font-size:18px; font-weight:bold; color:#0F69B4; margin-bottom: 12px;'>Continuidad Operacional</div>""", unsafe_allow_html=True)
    try:
        img_bytes = img_to_bytes("Vacaciones_feriados.png")
        st.markdown(f'<div style="text-align: center; margin-bottom: 15px;"><a href="https://sct-vacaciones-feriados.streamlit.app/" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Vacaciones/Feriados</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen vacaciones_feriados.png")
    try:
        img_bytes = img_to_bytes("Control-Paro.png")
        st.markdown(f'<div style="text-align: center; margin-bottom: 15px;"><a href="https://sct-planilla2.streamlit.app/" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Control/Movilización</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen Control-Paro.png")
    try:
        img_bytes = img_to_bytes("Control-Emergencias.png")
        st.markdown(f'<div style="text-align: center;"><a href="https://sct-planilla3.streamlit.app/" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Control/Emergencias</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen Control-Emergencias.png")

# --- Columna 5
with col5:
    st.markdown("""<div style='text-align: center; font-size:18px; font-weight:bold; color:#0F69B4; margin-bottom: 12px;'>Otros</div>""", unsafe_allow_html=True)
    try:
        img_bytes = img_to_bytes("Contactos.png")
        st.markdown(f'<div style="text-align: center; margin-bottom: 15px;"><a href="https://sct-contactos.streamlit.app/" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Contactos</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen Contactos.png")
    try:
        img_bytes = img_to_bytes("preguntas.png")
        st.markdown(f'<div style="text-align: center;"><a href="https://sct-preguntas.streamlit.app/" target="_blank"><img src="data:image/png;base64,{img_bytes}" style="width:100px; height:100px;border-radius:8px; box-shadow:2px 2px 6px rgba(0,0,0,0.3);"></a><div style="margin-top:8px; font-size:14px; font-weight:700; color:#333;">Preguntas Frecuentes</div></div>', unsafe_allow_html=True)
    except:
        st.error("No se pudo cargar la imagen preguntas.png")

# Espaciado adicional
st.markdown("<br><br>", unsafe_allow_html=True)

























