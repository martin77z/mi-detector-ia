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
st.set_page_config(page_title="NEXUS-7 FINAL BUILD v10.1", layout="wide", page_icon="📡")

if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# CSS Consolidado: Estética Centro de Mando
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3, h4 { color: #00FF41 !important; text-transform: uppercase; letter-spacing: 1px; }
    .telemetria-card { 
        border: 2px solid #00FF41; 
        padding: 20px; 
        border-radius: 5px; 
        background-color: rgba(0, 15, 0, 0.9); 
        margin-top: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stSelectbox label, .stSlider label { color: #00FF41 !important; font-weight: bold; }
    .stButton>button { 
        border: 2px solid #00FF41; 
        background-color: #000; 
        color: #00FF41; 
        font-weight: bold; 
        text-transform: uppercase;
        border-radius: 0;
        width: 100%;
        transition: 0.3s ease;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 20px #00FF41; }
    [data-testid="stHeader"], [data-testid="stSidebar"], footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 3. CATÁLOGO ESTELAR COMPLETO (RESTAURADO) ---
objetivos_db = {
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000.0 AL", "retraso": "26,000.0 años", "emision": "Edad de Hielo", "info": "Centro Galáctico. Agujero negro supermasivo."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470.0 AL", "retraso": "1,470.0 años", "emision": "Año 556", "info": "Anomalía de oscurecimiento masivo. ¿Megaestructura?"},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "retraso": "4.2 años", "emision": "Hace 4 años", "info": "Exoplaneta rocoso en zona habitable cercano."},
    "Ross 128 b": {"cat": "Ross 128", "dist": "11.0 AL", "retraso": "11.0 años", "emision": "Hace 11 años", "info": "Mundo templado en una enana roja tranquila."},
    "Gliese 581g": {"cat": "GJ 581", "dist": "20.0 AL", "retraso": "20.0 años", "emision": "Hace 20 años", "info": "Candidato histórico a mundo habitable."},
    "TRAPPIST-1e": {"cat": "2MASS J2306", "dist": "40.0 AL", "retraso": "40.0 años", "emision": "Hace 40 años", "info": "Sistema con 7 planetas similares a la Tierra."},
    "K2-18b": {"cat": "EPIC 20191", "dist": "124.0 AL", "retraso": "124.0 años", "emision": "Siglo XIX", "info": "Detección de metano y posible océano por JWST."},
    "Sector Wow!": {"cat": "7UC Sgr", "dist": "1,800.0 AL", "retraso": "1,800.0 años", "emision": "Año 226", "info": "Lugar de origen de la señal detectada en 1977."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000.0 AL", "retraso": "25,000.0 años", "emision": "Pre-historia", "info": "Objetivo del Mensaje de Arecibo enviado en 1974."},
    "Andrómeda": {"cat": "M31", "dist": "2.5M AL", "retraso": "2.5M años", "emision": "Plioceno", "info": "Búsqueda de civilizaciones extragalácticas."}
}

st.title("📡 NEXUS-7 OMNIBUS: FINAL BUILD v10.1")

# --- 4. PANEL DE CONTROL ---
ctrl_col, spacer, tele_col = st.columns([1, 0.1, 1.2])

with ctrl_col:
    st.subheader("🧭 NAVEGACIÓN")
    target_sel = st.selectbox("OBJETIVO", list(objetivos_db.keys()))
    k_level = st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"], value="Tipo II")
    gain_db = st.slider("GANANCIA (dB)", 100, 500, 100)
    btn_scan = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with tele_col:
    t = objetivos_db[target_sel]
    st.markdown(f"""
    <div class="telemetria-card">
        <h4 style='margin-top:0;'>📊 TELEMETRÍA AUTOMÁTICA</h4>
        <b>SISTEMA:</b> {target_sel.upper()} | <b>CATÁLOGO:</b> {t['cat']}<br>
        <b>DISTANCIA:</b> {t['dist']} | <b>RETRASO LUZ:</b> {t['retraso']}<br>
        <b>ORIGEN ESTIMADO:</b> {t['emision']}<br>
        <hr style='border:0.5px solid #00FF41'>
        <i>{t['info']}</i>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- 5. VISUALIZACIÓN ---
radar_col, ia_col = st.columns([2, 1])

with radar_col:
    st.subheader("🛰️ VISUALIZACIÓN DE ESPECTRO")
    v_water = st.empty()
    v_spec = st.empty()

with ia_col:
    st.subheader("📟 ANÁLISIS IA")
    v_alert = st.empty()
    v_log = st.empty()
    v_data = st.empty()

# --- 6. LÓGICA DE ESCANEO ---
if btn_scan:
    data_radar = np.random.normal(0.2, 0.05, (40, 100))
    is_hit = random.random() > 0.4
    
    for i in range(60):
        frame = np.random.normal(0.2, 0.05, 100)
        if is_hit:
            frame[50] += (gain_db / 35) # Línea de señal coherente
        
        data_radar = np.roll(data_radar, -1, axis=0)
        data_radar[-1] = frame
        
        # Waterfall - Contraste Gnuplot2
        fig_w, ax_w = plt.subplots(figsize=(10, 5), facecolor='black')
        ax_w.imshow(data_radar, aspect='auto', cmap='gnuplot2', vmin=0, vmax=2.5)
        ax_w.axis('off')
        v_water.pyplot(fig_w)
        plt.close(fig_w)
        
        # Spectrum - Gráfico de picos
        fig_s, ax_s = plt.subplots(figsize=(10, 1.2), facecolor='black')
        ax_s.plot(frame, color='#00FF41' if not is_hit else '#FF3131', linewidth=1.5)
        ax_s.set_facecolor('black')
        ax_s.set_ylim(0, 5)
        ax_s.axis('off')
        v_spec.pyplot(fig_s)
        plt.close(fig_s)
        
        v_log.code(f"SCAN: {i*1.6:.1f}%\nSNR: {np.max(frame)*8:.2f} dB\nSTATUS: {'DETECTADO' if is_hit else 'BUSCANDO...'}")
        time.sleep(0.04)

    if is_hit:
        v_alert.success("⚠️ CONTACTO INTELIGENTE CONFIRMADO")
        new_entry = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Lugar": target_sel, "K-Scale": k_level, "Result": "ÉXITO"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_entry], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
        v_data.table(np.random.choice([0, 1], size=(5, 8)))
    else:
        v_alert.error("SCAN COMPLETO: RUIDO ESPACIAL")

# --- 7. ARCHIVO DE REGISTRO ---
st.write("---")
st.subheader("📂 ARCHIVO DE CIVILIZACIONES")
if len(st.session_state.historial_df) > 0:
    st.dataframe(st.session_state.historial_df, use_container_width=True)
else:
    st.info("Base de datos vacía.")
