import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# =========================================================
# 1. FORZADO DE MODO OSCURO (ESENCIA NEXUS-7)
# =========================================================
st.set_page_config(page_title="NEXUS-7: DEEP SPACE ANALYZER", layout="wide")

# Este bloque de CSS es el más importante: fuerza el fondo NEGRO y textos VERDES
st.markdown("""
<style>
    /* Forzar fondo negro en toda la app */
    .stApp {
        background-color: #000000;
    }
    header, .stToolbar {
        background-color: #000000 !important;
    }
    /* Estilo para los textos y títulos */
    h1, h2, h3, p, span, label {
        color: #33FF33 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    /* Estilo para los cuadros de la derecha */
    .status-box {
        border: 2px solid #33FF33;
        padding: 15px;
        background-color: #001100;
        margin-bottom: 20px;
    }
    .terminal-log {
        border: 1px solid #33FF33;
        padding: 10px;
        background-color: #000800;
        height: 250px;
        font-size: 11px;
        line-height: 1.4;
    }
    /* Estilo para los sliders */
    .stSlider label { color: #33FF33 !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. GENERADOR DE MAPA ESTELAR / WATERFALL
# =========================================================
def generar_espacio_profundo():
    # Creamos un fondo negro con "estrellas" (puntos blancos) como en tu foto
    width, height = 800, 500
    img = np.zeros((height, width))
    # Añadimos ruido aleatorio (estrellas)
    num_estrellas = 150
    for _ in range(num_estrellas):
        y = np.random.randint(0, height)
        x = np.random.randint(0, width)
        img[y-1:y+1, x-1:x+1] = 255
    
    # Inyectamos la señal inclinada característica del NEXUS-7
    for i in range(height):
        pos = 450 + int(i * 0.05) 
        if pos < width:
            img[i, pos-1:pos+2] = 200 # Señal de tecnofirma
    return img

# =========================================================
# 3. INTERFAZ DE COMANDO NEXUS-7
# =========================================================

# Título Principal
st.markdown("<h1 style='text-align: left;'>NEXUS-7: DEEP SPACE ANALYZER v9.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top: -20px;'>HEURISTIC CORE ENABLED // SIGNAL CAPTURE ACTIVE</p>", unsafe_allow_html=True)

# Fila Superior: Selectores
c1, c2, c3 = st.columns([2, 2, 3])
with c1:
    target = st.selectbox("OBJETIVO", ["Ross 128 b", "Próxima b", "Kepler-186f"])
with c2:
    st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
with c3:
    st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.markdown("<hr style='border: 1px solid #33FF33;'>", unsafe_allow_html=True)

# Cuerpo Principal
col_mapa, col_info = st.columns([2.5, 1])

with col_mapa:
    # Mostramos el mapa estelar con fondo negro
    espacio = generar_espacio_profundo()
    st.image(espacio, use_container_width=True, clamp=True)
    st.caption("SCANNER_MODE: BANDA ESTRECHA | FREQ_LOCK: 1420.405 MHz")

with col_info:
    # Cuadro de Sistema (Superior Derecha)
    st.markdown(f"""
    <div class="status-box">
        SISTEMA: {target} | DISTANCIA: 4.22 AL<br>
        ZONA: Habitable | ESTRELLA: Enana Roja<br>
        <span style="color: #FF0000;">● ANALIZANDO</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧠 AI HEURISTIC ENGINE")
    st.write("CONFIANZA DE LA IA: 94.8%")
    st.progress(0.94)
    
    # Mensaje del Operador
    st.markdown("""
    <p style='font-style: italic; font-size: 13px; color: #77FF77 !important;'>
    "Operador, la señal en 298px es de origen tecnológico. La entropía está bajando. No es un fenómeno natural. Coherencia confirmada en la línea de Hidrógeno."
    </p>
    """, unsafe_allow_html=True)
    
    # Terminal de Logs
    st.markdown(f"""
    <div class="terminal-log">
        [{datetime.now().strftime('%H:%M:%S')}] Patrón detectado. Extrayendo estructura...<br>
        [LOG] Confirmado: Drift doppler coincide con rotación.<br>
        [LOG] Detectando anomalía de banda estrecha...<br>
        [LOG] Iniciando barrido en {target}...<br>
        ◆ SISTEMA NEXUS-7 INICIALIZADO...<br>
        ◆ IA HEURÍSTICA ONLINE.<br>
        -------------------------------------------<br>
        READY FOR DATA INGESTION...
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><hr style='border: 0.5px solid #33FF33;'>", unsafe_allow_html=True)
st.caption("SISTEMA DE SEGURIDAD NEXUS-7 | ACCESO RESTRINGIDO")
