import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN MAESTRA
st.set_page_config(page_title="NEXUS-7 OMNIBUS v7.6", page_icon="📡", layout="wide")

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
    .archive-card { background-color: #001a00; border: 1px dashed #00FF41; padding: 15px; margin-top: 10px; }
    .alert-active { color: #ff0000; animation: blink 1s infinite; font-weight: bold; font-size: 1.4em; text-align: center; border: 2px solid #ff0000; padding: 10px; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# BASE DE DATOS MAESTRA
info_objetivos = {
    "Próxima b": {"Dist": "4.2 AL", "Tipo": "Rocoso / Habitable", "Retraso": "4.2 años", "Nota": "Vecino más cercano. Posible civilización Tipo I."},
    "Ross 128 b": {"Dist": "11.0 AL", "Tipo": "Exoplaneta Templado", "Retraso": "11.0 años", "Nota": "Estrella estable. Señal limpia."},
    "TRAPPIST-1e": {"Dist": "40.0 AL", "Tipo": "Sistema Multi-planetario", "Retraso": "40.0 años", "Nota": "7 planetas similares a la Tierra."},
    "K2-18b": {"Dist": "124.0 AL", "Tipo": "Mundo Hicéano", "Retraso": "124.0 años", "Nota": "JWST detectó metano y vapor de agua."},
    "Estrella de Tabby": {"Dist": "1,470 AL", "Tipo": "Anomalía KIC 8462852", "Retraso": "1,470 años", "Nota": "Oscurecimientos masivos. ¿Megaestructura?"},
    "Sector Wow!": {"Dist": "1,800 AL", "Tipo": "Histórico SETI", "Retraso": "1,800 años", "Nota": "Origen de la señal captada en 1977."},
    "Andrómeda (M31)": {"Dist": "2.5M AL", "Tipo": "Galaxia Vecina", "Retraso": "2.5M años", "Nota": "Búsqueda Tipo III extragaláctica."}
}

st.title("📡 NEXUS-7 OMNIBUS: FIRST CONTACT v7.6")

# --- PANEL DE CONTROL ---
c_ctrl, c_gain, c_tele = st.columns([1.5, 1.5, 3])

with c_ctrl:
    st.subheader("🎯 NAVEGACIÓN")
    objetivo = st.selectbox("OBJETIVO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 NIVEL KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c_gain:
    st.subheader("📶 ANTENA")
    ganancia = st.slider("GANANCIA (dB)", 100, 500, 250)
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

if trigger:
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    prob_map = {"Tipo I": 0.8, "Tipo II": 0.5, "Tipo III": 0.2}
    es_alien = random.random() > prob_map[k_scale]
    
    if audio: st.components.v1.html("<script>new Audio('https://www.soundjay.com/misc/sounds/white-noise-01.mp3').play();</script>", height=0)

    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.06)
        if 0 <= centro < 400:
            if es_alien:
                ruido[centro] += (ganancia / 4.5)
            else:
                ruido[centro-8:centro+9] += (ganancia / 15)
        matriz[t] = ruido
        
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41' if not es_alien else '#ff0000', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 150)
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        
        v_terminal.code(f"SCANNING: {objetivo}\nCOHERENCIA: {'DETECTADA' if es_alien and t > 50 else 'BUSCANDO...'}")
        time.sleep(0.01)

    if es_alien:
        v_alerta.markdown('<p class="alert-active">⚠️ CONTACTO INTELIGENTE ⚠️</p>', unsafe_allow_html=True)
        msg_data = np.random.choice([0, 1], size=(8, 8))
        v_matrix.table(msg_data)
        
        # GUARDAR EN HISTORIAL CON DETALLES DE CÁLCULO
        st.session_state.historial.append({
            "ID": len(st.session_state.historial) + 1,
            "Hora": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Lugar": objetivo,
            "Distancia": data['Dist'],
            "Tipo": data['Tipo'],
            "K-Scale": k_scale,
            "Retraso": data['Retraso'],
            "Mensaje": msg_data.tolist()
        })
    else:
        v_alerta.error("SCAN COMPLETO: Ruido de fondo.")

# --- ARCHIVO DE CIVILIZACIONES INTERACTIVO ---
if st.session_state.historial:
    st.divider()
    st.subheader("📂 ARCHIVO DE CIVILIZACIONES")
    
    # Crear una lista de IDs para el selector
    log_ids = [f"Hallazgo #{h['ID']} - {h['Lugar']} ({h['Hora']})" for h in st.session_state.historial]
    seleccion = st.selectbox("🔍 SELECCIONAR HALLAZGO PARA ANÁLISIS DETALLADO:", log_ids)
    
    # Obtener el hallazgo seleccionado
    idx = int(seleccion.split('#')[1].split(' ')[0]) - 1
    h = st.session_state.historial[idx]
    
    # Mostrar la información del hallazgo "con un click"
    c_arch1, c_arch2 = st.columns([2, 1])
    with c_arch1:
        st.markdown(f"""
        <div class="archive-card">
            <h4>📄 REPORTE DE ANÁLISIS: {h['Lugar']}</h4>
            <p><b>FECHA DE REGISTRO:</b> {h['Hora']}</p>
            <p><b>ESTADO DE CIVILIZACIÓN:</b> Kardashov {h['K-Scale']}</p>
            <p><b>DISTANCIA AL ORIGEN:</b> {h['Distancia']}</p>
            <p><b>RETRASO DE SEÑAL LUZ:</b> {h['Retraso']}</p>
            <p><b>TIPO DE CUERPO:</b> {h['Tipo']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c_arch2:
        st.write("🛰️ **MATRIZ DE DATOS ARCHIVADA:**")
        st.table(np.array(h['Mensaje']))
    
