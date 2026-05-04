import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE SISTEMA NEXUS-7 v9.0 ULTIMATE ---
st.set_page_config(page_title="NEXUS-7 AI v9.0", page_icon="👽", layout="wide")

# --- BASE DE DATOS CIENTÍFICA ---
INFO_SISTEMAS = {
    "Próxima b": {"dist": "4.24 AL", "tipo": "Rocoso", "estrella": "Enana Roja (M)", "hab": "Zona Alta"},
    "Ross 128 b": {"dist": "11.03 AL", "tipo": "Templado", "estrella": "Enana Roja Inactiva", "hab": "Confirmada"},
    "K2-18b": {"dist": "124 AL", "tipo": "Hicéano", "estrella": "Enana K", "hab": "Vapor de Agua"},
    "Sector Wow!": {"dist": "1,800 AL", "tipo": "Desconocido", "estrella": "Análogo Solar", "hab": "Señal Histórica"},
    "Andrómeda": {"dist": "2.5M AL", "tipo": "Galaxia", "estrella": "Cúmulo Estelar", "hab": "Extragaláctica"}
}

# --- ESTILO VISUAL INYECTADO (MIL-SPEC) ---
st.markdown("""
    <style>
    .stApp { background-color: #010a01; color: #00FF41; font-family: 'Courier New', monospace; }
    .ai-terminal { 
        background-color: rgba(0, 15, 0, 0.95); border: 1px solid #00FF41; 
        padding: 15px; font-size: 0.8rem; height: 320px; overflow-y: auto;
        box-shadow: inset 0 0 20px rgba(0, 255, 65, 0.1);
    }
    .ai-card { border: 1px solid #00FF41; padding: 15px; background: rgba(0,40,0,0.3); border-radius: 5px; }
    .ai-description { border-left: 4px solid #00FF41; padding-left: 15px; margin: 15px 0; color: #ccffcc; font-style: italic; background: rgba(0,255,65,0.05); padding-top: 5px; padding-bottom: 5px;}
    .stButton>button { border: 2px solid #00FF41 !important; background-color: #000 !important; color: #00FF41 !important; width: 100%; font-weight: bold; height: 3em; text-transform: uppercase; }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000 !important; box-shadow: 0 0 40px #00FF41; transition: 0.3s; }
    .critical-alert { color: #ff0000; font-weight: bold; animation: blinker 0.8s linear infinite; text-align: center; font-size: 1.2em; border: 1px solid #ff0000; padding: 10px; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# Motor de Audio (JS Inyectado)
def play_sound(sound_type="noise"):
    url = "https://www.soundjay.com/buttons/beep-01a.mp3" if sound_type == "alien" else "https://www.soundjay.com/misc/sounds/white-noise-01.mp3"
    st.components.v1.html(f"<script>new Audio('{url}').play();</script>", height=0)

# Memoria de Sesión
if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ NÚCLEO IA NEXUS-7 ACTIVADO", "◈ PROTOCOLO DE ESCANEO LISTO."]
if 'historial' not in st.session_state:
    st.session_state.historial = []

def push_log(msg):
    t = time.strftime("%H:%M:%S")
    st.session_state.ai_log.insert(0, f"[{t}] {msg}")

# --- CABECERA ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.0")
st.write("---")

col_top_left, col_top_right = st.columns([2, 1])

with col_top_left:
    c1, c2 = st.columns(2)
    target = c1.selectbox("🎯 DESTINO GALÁCTICO", list(INFO_SISTEMAS.keys()))
    k_scale = c2.select_slider("🌌 NIVEL DE CIVILIZACIÓN (KARDASHOV)", ["Tipo I", "Tipo II", "Tipo III"])
    
    c3, c4 = st.columns([2, 1])
    gain = c3.slider("📶 GANANCIA DEL SENSOR (dB)", 200, 800, 400)
    audio_on = c4.checkbox("🔊 AUDIO-LOG", value=True)

with col_top_right:
    d = INFO_SISTEMAS[target]
    st.markdown(f"""
    <div class="ai-card">
        <b>SISTEMA:</b> {target} | <b>DIST:</b> {d['dist']}<br>
        <b>ESTRELLA:</b> {d['estrella']}<br>
        <b>CONDICIÓN:</b> {d['hab']}<br>
        <small style="color:#666;">ESTADO: LISTO PARA BARRIDO TÉRMICO</small>
    </div>
    """, unsafe_allow_html=True)

# --- PROCESADOR DE DATOS (FRAGMENTO) ---
@st.fragment
def run_ai_scanner():
    col_viz, col_brain = st.columns([2, 1])
    
    with col_viz:
        v_waterfall = st.empty()
        v_power = st.empty()
        v_message = st.empty()
    
    with col_brain:
        st.subheader("🧠 IA HEURÍSTICA CORE")
        v_conf = st.empty()
        v_desc = st.empty()
        v_log = st.empty()

    if st.button("🚀 INICIAR ESCANEO PROFUNDO"):
        st.session_state.ai_log = ["◈ INICIANDO BARRIDO DE FRECUENCIA..."]
        if audio_on: play_sound("noise")
        
        steps = 100
        data_matrix = np.random.normal(0.05, 0.02, (steps, 400))
        
        prob_map = {"Tipo I": 0.25, "Tipo II": 0.55, "Tipo III": 0.85}
        is_alien = random.random() < prob_map[k_scale]
        drift = random.uniform(-0.25, 0.25)
        start_px = random.randint(100, 300)
        
        for t in range(steps):
            line = np.random.normal(0.05, 0.02, 400)
            if is_alien:
                curr_px = int(start_px + (t * drift))
                if 0 <= curr_px < 400:
                    line[curr_px] = (gain / 80) * (1 + random.random()*0.2)
                    line[max(0, curr_px-1)] = line[curr_px] * 0.4
                    line[min(399, curr_px+1)] = line[curr_px] * 0.4
            
            data_matrix[t] = line
            
            # Inteligencia IA
            conf_val = min(100, int((t/steps)*120)) if is_alien else random.randint(3, 18)
            v_conf.progress(min(100, conf_val)/100, text=f"CONFIANZA IA: {min(100, conf_val)}%")
            
            if t == 15: push_log(f"Analizando espectro en {target}...")
            if t == 40 and is_alien: 
                push_log("¡ALERTA! Detectada portadora de banda estrecha.")
                if audio_on: play_sound("alien")
            if t == 70 and is_alien: push_log("Sincronización exitosa. Extrayendo paquetes...")

            # Render Waterall
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
            ax1.imshow(data_matrix, aspect='auto', cmap='magma' if is_alien else 'viridis', origin='lower')
            if is_alien and t > 20:
                ax1.axvspan(curr_px-12, curr_px+12, color='#00FF41', alpha=0.1)
                ax1.text(curr_px+15, t, "LOCK-ON", color='#00FF41', fontsize=8, fontweight='bold')
            ax1.axis('off')
            v_waterfall.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # Render Potencia
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
            cp = '#ff0000' if is_alien and k_scale == "Tipo III" else '#00FF41'
            ax2.plot(line, color=cp, linewidth=0.8)
            ax2.fill_between(range(400), line, color=cp, alpha=0.1)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, 12)
            ax2.axis('off')
            v_power.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # Logs y Descripción
            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            ai_msg = f"IA: 'Detectada posible Tecnosignatura Tipo {k_scale}. El patrón no es natural.'" if is_alien else "IA: 'Buscando... Ruido de fondo dentro de parámetros normales.'"
            v_desc.markdown(f'<div class="ai-description">{ai_msg}</div>', unsafe_allow_html=True)

            time.sleep(0.02)

        if is_alien:
            if k_scale == "Tipo III":
                st.markdown('<div class="critical-alert">⚠️ CONTACTO TIPO III: CIVILIZACIÓN SUPERIOR IDENTIFICADA ⚠️</div>', unsafe_allow_html=True)
            
            with v_message:
                st.subheader("📟 MATRIZ DE DATOS DECODIFICADA")
                st.table(np.random.choice([0, 1], size=(8, 20)))
            
            st.session_state.historial.append({"Hora": datetime.now().strftime("%H:%M"), "Origen": target, "Escala": k_scale})
            st.balloons()
        else:
            st.info("BARRIDO COMPLETADO: No se detectaron anomalías inteligentes.")

run_ai_scanner()

# --- HISTORIAL ---
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 LOG DE CIVILIZACIONES DETECTADAS")
    st.table(pd.DataFrame(st.session_state.historial))

# --- FOOTER IA ---
st.write("---")
st.caption(f"NEXUS-7 v9.0 | IA Load: {random.randint(20,45)}% | Kernell: SETI-OS 2026")
