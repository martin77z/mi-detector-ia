import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN TÁCTICA
st.set_page_config(page_title="NEXUS-7 HUNTER", page_icon="🛸", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO VISUAL "RADAR MILITAR"
st.markdown("""
    <style>
    .stApp { background-color: #040804; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; border-radius: 0px; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 40px #00FF41; }
    .sidebar .sidebar-content { background-image: linear-gradient(#040804, #000); }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# DATOS DE OBJETIVOS
info_objetivos = {
    "Próxima b": {"Distancia": "4.24 AL", "Estrella": "Enana Roja", "Riesgo_RFI": 0.2},
    "Kepler-186f": {"Distancia": "582 AL", "Estrella": "Enana K", "Riesgo_RFI": 0.1},
    "TRAPPIST-1e": {"Distancia": "40.7 AL", "Estrella": "Enana ultrafría", "Riesgo_RFI": 0.4},
    "Estrella de Tabby": {"Distancia": "1,470 AL", "Estrella": "Tipo F", "Riesgo_RFI": 0.05},
    "Sagitario A*": {"Distancia": "26,670 AL", "Estrella": "Agujero Negro", "Riesgo_RFI": 0.6}
}

st.title("📡 NEXUS-7: SIGNAL HUNTER v4.5")
st.write("---")

# --- SIDEBAR ---
st.sidebar.title("🎛️ RECEPCIÓN")
target = st.sidebar.selectbox("Objetivo", list(info_objetivos.keys()))
modo_escaneo = st.sidebar.radio("Modo de Análisis", ["Rápido (Tactical)", "Profundo (Deep Scan)"])
potencia = st.sidebar.slider("Ganancia LNA (dB)", 10, 120, 95)

# --- UI PRINCIPAL ---
c_radar, c_info = st.columns([2, 1])

with c_radar:
    v_waterfall = st.empty()
    v_power = st.empty()

with c_info:
    st.subheader("📟 STATUS LOG")
    v_consola = st.empty()
    v_ai_box = st.empty()

if st.button("🛰️ CAPTURAR ESPECTRO"):
    # Configurar según modo
    pasos = 150 if modo_escaneo == "Profundo (Deep Scan)" else 60
    columnas = 400
    datos = np.zeros((pasos, columnas))
    
    # Decidir si hay Interferencia (RFI)
    es_rfi = random.random() < info_objetivos[target]['Riesgo_RFI']
    
    pos_x = random.randint(100, 300)
    deriva = random.uniform(-0.3, 0.3)

    for t in range(pasos):
        linea = np.random.normal(0.6, 0.2, columnas)
        
        # Inyectar Señal
        centro = int(pos_x + t * deriva)
        if 0 <= centro < columnas:
            if es_rfi:
                # Señal RFI: más gorda y errática
                linea[centro-5:centro+6] += (potencia / 8) + random.random()*2
            else:
                # Señal Inteligente: fina y definida
                linea[centro-1:centro+2] += (potencia / 10)
        
        datos[t] = linea
        
        # Plot Cascada
        fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
        ax1.imshow(datos, aspect='auto', cmap='viridis' if es_rfi else 'magma', origin='lower')
        ax1.axis('off')
        v_waterfall.pyplot(fig1)
        plt.close(fig1)
        
        # Plot Potencia
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(linea, color='#00FF41', alpha=0.7)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 18)
        ax2.axis('off')
        v_power.pyplot(fig2)
        plt.close(fig2)
        
        v_consola.code(f"READ_BLK_{t}..OK\nSNR: {np.max(linea):.1f}dB\nTARGET: {target}\nTYPE: {'UNCERTAIN' if es_rfi else 'STABLE'}")
        time.sleep(0.02)

    # --- VEREDICTO ---
    score = random.randint(90, 99) if not es_rfi else random.randint(30, 60)
    
    with v_ai_box:
        if es_rfi:
            st.error("❌ CLASIFICACIÓN: INTERFERENCIA TERRESTRE (RFI)")
            st.write("La señal carece de coherencia orbital. Probable rebote en satélite LEO.")
        else:
            st.success(f"✅ TECNOFIRMA DETECTADA ({score}%)")
            st.write(f"Patrón detectado en {target}. Origen extra-solar confirmado.")
            if st.button("💾 GUARDAR HALLAZGO"):
                st.session_state.historial.append({"Fecha": datetime.now().strftime("%H:%M"), "Sector": target, "Status": "ÉXITO"})
                st.toast("Guardado en archivo")

# HISTORIAL
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 ARCHIVO DE SEÑALES CONFIRMADAS")
    st.table(st.session_state.historial)
