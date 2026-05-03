import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- GESTIÓN DE BASE DE DATOS ---
DB_FILE = "registro_civilizaciones.csv"
def cargar_db():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Hora", "Lugar", "Result"])
    return pd.DataFrame(columns=["Hora", "Lugar", "Result"])

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="NEXUS-7 ORIGINAL BLUE", layout="wide")
if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# --- ESTILO ORIGINAL (AZUL/CIAN) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .telemetria-card { border: 2px solid #00FF41; padding: 15px; background: rgba(0, 50, 50, 0.2); }
    .stButton>button { border: 2px solid #00FF41; background: #000; color: #00FF41; width: 100%; }
    [data-testid="stHeader"], footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- LOS 10 OBJETIVOS COMPLETOS ---
objetivos_db = {
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000.0 AL", "info": "Centro Galáctico."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470.0 AL", "info": "¿Megaestructuras?"},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "info": "Vecino habitable."},
    "Ross 128 b": {"cat": "Ross 128", "dist": "11.0 AL", "info": "Mundo templado."},
    "Gliese 581g": {"cat": "GJ 581", "dist": "20.0 AL", "info": "Super-Tierra."},
    "TRAPPIST-1e": {"cat": "2MASS J2306", "dist": "40.0 AL", "info": "7 mundos rocosos."},
    "K2-18b": {"cat": "EPIC 20191", "dist": "124.0 AL", "info": "JWST detectó metano."},
    "Sector Wow!": {"cat": "7UC Sgr", "dist": "1,800.0 AL", "info": "Señal de 1977."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000.0 AL", "info": "Mensaje Arecibo."},
    "Andrómeda": {"cat": "M31", "dist": "2.5M AL", "info": "Galaxia vecina."}
}

st.title("📡 NEXUS-7 | RECUERDO AZUL")

c1, _, c2 = st.columns([1, 0.1, 1.3])
with c1:
    target_sel = st.selectbox("DESTINO", list(objetivos_db.keys()))
    gain_db = st.slider("GANANCIA (dB)", 100, 500, 100)
    btn_scan = st.button("🚀 INICIAR ESCANEO")

with c2:
    t = objetivos_db[target_sel]
    st.markdown(f"<div class='telemetria-card'><h4>📊 DATOS: {target_sel}</h4><b>DISTANCIA:</b> {t['dist']}<br><hr>{t['info']}</div>", unsafe_allow_html=True)

v_water = st.empty()
v_spec = st.empty()

if btn_scan:
    data_radar = np.random.rand(40, 100) * 0.6 
    is_hit = random.random() > 0.4
    
    for i in range(60):
        frame = np.random.rand(100) * 0.5
        if is_hit: frame[50] += (gain_db / 110)
        
        data_radar = np.roll(data_radar, -1, axis=0)
        data_radar[-1] = frame
        
        # EL COLOR AZUL/CIAN ORIGINAL (Mapa 'cool')
        fig_w, ax_w = plt.subplots(figsize=(10, 5), facecolor='black')
        ax_w.imshow(data_radar, aspect='auto', cmap='cool', vmin=0, vmax=1.5)
        ax_w.axis('off')
        v_water.pyplot(fig_w)
        plt.close(fig_w)
        
        # Gráfico de línea
        fig_s, ax_s = plt.subplots(figsize=(10, 1), facecolor='black')
        ax_s.plot(frame, color='#00FF41' if not is_hit else '#FF3131')
        ax_s.set_facecolor('black')
        ax_s.set_ylim(0, 2.5)
        ax_s.axis('off')
        v_spec.pyplot(fig_s)
        plt.close(fig_s)
        time.sleep(0.04)

st.write("---")
st.subheader("📂 ARCHIVO DE REGISTRO")
st.dataframe(st.session_state.historial_df, use_container_width=True)
