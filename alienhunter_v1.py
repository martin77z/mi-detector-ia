import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN NEXUS-7 ACADEMY
st.set_page_config(page_title="NEXUS-7 ACADEMY v6.0", page_icon="🎓", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO VISUAL ORIGINAL RESTAURADO
st.markdown("""
    <style>
    .stApp { background-color: #030603; color: #00FF41; font-family: 'Courier New', monospace; }
    .stSelectbox, .stSlider { background-color: #091309; border-radius: 5px; padding: 10px; border: 1px solid #1a3a1a; }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; height: 3.5em; width: 100%; border-radius: 0px;
    }
    .stButton>button:hover { 
        background-color: #00FF41; color: #000; box-shadow: 0 0 40px #00FF41; 
    }
    .detail-card { 
        background-color: #091309; border: 1px solid #1a3a1a; padding: 15px; border-radius: 5px; color: #00FF41;
    }
    .guide-card {
        background-color: #051005; border-left: 5px solid #00FF41; padding: 10px; margin-bottom: 20px; font-size: 0.85em;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;} 
    </style>
    """, unsafe_allow_html=True)

# BASE DE DATOS DETALLADA (RESTAURADA)
info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Tipo": "Planeta Rocoso", "Retraso": "4.2 años", "Nota": "Ubicado en la zona habitable de Próxima Centauri. Candidato principal para vida cercana."},
    "Ross 128 b": {"Dist": 11.0, "Tipo": "Mundo Templado", "Retraso": "11.0 años", "Nota": "Orbita una enana roja inactiva, lo que aumenta las posibilidades de atmósfera estable."},
    "Gliese 581g": {"Dist": 20.0, "Tipo": "Super-Tierra", "Retraso": "20.0 años", "Nota": "Mundo de masa superior a la Tierra, posiblemente con agua líquida en superficie."},
    "TRAPPIST-1e": {"Dist": 40.0, "Tipo": "Planeta Rocoso", "Retraso": "40.0 años", "Nota": "Uno de los 7 planetas terrestres del sistema. Altamente similar a la Tierra en densidad."},
    "K2-18b": {"Dist": 124.0, "Tipo": "Mundo Hicéano", "Retraso": "124.0 años", "Nota": "Posible océano global bajo una atmósfera rica en hidrógeno. Detectado por el JWST."},
    "Estrella de Tabby": {"Dist": 1470.0, "Tipo": "Anomalía Estelar", "Retraso": "1470 años", "Nota": "Sus fluctuaciones de luz no coinciden con ningún modelo natural conocido. ¿Dyson?"},
    "Sector Wow!": {"Dist": 1800.0, "Tipo": "Región Histórica", "Retraso": "1800 años", "Nota": "Coordenadas exactas de la señal de 72 segundos captada por el Big Ear en 1977."},
    "Cúmulo M13": {"Dist": 25000.0, "Tipo": "Cúmulo Globular", "Retraso": "25000 años", "Nota": "Contiene ~300,000 estrellas. Recibió el mensaje de Arecibo diseñado por Drake y Sagan."},
    "Sagitario A*": {"Dist": 26000.0, "Tipo": "Agujero Negro", "Retraso": "26000 años", "Nota": "El corazón masivo de nuestra galaxia. Emite radiación violenta y ruidosa."},
    "Andrómeda (M31)": {"Dist": 2500000.0, "Tipo": "Galaxia Espiral", "Retraso": "2.5M años", "Nota": "Nuestra vecina más grande. Las señales recibidas hoy salieron antes de los humanos."}
}

st.title("📡 NEXUS-7: DEEP SPACE ACADEMY v6.0")

# --- GUÍA DE INTERPRETACIÓN (PUNTO A) ---
with st.expander("📖 GUÍA DE INTERPRETACIÓN DE DATOS (PUNTO A)"):
    st.markdown("""
    <div class="guide-card">
    <b>1. Radar de Cascada:</b> El eje horizontal es la frecuencia. El eje vertical es el tiempo (arriba es el presente).
    <br><b>2. Banda Estrecha:</b> Si ves una línea fina (1-2px), es tecnología artificial.
    <br><b>3. Banda Ancha:</b> Bloques gruesos indican interferencia (RFI) o ruido estelar natural.
    <br><b>4. Deriva Doppler:</b> Si la línea está inclinada, la fuente se mueve respecto a la Tierra.
    </div>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL SUPERIOR ---
c_ctrl, c_desc = st.columns([2, 3])

with c_ctrl:
    st.subheader("⌨️ PANEL DE CONTROL")
    objetivo = st.selectbox("Seleccionar Objetivo", list(info_objetivos.keys()))
    ganancia = st.slider("Potencia de Antena (dB)", 100, 300, 180)
    trigger = st.button("🚀 INICIAR CAPTURA ESPECTRAL")

with c_desc:
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <h3>DETALLES DEL SECTOR:</h3>
        <p>🔭 <b>Tipo:</b> {data['Tipo']}</p>
        <p>📏 <b>Distancia:</b> {data['Dist']} años luz</p>
        <p>⏳ <b>Retraso de señal:</b> {data['Retraso']}</p>
        <p>📝 <i>{data['Nota']}</i></p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- PANTALLAS DE DATOS ---
col_vis, col_ia = st.columns([2, 1])

with col_vis:
    st.write("🛰️ **VISUALIZACIÓN DE ESPECTRO EN VIVO**")
    v_cascada = st.empty()
    v_potencia = st.empty() 

with col_ia:
    st.write("🤖 **INFORME DE IA**")
    v_terminal = st.empty()
    v_resultado = st.empty()

# LÓGICA DE ESCANEO
if trigger:
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    es_alien = random.random() > 0.4 
    
    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.07)
        
        if 0 <= centro < 400:
            if es_alien:
                ruido[centro] += (ganancia / 5)
            else:
                ruido[centro-8:centro+9] += (ganancia / 15)
            
        matriz[t] = ruido
        
        # Plot Cascada
        fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        # Plot Potencia
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 70) 
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        
        v_terminal.code(f"REC_SIG: {t}/{pasos}\nVELOCIDAD: 300.000 KM/S\nESTADO: ANALIZANDO FRECUENCIAS...\nCOHERENCIA: {'ALTA' if es_alien else 'BAJA'}")
        time.sleep(0.01)

    if es_alien:
        v_resultado.success("✅ TECNOSÍGNAL DETECTADA: ORIGEN INTELIGENTE")
        st.session_state.historial.append({"Hora": datetime.now().strftime("%H:%M"), "Sector": objetivo, "Resultado": "EXITO"})
    else:
        v_resultado.error("❌ RFI DETECTADA: INTERFERENCIA LOCAL")

# HISTORIAL
if st.session_state.historial:
    st.divider()
    st.subheader("📂 ARCHIVO DE HALLAZGOS")
    st.table(st.session_state.historial)
