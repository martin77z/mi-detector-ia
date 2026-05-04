import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS-7 DEEP SPACE ANALYZER v8.0", page_icon="📡", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# --- ESTILO VISUAL CRT / CYBERPUNK ---
st.markdown("""
    <style>
    .stApp { background-color: #010a01; color: #00FF41; font-family: 'Courier New', monospace; }
    .stSelectbox, .stSlider, .stSlider [data-baseweb="slider"] { background-color: #051505; border-radius: 5px; color: #00FF41; }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; height: 3.5em; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 30px #00FF41; }
    .status-box { background-color: rgba(0, 255, 65, 0.1); border: 1px solid #00FF41; padding: 15px; border-radius: 3px; }
    .guide-box { background-color: #001100; border-left: 5px solid #00FF41; padding: 15px; margin-bottom: 20px; }
    .alert-contact { color: #ff0000; animation: blink 0.8s infinite; font-weight: bold; font-size: 1.2em; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- GUÍA DE USUARIO (INJECTADA) ---
with st.expander("📖 MANUAL DE OPERACIONES NEXUS-7 (LEER PRIMERO)"):
    st.markdown("""
    <div class="guide-box">
    <h3>SISTEMA DE DETECCIÓN ETI v8.0</h3>
    <p>Bienvenido, Operador. Este sistema analiza señales de radio de banda estrecha en busca de tecnofirmas no humanas.</p>
    <ul>
        <li><b>Escala de Kardashov:</b> Define el nivel energético de la civilización. A mayor tipo (II o III), la señal será más estable y compleja, pero más rara de encontrar.</li>
        <li><b>Deriva Doppler (Drift):</b> Debido a la rotación planetaria, una señal alienígena real aparecerá como una <b>diagonal</b> en el espectrograma.</li>
        <li><b>RFI (Interferencia):</b> Las líneas perfectamente verticales suelen ser satélites terrestres o ruido local.</li>
        <li><b>Ganancia:</b> Ajusta la sensibilidad. Demasiada ganancia puede saturar el receptor con ruido cósmico.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE OBJETIVOS ---
info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Freq": "1420 MHz (Hidrógeno)", "Nota": "Candidato rocoso más cercano."},
    "Ross 128 b": {"Dist": 11.0, "Freq": "1665 MHz (OH)", "Nota": "Señal estable, zona templada."},
    "K2-18b": {"Dist": 124.0, "Freq": "22.2 GHz (Agua)", "Nota": "Posible mundo oceánico."},
    "Sector Wow!": {"Dist": 1800.0, "Freq": "1420 MHz", "Nota": "Origen de la señal de 1977."},
}

st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v8.0")

# --- PANEL DE CONTROL ---
with st.container():
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        objetivo = st.selectbox("🎯 DESTINO GALÁCTICO", list(info_objetivos.keys()))
        k_scale = st.select_slider("🌌 ESCALA DE KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
    with c2:
        ganancia = st.slider("📶 SENSIBILIDAD (dB)", 150, 400, 250)
        audio_on = st.checkbox("🔊 MONITOR DE AUDIO", value=True)
    with c3:
        data = info_objetivos[objetivo]
        st.markdown(f"""
        <div class="status-box">
            <b>SISTEMA:</b> {objetivo} | <b>DISTANCIA:</b> {data['Dist']} AL<br>
            <b>FRECUENCIA:</b> {data['Freq']}<br>
            <b>LOG:</b> {data['Nota']}
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# --- MOTOR DE ESCANEO (Optimizado) ---
@st.fragment
def start_deep_scan():
    col_viz, col_data = st.columns([3, 1])
    v_cascada = col_viz.empty()
    v_potencia = col_viz.empty()
    v_stats = col_data.empty()
    v_alert = col_data.empty()

    if st.button("🚀 INICIAR ESCANEO DE BANDA ESTRECHA"):
        pasos = 80
        matriz = np.random.normal(0.5, 0.1, (pasos, 400))
        pos_x = random.randint(150, 250)
        
        # Lógica de probabilidad
        prob_map = {"Tipo I": 0.8, "Tipo II": 0.6, "Tipo III": 0.3}
        es_alien = random.random() > prob_map[k_scale]
        
        # Drift Doppler: Inclinación diagonal para aliens, vertical para RFI
        drift_rate = random.uniform(-0.4, 0.4) if es_alien else 0.0 
        
        for t in range(pasos):
            centro = int(pos_x + t * drift_rate)
            if 0 <= centro < 400:
                intensidad = (ganancia / 5) + random.uniform(0, 10)
                matriz[t, centro] = intensidad
                # Armónico secundario (Referencia visual imagen 6aab3a16)
                if es_alien and centro + 20 < 400:
                    matriz[t, centro + 20] = intensidad * 0.6

            # Renderizado Waterfall
            fig1, ax1 = plt.subplots(figsize=(12, 4), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='magma', origin='lower')
            ax1.axis('off')
            v_cascada.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # Renderizado Power Spectrum
            ruido_linea = matriz[t]
            fig2, ax2 = plt.subplots(figsize=(12, 1.5), facecolor='black')
            ax2.plot(ruido_linea, color='#00FF41', linewidth=1)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, 100)
            ax2.axis('off')
            v_potencia.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            v_stats.markdown(f"""
            **SENSING:** {t}ms  
            **DRIFT:** {drift_rate:.4f} Hz/s  
            **STATUS:** {'SIGNAL DETECTED' if es_alien else 'NOISE'}
            """)
            time.sleep(0.01)

        # Diagnóstico
        if es_alien:
            if drift_rate != 0:
                v_alert.markdown('<p class="alert-contact">⚠️ TECNOFIRMA DETECTADA: ORIGEN NO HUMANO</p>', unsafe_allow_html=True)
                st.session_state.historial.append({"Fecha": datetime.now().strftime("%H:%M"), "Origen": objetivo, "Clase": "EXTRATERRESTRE"})
            else:
                v_alert.warning("📡 RFI: INTERFERENCIA DE SATÉLITE TERRESTRE")
        else:
            v_alert.info("🌌 VACÍO: SOLO RUIDO TÉRMICO")

start_deep_scan()

# --- HISTORIAL ---
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 ARCHIVO DE SEÑALES CONFIRMADAS")
    st.table(pd.DataFrame(st.session_state.historial))
