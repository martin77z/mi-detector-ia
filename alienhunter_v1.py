import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN MAESTRA
st.set_page_config(page_title="NEXUS-7 OMNIBUS v7.5", page_icon="📡", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# --- ESTILO VISUAL INTEGRAL ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .stSelectbox, .stSlider { background-color: #051205; border-radius: 5px; padding: 10px; border: 1px solid #00FF41; }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; height: 3.5em; width: 100%; text-transform: uppercase; border-radius: 0;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 50px #00FF41; }
    .detail-card { background-color: #051205; border: 1px solid #00FF41; padding: 20px; border-radius: 5px; height: 100%; }
    .guide-box { background-color: #021a02; border-left: 4px solid #00FF41; padding: 10px; font-size: 0.8em; margin-bottom: 15px; }
    .alert-active { color: #ff0000; animation: blink 1s infinite; font-weight: bold; font-size: 1.4em; text-align: center; border: 2px solid #ff0000; padding: 10px; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# BASE DE DATOS MAESTRA (TODOS LOS DETALLES)
info_objetivos = {
    "Próxima b": {"Dist": "4.2 AL", "Tipo": "Rocoso / Habitable", "Retraso": "4.2 años", "Nota": "Vecino más cercano. Posible civilización Tipo I."},
    "Ross 128 b": {"Dist": "11.0 AL", "Tipo": "Exoplaneta Templado", "Retraso": "11.0 años", "Nota": "Estrella enana roja muy estable. Señal limpia."},
    "Gliese 581g": {"Dist": "20.0 AL", "Tipo": "Super-Tierra", "Retraso": "20.0 años", "Nota": "Primer candidato histórico a mundo habitable."},
    "TRAPPIST-1e": {"Dist": "40.0 AL", "Tipo": "Sistema Multi-planetario", "Retraso": "40.0 años", "Nota": "7 planetas similares a la Tierra en órbita cerrada."},
    "K2-18b": {"Dist": "124.0 AL", "Tipo": "Mundo Hicéano", "Retraso": "124.0 años", "Nota": "JWST detectó metano y vapor de agua aquí."},
    "Estrella de Tabby": {"Dist": "1,470 AL", "Tipo": "Anomalía KIC 8462852", "Retraso": "1,470 años", "Nota": "Oscurecimientos masivos. ¿Enjambre de Dyson?"},
    "Sector Wow!": {"Dist": "1,800 AL", "Tipo": "Histórico SETI", "Retraso": "1,800 años", "Nota": "Origen de la famosa señal captada en 1977."},
    "Cúmulo M13": {"Dist": "25,000 AL", "Tipo": "Cúmulo Globular", "Retraso": "25,000 años", "Nota": "Contiene 300,000 estrellas. Alta densidad de objetivos."},
    "Sagitario A*": {"Dist": "26,000 AL", "Tipo": "Agujero Negro Supermasivo", "Retraso": "26,000 años", "Nota": "Corazón de la Vía Láctea. Mucha radiación de fondo."},
    "Andrómeda (M31)": {"Dist": "2.5M AL", "Tipo": "Galaxia Vecina", "Retraso": "2.5 Millones años", "Nota": "Búsqueda de civilizaciones Tipo III extragalácticas."}
}

st.title("📡 NEXUS-7 OMNIBUS: FIRST CONTACT v7.5")

# --- GUÍA RÁPIDA DE OPERADOR ---
with st.expander("📖 MANUAL DE OPERACIONES SETI (PUNTO A)"):
    st.markdown("""
    <div class="guide-box">
    <b>IDENTIFICACIÓN:</b><br>
    - 🟢 <b>Línea fina vertical:</b> Señal artificial de banda estrecha (Contacto).<br>
    - 🔵 <b>Manchas gruesas:</b> Ruido térmico o interferencia humana (RFI).<br>
    - 📐 <b>Inclinación:</b> Deriva Doppler causada por el movimiento planetario.<br>
    - ⚡ <b>Amplitud:</b> A mayor Ganancia, más definición del pico en el espectro.
    </div>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL SUPERIOR ---
c_ctrl, c_gain, c_tele = st.columns([1.5, 1.5, 3])

with c_ctrl:
    st.subheader("🎯 NAVEGACIÓN")
    objetivo = st.selectbox("OBJETIVO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 NIVEL KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c_gain:
    st.subheader("📶 ANTENA")
    ganancia = st.slider("GANANCIA (dB)", 100, 500, 200)
    audio = st.checkbox("🔊 AUDIO-MONITOR", value=True)
    trigger = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with c_tele:
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <h3 style='margin:0; color:#00FF41;'>📊 TELEMETRÍA DE SECTOR</h3>
        <p style='margin:5px 0;'><b>SISTEMA:</b> {objetivo.upper()} | <b>TIPO:</b> {data['Tipo']}</p>
        <p style='margin:5px 0;'><b>DISTANCIA:</b> {data['Dist']} | <b>RETRASO:</b> {data['Retraso']}</p>
        <hr style='border:0.5px solid #1a3a1a;'>
        <p style='margin:0; font-size:0.9em; color:#888;'><i>{data['Nota']}</i></p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- ÁREA DE TRABAJO ---
col_radar, col_decoder = st.columns([2, 1])

with col_radar:
    st.write("🛰️ **VISUALIZACIÓN DE ESPECTRO**")
    v_cascada = st.empty()
    v_potencia = st.empty()

with col_decoder:
    st.subheader("📟 DECODER IA")
    v_alerta = st.empty()
    v_terminal = st.empty()
    v_matrix = st.empty()

# LÓGICA DE ESCANEO
if trigger:
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    
    # Probabilidad según Kardashev (Más fácil detectar Tipo III)
    prob_map = {"Tipo I": 0.8, "Tipo II": 0.5, "Tipo III": 0.2}
    es_alien = random.random() > prob_map[k_scale]
    
    # Audio inicial
    if audio: st.components.v1.html("<script>new Audio('https://www.soundjay.com/misc/sounds/white-noise-01.mp3').play();</script>", height=0)

    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.06)
        
        if 0 <= centro < 400:
            if es_alien:
                # SEÑAL ALIEN (Banda estrecha)
                ruido[centro] += (ganancia / 4.5)
            else:
                # RFI (Banda ancha)
                ruido[centro-8:centro+9] += (ganancia / 15)
            
        matriz[t] = ruido
        
        # Render Waterfall
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        # Render Potencia
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41' if not es_alien else '#ff0000', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 150)
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        
        v_terminal.code(f"SCANNING: {objetivo}\nGANANCIA: {ganancia} dB\nPROCESANDO TRAMA: {t}%\nCOHERENCIA: {'DETECTADA' if es_alien and t > 50 else 'BUSCANDO...'}")
        time.sleep(0.01)

    # FINAL DE ESCANEO
    if es_alien:
        if audio: st.components.v1.html("<script>new Audio('https://www.soundjay.com/buttons/beep-01a.mp3').play();</script>", height=0)
        v_alerta.markdown('<p class="alert-active">⚠️ ALERTA: CONTACTO INTELIGENTE ⚠️</p>', unsafe_allow_html=True)
        
        # Generar matriz binaria (Decodificación)
        msg = np.random.choice([0, 1], size=(8, 8))
        v_matrix.write("🔢 MATRIZ BINARIA DECODIFICADA:")
        v_matrix.table(msg)
        
        st.session_state.historial.append({"Hora": datetime.now().strftime("%H:%M"), "Lugar": objetivo, "K-Scale": k_scale, "Result": "ÉXITO"})
    else:
        v_alerta.error("SCAN COMPLETO: Sin patrones de inteligencia.")

# HISTORIAL
if st.session_state.historial:
    st.divider()
    st.subheader("📂 ARCHIVO DE CIVILIZACIONES")
    st.table(st.session_state.historial)
