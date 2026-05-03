import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- 1. GESTIÓN DE BASE DE DATOS PERMANENTE ---
DB_FILE = "registro_civilizaciones.csv"

def cargar_db():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])
    return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])

# --- 2. CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="NEXUS-7 FINAL BUILD", layout="wide", page_icon="📡")

if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# CSS Personalizado (Fiel a la estética de tus fotos)
st.markdown("""
    <style>
    .stApp { background-color: #010a01; color: #00FF41; font-family: 'Courier New', monospace; }
    .telemetria-card { 
        border: 1px solid #00FF41; padding: 15px; border-radius: 5px; 
        background-color: rgba(0, 255, 65, 0.05);
    }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 20px #00FF41; }
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATOS DE NAVEGACIÓN ---
objetivos_db = {
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470.0 AL", "retraso": "1,470.0 años", "emision": "Año 556", "info": "Anomalía de oscurecimiento masivo."},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "retraso": "4.2 años", "emision": "Hace 4 años", "info": "Planeta rocoso en zona habitable."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000.0 AL", "retraso": "25,000.0 años", "emision": "Pre-historia", "info": "Objetivo del Mensaje de Arecibo."},
    "Andrómeda": {"cat": "M31", "dist": "2.5M AL", "retraso": "2.5M años", "emision": "Plioceno", "info": "Civilizaciones extragalácticas potenciales."}
}

st.title("📡 NEXUS-7 OMNIBUS: FIRST CONTACT v8.9")

# --- 4. PANELES DE CONTROL ---
c1, c2, c3 = st.columns([1.5, 1.5, 3])

with c1:
    st.subheader("🧭 NAVEGACIÓN")
    obj_sel = st.selectbox("OBJETIVO", list(objetivos_db.keys()))
    k_scale = st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c2:
    st.subheader("📶 ANTENA")
    gain = st.slider("GANANCIA (dB)", 100, 500, 250)
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

# --- 5. VISUALIZACIÓN Y ANÁLISIS IA ---
col_radar, col_ia = st.columns([2, 1])

with col_radar:
    st.write("🛰️ **VISUALIZACIÓN DE ESPECTRO**")
    v_waterfall = st.empty()
    v_spectrum = st.empty()

with col_ia:
    st.subheader("📟 DECODER IA")
    v_status = st.empty()
    v_log = st.empty()
    v_data = st.empty()

# --- 6. LÓGICA DE EJECUCIÓN ---
if btn_scan:
    steps = 60
    rows = 40
    data_stream = np.zeros((rows, 100))
    # Probabilidad de éxito según Kardashov
    chance = {"Tipo I": 0.8, "Tipo II": 0.5, "Tipo III": 0.3}
    is_alien = random.random() > chance[k_scale]
    
    for i in range(steps):
        # Generar ruido y señal
        new_row = np.random.normal(0.5, 0.2, 100)
        if is_alien:
            new_row[50] += (gain / 8) # Pico de señal artificial
        
        data_stream = np.roll(data_stream, -1, axis=0)
        data_stream[-1] = new_row
        
        # Waterfall Plot
        fig, ax = plt.subplots(figsize=(10, 4), facecolor='black')
        ax.imshow(data_stream, aspect='auto', cmap='magma' if is_alien else 'viridis')
        ax.axis('off')
        v_waterfall.pyplot(fig)
        plt.close(fig)
        
        # Spectrum Plot
        fig2, ax2 = plt.subplots(figsize=(10, 1.5), facecolor='black')
        ax2.plot(new_row, color='#00FF41' if not is_alien else '#ff0000')
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 100)
        ax2.axis('off')
        v_spectrum.pyplot(fig2)
        plt.close(fig2)
        
        # ANÁLISIS IA (Restaurado)
        v_log.code(f"""
        [ANALYSIS_MODE]: ACTIVE
        [SAMPLE]: {i}/{steps}
        [SNR_RATIO]: {np.max(new_row):.2f}
        [COHERENCE]: {'HIGH' if is_alien and i > 15 else 'SEARCHING...'}
        [K-TYPE]: {k_scale}
        """)
        time.sleep(0.05)

    if is_alien:
        v_status.success("⚠️ CONTACTO INTELIGENTE CONFIRMADO")
        # Guardar éxito en el archivo (Persistencia)
        new_entry = pd.DataFrame([{
            "Hora": datetime.now().strftime("%H:%M"),
            "Lugar": obj_sel,
            "K-Scale": k_scale,
            "Result": "ÉXITO"
        }])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_entry], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
        
        # Mostrar matriz binaria
        v_data.table(np.random.choice([0, 1], size=(5, 10)))
    else:
        v_status.error("SCAN COMPLETO: RUIDO TÉRMICO")

# --- 7. ARCHIVO DE CIVILIZACIONES (CONSULTA) ---
st.write("---")
st.subheader("📂 ARCHIVO DE CIVILIZACIONES (REGISTRO)")

# Verificación de seguridad para evitar el errorAttributeError
if len(st.session_state.historial_df) > 0:
    st.dataframe(st.session_state.historial_df, use_container_width=True)
    if st.button("🗑️ Resetear Archivo"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.historial_df = pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])
        st.rerun()
else:
    st.info("No se han registrado hallazgos en la base de datos local.")
