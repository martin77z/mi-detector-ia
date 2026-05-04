import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# =========================================================
# 1. CONFIGURACIÓN TÉCNICA (Elimina los warnings de la consola)
# =========================================================
st.set_page_config(page_title="NEXUS-7: DEEP SPACE ANALYZER", layout="wide")

# Forzado de tema oscuro y eliminación de márgenes innecesarios
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p, span, label { 
        color: #33FF33 !important; 
        font-family: 'Courier New', Courier, monospace !important; 
    }
    
    /* MODIFICACIÓN DE SLIDERS A ROJO (como en tu foto original) */
    div[data-baseweb="slider"] > div > div {
        background-color: #FF0000 !important;
    }
    div[role="slider"] {
        background-color: #FF0000 !important;
        border: 2px solid #AA0000 !important;
    }

    .status-box { border: 2px solid #33FF33; padding: 15px; background-color: #001100; margin-bottom: 20px; }
    .terminal-log { border: 1px solid #33FF33; padding: 10px; background-color: #000800; font-size: 11px; }
    
    /* Color para la barra de progreso de la IA */
    .stProgress > div > div > div > div {
        background-color: #33CCFF;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. GENERADOR DE MAPA CON COLOR (MODIFICADO)
# =========================================================
def generar_mapa_estelar_color():
    # Creamos un lienzo RGB para tener control total del color
    # h, w = Altura, Anchura del visualizador central
    h, w = 500, 1000
    img = np.zeros((h, w, 3), dtype=np.uint8)
    
    # === ¡AQUÍ ESTÁ EL CAMBIO DE COLOR! ===
    # En lugar de blanco, ponemos un fondo Azul Espacial Profundo (Deep Blue)
    # RGB: [0, 10, 35]
    img[:] = [0, 10, 35] 
    
    # Añadimos ruido estelar granulado (estrellas)
    # Las estrellas serán de un color Cian Brillante
    # RGB: [50, 255, 255]
    num_estrellas = 250
    for _ in range(num_estrellas):
        y = np.random.randint(0, h)
        x = np.random.randint(0, w)
        img[y-1:y+1, x-1:x+1] = [50, 255, 255] # Estrellas Cian
    
    # Línea de señal Doppler (la traza central)
    # La señal será de un color Verde Neón Brilhante
    # RGB: [51, 255, 51]
    for i in range(h):
        # La señal central (el "Drift")
        centro = 450 + int(i * 0.05)
        if centro < w:
            img[i, centro-1:centro+2] = [51, 255, 51] # Señal Verde
            
    return img

# =========================================================
# 3. INTERFAZ DE COMANDO NEXUS-7
# =========================================================

# Título Principal (v9.0)
st.markdown("<h1>NEXUS-7: DEEP SPACE ANALYZER v9.0</h1>", unsafe_allow_html=True)
st.write("HEURISTIC CORE ENABLED // SIGNAL CAPTURE ACTIVE")

# Fila Superior: Controles (Sliders ROJOS)
col_input1, col_input2, col_input3 = st.columns([2, 3, 3])
with col_input1:
    objetivo = st.selectbox("OBJETIVO", ["Ross 128 b", "Próxima b", "Andrómeda"])
with col_input2:
    st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"], value="Tipo III")
with col_input3:
    st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.markdown("<hr style='border: 1px solid #33FF33;'>", unsafe_allow_html=True)

# Layout Principal: Visualizador | Panel de IA
col_viz, col_ia = st.columns([2.5, 1])

with col_viz:
    # Generamos el mapa estelar con los NUEVOS COLORES
    mapa_color = generar_mapa_estelar_color()
    # USAMOS use_container_width=True para la visualización modular correcta
    st.image(mapa_color, use_container_width=True)
    st.markdown("<p style='font-size: 10px; color: #33FF33;'>BARRIDO DE FRECUENCIA ACTIVO | SENSOR: VLA-ARRAY 4</p>", unsafe_allow_html=True)

with col_ia:
    # Cuadro de Info del Sistema (Superior Derecha)
    st.markdown(f"""
    <div class="status-box">
        SISTEMA: {objetivo} | DISTANCIA: 4.22 AL<br>
        ZONA: Habitable | ESTRELLA: Enana Roja<br>
        <span style="color: #FF0000;">● ANALIZANDO...</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧠 AI HEURISTIC ENGINE")
    st.write("CONFIANZA DE LA IA: 94.8%")
    st.progress(0.94)
    
    # El mensaje del Operador (Cita textual en verde brillante)
    st.markdown("""
    <p style='color: #33FF33; font-style: italic; font-size: 13px; background-color: #001100; padding: 10px; border-left: 3px solid #33FF33;'>
    *"Operador, la señal detectada es de origen tecnológico. La entropía está bajando. No es un fenómeno natural. Coherencia confirmada en la línea de Hidrógeno."*
    </p>
    """, unsafe_allow_html=True)
    
    # Terminal Log (El cuadro de logs estilo terminal de la foto)
    st.markdown(f"""
    <div class="terminal-log">
        [{datetime.now().strftime('%H:%M:%S')}] Iniciando escaneo sector Ross...<br>
        [00:23:50] Confirmado: Drift doppler detectado.<br>
        [00:21:43] Anomalía de banda estrecha en 1420MHz.<br>
        -------------------------------------------<br>
        ◆ SISTEMA NEXUS-7 INICIALIZADO...<br>
        ◆ IA HEURÍSTICA: BUSCANDO PATRONES...
    </div>
    """, unsafe_allow_html=True)

# Footer de Seguridad
st.markdown("<br><hr style='border: 0.5px solid #33FF33;'>", unsafe_allow_html=True)
st.caption("SISTEMA DE SEGURIDAD NEXUS-7 v9.5 | PROTOCOLO DE RADIOASTRONOMÍA ACTIVO")
