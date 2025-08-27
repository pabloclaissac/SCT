import streamlit as st
import pandas as pd
import base64

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(page_title="Preguntas Frecuentes", layout="centered")

# =========================
# ENCABEZADO PERSONALIZADO
# =========================
COLOR_FONDO = "#005f99"
IMAGEN_LOCAL = "LOGO-PROPIO-ISL-2023-CMYK-01.png"
TITULO = "Preguntas Frecuentes"
SUBTITULO = "Sección de Coordinación Territorial"

def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    img_base64 = image_to_base64(IMAGEN_LOCAL)
    img_src = f"data:image/png;base64,{img_base64}"
except FileNotFoundError:
    st.error("❌ No se encontró el logo. Asegúrate de tener el archivo 'LOGO-PROPIO-ISL-2023-CMYK-01.png' en la misma carpeta.")
    img_src = ""

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
    </style>

    <div class="header-container">
        <div class="header-logo">
            <img src="{img_src}" alt="Logo">
        </div>
        <div class="header-subtitle">{SUBTITULO}</div>
        <div class="header-title">{TITULO}</div>
    </div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# =========================
# ESTILOS CSS
# =========================
st.markdown("""
<style>
h1 {
    text-align: center;
    color: #3CB9F7;
}
.respuesta {
    color: #0F69B4;
    font-size: 14px;
    margin: 4px 0 12px 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CARGAR ARCHIVO EXCEL AUTOMÁTICAMENTE
# =========================
try:
    df = pd.read_excel("preguntas.xlsx")

    # Validar columnas
    if "Pregunta" not in df.columns or "Respuesta" not in df.columns:
        st.error("⚠️ El archivo debe tener dos columnas llamadas 'Pregunta' y 'Respuesta'")
    else:
        # =========================
        # MOSTRAR PREGUNTAS
        # =========================
        for i, row in df.iterrows():
            with st.expander(f"❓ {row['Pregunta']}", expanded=False):
                st.markdown(f"<div class='respuesta'>{row['Respuesta']}</div>", unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'preguntas.xlsx' en la misma carpeta que la aplicación.")
except Exception as e:
    st.error(f"❌ Error al leer el archivo: {e}")

