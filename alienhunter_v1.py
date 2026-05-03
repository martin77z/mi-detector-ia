import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime
import base64

# CONFIGURACIÓN NEXUS-7 ULTIMATE
st.set_page_config(page_title="NEXUS-7 ULTIMATE v7.0", page_icon="👽", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# --- MOTOR DE AUDIO (Simulación) ---
def play_tone(freq_type="noise"):
    # Generamos un sonido sintético simple mediante HTML5
    if freq_type == "alien":
        tone_script = "new Audio('https://www.soundjay.com/buttons/beep-01a.mp3').play();"
    else:
        tone_script = "new Audio('https://www.soundjay.com/misc/sounds/white-noise-01.mp3').play();"
    st.components.v1.html(f"<script>{tone_script}</script>", height=0)

# --- ESTILO VISUAL DINÁMICO ---
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
    .decoding-box { background-color: #000; border: 2px dashed #00FF41; padding: 15px; font-family: monospace; color: #00FF41; }
    [data-testid="stSidebar"] {display: none;}
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .alert-active { color: #ff0000; animation: blink 1s infinite; font-weight: bold; font-size: 1.5em; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Tipo": "Rocoso", "Nota": "Candidato cercano."},
    "Ross 128 b": {"Dist": 11.0, "Tipo": "Templado", "Nota": "Estrella estable."},
    "K2-18b": {"Dist": 124.0, "Tipo": "Hicéano", "Nota": "Vapor de agua detectado."},
    "Sector Wow!": {"Dist": 1800.0, "Tipo": "Histórico", "Nota": "Señal de 1977."},
    "Andrómeda": {"Dist": 2.5e6, "Tipo": "Galaxia", "Nota": "Búsqueda Extragaláctica."}
}

st.title("📡 NEXUS-7: ULTIMATE CONTACT v7.0")

# --- PANEL DE CONTROL SUPERIOR (Kardashov & Target) ---
c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    objetivo = st.selectbox("🎯 DESTINO GALÁCTICO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 ESCALA DE KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
with c2:
    ganancia = st.slider("📶 GANANCIA SENSORIAL (dB)", 150, 400, 250)
    audio_on = st.checkbox("🔊 ACTIVAR AUDIO-LOG", value=True)
with c3:
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <b>SISTEMA:</b> {objetivo} | <b>CIVILIZACIÓN BUSCADA:</b> {k_scale}<br>
        <b>DISTANCIA:</b> {data['Dist']} AL | <b>ESTADO:</b> LISTO PARA ESCANEO<br>
        <b>LOG:</b> {data['Nota']}
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col_main, col_decoder = st.columns([2, 1])

with col_main:
    v_cascada = st.empty()
    v_potencia = st.empty()

with col_decoder:
    st.subheader("📟 MÓDULO DE DECODIFICACIÓN")
    v_alerta = st.empty()
    v_terminal = st.empty()
    v_binary = st.empty()
    v_matrix = st.empty()

# LÓGICA DE ESCANEO
if st.button("🚀 INICIAR ESCANEO PROFUNDO"):
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    
    # Ajuste de probabilidad según Kardashov (Tipo III es casi seguro encontrar algo)
    prob_map = {"Tipo I": 0.7, "Tipo II": 0.5, "Tipo III": 0.3}
    es_alien = random.random() > prob_map[k_scale]
    
    if audio_on: play_tone("noise")

    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.05)
        
        if 0 <= centro < 400:
            if es_alien:
                # SEÑAL INTELIGENTE
                pico = (ganancia / 4)
                ruido[centro] += pico
                if t == 50 and audio_on: play_tone("alien")
            else:
                # RUIDO
                ruido[centro-10:centro+11] += (ganancia / 15)
            
        matriz[t] = ruido
        
        # Gráficos
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41' if not es_alien else '#ff0000', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 100)
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        
        v_terminal.code(f"BANDA: {k_scale}\nPROCESANDO TRAMA: {t}ms\nCALIDAD: {np.max(ruido)/10:.1f}%")
        time.sleep(0.01)

    # RESULTADO Y DECODIFICACIÓN
    if es_alien:
        v_alerta.markdown('<p class="alert-active">⚠️ CONTACTO INTELIGENTE CONFIRMADO ⚠️</p>', unsafe_allow_html=True)
        
        # Simulación de decodificación de imagen (Patrón de Arecibo)
        v_binary.markdown("**DECODIFICANDO PATRÓN BINARIO...**")
        progress = st.progress(0)
        for p in range(100):
            time.sleep(0.02)
            progress.progress(p + 1)
        
        # Generar "Mensaje" de píxeles
        msg = np.random.choice([0, 1], size=(10, 10))
        st.session_state['msg'] = msg
        v_matrix.table(msg)
        
        st.success(f"MENSAJE RECIBIDO DESDE {objetivo}")
        if st.button("💾 REGISTRAR EN ARCHIVO"):
            st.session_state.historial.append({"Fecha": datetime.now().strftime("%H:%M"), "Origen": objetivo, "K-Scale": k_scale})
    else:
        v_alerta.error("SCAN COMPLETO: Solo ruido de fondo detectado.")

# HISTORIAL
if st.session_state.historial:
    st.divider()
    st.subheader("📂 LOG DE CIVILIZACIONES DETECTADAS")
    st.write(pd.DataFrame(st.session_state.historial))
