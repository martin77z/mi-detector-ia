import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURACIÓN NEXUS-7 v10.0 REAL-DATA ---
st.set_page_config(page_title="NEXUS-7 REAL DATA", page_icon="📡", layout="wide")

# --- BASE DE DATOS CIENTÍFICA ---
INFO_SISTEMAS = {
    "Ross 128 b": {"dist": "11.03 AL", "estrella": "Enana Roja Inactiva", "hab": "Confirmada"},
    "Andrómeda M31": {"dist": "2.5M AL", "estrella": "Núcleo Galáctico", "hab": "Tipo III"},
    "Procesamiento Manual": {"dist": "---", "estrella": "Antena Local", "hab": "Datos Crudos"}
}

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .ai-terminal { 
        background-color: rgba(0, 10, 0, 0.95); border: 1px solid #00FF41; 
        padding: 15px; font-size: 0.8rem; height: 200px; overflow-y: auto;
    }
    .alert-active { color: #ff0000; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ SISTEMA DE RECEPCIÓN REAL ONLINE", "◈ ESPERANDO FLUJO DE DATOS DE ANTENA..."]

def push_log(msg):
    st.session_state.ai_log.insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")

# --- TÍTULO ---
st.title("📡 NEXUS-7: ANALIZADOR DE CAMPO REAL")

# --- CONTROL DE ENTRADA ---
col_ctrl, col_stats = st.columns([2, 1])

with col_ctrl:
    target = st.selectbox("🎯 SELECCIONAR ORIGEN DE SEÑAL", list(INFO_SISTEMAS.keys()))
    gain = st.slider("📶 SENSIBILIDAD DEL FILTRO (Threshold)", 1.0, 10.0, 4.5)

with col_stats:
    d = INFO_SISTEMAS[target]
    st.markdown(f"**SISTEMA:** {target}  \n**DISTANCIA:** {d['dist']}  \n**STATUS:** BUSCANDO ARCHIVO 'datos_antena.csv'")

st.divider()

# --- NÚCLEO DE PROCESAMIENTO REAL ---
@st.fragment
def start_real_scan():
    col_viz, col_ai = st.columns([2, 1])
    v_wat = col_viz.empty()
    v_pow = col_viz.empty()
    v_conf = col_ai.empty()
    v_desc = col_ai.empty()
    v_log = col_ai.empty()

    if st.button("🛰️ INICIAR ESCANEO DE ANTENA"):
        # 1. Verificación de Hardware
        if not os.path.exists("datos_antena.csv"):
            st.error("ERROR: No se detecta 'datos_antena.csv'. Conecta la antena o carga el archivo.")
            return

        # 2. Carga de Datos
        try:
            raw_data = np.genfromtxt("datos_antena.csv", delimiter=',')
            if raw_data.ndim > 1: raw_data = raw_data.flatten()
        except:
            st.error("Archivo corrupto o formato no válido.")
            return

        push_log("Archivo detectado. Iniciando procesamiento de espectro...")
        
        # Preparamos la matriz visual (cascada)
        steps = 60
        longitud = 400
        matriz = np.zeros((steps, longitud))
        
        # Troceamos los datos reales para la animación
        chunk_size = len(raw_data) // steps
        
        for t in range(steps):
            # Extraemos una porción real de los datos de la antena
            linea_real = raw_data[t*chunk_size : (t+1)*chunk_size]
            # Ajustamos al ancho de la gráfica
            linea_plot = np.interp(np.linspace(0, len(linea_real), longitud), np.arange(len(linea_real)), linea_real)
            
            matriz[t] = linea_plot
            
            # --- LÓGICA DE DETECCIÓN IA ---
            max_val = np.max(linea_plot)
            is_anomaly = max_val > gain
            
            # Gráfica Waterfall
            fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='viridis', origin='lower')
            if is_anomaly:
                pos = np.argmax(linea_plot)
                ax1.axvspan(pos-5, pos+5, color='#00FF41', alpha=0.3)
                ax1.text(pos+10, t, "ANOMALÍA", color='#00FF41', fontweight='bold')
            ax1.axis('off')
            v_wat.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # Gráfica de Potencia
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
            color = '#ff3300' if is_anomaly else '#00FF41'
            ax2.plot(linea_plot, color=color, linewidth=1)
            ax2.set_ylim(0, np.max(raw_data) * 1.2)
            ax2.axis('off')
            v_pow.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # Actualización de UI
            conf = min(100.0, (max_val / gain) * 50) if is_anomaly else 0.5
            v_conf.progress(conf/100, text=f"CONFIANZA IA: {conf:.1f}%")
            
            if is_anomaly:
                v_desc.markdown('<p class="alert-active">¡ALERTA! SEÑAL NO IDENTIFICADA DETECTADA</p>', unsafe_allow_html=True)
            else:
                v_desc.write("IA: Analizando ruido estelar...")

            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            time.sleep(0.05)

        push_log("Escaneo finalizado. Datos almacenados.")

start_real_scan()
st.caption("NEXUS-7 v10.0 | Modo: Radioastronomía Real | 2026")
