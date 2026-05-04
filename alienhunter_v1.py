import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN NEXUS-7 v9.8 OMNI ---
st.set_page_config(page_title="NEXUS-7 v9.8 OMNI", page_icon="📡", layout="wide")

# --- BASE DE DATOS CIENTÍFICA ---
INFO_SISTEMAS = {
    "Próxima b": {"dist": "4.24 AL", "tipo": "Terrestre", "estrella": "Enana Roja", "hab": "Zona Habitable"},
    "Ross 128 b": {"dist": "11.03 AL", "tipo": "Templado", "estrella": "Enana Roja Inactiva", "hab": "Confirmada"},
    "Sector Wow!": {"dist": "1,800 AL", "tipo": "Anomalía", "estrella": "Análogo Solar", "hab": "Señal Histórica"},
    "TRAPPIST-1e": {"dist": "40.7 AL", "tipo": "Rocoso", "estrella": "Enana Ultra-fría", "hab": "Alta Prob."},
    "Andrómeda M31": {"dist": "2.5M AL", "tipo": "Galaxia", "estrella": "Núcleo Galáctico", "hab": "Tipo III"}
}

# --- ESTILOS CSS (Fusión Total) ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .ai-terminal { 
        background-color: rgba(0, 10, 0, 0.95); border: 1px solid #00FF41; 
        padding: 15px; font-size: 0.8rem; height: 180px; overflow-y: auto;
    }
    .explainer-box {
        background-color: rgba(0, 255, 65, 0.05); border: 2px solid #00FF41;
        padding: 15px; border-radius: 5px; margin-bottom: 10px;
    }
    .decoding-box { border: 2px dashed #00FF41; padding: 15px; background: rgba(0,255,65,0.03); margin-top: 10px; }
    .stButton>button { border: 1px solid #00FF41 !important; background-color: transparent !important; color: #00FF41 !important; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000 !important; box-shadow: 0 0 20px #00FF41; }
    @keyframes blink { 50% { opacity: 0; } }
    .alert-active { color: #ff0000; animation: blink 1s linear infinite; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DE MEMORIA ---
if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ NÚCLEO OMNI ONLINE", "◈ SISTEMAS LISTOS."]
if 'historial' not in st.session_state:
    st.session_state.historial = []

def push_log(msg):
    st.session_state.ai_log.insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")

# --- INTERFAZ SUPERIOR ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.8 OMNI")

col_ctrl, col_stats = st.columns([2, 1])
with col_ctrl:
    c1, c2, c3 = st.columns(3)
    target = c1.selectbox("🎯 OBJETIVO", list(INFO_SISTEMAS.keys()))
    k_scale = c2.select_slider("🌌 KARDASHOV", ["Tipo I", "Tipo II", "Tipo III"])
    audio_on = c3.checkbox("🔊 AUDIO", value=True)
    gain = st.slider("📶 GANANCIA (dB)", 150, 600, 347)

with col_stats:
    d = INFO_SISTEMAS[target]
    st.markdown(f"""<div style="border:1px solid #00FF41; padding:10px; background:rgba(0,255,65,0.05);">
        <b>SISTEMA:</b> {target}<br><b>DIST:</b> {d['dist']}<br><b>TIPO:</b> {d['tipo']}</div>""", unsafe_allow_html=True)

st.divider()

# --- MOTOR DE ESCANEO OMNI ---
@st.fragment
def run_omni_scan():
    col_viz, col_ai = st.columns([2, 1])
    
    with col_viz:
        v_wat = st.empty()
        v_pow = st.empty()
        v_decoding = st.empty()
    
    with col_ai:
        # 1. Módulo de Explicación (v9.7)
        st.markdown('<div class="explainer-box">', unsafe_allow_html=True)
        st.markdown('<b style="color:#fff;">🔍 INTERPRETACIÓN IA</b>', unsafe_allow_html=True)
        v_explain = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 2. Telemetría Técnica (v9.5)
        st.subheader("🧠 IA HEURÍSTICA")
        v_conf = st.empty()
        v_quality = st.empty() # Calidad SNR rescatada
        v_desc = st.empty()
        v_log = st.empty()

    if st.button("🚀 INICIAR ESCANEO TOTAL"):
        st.session_state.ai_log = ["◈ INICIANDO BARRIDO..."]
        steps = 80
        matriz = np.random.normal(0.05, 0.02, (steps, 400))
        is_alien = random.random() < 0.75
        drift = random.uniform(-0.25, 0.25)
        start_px = random.randint(130, 270)
        
        for t in range(steps):
            linea = np.random.normal(0.05, 0.01, 400)
            max_peak = np.max(linea)
            
            if is_alien:
                pos = int(start_px + (t * drift))
                if 0 <= pos < 400:
                    linea[pos] = (gain / 70)
                    linea[max(0,pos-1):min(400,pos+2)] += (gain/140)
                    max_peak = linea[pos]
            
            matriz[t] = linea
            
            # --- RENDERIZADO WATERFALL ---
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='magma', origin='lower')
            if is_alien and t > 15:
                ax1.axvspan(pos-12, pos+12, color='#00FF41', alpha=0.15)
                ax1.text(pos+15, t, "LOCK-ON", color='#00FF41', fontsize=9, fontweight='bold')
            ax1.axis('off')
            v_wat.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # --- RENDERIZADO POTENCIA ---
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
            ax2.plot(linea, color='#00FF41', linewidth=0.8)
            ax2.fill_between(range(400), linea, color='#00FF41', alpha=0.1)
            ax2.axis('off')
            v_pow.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # --- EXPLICACIÓN DINÁMICA ---
            exp = "Analizando ruido estelar..."
            if is_alien:
                if t < 30: exp = "<b>EFECTO DOPPLER:</b> Inclinación detectada. El emisor está en movimiento planetario."
                elif t < 60: exp = f"<b>KARDASHOV {k_scale}:</b> Energía detectada compatible con tecnología escala {k_scale}."
                else: exp = "<b>PORTADORA ESTABLE:</b> La señal es artificial. Iniciando captura de paquetes."
            v_explain.markdown(f'<div style="color:#aaffaa; font-size:0.85rem;">{exp}</div>', unsafe_allow_html=True)
            
            # --- CALIDAD SNR (RESCATADO) ---
            snr = (max_peak / 10) * 100
            v_quality.code(f"CALIDAD SEÑAL: {snr:.1f}%")
            
            conf = min(100, int((t/steps)*100)) if is_alien else random.randint(1, 8)
            v_conf.progress(conf/100, text=f"CONFIANZA: {conf}%")
            
            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            time.sleep(0.04)

        # --- FASE DE DECODIFICACIÓN (RESCATADO) ---
        if is_alien:
            with v_decoding:
                st.markdown('<div class="decoding-box">', unsafe_allow_html=True)
                st.write("🧩 DECODIFICANDO MENSAJE BINARIO...")
                p = st.progress(0)
                for i in range(100):
                    time.sleep(0.01); p.progress(i+1)
                
                # Tabla de datos (v9.5)
                st.table(np.random.choice([0, 1], size=(5, 15)))
                
                # Botón de Registro (RESCATADO)
                if st.button("💾 REGISTRAR CONTACTO"):
                    st.session_state.historial.append({
                        "Fecha": datetime.now().strftime("%H:%M"),
                        "Origen": target, "Tipo": k_scale, "SNR": f"{snr:.1f}%"
                    })
                    st.success("Guardado en Logs Históricos.")
                st.markdown('</div>', unsafe_allow_html=True)

run_omni_scan()

# --- HISTORIAL (RESCATADO) ---
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 ARCHIVO HISTÓRICO DE CONTACTOS")
    st.table(pd.DataFrame(st.session_state.historial))

st.caption("NEXUS-7 v9.8 OMNI | 2024")
