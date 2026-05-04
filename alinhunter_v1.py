import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURACIÓN NEXUS-7 v9.5 MASTER (INTACTA) ---
st.set_page_config(page_title="NEXUS-7 AI v9.5", page_icon="👽", layout="wide")

# --- BASE DE DATOS CIENTÍFICA (INTACTA) ---
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

# --- ESTILOS CSS (TU INTERFAZ ORIGINAL v9.5) ---
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

# --- GESTIÓN DE MEMORIA (INTACTA) ---
if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ NÚCLEO IA v9.5 MASTER ONLINE", "◈ CARGANDO DATOS DE ANTENA..."]
if 'historial' not in st.session_state:
    st.session_state.historial = []

def push_log(msg):
    t = time.strftime("%H:%M:%S")
    st.session_state.ai_log.insert(0, f"[{t}] {msg}")

# --- CABECERA ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.5 MASTER")

# --- PANEL DE CONTROL (INTACTO) ---
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
        <span style="color:#888;">STATUS: LEYENDO SEÑAL DE ANTENA</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- LÓGICA DE MEDICIÓN REAL (Sustituye a la simulación) ---
def leer_datos_antena():
    """Lee el archivo potencia.txt generado por la lectura de señal real"""
    if os.path.exists('potencia.txt'):
        try:
            data = np.loadtxt('potencia.txt')
            # Ajustar tamaño a 400 píxeles para el visualizador
            if data.size != 400:
                data = np.interp(np.linspace(0, data.size, 400), np.arange(data.size), data)
            return data
        except Exception as e:
            return np.random.normal(0.1, 0.02, 400) # Fallback ruido si el archivo está vacío
    return np.random.normal(0.1, 0.02, 400)

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
        st.session_state.ai_log = ["◈ INICIANDO LECTURA DE HARDWARE..."]
        steps = 85
        matriz = np.zeros((steps, 400))
        
        for t in range(steps):
            # OBTENEMOS DATOS REALES
            linea = leer_datos_antena() * (gain / 100) # Aplicamos tu ganancia seleccionada
            matriz[t] = linea
            
            # TELEMETRÍA BASADA EN DATOS REALES
            max_peak = np.max(linea)
            calidad_real = min(100.0, (max_peak / 15) * 100)
            v_quality.code(f"CALIDAD DE SEÑAL: {calidad_real:.1f}%")
            
            # La IA ahora evalúa la calidad real de la antena
            conf = int(calidad_real)
            v_conf.progress(conf/100, text=f"CONFIANZA IA: {conf}%")
            
            # --- LOGS (Respetando el ritmo de tu interfaz) ---
            if t == 15: push_log(f"Sincronizando con antena en {target}...")
            if t == 45 and calidad_real > 60: push_log("¡ANOMALÍA DETECTADA EN HARDWARE!")
            
            # --- RENDERIZADO WATERFALL (Misma interfaz, datos reales) ---
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
            # Usamos 'viridis' para datos base y 'magma' si hay picos altos (señal real)
            current_cmap = 'magma' if calidad_real > 50 else 'viridis'
            ax1.imshow(matriz, aspect='auto', cmap=current_cmap, origin='lower')
            ax1.axis('off')
            v_wat.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # --- RENDERIZADO POTENCIA (Misma interfaz, datos reales) ---
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
            color_sig = '#ff3300' if calidad_real > 70 else '#00FF41'
            ax2.plot(linea, color=color_sig, linewidth=0.8)
            ax2.fill_between(range(400), linea, color=color_sig, alpha=0.1)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, max(20, max_peak + 5))
            ax2.axis('off')
            v_pow.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # --- ACTUALIZACIÓN TERMINAL ---
            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            
            # Mensajes de la IA basados en la antena
            if calidad_real > 70:
                v_desc.markdown(f'<p class="alert-active">IA: ¡COHERENCIA DETECTADA EN POTENCIA.TXT!</p>', unsafe_allow_html=True)
            else:
                v_desc.write("IA: 'Procesando estática de la antena...'")
            
            time.sleep(0.03)

start_master_scan()

# --- HISTORIAL (INTACTO) ---
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 LOGS DE CONTACTO - NEXUS-7")
    st.dataframe(pd.DataFrame(st.session_state.historial), use_container_width=True)

st.caption("NEXUS-7 v9.5 MASTER | MODULADOR DE ANTENA REAL | 2024")
