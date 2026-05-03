import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime
import os

# --- 1. GESTIÓN DE ARCHIVOS FÍSICOS ---
DB_FILE = "nexus7_civilization_archive.csv"

def load_archive():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["ID", "Hora", "Objetivo", "ID Técnico", "Distancia", "Retraso", "SNR", "Resultado"])
    return pd.DataFrame(columns=["ID", "Hora", "Objetivo", "ID Técnico", "Distancia", "Retraso", "SNR", "Resultado"])

# --- 2. CONFIGURACIÓN MAESTRA ---
st.set_page_config(page_title="NEXUS-7 OMNIBUS v8.1", page_icon="📡", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = load_archive()

# Inyección de CSS para estética de Terminal SETI
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .stSelectbox, .stSlider { background-color: #051205; border: 1px solid #00FF41; padding: 10px; border-radius: 5px; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; font-weight: bold; width: 100%; height: 3.5em; text-transform: uppercase; }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 30px #00FF41; }
    .telemetry-card { background-color: #051205; border: 1px solid #00FF41; padding: 20px; border-radius: 5px; min-height: 200px; }
    .alert-contact { color: #ff0000; animation: blink 1.2s infinite; font-weight: bold; text-align: center; border: 2px solid #ff0000; padding: 15px; font-size: 1.3em; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.1; } 100% { opacity: 1; } }
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DICCIONARIO DE OBJETIVOS CON TELEMETRÍA ---
TARGETS = {
    "Estrella de Tabby": {"ID": "KIC 8462852", "Dist": 1470.0, "Nota": "Anomalía de oscurecimiento masivo."},
    "Próxima b": {"ID": "HIP 70890", "Dist": 4.24, "Nota": "Exoplaneta rocoso más cercano."},
    "Ross 128 b": {"ID": "HIP 57548", "Dist": 11.0, "Nota": "Mundo templado en enana roja."},
    "Sector Wow!": {"ID": "SETI-77-SRC", "Dist": 1800.0, "Nota": "Firma de banda estrecha histórica."},
    "TRAPPIST-1e": {"ID": "KIC-2016-1e", "Dist": 40.0, "Nota": "Sistema de 7 mundos rocosos."},
    "Andrómeda": {"ID": "M31-NGC-224", "Dist": 2537000.0, "Nota": "Objetivo de Galaxia Vecina (Tipo III)."}
}

st.title("📡 NEXUS-7 OMNIBUS: FIRST CONTACT v8.1")

# --- 4. INTERFAZ DE OPERADOR ---
c1, c2, c3 = st.columns([1.5, 1.5, 3])

with c1:
    st.subheader("🎯 NAVEGACIÓN")
    obj_sel = st.selectbox("OBJETIVO", list(TARGETS.keys()))
    k_scale = st.select_slider("🌌 ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c2:
    st.subheader("📶 ANTENA")
    ganancia = st.slider("GANANCIA (dB)", 100, 500, 250)
    trigger = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with c3:
    t_data = TARGETS[obj_sel]
    anio_origen = datetime.now().year - int(t_data['Dist'])
    st.markdown(f"""
    <div class="telemetry-card">
        <h3 style='margin:0; color:#00FF41;'>📊 TELEMETRÍA AUTOMÁTICA</h3>
        <p style='margin:5px 0;'><b>SISTEMA:</b> {obj_sel.upper()} | <b>CATÁLOGO:</b> {t_data['ID']}</p>
        <p style='margin:5px 0;'><b>DISTANCIA:</b> {t_data['Dist']:,} AL</p>
        <p style='margin:5px 0;'><b>RETRASO LUZ:</b> {t_data['Dist']:,} años (Emisión: Año {anio_origen})</p>
        <hr style='border:0.5px solid #1a3a1a;'>
        <p style='margin:0; font-size:0.85em; color:#888;'><i>{t_data['Nota']}</i></p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 5. ÁREA DE PROCESAMIENTO (RADAR Y DECODER) ---
col_vis, col_dec = st.columns([2, 1])

with col_vis:
    st.write("🛰️ **VISUALIZACIÓN DE ESPECTRO**")
    v_cascada = st.empty()
    v_potencia = st.empty()

with col_dec:
    st.subheader("📟 DECODER IA")
    v_alerta = st.empty()
    v_terminal = st.empty()
    v_matrix = st.empty()

if trigger:
    # Probabilidad basada en Kardashov
    prob_map = {"Tipo I": 0.3, "Tipo II": 0.5, "Tipo III": 0.8}
    es_alien = random.random() < prob_map[k_scale]
    
    pasos = 80
    matriz = np.random.normal(0.5, 0.1, (pasos, 400))
    pos_x = random.randint(120, 280)
    deriva = random.uniform(-0.08, 0.08) # Efecto Doppler real

    for t in range(pasos):
        if es_alien:
            centro = int(pos_x + t * deriva)
            if 0 <= centro < 400:
                matriz[t, centro-1:centro+2] += (ganancia / 80)
        
        # Render Waterfall
        fig1, ax1 = plt.subplots(figsize=(10, 4.5), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)

        # Render Potencia (Sonido)
        fig2, ax2 = plt.subplots(figsize=(10, 1.8), facecolor='black')
        ax2.plot(matriz[t], color='#FF0000' if es_alien else '#00FF41', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 6)
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)

        v_terminal.code(f"ANÁLISIS DE SECTOR: {obj_sel}\nCOHERENCIA BINARIA: {'ALTA' if es_alien and t>40 else 'BUSCANDO...'}\nSNR: {round(ganancia/18.5, 1)} dB")
        time.sleep(0.01)

    if es_alien:
        v_alerta.markdown('<p class="alert-contact">🎯 CONTACTO INTELIGENTE DETECTADO 🎯</p>', unsafe_allow_html=True)
        msg_dec = np.random.choice([0, 1], size=(8, 8))
        v_matrix.table(msg_dec)
        
        # GUARDAR HALLAZGO PERMANENTE
        nuevo = pd.DataFrame([{
            "ID": len(st.session_state.historial) + 1,
            "Hora": datetime.now().strftime("%H:%M"),
            "Objetivo": obj_sel,
            "ID Técnico": t_data['ID'],
            "Distancia": f"{t_data['Dist']} AL",
            "Retraso": f"{t_data['Dist']} años",
            "SNR": round(ganancia/18.5, 1),
            "Resultado": "ÉXITO"
        }])
        st.session_state.historial = pd.concat([st.session_state.historial, nuevo], ignore_index=True)
        st.session_state.historial.to_csv(DB_FILE, index=False)
    else:
        v_alerta.error("SCAN COMPLETO: Sin señales de origen artificial.")

# --- 6. ARCHIVO DE CIVILIZACIONES (EVIDENCIA B) ---
if not st.session_state.historial.empty:
    st.divider()
    st.subheader("📂 ARCHIVO DE CIVILIZACIONES (REGISTROS GUARDADOS)")
    st.table(st.session_state.historial)
    
    # Herramientas de Archivo
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        csv_data = st.session_state.historial.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DESCARGAR REPORTE NEXUS-7", csv_data, "archivo_seti.csv", "text/csv")
    with col_f2:
        if st.button("🗑️ BORRAR HISTORIAL FÍSICO"):
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            st.session_state.historial = pd.DataFrame(columns=["ID", "Hora", "Objetivo", "ID Técnico", "Distancia", "Retraso", "SNR", "Resultado"])
            st.rerun()
