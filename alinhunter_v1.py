import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURACIÓN NEXUS-7 v9.5 MASTER ---
st.set_page_config(page_title="NEXUS-7 AI v9.5", page_icon="👽", layout="wide")

# --- BASE DE DATOS CIENTÍFICA EXPANDIDA ---
INFO_SISTEMAS = {
    "Próxima b": {"dist": "4.24 AL", "tipo": "Terrestre", "estrella": "Enana Roja (M)", "hab": "Zona Habitable"},
    "Ross 128 b": {"dist": "11.03 AL", "tipo": "Templado", "estrella": "Enana Roja Inactiva", "hab": "Confirmada"},
    "K2-18b": {"dist": "124 AL", "tipo": "Hicéano", "estrella": "Enana K", "hab": "Vapor de Agua"},
    "TRAPPIST-1e": {"dist": "40.7 AL", "tipo": "Rocoso", "estrella": "Enana Ultra-fría", "hab": "Alta Probabilidad"},
    "Kepler-186f": {"dist": "582 AL", "tipo": "Análogo Tierra", "estrella": "Enana Roja", "hab": "Bosques Posibles"},
    "Sector Wow!": {"dist": "1,800 AL", "tipo": "Anomalía", "estrella": "Análogo Solar", "hab": "Señal Histórica 1977"},
    "Teegarden b": {"dist": "12.5 AL", "tipo": "Rocoso", "estrella": "Enana Teegarden", "hab": "Índice Similitud 95%"},
    "Andrómeda M31": {"dist": "2.5M AL", "tipo": "Extragaláctico", "estrella": "Núcleo Galáctico", "hab": "Tipo III"},
    "Luyten b": {"dist": "12.2 AL", "tipo": "Super-Tierra", "estrella": "Enana Roja", "hab": "Óptima"},
    "Gliese 581g": {"dist": "20.3 AL", "tipo": "Rocoso", "estrella": "Enana Roja", "hab": "Confirmación Pendiente"}
}

# --- ESTILOS CSS (Respetando Blinker y Estilo Hacker Original) ---
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
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DE MEMORIA Y ESTADO ---
if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ NÚCLEO IA v9.5 MASTER ONLINE", "◈ CARGANDO PROTOCOLOS DE HARDWARE..."]
if 'historial' not in st.session_state:
    st.session_state.historial = []

def push_log(msg):
    t = time.strftime("%H:%M:%S")
    st.session_state.ai_log.insert(0, f"[{t}] {msg}")

# --- FUNCIÓN DE LECTURA DE HARDWARE (Antena) ---
def leer_potencia_real():
    """Lee el archivo generado por la antena o sensor"""
    if os.path.exists('potencia.txt'):
        try:
            with open('potencia.txt', 'r') as f:
                data = [float(line.strip()) for line in f if line.strip()]
            # Ajustar a 400 puntos para que encaje en la interfaz
            if len(data) >= 400:
                return np.array(data[:400])
            else:
                return np.pad(data, (0, 400 - len(data)), 'constant')
        except:
            return np.random.normal(0.08, 0.02, 400)
    return np.random.normal(0.08, 0.02, 400)

# --- CABECERA ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.5 MASTER")

with st.expander("📖 MANUAL DE OPERACIONES TÉCNICAS"):
    st.markdown("""
    - **TARGET:** Seleccione un objetivo del catálogo estelar.
    - **GAIN (dB):** Ajuste la sensibilidad. Picos superiores a 6.0 sugieren origen artificial.
    - **LOCK-ON:** Si aparece el cuadro verde, la IA ha detectado un patrón en la antena.
    """)

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
        <span style="color:#00FF41;">STATUS: LEYENDO HARDWARE REAL</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

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

    if st.button("🚀 EJECUTAR ESCANEO PROFUNDO"):
        st.session_state.ai_log = ["◈ SINCRONIZANDO CON ANTENA...", "◈ BARRIDO DE FRECUENCIAS ACTIVO..."]
        steps = 85
        matriz = np.zeros((steps, 400))
        
        for t in range(steps):
            # LECTURA REAL DE LA ANTENA
            linea_real = leer_potencia_real()
            # Aplicar la ganancia del slider a los datos reales
            linea = linea_real * (gain / 350)
            
            max_peak = np.max(linea)
            matriz[t] = linea
            
            # --- TELEMETRÍA REAL ---
            calidad_real = min(100.0, (max_peak / 10) * 100)
            v_quality.code(f"CALIDAD DE SEÑAL REAL: {calidad_real:.1f}%")
            
            # Lógica de detección IA basada en los datos de la antena
            is_anomaly = max_peak > 6.0
            conf = min(100, int(calidad_real)) if is_anomaly else random.randint(1, 15)
            v_conf.progress(conf/100, text=f"CONFIANZA IA: {conf}%")
            
            # --- LOGS ---
            if t == 15: push_log(f"Analizando flujo de datos de antena...")
            if t == 45 and is_anomaly: push_log("⚠️ ¡PATRÓN NO NATURAL DETECTADO EN HARDWARE!")

            # --- RENDERIZADO WATERFALL ---
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='magma' if is_anomaly else 'viridis', origin='lower')
            ax1.axis('off')
            v_wat.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # --- RENDERIZADO POTENCIA ---
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
            color_sig = '#ff3300' if is_anomaly else '#00FF41'
            ax2.plot(linea, color=color_sig, linewidth=0.8)
            ax2.fill_between(range(400), linea, color=color_sig, alpha=0.1)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, 15) # Ajustado para datos reales
            ax2.axis('off')
            v_pow.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # --- TERMINAL ---
            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            
            if is_anomaly:
                status_text = f"IA: '¡COHERENCIA DETECTADA EN ANTENA! Probable {k_scale}.'"
                v_desc.markdown(f'<p class="alert-active">{status_text}</p>', unsafe_allow_html=True)
            else:
                v_desc.write("IA: 'Escaneando ruido de fondo...'")
            
            time.sleep(0.03)

start_master_scan()

st.caption("NEXUS-7 v9.5 MASTER | ANTENNA HARDWARE LINK | 2024")
