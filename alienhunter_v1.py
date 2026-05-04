import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# =========================================================
# 1. NEXUS CORE: CONFIGURACIÓN DE INTERFAZ OSCURA
# =========================================================
st.set_page_config(page_title="NEXUS-7: DEEP SPACE ANALYZER", layout="wide")

# CSS para forzar el fondo negro y el verde neón de tu foto
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p, span, label, .stMarkdown { 
        color: #33FF33 !important; 
        font-family: 'Courier New', Courier, monospace !important; 
    }
    .status-box { border: 2px solid #33FF33; padding: 15px; background-color: #001100; margin-bottom: 20px; }
    .terminal-log { border: 1px solid #33FF33; padding: 10px; background-color: #000800; font-size: 11px; color: #33FF33; }
    .stProgress > div > div > div > div { background-color: #33FF33; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. GENERADOR DE SEÑAL DOPPLER (La línea inclinada)
# =========================================================
def generar_visualizador_pro():
    # Creamos el mapa estelar de tu monitor
    width, height = 800, 450
    # Fondo con ruido estático
    img = np.random.normal(40, 10, (height, width))
    
    # Inyección de la señal con "Drift Doppler" (inclinación)
    for i in range(height):
        # La señal se desplaza lateralmente a medida que baja (como en tu foto)
        centro = 380 + int(i * 0.08)
        if centro < width:
            img[i, centro-2:centro+3] = 220  # El núcleo blanco de la señal
            img[i, centro-5:centro+6] = 160  # El resplandor naranja/verde
            
    return img

# =========================================================
# 3. DASHBOARD DE CONTROL NEXUS-7
# =========================================================

# Título y Estado
st.markdown("<h1>NEXUS-7: DEEP SPACE ANALYZER v9.0</h1>", unsafe_allow_html=True)
st.write("HEURISTIC CORE ENABLED // SIGNAL CAPTURE ACTIVE")

# Fila de Controles Superiores
c1, c2, c3 = st.columns([2, 2, 3])
with c1:
    target = st.selectbox("OBJETIVO", ["Ross 128 b", "Próxima b", "Kepler-452b"])
with c2:
    st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
with c3:
    st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.markdown("<hr style='border: 1px solid #33FF33;'>", unsafe_allow_html=True)

# Layout Principal: Visualizador | Panel de IA
col_viz, col_ia = st.columns([2.5, 1])

with col_viz:
    # Generamos la imagen del waterfall
    data_wf = generar_visualizador_pro()
    # USAMOS use_container_width=True para eliminar los avisos de la foto 1
    st.image(data_wf, use_container_width=True, clamp=True)
    st.caption("BARRIDO DE BANDA BASE - FRECUENCIA CENTRAL: 1420.405 MHz (H-Line)")

with col_ia:
    # Info del Sistema
    st.markdown(f"""
    <div class="status-box">
        SISTEMA: {target} | DISTANCIA: 4.22 AL<br>
        ZONA: Habitable | ESTRELLA: Enana Roja<br>
        <span style="color: #FF3333;">● ANALIZANDO</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧠 AI HEURISTIC ENGINE")
    st.write("CONFIANZA DE LA IA: 94.8%")
    st.progress(0.94)
    
    # Mensaje del Operador (Cita textual de tu monitor)
    st.info("""
    *"Operador, la señal en 298px es de origen tecnológico. La entropía está bajando. No es un fenómeno natural. 
    Coherencia confirmada en la línea de Hidrógeno."*
    """)
    
    # Terminal de Logs (Mismo contenido que tu foto 2)
    st.markdown(f"""
    <div class="terminal-log">
        [00:22:02] Patrón detectado. Extrayendo estructura...<br>
        [00:23:50] Confirmado: Drift doppler coincide con rotación.<br>
        [00:21:43] Detectando anomalía de banda estrecha...<br>
        [00:21:39] Iniciando barrido en {target}...<br>
        ◆ SISTEMA NEXUS-7 INICIALIZADO...<br>
        ◆ IA HEURÍSTICA ONLINE.<br>
        -------------------------------------------<br>
        RECEIVING_DATA_STREAM...
    </div>
    """, unsafe_allow_html=True)

# Footer de Seguridad
st.divider()
st.caption("SISTEMA NEXUS-7 v9.5 | PROTOCOLO DE TRANSMISIÓN ENCRIPTADO")
