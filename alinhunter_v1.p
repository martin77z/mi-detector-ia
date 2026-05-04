import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

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

# --- ESTILOS CSS ---
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

if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ NÚCLEO IA v9.5 MASTER ONLINE", "◈ CARGANDO PROTOCOLOS DE DECODIFICACIÓN..."]
if 'historial' not in st.session_state:
    st.session_state.historial = []

def push_log(msg):
    t = time.strftime("%H:%M:%S")
    st.session_state.ai_log.insert(0, f"[{t}] {msg}")

# --- CABECERA ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.5 MASTER")

with st.expander("📖 MANUAL DE OPERACIONES TÉCNICAS"):
    st.markdown("""
    - **TARGET:** Seleccione un objetivo del catálogo estelar.
    - **GAIN (dB):** Ajuste la sensibilidad. Picos superiores a 6.0 sugieren origen artificial.
    - **LOCK-ON:** Si aparece el cuadro verde, no aborte el proceso; la IA está triangulando.
    - **AUDIO-TYPE:** El sistema emite ráfagas de estática o tonos de datos según la señal.
    """)

col_ctrl, col_stats = st.columns([2, 1])

with col_ctrl:
    c1, c2, c3 = st.columns([1, 1, 1])
    target = c1.selectbox("🎯 OBJETIVO", list(INFO_SISTEMAS.keys()))
    k_scale = c2.select_slider("🌌 ESCALA KARDASHOV", ["Tipo I", "Tipo II", "Tipo III"])
    audio_mode = c3.checkbox("🔊 AUDIO ANALYZER", value=True)
    gain = st.slider("📶 GANANCIA DEL SENSOR (dB)", 150, 600, 347)

with col_stats:
    d = INFO_SISTEMAS[target]
    st.markdown(f"""
    <div class="ai-card">
        <b>SISTEMA:</b> {target}<br>
        <b>DATA:</b> {d['dist']} | {d['estrella']}<br>
        <b>PROB. HABIT:</b> {d['hab']}<br>
        <span style="color:#888;">STATUS: SISTEMA DE ESCANEO ARMADO</span>
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
        st.session_state.ai_log = ["◈ INICIANDO BARRIDO DE FRECUENCIAS..."]
        steps = 85
        matriz = np.random.normal(0.08, 0.02, (steps, 400))
        
        prob_map = {"Tipo I": 0.25, "Tipo II": 0.55, "Tipo III": 0.90}
        is_alien = random.random() < prob_map[k_scale]
        drift = random.uniform(-0.28, 0.28)
        start_px = random.randint(110, 290)
        
        for t in range(steps):
            linea = np.random.normal(0.08, 0.02, 400)
            max_peak = np.max(linea)
            
            if is_alien:
                pos = int(start_px + (t * drift))
                if 0 <= pos < 400:
                    linea[pos] = (gain / 70) * (1 + random.random()*0.1)
                    linea[max(0,pos-1):min(400,pos+2)] += (gain/140)
                    max_peak = linea[pos]
            
            matriz[t] = linea
            
            # --- TELEMETRÍA (Estilo Mejorado para visibilidad) ---
            calidad_real = (max_peak / 10) * 100
            v_quality.markdown(f'<div style="color:#00FF41; font-family:monospace; margin-bottom:10px;">CALIDAD DE SEÑAL: {calidad_real:.1f}%</div>', unsafe_allow_html=True)
            
            conf = min(100, int((t/steps)*100)) if is_alien else random.randint(1, 12)
            v_conf.progress(conf/100, text=f"CONFIANZA IA: {conf}%")
            
            # --- LOGS NARRATIVOS Y SONIDO ---
            if t == 15: push_log(f"Triangulando coordenadas de {target}...")
            
            if t == 45 and is_alien: 
                push_log("¡LOCK-ON CONFIRMADO! Estabilizando portadora.")
                # INYECCIÓN DE SONIDO
                if audio_mode:
                    sr = 44100
                    dur = 1.2
                    freq = 880 
                    t_audio = np.linspace(0, dur, int(sr * dur))
                    # Tono senoidal + un poco de ruido blanco para efecto espacial
                    audio_signal = (0.3 * np.sin(2 * np.pi * freq * t_audio)) + np.random.normal(0, 0.02, len(t_audio))
                    st.audio(audio_signal, format="audio/wav", sample_rate=sr, autoplay=True)

            if t == 70 and is_alien: push_log("Sincronizando frames de datos binarios...")

            # --- RENDERIZADO WATERFALL ---
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='magma' if is_alien else 'viridis', origin='lower')
            if is_alien and t > 15:
                ax1.axvspan(pos-12, pos+12, color='#00FF41', alpha=0.15)
                ax1.text(pos+15, t, "LOCK-ON", color='#00FF41', fontsize=9, fontweight='bold')
            ax1.axis('off')
            v_wat.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # --- RENDERIZADO POTENCIA ---
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
            color_sig = '#ff3300' if is_alien and k_scale == "Tipo III" else '#00FF41'
            ax2.plot(linea, color=color_sig, linewidth=0.8)
            ax2.fill_between(range(400), linea, color=color_sig, alpha=0.1)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, 12)
            ax2.axis('off')
            v_pow.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # --- ACTUALIZACIÓN TERMINAL ---
            v_log.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            
            status_text = "IA: 'Esperando señal coherente...'"
            if is_alien:
                status_text = f"IA: '¡ANOMALÍA DETECTADA! Confirmada civilización {k_scale}.'"
                if k_scale == "Tipo III":
                    v_desc.markdown(f'<p class="alert-active">{status_text}</p>', unsafe_allow_html=True)
                else:
                    v_desc.markdown(f'<div style="color:#00FF41;">{status_text}</div>', unsafe_allow_html=True)
            else:
                v_desc.write(status_text)
            
            time.sleep(0.03)

        # --- FASE DE DECODIFICACIÓN ---
        if is_alien:
            st.toast("CONTACTO ESTABLECIDO", icon="🛸")
            with v_decoding:
                st.markdown('<div class="decoding-box">', unsafe_allow_html=True)
                st.write("🧩 PROCESANDO MENSAJE BINARIO...")
                prog_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    prog_bar.progress(i + 1)
                
                msg_data = np.random.choice([0, 1], size=(8, 20), p=[0.7, 0.3])
                st.table(msg_data)
                
                if st.button("💾 REGISTRAR EN ARCHIVO HISTÓRICO"):
                    st.session_state.historial.append({
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Objetivo": target,
                        "Tipo": k_scale,
                        "Calidad": f"{calidad_real:.1f}%"
                    })
                    st.success("REGISTRO GUARDADO.")
                st.markdown('</div>', unsafe_allow_html=True)

start_master_scan()

if st.session_state.historial:
    st.write("---")
    st.subheader("📂 LOGS DE CONTACTO - NEXUS-7")
    st.dataframe(pd.DataFrame(st.session_state.historial), use_container_width=True)

st.caption("NEXUS-7 v9.5 MASTER | AI Intelligence & SETI Protocols | 2026")
