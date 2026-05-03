import streamlit as st
import numpy as np
import time
import random
import pandas as pd
from datetime import datetime
from PIL import Image

# CONFIGURACIÓN MAESTRA
st.set_page_config(page_title="NEXUS-7 OMNIBUS v8.0", page_icon="📡", layout="wide")

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

# LÓGICA DE DECODIFICACIÓN (PATRONES REALES)
def obtener_mensaje_alien():
    patrones = [
        np.array([[0,0,1,1,1,1,0,0],[0,1,0,0,0,0,1,0],[1,0,1,0,0,1,0,1],[1,0,0,0,0,0,0,1],[1,0,1,1,1,1,0,1],[1,0,0,0,0,0,0,1],[0,1,0,1,1,0,1,0],[0,0,1,1,1,1,0,0]]), # Rostro
        np.array([[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,1,0,0,1,1,0,0],[0,0,1,1,0,0,1,1],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,1,0,0,1,1,0,0],[0,0,1,1,0,0,1,1]]), # ADN
        np.array([[0,0,0,1,1,0,0,0],[0,0,1,1,1,1,0,0],[0,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,1],[0,0,1,1,1,1,0,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,1,0,0]])  # Cohete/Señal
    ]
    return random.choice(patrones)

# BASE DE DATOS
info_objetivos = {
    "Próxima b": {"Dist": "4.2 AL", "Tipo": "Rocoso / Habitable", "Retraso": "4.2 años", "Nota": "Señal Tipo I detectada anteriormente."},
    "Ross 128 b": {"Dist": "11.0 AL", "Tipo": "Exoplaneta Templado", "Retraso": "11.0 años", "Nota": "Estrella enana roja estable."},
    "Sector Wow!": {"Dist": "1,800 AL", "Tipo": "Histórico SETI", "Retraso": "1,800 años", "Nota": "Frecuencia de Hidrógeno 1420 MHz."},
    "Andrómeda (M31)": {"Dist": "2.5M AL", "Tipo": "Galaxia Vecina", "Retraso": "2.5M años", "Nota": "Candidato Tipo III."}
}

st.title("📡 NEXUS-7 OMNIBUS v8.0")

# --- PANEL DE CONTROL ---
c_ctrl, c_gain, c_tele = st.columns([1.5, 1.5, 3])

with c_ctrl:
    st.subheader("🎯 NAVEGACIÓN")
    objetivo = st.selectbox("OBJETIVO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 NIVEL KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c_gain:
    st.subheader("📶 ANTENA")
    ganancia = st.slider("GANANCIA (dB)", 100, 500, 200)
    umbral = st.slider("FILTRO SQUELCH (Umbral)", 0, 100, 20)
    trigger = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with c_tele:
    data = info_objetivos[objetivo]
    st.markdown(f"""<div class="detail-card">
        <h3 style='margin:0; color:#00FF41;'>📊 TELEMETRÍA DE SECTOR</h3>
        <p><b>SISTEMA:</b> {objetivo.upper()} | <b>DISTANCIA:</b> {data['Dist']}</p>
        <p><i>{data['Nota']}</i></p>
    </div>""", unsafe_allow_html=True)

st.write("---")

col_radar, col_decoder = st.columns([2, 1])

with col_radar:
    st.write("🛰️ **REAL-TIME SPECTROGRAM**")
    v_cascada = st.empty()
    v_potencia = st.empty()

with col_decoder:
    st.subheader("📟 DECODER IA")
    v_alerta = st.empty()
    v_terminal = st.empty()
    v_matrix = st.empty()

if trigger:
    pasos = 120
    ancho = 400
    matriz_visual = np.zeros((pasos, ancho, 3), dtype=np.uint8)
    
    prob_map = {"Tipo I": 0.7, "Tipo II": 0.4, "Tipo III": 0.1}
    es_alien = random.random() > prob_map[k_scale]
    pos_x = random.randint(100, 300)

    # Audio inicial
    st.components.v1.html("<script>new Audio('https://www.soundjay.com/misc/sounds/white-noise-01.mp3').play();</script>", height=0)

    for t in range(pasos):
        # Generar ruido base
        fila_ruido = np.random.normal(50, 20, ancho).clip(0, 255)
        
        # Aplicar Filtro Squelch (Punto 3)
        fila_ruido[fila_ruido < umbral] = 0
        
        # Inyectar Señal
        centro = int(pos_x + t * 0.1) # Doppler drift
        if 0 <= centro < ancho:
            if es_alien:
                # Señal coherente (Roja/Naranja)
                intensidad = min(255, ganancia // 1.5)
                fila_ruido[centro] = intensidad
                color_fila = [intensidad, intensidad // 2, 0] 
            else:
                # RFI Humano (Azul/Verde)
                fila_ruido[centro-5:centro+5] += 30
                color_fila = [0, 100, 255]
        
        # Actualizar Matriz Visual (Punto 1 - Optimización st.image)
        for i in range(ancho):
            val = int(fila_ruido[i])
            if es_alien and i == centro:
                matriz_visual[t, i] = [255, 50, 0]
            else:
                matriz_visual[t, i] = [0, val, val//4]

        # Renderizado ultra-rápido
        v_cascada.image(matriz_visual, use_container_width=True)
        
        # Mini Terminal
        v_terminal.code(f"FRAME: {t} | COHERENCIA: {random.randint(10, 99) if es_alien else 0}%")
        time.sleep(0.01)

    # FINAL DE ESCANEO (Punto 2 - Decodificación Real)
    if es_alien:
        st.components.v1.html("<script>new Audio('https://www.soundjay.com/buttons/beep-01a.mp3').play();</script>", height=0)
        v_alerta.markdown('<p class="alert-active">⚠️ CONTACTO INTELIGENTE CONFIRMADO ⚠️</p>', unsafe_allow_html=True)
        
        # Mostrar mensaje estructurado
        mensaje = obtener_mensaje_alien()
        v_matrix.write("🔢 ESTRUCTURA DE DATOS RECUPERADA:")
        v_matrix.table(mensaje)
        
        st.session_state.historial.append({"Hora": datetime.now().strftime("%H:%M"), "Lugar": objetivo, "Result": "CONTACTO"})
    else:
        v_alerta.error("SCAN COMPLETO: Solo ruido cósmico detectado.")

# HISTORIAL
if st.session_state.historial:
    st.divider()
    st.subheader("📂 ARCHIVO DE CIVILIZACIONES")
    st.dataframe(pd.DataFrame(st.session_state.historial), use_container_width=True)
