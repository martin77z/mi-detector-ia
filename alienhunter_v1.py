import streamlit as st
import numpy as np
from datetime import datetime

# =========================================================
# 1. CSS DE ALTA PRECISIÓN (NEXUS-7 LOOK)
# =========================================================
st.set_page_config(page_title="NEXUS-7: DEEP SPACE ANALYZER", layout="wide")

st.markdown("""
<style>
    /* Fondo negro absoluto */
    .stApp { background-color: #000000; }
    
    /* Forzar el color verde neón en todos los textos */
    h1, h2, h3, p, span, label, .stSelectbox label, .stSlider label {
        color: #33FF33 !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Estilo de los contenedores de la derecha (Bordes brillantes) */
    .nexus-container {
        border: 2px solid #33FF33;
        padding: 15px;
        background-color: #000800;
        margin-bottom: 15px;
        box-shadow: 0 0 10px #114411;
    }

    /* Mensajes de IA (Cuadro verde con cursiva) */
    .ai-msg {
        background-color: #002200;
        border-left: 5px solid #33FF33;
        padding: 10px;
        font-style: italic;
        font-size: 0.9em;
    }

    /* Terminal Log */
    .terminal {
        border: 1px solid #225522;
        padding: 8px;
        background-color: #000500;
        font-size: 11px;
        height: 200px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. GENERADOR DE SEÑAL DINÁMICA (Efecto Foto)
# =========================================================
def generar_signal_pro():
    h, w = 450, 800
    # Ruido de fondo granulado (como el de tu monitor)
    img = np.random.normal(50, 20, (h, w))
    
    # Dibujar la señal inclinada (Tecnofirma)
    for i in range(h):
        # Desplazamiento Doppler (inclinación)
        centro = 420 + int(i * 0.07)
        if centro < w:
            # Resplandor naranja/verde (capas de brillo)
            img[i, centro-6:centro+7] = 120 # Aura
            img[i, centro-2:centro+3] = 255 # Núcleo blanco
    return img

# =========================================================
# 3. ESTRUCTURA DE LA INTERFAZ
# =========================================================

# Encabezado
st.markdown("<h1>NEXUS-7: DEEP SPACE ANALYZER v9.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top:-20px'>HEURISTIC CORE ENABLED // SIGNAL CAPTURE ACTIVE</p>", unsafe_allow_html=True)

# Fila 1: Selectores y Ganancia
c1, c2, c3 = st.columns([2, 2, 4])
with c1:
    target = st.selectbox("OBJETIVO", ["Ross 128 b", "Próxima b", "Kepler-452b"])
with c2:
    st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
with c3:
    st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.divider()

# Fila 2: Main Display y AI Engine
col_main, col_side = st.columns([2.5, 1])

with col_main:
    # Generamos la señal exactamente como se ve en tu monitor
    display_data = generar_signal_pro()
    # use_container_width=True es CLAVE para evitar errores en consola
    st.image(display_data, use_container_width=True, clamp=True)
    st.caption("BARRIDO DE FRECUENCIA ACTIVO | SENSOR: VLA-ARRAY 4")

with col_side:
    # Cuadro de Sistema
    st.markdown(f"""
    <div class="nexus-container">
        SISTEMA: {target} | DISTANCIA: 4.22 AL<br>
        ZONA: Habitable | ESTRELLA: Enana Roja<br>
        <span style="color: #FF0000;">● ANALIZANDO...</span>
    </div>
    """, unsafe_allow_html=True)

    # AI Engine
    st.markdown("### 🧠 AI HEURISTIC ENGINE")
    st.write("CONFIANZA: 94.8%")
    st.progress(0.94)

    # Cita del Operador
    st.markdown(f"""
    <div class="ai-msg">
        "Operador, la señal detectada es de origen tecnológico. 
        Coherencia confirmada en la línea de Hidrógeno (1420 MHz)."
    </div>
    """, unsafe_allow_html=True)

    # Terminal de logs
    st.markdown(f"""
    <div class="terminal">
        [{datetime.now().strftime('%H:%M:%S')}] Escaneando sector...<br>
        [LOG] Anomalía detectada en canal 298.<br>
        [LOG] Coherencia de señal confirmada.<br>
        [LOG] Desplazamiento Doppler detectado.<br>
        ◆ NEXUS-7 CORE: ONLINE<br>
        ◆ IA HEURÍSTICA: BUSCANDO PATRONES...
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("SISTEMA DE SEGURIDAD NEXUS-7 v9.5 | PROYECTO DE RADIOASTRONOMÍA AVANZADA")
