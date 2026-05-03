import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN MAESTRA
st.set_page_config(page_title="NEXUS-7 v7.8 AUTO", page_icon="📡", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .detail-card { background-color: #051205; border: 1px solid #00FF41; padding: 20px; border-radius: 5px; height: 100%; }
    .stSelectbox, .stSlider { background-color: #051205; border-radius: 5px; padding: 10px; border: 1px solid #00FF41; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; font-weight: bold; width: 100%; }
    .alert-active { color: #ff0000; animation: blink 1s infinite; font-weight: bold; text-align: center; border: 2px solid #ff0000; padding: 10px; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE OBJETIVOS (DISTANCIAS AUTOMÁTICAS) ---
info_objetivos = {
    "Próxima b": {"Dist": "4.2 AL", "Tipo": "Rocoso", "Retraso": "4.2 años", "Factor": 4.2},
    "Ross 128 b": {"Dist": "11.0 AL", "Tipo": "Templado", "Retraso": "11.0 años", "Factor": 11.0},
    "TRAPPIST-1e": {"Dist": "40.0 AL", "Tipo": "Multi-planetario", "Retraso": "40.0 años", "Factor": 40.0},
    "K2-18b": {"Dist": "124.0 AL", "Tipo": "Hicéano", "Retraso": "124.0 años", "Factor": 124.0},
    "Estrella de Tabby": {"Dist": "1,470 AL", "Tipo": "Anomalía KIC", "Retraso": "1,470 años", "Factor": 1470.0},
    "Sector Wow!": {"Dist": "1,800 AL", "Tipo": "SETI Histórico", "Retraso": "1,800 años", "Factor": 1800.0},
    "Cúmulo M13": {"Dist": "25,000 AL", "Tipo": "Cúmulo Globular", "Retraso": "25,000 años", "Factor": 25000.0},
    "Andrómeda (M31)": {"Dist": "2.5M AL", "Tipo": "Galaxia", "Retraso": "2.5M años", "Factor": 2500000.0}
}

st.title("📡 NEXUS-7 OMNIBUS: AUTO-TARGET v7.8")

# PANEL DE CONTROL
c_ctrl, c_gain, c_tele = st.columns([1.5, 1.5, 3])

with c_ctrl:
    st.subheader("🎯 NAVEGACIÓN")
    # Al cambiar el selectbox, todo lo demás se actualiza automáticamente
    objetivo = st.selectbox("SELECCIONAR OBJETIVO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 NIVEL KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c_gain:
    st.subheader("📶 ANTENA")
    ganancia = st.slider("GANANCIA (dB)", 100, 500, 250)
    trigger = st.button("🚀 INICIAR ESCANEO")

with c_tele:
    # AQUÍ SE MUESTRA LA DISTANCIA AUTOMÁTICA
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <h3 style='margin:0; color:#00FF41;'>📊 TELEMETRÍA AUTOMÁTICA</h3>
        <p style='margin:5px 0;'><b>SISTEMA:</b> {objetivo.upper()}</p>
        <p style='margin:5px 0;'><b>DISTANCIA:</b> {data['Dist']}</p>
        <p style='margin:5px 0;'><b>RETRASO DE SEÑAL:</b> {data['Retraso']}</p>
        <p style='margin:5px 0;'><b>TIPO:</b> {data['Tipo']}</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- LÓGICA DE ESCANEO ---
v_cascada = st.empty()
v_potencia = st.empty()
v_alerta = st.empty()

if trigger:
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    es_alien = random.random() > 0.4 # Probabilidad de contacto

    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.05)
        if 0 <= centro < 400 and es_alien:
            ruido[centro] += (ganancia / 5)
        
        matriz[t] = ruido
        
        # Render Waterfall
        fig1, ax1 = plt.subplots(figsize=(10, 3), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        time.sleep(0.01)

    if es_alien:
        v_alerta.markdown('<p class="alert-active">⚠️ CONTACTO DETECTADO ⚠️</p>', unsafe_allow_html=True)
        # Guardar automáticamente con la distancia del objetivo
        st.session_state.historial.append({
            "ID": len(st.session_state.historial) + 1,
            "Hora": datetime.now().strftime("%H:%M"),
            "Lugar": objetivo,
            "Distancia": data['Dist'], # Distancia automática guardada
            "K-Scale": k_scale,
            "Retraso": data['Retraso']
        })

# HISTORIAL DE CIVILIZACIÓN
if st.session_state.historial:
    st.divider()
    st.subheader("📂 ARCHIVO DE CIVILIZACIONES")
    st.table(pd.DataFrame(st.session_state.historial)[["ID", "Hora", "Lugar", "Distancia", "Retraso", "K-Scale"]])
