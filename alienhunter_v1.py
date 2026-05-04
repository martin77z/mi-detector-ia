import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN NEXUS-7 v9.9 DNA 9.5 ---
st.set_page_config(page_title="NEXUS-7 MASTER", page_icon="📡", layout="wide")

# --- MEMORIA DE SESIÓN ---
if 'historial_global' not in st.session_state:
    st.session_state.historial_global = []
if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ NÚCLEO v9.9 ONLINE", "◈ PROTOCOLO ESTÉTICO 9.5 ACTIVO."]

def push_log(msg):
    st.session_state.ai_log.insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")

# --- CSS: EL LOOK DE LAS FOTOS ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .ai-terminal { background-color: rgba(0, 10, 0, 0.95); border: 1px solid #00FF41; padding: 15px; font-size: 0.8rem; height: 160px; overflow-y: auto; }
    .explainer-box { background-color: rgba(0, 255, 65, 0.05); border: 2px solid #00FF41; padding: 15px; border-radius: 5px; }
    .guide-box { background-color: rgba(0, 30, 0, 0.5); border: 1px double #00FF41; padding: 12px; font-size: 0.85rem; color: #fff; margin-bottom: 20px; }
    @keyframes blink { 50% { opacity: 0; } }
    .alert-active { color: #ff0000; animation: blink 1s linear infinite; font-weight: bold; border: 1px solid #ff0000; padding: 10px; text-align: center; margin-bottom: 10px; }
    .decoding-box { border: 2px dashed #00FF41; padding: 15px; background: rgba(0,255,65,0.05); margin-top: 15px; }
    .stButton>button { border: 1px solid #00FF41 !important; background-color: transparent !important; color: #00FF41 !important; width: 100%; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000 !important; box-shadow: 0 0 20px #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.9 MASTER")
st.markdown('<div class="guide-box"><b>OPERACIONES:</b> 1. Target | 2. Gain | 3. Scan. El sistema 9.5 Heurístico detectará automáticamente patrones Doppler.</div>', unsafe_allow_html=True)

# --- CONTROLES ---
col_ctrl, col_stats = st.columns([2, 1])
with col_ctrl:
    c1, c2, c3 = st.columns(3)
    target = c1.selectbox("🎯 TARGET", ["Próxima b", "Ross 128 b", "Sector Wow!", "Andrómeda M31", "Kepler-186f"])
    k_scale = c2.select_slider("🌌 ESCALA K.", ["Tipo I", "Tipo II", "Tipo III"])
    audio = c3.checkbox("🔊 AUDIO ANALIZER", value=True)
    gain = st.slider("📶 GAIN (dB)", 150, 600, 350)

with col_stats:
    st.markdown(f"""<div style="border:1px solid #00FF41; padding:10px; background:rgba(0,255,65,0.05);">
        <b>SISTEMA:</b> {target}<br><b>ESTADO:</b> ARMADO<br><b>FILTRO:</b> {k_scale}</div>""", unsafe_allow_html=True)

st.divider()

# --- MOTOR DE ESCANEO ---
@st.fragment
def run_full_scan():
    col_viz, col_ai = st.columns([2, 1])
    with col_viz:
        v_wat = st.empty()
        v_pow = st.empty()
        v_final = st.empty()
    with col_ai:
        v_alert = st.empty()
        st.markdown('<div class="explainer-box"><div class="explainer-title">🔍 INTERPRETACIÓN IA</div>', unsafe_allow_html=True)
        v_explain = st.empty()
        st.markdown('</div><br>', unsafe_allow_html=True)
        v_conf = st.empty()
        v_qual = st.empty() # Bloque de calidad técnica
        v_log = st.empty()

    if st.button("🚀 INICIAR PROCESAMIENTO TOTAL"):
        steps = 85
        matriz = np.random.normal(0.05, 0.01, (steps, 400)) 
        is_alien = random.random() < 0.8
        drift = random.uniform(-0.25, 0.25)
        start_px = random.randint(130, 270)
        
        for t in range(steps):
            linea = np.random.normal(0.05, 0.01, 400)
            if is_alien:
                pos = int(start_px + (t * drift))
                if 0 <= pos < 400:
                    linea[pos] = (gain / 70)
                    linea[max(0,pos-1):min(400,pos+2)] += (gain/140)
            matriz[t] = linea
            
            # Waterfall (Estilo 9.5 puro)
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='magma', origin='lower')
            if is_alien and t > 15:
                ax1.axvspan(pos-12, pos+12, color='#00FF41', alpha=0.15)
                ax1.text(pos+15, t, "LOCK-ON", color='#00FF41', fontsize=9, fontweight='bold')
            ax1.axis('off')
            v_wat.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # Potencia (RESCATADO: Relleno Fill de la 9.5)
            fig2, ax2 = plt.subplots(figsize=(10, 1.5), facecolor='black')
            ax2.plot(linea, color='#00FF41', linewidth=0.8)
            ax2.fill_between(range(400), linea, color='#00FF41', alpha=0.15) # DNA 9.5
            ax2.axis('off')
            v_pow.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # Interpretación Dinámica
            exp = "Escaneando..."
            if is_alien:
                if t < 40: exp = "<b>DOPPLER:</b> Curvatura detectada. Emisor en rotación planetaria."
                else: exp = "<b>POTENCIA:</b> Amplitud artificial confirmada."
                if k_scale == "Tipo III" and t > 50:
                    v_alert.markdown('<div class="alert-active">ALERTA: CONTACTO TIPO III</div>', unsafe_allow_html=True)
            v_explain.markdown(f'<div class="explainer-text">{exp}</div>', unsafe_allow_html=True)
            
            v_conf.progress(min(100, int((t/steps)*100)) if is_alien else 5/100)
            v_qual.code(f"QUALITY INDEX: {(np.max(linea)/12)*100:.2f}%") # DNA 9.5
            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            time.sleep(0.04)

        if is_alien:
            push_log(f"Señal fija en {target}")
            st.session_state.historial_global.append({"H": datetime.now().strftime("%H:%M"), "T": target, "K": k_scale})
            with v_final:
                st.markdown('<div class="decoding-box">', unsafe_allow_html=True)
                st.write("🧩 DECODIFICANDO BINARIO...")
                p_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.015)
                    p_bar.progress(i+1)
                st.table(np.random.choice([0, 1], size=(4, 15))) # DNA 9.5 Dashed Box
                st.markdown('</div>', unsafe_allow_html=True)

run_full_scan()

if st.session_state.historial_global:
    st.write("### 📂 ARCHIVO DE CONTACTOS")
    st.dataframe(pd.DataFrame(st.session_state.historial_global), use_container_width=True)
