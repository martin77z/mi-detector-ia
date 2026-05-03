import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN NEXUS-7 ULTIMATE v8.0 ---
st.set_page_config(page_title="NEXUS-7 ULTIMATE v8.0", page_icon="📡", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# --- ESTILO VISUAL "CRT MONITOR" ---
st.markdown("""
    <style>
    .stApp { 
        background-color: #010a01; 
        color: #00FF41; 
        font-family: 'Courier New', monospace;
        background-image: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), 
                          linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 255, 0, 0.03));
        background-size: 100% 3px, 3px 100%;
    }
    .detail-card { 
        background-color: rgba(5, 21, 5, 0.8); 
        border: 1px solid #00FF41; 
        padding: 15px; 
        border-radius: 5px;
        box-shadow: 0 0 10px #00FF41;
    }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; height: 3.5em; width: 100%;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 20px #00FF41; }
    .alert-active { color: #ff0000; animation: blink 1s infinite; font-weight: bold; text-align: center; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Freq": "1420 MHz", "Nota": "Zona Habitable."},
    "Kepler-186f": {"Dist": 490, "Freq": "1665 MHz", "Nota": "Análogo a la Tierra."},
    "K2-18b": {"Dist": 124, "Freq": "1420 MHz", "Nota": "Atmósfera con vapor."},
    "Señal Wow!": {"Dist": 1800, "Freq": "1420 MHz", "Nota": "Origen desconocido 1977."}
}

# --- MOTOR DE AUDIO (HTML5) ---
def play_audio(type="noise"):
    url = "https://www.soundjay.com/misc/sounds/white-noise-01.mp3" if type=="noise" else "https://www.soundjay.com/buttons/beep-01a.mp3"
    st.components.v1.html(f"<script>var audio = new Audio('{url}'); audio.volume = 0.2; audio.play();</script>", height=0)

# --- UI PRINCIPAL ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v8.0")

col_params, col_info = st.columns([1, 2])

with col_params:
    objetivo = st.selectbox("🎯 OBJETIVO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 ESCALA DE KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
    ganancia = st.slider("📶 GANANCIA (dB)", 100, 500, 250)

with col_info:
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <b>SISTEMA:</b> {objetivo} | <b>DISTANCIA:</b> {data['Dist']} AL<br>
        <b>FRECUENCIA DE ESCUCHA:</b> {data['Freq']} (Línea de Hidrógeno)<br>
        <b>ESTADO:</b> Escaneando fluctuaciones térmicas...
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- FRAGMENTO DE ESCANEO (Optimización de rendimiento) ---
@st.fragment
def iniciar_escaneo():
    c_main, c_side = st.columns([2, 1])
    v_cascada = c_main.empty()
    v_potencia = c_main.empty()
    v_terminal = c_side.empty()
    v_msg = c_side.empty()

    if st.button("🚀 INICIAR ESCANEO DE BANDA ANCHA"):
        play_audio("noise")
        pasos = 80
        matriz = np.random.normal(0.5, 0.1, (pasos, 300))
        
        # Probabilidades basadas en Kardashov
        es_alien = random.random() > {"Tipo I": 0.8, "Tipo II": 0.5, "Tipo III": 0.1}[k_scale]
        pos_inicio = random.randint(50, 250)
        drift = random.uniform(-0.3, 0.3) # EFECTO DOPPLER (Deriva)

        for t in range(pasos):
            # Crear interferencia o señal
            if es_alien:
                centro = int(pos_inicio + (t * drift))
                if 0 <= centro < 300:
                    matriz[t, centro] += (ganancia / 50) # Señal coherente
                    # Añadir armónicos para señales Tipo II/III
                    if k_scale != "Tipo I" and centro + 20 < 300:
                        matriz[t, centro+20] += (ganancia / 100)

            # Visualización Cascada (Waterfall)
            fig1, ax1 = plt.subplots(figsize=(10, 3), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='inferno' if es_alien else 'viridis', origin='lower')
            ax1.axis('off')
            v_cascada.pyplot(fig1)
            plt.close(fig1)

            # Visualización Espectro de Potencia
            fig2, ax2 = plt.subplots(figsize=(10, 1.5), facecolor='black')
            ax2.plot(matriz[t], color='#00FF41', linewidth=0.8)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, 10)
            ax2.axis('off')
            v_potencia.pyplot(fig2)
            plt.close(fig2)

            v_terminal.code(f"SCANNING: {t}ms\nDRIFT: {drift:.4f} Hz/s\nSTATUS: {'SIGNAL FOUND' if es_alien else 'NOISE'}")
            time.sleep(0.01)

        if es_alien:
            play_audio("alien")
            v_msg.markdown('<p class="alert-active">⚠️ SEÑAL INTELIGENTE DETECTADA</p>', unsafe_allow_html=True)
            
            # Mensaje basado en matriz de 11x11 (Número primo)
            st.subheader("📟 DECODIFICACIÓN BINARIA (Matriz 11x11)")
            mensaje = np.random.choice([0, 1], size=(11, 11), p=[0.7, 0.3])
            # Dibujar un patrón simple central
            mensaje[4:7, 4:7] = 1 
            st.table(mensaje)
            
            log_entry = {"Fecha": datetime.now().strftime("%H:%M"), "Origen": objetivo, "Tipo": k_scale}
            st.session_state.historial.append(log_entry)
            st.success("Coordenadas de la señal guardadas en el historial.")
        else:
            st.error("Escaneo finalizado sin resultados positivos.")

iniciar_escaneo()

# --- HISTORIAL ---
if st.session_state.historial:
    st.divider()
    st.subheader("📂 REGISTRO DE CONTACTOS CONFIRMADOS")
    st.dataframe(pd.DataFrame(st.session_state.historial), use_container_width=True)
