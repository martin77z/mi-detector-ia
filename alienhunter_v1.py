import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- 1. GESTIÓN DE BASE DE DATOS PERMANENTE (EVIDENCIA B) ---
DB_FILE = "registro_civilizaciones.csv"

def cargar_db():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])
    return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])

# --- 2. CONFIGURACIÓN DE INTERFAZ Y ESTILO ---
st.set_page_config(page_title="NEXUS-7 OMNIBUS v9.0", layout="wide", page_icon="📡")

if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

st.markdown("""
    <style>
    .stApp { background-color: #010a01; color: #00FF41; font-family: 'Courier New', monospace; }
    .telemetria-card { 
        border: 1px solid #00FF41; padding: 15px; border-radius: 5px; 
        background-color: rgba(0, 255, 65, 0.05); height: 100%;
    }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; width: 100%; height: 3em; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 20px #00FF41; }
    .alert-msg { color: #ff0000; font-weight: bold; text-align: center; border: 1px solid #ff0000; padding: 10px; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. CATÁLOGO ESTELAR COMPLETO ---
objetivos_db = {
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "retraso": "4.2 años", "emision": "Hace 4 años", "info": "Planeta rocoso en zona habitable. El vecino más cercano."},
    "Ross 128 b": {"cat": "Ross 128", "dist": "11.0 AL", "retraso": "11.0 años", "emision": "Hace 11 años", "info": "Exoplaneta templado. Estrella enana roja muy estable."},
    "Gliese 581g": {"cat": "GJ 581", "dist": "20.0 AL", "retraso": "20.0 años", "emision": "Hace 20 años", "info": "Super-Tierra en zona habitable confirmada."},
    "TRAPPIST-1e": {"cat": "2MASS J2306", "dist": "40.0 AL", "retraso": "40.0 años", "emision": "Hace 40 años", "info": "Sistema de 7 planetas similares a la Tierra."},
    "K2-18b": {"cat": "EPIC 20191", "dist": "124.0 AL", "retraso": "124.0 años", "emision": "Siglo XIX", "info": "Mundo Hicéano con detección de metano por el JWST."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470.0 AL", "retraso": "1,470.0 años", "emision": "Año 556", "info": "Anomalía de oscurecimiento. ¿Posible Megaestructura?"},
    "Sector Wow!": {"cat": "7UC Sgr", "dist": "1,800.0 AL", "retraso": "1,800.0 años", "emision": "Año 226", "info": "Origen de la señal histórica detectada en 1977."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000.0 AL", "retraso": "25,000.0 años", "emision": "Pre-historia", "info": "Cúmulo de 300,000 estrellas. Objetivo de Arecibo."},
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000.0 AL", "retraso": "26,000.0 años", "emision": "Edad de Hielo", "info": "Corazón de la galaxia. Agujero negro supermasivo."},
    "Andrómeda": {"cat": "M31", "dist": "2.5M AL", "retraso": "2.5M años", "emision": "Plioceno", "info": "Búsqueda de civilizaciones Tipo III extragalácticas."}
}

st.title("📡 NEXUS-7 OMNIBUS: FIRST CONTACT v9.0")

# --- 4. PANEL DE CONTROL SUPERIOR ---
with st.expander("📖 MANUAL DE OPERACIONES SETI"):
    st.write("🟢 Línea vertical = Inteligencia | 🔵 Manchas = Ruido | 📐 Inclinación = Doppler")

c1, c2, c3 = st.columns([1.5, 1.5, 3])
with c1:
    st.subheader("🧭 NAVEGACIÓN")
    obj_sel = st.selectbox("OBJETIVO", list(objetivos_db.keys()))
    k_scale = st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c2:
    st.subheader("📶 ANTENA")
    gain = st.slider("GANANCIA (dB)", 100, 500, 250)
    audio = st.checkbox("🔊 AUDIO-LOG", value=True)
    btn_scan = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with c3:
    target = objetivos_db[obj_sel]
    st.markdown(f"""
    <div class="telemetria-card">
        <h4 style='margin-top:0;'>📊 TELEMETRÍA AUTOMÁTICA</h4>
        <b>SISTEMA:</b> {obj_sel.upper()} | <b>CATÁLOGO:</b> {target['cat']}<br>
        <b>DISTANCIA:</b> {target['dist']} | <b>RETRASO LUZ:</b> {target['retraso']}<br>
        <b>ORIGEN ESTIMADO:</b> {target['emision']}<br>
        <hr style='border:0.5px solid #00FF41'>
        <i>{target['info']}</i>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- 5. ÁREA DE TRABAJO (RADAR + ANÁLISIS IA) ---
col_radar, col_ia = st.columns([2, 1])

with col_radar:
    st.write("🛰️ **VISUALIZACIÓN DE ESPECTRO**")
    v_waterfall = st.empty()
    v_spectrum = st.empty()

with col_ia:
    st.subheader("📟 DECODER & ANÁLISIS IA")
    v_status = st.empty()
    v_log = st.empty()
    v_data = st.empty()

# --- 6. LÓGICA DE ESCANEO ---
if btn_scan:
    steps = 60
    data_stream = np.zeros((40, 100))
    chance = {"Tipo I": 0.8, "Tipo II": 0.5, "Tipo III": 0.25}
    is_alien = random.random() > chance[k_scale]
    
    if audio: st.components.v1.html("<script>new Audio('https://www.soundjay.com/misc/sounds/white-noise-01.mp3').play();</script>", height=0)

    for i in range(steps):
        new_row = np.random.normal(0.5, 0.2, 100)
        if is_alien: new_row[50] += (gain / 7.5)
        
        data_stream = np.roll(data_stream, -1, axis=0)
        data_stream[-1] = new_row
        
        # Radar Waterfall
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(data_stream, aspect='auto', cmap='magma' if is_alien else 'viridis')
        ax1.axis('off')
        v_waterfall.pyplot(fig1)
        plt.close(fig1)
        
        # Spectrum
        fig2, ax2 = plt.subplots(figsize=(10, 1.5), facecolor='black')
        ax2.plot(new_row, color='#00FF41' if not is_alien else '#ff0000', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 150)
        ax2.axis('off')
        v_spectrum.pyplot(fig2)
        plt.close(fig2)
        
        # ANÁLISIS IA EN TIEMPO REAL
        v_log.code(f"""
        [STATUS]: ANALYZING...
        [SAMPLE]: {i}/{steps}
        [SNR]: {np.max(new_row):.2f} dB
        [COHERENCE]: {'STABLE' if is_alien and i > 15 else 'NULL'}
        [BITRATE]: 1.44 Pbps
        """)
        time.sleep(0.04)

    if is_alien:
        if audio: st.components.v1.html("<script>new Audio('https://www.soundjay.com/buttons/beep-01a.mp3').play();</script>", height=0)
        v_status.markdown('<div class="alert-msg">⚠️ CONTACTO INTELIGENTE CONFIRMADO ⚠️</div>', unsafe_allow_html=True)
        
        # Persistencia en Archivo B
        new_entry = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Lugar": obj_sel, "K-Scale": k_scale, "Result": "ÉXITO"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_entry], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
        
        # Matriz de datos
        v_data.write("🔢 MATRIZ DE DATOS DECODIFICADA:")
        v_data.table(np.random.choice([0, 1], size=(6, 10)))
    else:
        v_status.error("SCAN COMPLETO: RUIDO ESPACIAL DETECTADO.")

# --- 7. ARCHIVO DE CIVILIZACIONES (REGISTRO PERMANENTE) ---
st.write("---")
st.subheader("📂 ARCHIVO DE CIVILIZACIONES (HISTORIAL)")

if len(st.session_state.historial_df) > 0:
    st.dataframe(st.session_state.historial_df, use_container_width=True)
    if st.button("🗑️ RESETEAR ARCHIVO CSV"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.historial_df = pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])
        st.rerun()
else:
    st.info("No hay registros previos en la base de datos local.")
