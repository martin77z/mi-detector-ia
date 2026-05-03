import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN NEXUS-7 ULTIMATE v7.1
st.set_page_config(page_title="NEXUS-7 ULTIMATE v7.1", page_icon="👽", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #010a01; color: #00FF41; font-family: 'Courier New', monospace; }
    .stSelectbox, .stSlider { background-color: #051505; border-radius: 5px; padding: 10px; border: 1px solid #00FF41; }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; height: 3.5em; width: 100%; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 50px #00FF41; }
    .detail-card { background-color: #051505; border: 1px solid #00FF41; padding: 20px; border-radius: 5px; }
    .alert-active { color: #ff0000; animation: blink 1s infinite; font-weight: bold; font-size: 1.5em; text-align: center; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# BASE DE DATOS COMPLETA CON DISTANCIAS
info_objetivos = {
    "Próxima b": {"Dist": "4.2 AL", "Tipo": "Rocoso", "Nota": "Candidato cercano."},
    "Ross 128 b": {"Dist": "11.0 AL", "Tipo": "Templado", "Nota": "Estrella estable."},
    "Gliese 581g": {"Dist": "20.0 AL", "Tipo": "Super-Tierra", "Nota": "Zona habitable confirmada."},
    "TRAPPIST-1e": {"Dist": "40.0 AL", "Tipo": "Rocoso", "Nota": "Sistema de 7 planetas."},
    "K2-18b": {"Dist": "124.0 AL", "Tipo": "Hicéano", "Nota": "Vapor de agua detectado."},
    "Estrella de Tabby": {"Dist": "1,470 AL", "Tipo": "Anomalía", "Nota": "¿Megaestructura?"},
    "Sector Wow!": {"Dist": "1,800 AL", "Tipo": "Histórico", "Nota": "Señal de 1977."},
    "Cúmulo M13": {"Dist": "25,000 AL", "Tipo": "Cúmulo", "Nota": "Mensaje de Arecibo enviado aquí."},
    "Sagitario A*": {"Dist": "26,000 AL", "Tipo": "Agujero Negro", "Nota": "Centro Galáctico."},
    "Andrómeda": {"Dist": "2.5M AL", "Tipo": "Galaxia", "Nota": "Búsqueda Extragaláctica."}
}

st.title("📡 NEXUS-7: ULTIMATE CONTACT v7.1")

# --- PANEL DE CONTROL SUPERIOR (DATOS DE NAVEGACIÓN RESTAURADOS) ---
c1, c2, c3 = st.columns([1.5, 1.5, 3])

with c1:
    objetivo = st.selectbox("🎯 DESTINO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c2:
    ganancia = st.slider("📶 GANANCIA (dB)", 150, 400, 250)
    audio_on = st.checkbox("🔊 AUDIO-LOG", value=True)

with c3:
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <h3 style='margin:0; color:#00FF41;'>📊 TELEMETRÍA DE SECTOR</h3>
        <p style='margin:5px 0;'><b>DISTANCIA:</b> <span style='color:white;'>{data['Dist']}</span> | <b>RETRASO:</b> <span style='color:white;'>{data['Dist']}</span></p>
        <p style='margin:5px 0;'><b>TIPO:</b> {data['Tipo']} | <b>CIVILIZACIÓN:</b> {k_scale}</p>
        <p style='margin:5px 0; font-style:italic; font-size:0.9em;'>{data['Nota']}</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col_main, col_decoder = st.columns([2, 1])

with col_main:
    v_cascada = st.empty()
    v_potencia = st.empty()

with col_decoder:
    st.subheader("📟 DECODER & IA")
    v_alerta = st.empty()
    v_terminal = st.empty()
    v_matrix = st.empty()

# LÓGICA DE ESCANEO
if st.button("🚀 INICIAR ESCANEO PROFUNDO"):
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    
    prob_map = {"Tipo I": 0.7, "Tipo II": 0.5, "Tipo III": 0.2} # Tipo III es muy probable
    es_alien = random.random() > prob_map[k_scale]
    
    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.05)
        
        if 0 <= centro < 400:
            if es_alien:
                ruido[centro] += (ganancia / 4)
            else:
                ruido[centro-10:centro+11] += (ganancia / 15)
            
        matriz[t] = ruido
        
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41' if not es_alien else '#ff0000', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 120)
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        
        v_terminal.code(f"DESTINO: {objetivo}\nDISTANCIA: {data['Dist']}\nPROCESANDO: {t}%\nSTATUS: {'ANALIZANDO' if t<99 else 'COMPLETO'}")
        time.sleep(0.01)

    if es_alien:
        v_alerta.markdown('<p class="alert-active">⚠️ CONTACTO INTELIGENTE CONFIRMADO ⚠️</p>', unsafe_allow_html=True)
        msg = np.random.choice([0, 1], size=(8, 8))
        v_matrix.write("MATRIZ DE DATOS RECUPERADA:")
        v_matrix.table(msg)
        st.success(f"¡Señal decodificada desde {data['Dist']}!")
    else:
        v_alerta.error("SCAN COMPLETO: Ruido natural.")

# HISTORIAL
if st.session_state.historial:
    st.divider()
    st.table(st.session_state.historial)
