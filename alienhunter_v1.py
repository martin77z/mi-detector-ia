import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS-7 v9.8 (Layout Fixed)", layout="wide", page_icon="📡")

# --- PERSISTENCIA DE DATOS ---
DB_FILE = "registro_civilizaciones.csv"

def cargar_db():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])
    return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])

if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# --- INTERFAZ VISUAL MAESTRA (CSS AGRESIVO PARA ARREGLAR DISEÑO) ---
st.markdown("""
    <style>
    /* Fondo y Color Global Monocromo Verde */
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    
    /* Títulos Clásicos Neón */
    h1, h2, h3, h4 { color: #00FF41 !important; text-transform: uppercase; }
    
    /* Controles e Inputs con Ancho Controlado */
    .stSelectbox label, .stSlider label { color: #00FF41 !important; font-weight: bold; }
    
    /* Forzar que el desplegable de Navegación no se pegue al borde */
    .stSelectbox > div { margin-right: 15px; }

    /* Tarjeta de Telemetría (Fiel a la estética original) */
    .telemetria-card { 
        border: 2px solid #00FF41; 
        padding: 20px; 
        border-radius: 5px; 
        background-color: rgba(0, 0, 0, 0.9); 
        margin-top: 10px;
    }
    
    /* Botones Neón */
    .stButton>button { 
        border: 2px solid #00FF41; 
        background-color: #000; 
        color: #00FF41; 
        font-weight: bold; 
        text-transform: uppercase;
        border-radius: 0;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #00FF41; 
        color: #000; 
        box-shadow: 0 0 15px #00FF41;
    }

    /* !!! CORRECCIÓN DE LAYOUT PARA GRÁFICOS (Padding para evitar el amontonamiento) !!! */
    div[data-testid="stFigure"] {
        margin-left: 5%;
        margin-right: 5%;
    }

    /* Limpieza de Streamlit */
    [data-testid="stHeader"], [data-testid="stSidebar"], footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE OBJETIVOS ---
objetivos_db = {
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000.0 AL", "retraso": "26,000.0 años", "emision": "Edad de Hielo", "info": "Corazón de la galaxia. Agujero negro supermasivo."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470.0 AL", "retraso": "1,470.0 años", "emision": "Año 556", "info": "Anomalía de oscurecimiento masivo."},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "retraso": "4.2 años", "emision": "Hace 4 años", "info": "Planeta rocoso habitable."},
    "TRAPPIST-1e": {"cat": "2MASS J2306", "dist": "40.0 AL", "retraso": "40.0 años", "emision": "Hace 40 años", "info": "Sistema multi-planetario."},
    "K2-18b": {"cat": "EPIC 20191", "dist": "124.0 AL", "retraso": "124.0 años", "emision": "Siglo XIX", "info": "Detección de metano (JWST)."},
    "Sector Wow!": {"cat": "7UC Sgr", "dist": "1,800.0 AL", "retraso": "1,800.0 años", "emision": "Año 226", "info": "Señal histórica de 1977."},
    "Andrómeda": {"cat": "M31", "dist": "2.5M AL", "retraso": "2.5M años", "emision": "Plioceno", "info": "Civilización Tipo III potencial."}
}

st.title("📡 OMNIBUS: FIRST CONTACT | v9.8")

# --- PANEL DE CONTROL REESTRUCTURADO ---
# Forzar anchos de columna rígidos para que no se colapsen
ctrl_col, blank_col, tele_col = st.columns([1.2, 0.3, 1.5])

with ctrl_col:
    target_sel = st.selectbox("🎯 NAVEGACIÓN", list(objetivos_db.keys()), index=0)
    k_level = st.select_slider("🌌 ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"], value="Tipo III")
    gain_db = st.slider("📶 GANANCIA (dB)", 100, 500, 100) # 100 por defecto
    scan_btn = st.button("🚀 INICIAR ESCANEO PROFUNDO")

# Columna vacía de separación (blank_col) para forzar espacio

with tele_col:
    t = objetivos_db[target_sel]
    st.markdown(f"""
    <div class="telemetria-card">
        <h4 style='margin:0 0 10px 0;'>📊 TELEMETRÍA AUTOMÁTICA</h4>
        <p><b>SISTEMA:</b> {target_sel.upper()} | <b>CATÁLOGO:</b> {t['cat']}</p>
        <p><b>DISTANCIA:</b> {t['dist']} | <b>RETRASO LUZ:</b> {t['retraso']}</p>
        <p><b>ORIGEN ESTIMADO:</b> {t['emision']}</p>
        <hr style='border:0.5px solid #00FF41'>
        <p style='color:#888; font-style:italic; font-size:0.9em;'>{t['info']}</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- VISUALIZACIÓN DIVIDIDA (Radar a la izquierda, IA a la derecha) ---
col_left, blank_sep, col_right = st.columns([2.2, 0.2, 1.2])

with col_left:
    st.markdown("### 🛰️ VISUALIZACIÓN DE ESPECTRO")
    v_water = st.empty()
    v_spec = st.empty()

with col_right:
    st.markdown("### 📟 ANÁLISIS IA")
    v_alert = st.empty()
    v_ia_log = st.empty()
    v_data = st.empty()

# --- LÓGICA DE ESCANEO ---
if scan_btn:
    # Generar espectrograma inicial (Fiel al ruido base de la foto)
    data_radar = np.random.rand(40, 100) * 0.7 # Ruido base más apagado
    is_hit = random.random() > 0.3 # Tipo III es más probable
    
    for i in range(60):
        frame = np.random.normal(0.5, 0.2, 100)
        
        # Simular señal inteligente solo si se detecta
        if is_hit: frame[50] += (gain_db / 7.5)
        
        data_radar = np.roll(data_radar, -1, axis=0)
        data_radar[-1] = frame
        
        # !!! CORRECCIÓN CRÍTICA DE TAMAÑO (figsize reducido para forzar el layout) !!!
        # Usar 'figsize=(10, 5)' en lugar de algo mayor para que Streamlit no estire el gráfico
        fig_w, ax_w = plt.subplots(figsize=(10, 5), facecolor='black')
        
        # Usar 'viridis' para el ruido base, 'cool' para ruido cian/azul de la foto
        ax_w.imshow(data_radar, aspect='auto', cmap='cool' if not is_hit else 'magma')
        ax_w.axis('off')
        v_water.pyplot(fig_w)
        plt.close(fig_w)
        
        # Spectrum Plot (Verde/Rojo)
        fig_s, ax_s = plt.subplots(figsize=(10, 1.2), facecolor='black')
        ax_s.plot(frame, color='#00FF41' if not is_hit else '#ff0000')
        ax_s.set_facecolor('black')
        ax_s.set_ylim(0, 100)
        ax_s.axis('off')
        v_spec.pyplot(fig_s)
        plt.close(fig_s)
        
        # Log de IA limpio
        v_ia_log.code(f"PROCESANDO SECTOR... {i*1.6:.1f}%\nSNR: {np.max(frame):.2f}\nSTATUS: {'COHERENTE' if is_hit else 'BUSCANDO...'}")
        time.sleep(0.04)

    if is_hit:
        v_alert.success("⚠️ CONTACTO INTELIGENTE CONFIRMADO")
        new_row = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Lugar": target_sel, "K-Scale": k_level, "Result": "ÉXITO"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_row], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
        v_data.table(np.random.choice([0, 1], size=(5, 8)))
    else:
        v_alert.error("SCAN COMPLETO: NADA DETECTADO")

# --- HISTORIAL FINAL ---
st.write("---")
st.subheader("📂 ARCHIVO DE CIVILIZACIONES")
if len(st.session_state.historial_df) > 0:
    st.dataframe(st.session_state.historial_df, use_container_width=True)
else:
    st.info("Archivo de registros vacío.")
