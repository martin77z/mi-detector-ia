import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime

# =========================================================
# 1. CONFIGURACIÓN Y ESTILO NEXUS-7 (LOOK MILITAR)
# =========================================================
st.set_page_config(page_title="NEXUS-7: DEEP SPACE ANALYZER", layout="wide")

st.markdown("""
<style>
    .main { background-color: #000000; }
    .stMetric { background-color: #000000; border: 1px solid #33FF33; }
    .stProgress > div > div > div > div { background-color: #33FF33; }
    section[data-testid="stSidebar"] { background-color: #050505; }
    .status-box {
        border: 2px solid #33FF33;
        padding: 15px;
        border-radius: 5px;
        background-color: #001100;
        color: #33FF33;
        font-family: 'Courier New', monospace;
    }
    .terminal-log {
        border: 1px solid #33FF33;
        padding: 10px;
        background-color: #000800;
        color: #33FF33;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        height: 250px;
        overflow-y: hidden;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LÓGICA DE DATOS (RECONSTRUCCIÓN DE SEÑAL)
# =========================================================
def generar_waterfall_nexus():
    # Creamos el efecto de la línea inclinada (Drift Doppler) que se ve en tu foto
    rows, cols = 400, 600
    data = np.random.normal(50, 15, (rows, cols))
    
    # Inyección de la señal inclinada (la línea naranja/blanca de la foto)
    for i in range(rows):
        pos = 350 + int(i * 0.1) # La inclinación
        data[i, pos-2:pos+3] = 255 # Brillo máximo
    return data

# =========================================================
# 3. INTERFAZ NEXUS-7 (ESTRUCTURA DE TU FOTO)
# =========================================================

# Título Principal Neón
st.markdown("<h1 style='color: #33FF33; font-family: monospace;'>NEXUS-7: DEEP SPACE ANALYZER v9.0</h1>", unsafe_allow_html=True)
st.write("HEURISTIC CORE ENABLED // SIGNAL CAPTURE ACTIVE")

# Fila Superior: Controles (Sliders como en la foto)
col_input1, col_input2, col_input3 = st.columns([2, 2, 3])
with col_input1:
    objetivo = st.selectbox("OBJETIVO", ["Próxima b", "Ross 128 b", "Andrómeda"])
with col_input2:
    st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"], value="Tipo I")
with col_input3:
    ganancia = st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.divider()

# Fila Central: Visualizador y Panel de IA
col_viz, col_ia = st.columns([2, 1])

with col_viz:
    # El Waterfall grande que ocupa el centro
    wf_data = generar_waterfall_nexus()
    st.image(wf_data, use_container_width=True, clamp=True)
    st.caption("ESPECTRO DE BANDA BASE - FRECUENCIA CENTRAL: 1420.405 MHz")

with col_ia:
    # Cuadro de Info del Sistema
    st.markdown(f"""
    <div class="status-box">
        SISTEMA: {objetivo} | DISTANCIA: 4.22 AL<br>
        ZONA: Habitable | ESTRELLA: Enana Roja<br>
        <span style="color: #FF3333;">● ANALIZANDO</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧠 AI HEURISTIC ENGINE")
    st.write("CONFIANZA DE LA IA: 94.8%")
    st.progress(94)
    
    # El mensaje del operador (el texto en cursiva verde)
    st.info("""
    *"Operador, la señal en 298px es de origen tecnológico. La entropía está bajando. No es un fenómeno natural. 
    Coherencia confirmada en la línea de Hidrógeno."*
    """)
    
    # Terminal Log (El cuadro de logs de la derecha)
    st.markdown(f"""
    <div class="terminal-log">
        [00:22:02] Patrón detectado. Extrayendo estructura semántica...<br>
        [00:23:50] Confirmado: El drift doppler coincide con rotación planetaria.<br>
        [00:21:43] Detectando anomalía de banda estrecha...<br>
        [00:21:39] Iniciando barrido en Próxima b...<br>
        ◆ SISTEMA NEXUS-7 INICIALIZADO...<br>
        ◆ IA HEURÍSTICA ONLINE.
    </div>
    """, unsafe_allow_html=True)

# Footer técnico
st.write("---")
st.caption(f"TELEMETRÍA ACTUALIZADA: {datetime.now().strftime('%H:%M:%S')} UTC | ENCRIPTACIÓN DE DATOS: AES-256")
