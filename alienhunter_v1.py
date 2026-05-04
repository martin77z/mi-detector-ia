import streamlit as st
import numpy as np
from datetime import datetime

# =========================================================
# CONFIGURACIÓN RADICAL V9.5 (TOTALMENTE DIFERENTE)
# =========================================================
st.set_page_config(page_title="NEXUS-7 v9.5 PRO", layout="wide")

st.markdown("""
<style>
    /* Fondo oscuro para la zona exterior, pero la app es minimalista */
    .stApp {
        background-color: #0b0f0b;
    }

    /* TÍTULO VERDE V9.5 */
    .title-v95 {
        color: #33FF33;
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: bold;
        letter-spacing: 2px;
    }

    /* SLIDERS ROJOS LARGOS (Estilo v9.5) */
    div[data-baseweb="slider"] > div {
        height: 4px;
        background-color: #ff0000 !important;
    }
    div[role="slider"] {
        background-color: #ff0000 !important;
        width: 12px;
        height: 12px;
    }
    
    /* PANEL CENTRAL (El cambio que buscabas) */
    .canvas-container {
        border: 1px solid #33FF33;
        background-color: #e0e0e0; /* Fondo claro de la v9.5 */
        border-radius: 2px;
    }

    /* MÓDULOS DERECHA */
    .module-card {
        border: 1px solid #33FF33;
        background-color: #000000;
        padding: 10px;
        margin-bottom: 10px;
        color: #33FF33;
        font-family: 'Courier New', monospace;
        font-size: 12px;
    }

    /* Etiquetas de Sliders */
    label {
        color: #33FF33 !important;
        font-size: 10px !important;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# GENERADOR DEL VISUALIZADOR V9.5 (MAPA DE RADIO)
# =========================================================
def render_v95_visualizer():
    # Creamos el fondo claro con la línea de división central
    h, w = 550, 1100
    # Color base: Gris muy claro (como en tu foto)
    img = np.ones((h, w, 3), dtype=np.uint8) * 225
    
    # Línea de división central (Eje de frecuencia)
    img[:, w//2 - 1 : w//2 + 1] = [30, 30, 30]
    
    # Añadir los puntos de señal (Negros/Grises)
    # En la v9.5 los puntos son menos pero más marcados
    for _ in range(400):
        y, x = np.random.randint(0, h), np.random.randint(0, w)
        size = np.random.randint(1, 3)
        img[y:y+size, x:x+size] = [40, 40, 40]
        
    return img

# =========================================================
# ESTRUCTURA DE LA INTERFAZ V9.5
# =========================================================

# Encabezado v9.5
st.markdown('<div class="title-v95">NEXUS-7: DEEP SPACE ANALYZER v9.0</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#33FF33; font-size:12px; margin-top:-10px;">HEURISTIC CORE ENABLED // SIGNAL CAPTURE ACTIVE</p>', unsafe_allow_html=True)

# Sección de Sliders (Líneas Rojas que cruzan la pantalla)
col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    st.selectbox("OBJETIVO", ["Ross 128 b", "Próxima b", "Kepler"], label_visibility="visible")
with col2:
    st.select_slider("ESCALA KARDASHOV", options=["I", "II", "III"], value="III")
with col3:
    st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.markdown("<br>", unsafe_allow_html=True)

# Cuerpo Principal
main_col, side_col = st.columns([3, 1])

with main_col:
    # El visualizador central con el nuevo estilo
    canvas = render_v95_visualizer()
    st.image(canvas, use_container_width=True)
    st.markdown("<p style='color:#33FF33; font-size:10px;'>BARRIDO DE FRECUENCIA ACTIVO | SENSOR: VLA-ARRAY 4</p>", unsafe_allow_html=True)

with side_col:
    # Módulo de Datos
    st.markdown(f"""
    <div class="module-card">
        SISTEMA: ROSS 128 b | DISTANCIA: 4.22 AL<br>
        ZONA: Habitable | ESTRELLA: Enana Roja<br>
        <span style="color: #00FF00;">● ANALIZANDO...</span>
    </div>
    """, unsafe_allow_html=True)

    # Motor IA
    st.markdown("<p style='color:#33FF33; font-weight:bold; margin-bottom:2px;'>🧠 AI HEURISTIC ENGINE</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#33FF33; font-size:10px;'>CONFIANZA: 94.8%</p>", unsafe_allow_html=True)
    st.progress(0.94)

    # Mensaje del Operador
    st.markdown("""
    <div style="border-left: 2px solid #33FF33; padding-left: 10px; margin: 15px 0;">
        <i style="color:#33FF33; font-size:11px;">"Operador, la señal detectada es de origen tecnológico. Coherencia confirmada."</i>
    </div>
    """, unsafe_allow_html=True)

    # Log Terminal Compacto
    st.markdown(f"""
    <div class="module-card" style="height: 180px; overflow: hidden; font-size: 10px;">
        [{datetime.now().strftime('%H:%M:%S')}] Escaneando sector...<br>
        [LOG] Anomalía detectada en canal 298.<br>
        [LOG] Coherencia de señal confirmada.<br>
        [LOG] Desplazamiento Doppler detectado.<br>
        ------------------------------------<br>
        ◆ NEXUS-7 CORE: ONLINE<br>
        ◆ IA HEURÍSTICA: BUSCANDO...
    </div>
    """, unsafe_allow_html=True)

st.caption("v9.5 | SECURE LINK | ACCESO RESTRINGIDO")
