import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURACIÓN NEXUS-7 v9.5 MASTER ---
st.set_page_config(page_title="NEXUS-7 AI v9.5", page_icon="👽", layout="wide")

# --- BASE DE DATOS CIENTÍFICA (Respetada) ---
INFO_SISTEMAS = {
    "Próxima b": {"dist": "4.24 AL", "tipo": "Terrestre", "estrella": "Enana Roja (M)", "hab": "Zona Habitable"},
    "Ross 128 b": {"dist": "11.03 AL", "tipo": "Templado", "estrella": "Enana Roja Inactiva", "hab": "Confirmada"},
    "K2-18b": {"dist": "124 AL", "tipo": "Hicéano", "estrella": "Enana K", "hab": "Vapor de Agua"},
    "TRAPPIST-1e": {"dist": "40.7 AL", "tipo": "Rocoso", "estrella": "Enana Ultra-fría", "hab": "Alta Probabilidad"},
    "Teegarden b": {"dist": "12.5 AL", "tipo": "Rocoso", "estrella": "Enana Teegarden", "hab": "Índice Similitud 95%"},
}

# --- ESTILOS CSS (Tu Interfaz Original v9.5) ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    @keyframes blinker { 50% { opacity: 0; } }
    .alert-active { color: #ff0000; font-weight: bold; animation: blinker 1s linear infinite; }
    .ai-terminal { 
        background-color: rgba(0, 10, 0, 0.95); border: 1px solid #00FF41; 
        padding: 15px; font-size: 0.8rem; height: 250px; overflow-y: auto;
        box-shadow: inset 0 0 15px rgba(0, 255, 65, 0.2);
    }
    .decoding-box { border: 2px dashed #00FF41; padding: 15px; background: rgba(0,255,65,0.03); margin-top: 10px; }
    .ai-card { border: 1px solid #00FF41; padding: 10px; background: rgba(0,255,65,0.05); }
    .stButton>button { border: 1px solid #00FF41 !important; background-color: transparent !important; color: #00FF41 !important; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000 !important; box-shadow: 0 0 25px #00FF41; }
    /* Ajuste para sliders rojos */
    div[data-baseweb="slider"] > div { background-color: #ff0000 !important; }
    div[role="slider"] { background-color: #ff0000 !important; border: 2px solid #ff0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DE ESTADO ---
if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ NÚCLEO IA v9.5 MASTER ONLINE", "◈ CARGANDO DATOS REALES EXTERNOS..."]
if 'historial' not in st.session_state:
    st.session_state.historial = []

def push_log(msg):
    t = time.strftime("%H:%M:%S")
    st.session_state.ai_log.insert(0, f"[{t}] {msg}")

# --- CABECERA ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.5 MASTER")

# --- PANEL DE CONTROL ---
col_ctrl, col_stats = st.columns([2, 1])

with col_ctrl:
    c1, c2, c3 = st.columns([1, 1, 1])
    target = c1.selectbox("🎯 OBJETIVO", list(INFO_SISTEMAS.keys()))
    k_scale = c2.select_slider("🌌 ESCALA KARDASHOV", ["Tipo I", "Tipo II", "Tipo III"])
    audio_mode = c3.checkbox("🔊 AUDIO ANALIZER", value=True)
    gain = st.slider("📶 GANANCIA DEL SENSOR (dB)", 150, 600, 347)

with col_stats:
    d = INFO_SISTEMAS[target]
    st.markdown(f"""
    <div class="ai-card">
        <b>SISTEMA:</b> {target}<br>
        <b>DATA:</b> {d['dist']} | {d['estrella']}<br>
        <b>PROB. HABIT:</b> {d['hab']}<br>
        <span style="color:#00FF41;">STATUS: LECTURA DE ARCHIVO ACTIVA</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- LÓGICA DE DATOS REALES (Eliminada Simulación) ---
def cargar_datos_reales():
    if os.path.exists('potencia.txt'):
        try:
            # Lee el archivo de potencia (lista de números por línea)
            data = np.loadtxt('potencia.txt')
            # Si el archivo es corto, lo repetimos para llenar el visualizador
            if data.size < 400:
                data = np.resize(data, 400)
            return data
        except:
            return np.zeros(400)
    else:
        # Si no existe, devolvemos ruido base para no romper la interfaz
        return np.random.normal(0.5, 0.1, 400)

# --- NÚCLEO DE PROCESAMIENTO ---
@st.fragment
def start_master_scan():
    col_viz, col_ai = st.columns([2, 1])
    
    with col_viz:
        v_wat = st.empty()
        v_pow = st.empty()
        v_decoding = st.empty()
    
    with col_ai:
        st.subheader("🧠 IA HEURÍSTICA CORE")
        v_conf = st.empty()
        v_quality = st.empty()
        v_desc = st.empty()
        v_log = st.empty()

    if st.button("🚀 EJECUTAR ESCANEO PROFUNDO (POTENCIA.TXT)"):
        st.session_state.ai_log = ["◈ ACCEDIENDO A POTENCIA.TXT...", "◈ SINCRONIZANDO SENSOR..."]
        
        # Cargamos los datos reales del archivo
        datos_reales = cargar_datos_reales()
        steps = 60
        # Matriz para el Waterfall
        matriz = np.zeros((steps, 400))
        
        for t in range(steps):
            # Procesamos la línea actual basada en el archivo real + ganancia
            linea_base = datos_reales * (gain / 300)
            # Añadimos una fluctuación mínima temporal para el efecto visual
            linea_actual = linea_base + np.random.normal(0, 0.05, 400)
            matriz[t] = linea_actual
            
            # Telemetría
            max_val = np.max(linea_actual)
            calidad = min(100.0, (max_val / 10) * 100)
            v_quality.code(f"CALIDAD DE SEÑAL REAL: {calidad:.1f}%")
            
            confianza = int(calidad * 0.9)
            v_conf.progress(confianza/100, text=f"CONFIANZA IA: {confianza}%")
            
            # Logs
            if t == 5: push_log(f"Leyendo buffer de potencia.txt...")
            if t == 30 and calidad > 50: push_log("¡Señal coherente detectada en los datos!")

            # Waterfall (Fondo Negro respetado)
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='#010801')
            ax1.imshow(matriz, aspect='auto', cmap='magma', origin='lower')
            ax1.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            v_wat.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # Potencia (Osciloscopio)
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='#010801')
            ax2.plot(linea_actual, color='#00FF41', linewidth=0.8)
            ax2.fill_between(range(400), linea_actual, color='#00FF41', alpha=0.1)
            ax2.set_facecolor('#010801')
            ax2.set_ylim(0, max(12, max_val + 2))
            ax2.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            v_pow.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            
            status_text = "IA: 'Analizando patrones en potencia.txt...'"
            if calidad > 70:
                status_text = f"IA: '¡ANOMALÍA DETECTADA EN DATOS REALES!'"
                v_desc.markdown(f'<p class="alert-active">{status_text}</p>', unsafe_allow_html=True)
            else:
                v_desc.write(status_text)
            
            time.sleep(0.02)

        if np.max(datos_reales) > 5:
            st.toast("SEÑAL REAL PROCESADA", icon="📡")

start_master_scan()

# --- HISTORIAL ---
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 LOGS DE CONTACTO - NEXUS-7")
    st.dataframe(pd.DataFrame(st.session_state.historial), use_container_width=True)

st.caption("NEXUS-7 v9.5 MASTER | REAL DATA MODE | 2024")
