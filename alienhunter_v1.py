import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="NEXUS-7 ROSS 128b ANALYZER", page_icon="📡", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .ai-terminal { 
        background-color: rgba(0, 10, 0, 0.95); border: 1px solid #00FF41; 
        padding: 15px; font-size: 0.8rem; height: 200px; overflow-y: auto;
    }
    .decoding-box { border: 2px dashed #ff0000; padding: 15px; background: rgba(255,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ INICIALIZANDO LECTOR DE DATOS REALES...", "◈ BUSCANDO ARCHIVOS DE ROSS 128 b..."]

def push_log(msg):
    st.session_state.ai_log.insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")

st.title("📡 NEXUS-7: DATA ANALYZER - ROSS 128 b")

# --- CARGA DE DATOS ---
def load_custom_data():
    try:
        # Reemplaza con los nombres exactos de tus archivos
        # Si están en una carpeta, usa "carpeta/archivo.txt"
        potencia = np.loadtxt("potencia.txt") 
        return potencia
    except Exception as e:
        st.error(f"Error: No se encontraron los archivos. Asegúrate de que 'potencia.txt' esté en la carpeta.")
        return None

# --- NÚCLEO DE PROCESAMIENTO ---
@st.fragment
def run_real_analysis():
    col_viz, col_ai = st.columns([2, 1])
    
    with col_viz:
        v_wat = st.empty()
        v_pow = st.empty()
    
    with col_ai:
        st.subheader("🧠 IA TELEMETRY")
        v_status = st.empty()
        v_log = st.empty()

    if st.button("🚀 INICIAR LECTURA DE SEÑAL REAL"):
        data = load_custom_data()
        
        if data is not None:
            push_log("Archivo cargado exitosamente.")
            
            # Simulamos el barrido temporal usando tus datos
            # Creamos una matriz para el Waterfall basada en tus datos
            steps = len(data)
            # Expandimos los datos horizontalmente para que se vea como una señal de radio
            matriz_visual = np.zeros((steps, 100))
            
            for t in range(steps):
                # Insertamos tu valor de medición en el centro del espectro visual
                linea = np.random.normal(0.1, 0.05, 100)
                linea[50] = data[t] # El valor real de tu txt en el centro
                
                matriz_visual[t] = linea
                
                # Gráfico Cascada (Waterfall)
                fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
                ax1.imshow(matriz_visual[:t+1], aspect='auto', cmap='magma', origin='lower')
                ax1.axis('off')
                v_wat.pyplot(fig1, clear_figure=True)
                plt.close(fig1)
                
                # Gráfico de Potencia Actual
                fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
                ax2.plot(linea, color='#00FF41' if data[t] < 5 else '#ff0000', linewidth=1)
                ax2.set_ylim(0, 10)
                ax2.set_facecolor('black')
                ax2.axis('off')
                v_pow.pyplot(fig2, clear_figure=True)
                plt.close(fig2)
                
                # Lógica de detección IA
                if data[t] > 5.0:
                    v_status.error(f"⚠️ ¡ANOMALÍA DETECTADA! Intensidad: {data[t]} dB")
                    push_log(f"CRITICAL: Pico de energía detectado en frame {t}")
                else:
                    v_status.success("Buscando patrones...")

                v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
                time.sleep(0.1)

run_real_analysis()

st.info("Nota: Este módulo está configurado para leer 'potencia.txt'. Asegúrate de que el archivo contenga una lista de números (uno por línea).")
