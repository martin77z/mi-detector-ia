import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS-7 DEEP SPACE ANALYZER v8.5", page_icon="📡", layout="wide")

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

# --- GUÍA DE USUARIO ---
with st.expander("📖 MANUAL DE OPERACIONES NEXUS-7 (LEER PRIMERO)"):
    st.markdown("""
    <div class="guide-box">
    <h3>SISTEMA DE DETECCIÓN ETI v8.5</h3>
    <p>Bienvenido, Operador. El catálogo de objetivos ha sido actualizado con las últimas coordenadas de exoplanetas confirmados.</p>
    <ul>
        <li><b>Escala de Kardashov:</b> Ajusta el umbral de energía. Las civilizaciones Tipo III son detectables incluso a distancias extragalácticas.</li>
        <li><b>Deriva Doppler:</b> Si la señal es una diagonal clara, el origen está en un cuerpo en rotación (Exoplaneta).</li>
        <li><b>Señales Gemelas:</b> Las civilizaciones avanzadas suelen emitir armónicos paralelos para asegurar la integridad de los datos.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS AMPLIADA (CATÁLOGO GALÁCTICO) ---
info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Freq": "1420 MHz", "Nota": "Zona habitable, estrella Enana Roja."},
    "Ross 128 b": {"Dist": 11.0, "Freq": "1665 MHz", "Nota": "Entorno estelar muy tranquilo, alta probabilidad."},
    "TRAPPIST-1e": {"Dist": 39.5, "Freq": "1.42 GHz", "Nota": "Mundo oceánico en sistema de 7 planetas."},
    "Kepler-186f": {"Dist": 582.0, "Freq": "4.5 GHz", "Nota": "Primer planeta de tamaño terrestre en zona habitable."},
    "K2-18b": {"Dist": 124.0, "Freq": "22.2 GHz", "Nota": "Presencia confirmada de vapor de agua en atmósfera."},
    "Sector Wow!": {"Dist": 1800.0, "Freq": "1420 MHz", "Nota": "Coordenadas de la señal detectada en 1977."},
    "Cúmulo de Hércules (M13)": {"Dist": 25000.0, "Freq": "2.38 GHz", "Nota": "Destino del mensaje enviado desde Arecibo en 1974."},
    "Tabby's Star": {"Dist": 1470.0, "Freq": "Banda Ancha", "Nota": "Anomalías en tránsito, posible megaestructura."},
    "Andrómeda (M31)": {"Dist": 2.5e6, "Freq": "Varias", "Nota": "Escaneo extragaláctico para civilizaciones Tipo III."},
    "Gliese 667 Cc": {"Dist": 23.6, "Freq": "1.6 GHz", "Nota": "Super-Tierra en sistema estelar triple."},
    "Gliese 581g": {"Dist": 20.4, "Freq": "1420 MHz", "Nota": "Candidato polémico pero de alto interés científico."}
}

st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v8.5")

# --- PANEL DE CONTROL ---
with st.container():
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        objetivo = st.selectbox("🎯 SELECCIONAR OBJETIVO", list(info_objetivos.keys()))
        k_scale = st.select_slider("🌌 ESCALA DE KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
    with c2:
        ganancia = st.slider("📶 SENSIBILIDAD RECEPTOR (dB)", 150, 450, 300)
        audio_on = st.checkbox("🔊 MONITOR DE AUDIO (ON)", value=True)
    with c3:
        data = info_objetivos[objetivo]
        st.markdown(f"""
        <div class="status-box">
            <b>OBJETIVO:</b> {objetivo} | <b>DISTANCIA:</b> {data['Dist']} AL<br>
            <b>FRECUENCIA NOMINAL:</b> {data['Freq']}<br>
            <b>NOTAS DE CAMPO:</b> {data['Nota']}
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# --- MOTOR DE ESCANEO ---
@st.fragment
def start_deep_scan():
    col_viz, col_data = st.columns([3, 1])
    v_cascada = col_viz.empty()
    v_potencia = col_viz.empty()
    v_stats = col_data.empty()
    v_alert = col_data.empty()

    if st.button("🚀 INICIAR ESCANEO DE BANDA ESTRECHA"):
        pasos = 85
        matriz = np.random.normal(0.5, 0.12, (pasos, 400))
        pos_x = random.randint(100, 300)
        
        # Ajuste de probabilidad por Kardashov
        # Tipo III es casi seguro encontrar algo debido a su inmenso poder de emisión
        prob_map = {"Tipo I": 0.85, "Tipo II": 0.65, "Tipo III": 0.35}
        es_alien = random.random() > prob_map[k_scale]
        
        # Drift Doppler: Inclinación para aliens, vertical para RFI
        drift_rate = random.uniform(-0.45, 0.45) if es_alien else 0.0 
        
        for t in range(pasos):
            centro = int(pos_x + t * drift_rate)
            if 0 <= centro < 400:
                intensidad = (ganancia / 5) + random.uniform(0, 15)
                matriz[t, centro] = intensidad
                
                # Efecto de Señal Gemela (Referencia visual imagen 6aab3a16-e6ac-4743-b15c-7dfc9d4998bf)
                if es_alien and centro + 25 < 400:
                    matriz[t, centro + 25] = intensidad * 0.55

            # Waterfall Display
            fig1, ax1 = plt.subplots(figsize=(12, 4), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
            ax1.axis('off')
            v_cascada.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # Power Line Display
            ruido_linea = matriz[t]
            fig2, ax2 = plt.subplots(figsize=(12, 1.5), facecolor='black')
            ax2.plot(ruido_linea, color='#00FF41' if not es_alien else '#FF3333', linewidth=1)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, 110)
            ax2.axis('off')
            v_potencia.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            v_stats.markdown(f"""
            **SENSING:** {t}ms  
            **DRIFT:** {drift_rate:.5f} Hz/s  
            **POWER:** {np.max(ruido_linea):.2f} dB  
            **ANALYSIS:** {'SIGNAL LOCK' if es_alien else 'SCANNING...'}
            """)
            time.sleep(0.01)

        # Informe de Resultados
        if es_alien:
            if drift_rate != 0:
                v_alert.markdown('<p class="alert-contact">⚠️ TECNOFIRMA CONFIRMADA: ORIGEN NO HUMANO</p>', unsafe_allow_html=True)
                st.session_state.historial.append({"Fecha": datetime.now().strftime("%H:%M:%S"), "Origen": objetivo, "Clase": "EXTRATERRESTRE", "K-Type": k_scale})
            else:
                v_alert.warning("📡 RFI DETECTADA: INTERFERENCIA LOCAL DE SATÉLITE")
        else:
            v_alert.info("🌌 VACÍO CÓSMICO: NO SE DETECTAN PATRONES ARTIFICIALES")

start_deep_scan()

# --- ARCHIVO DE HISTORIAL ---
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 ARCHIVO DE SEÑALES CONFIRMADAS")
    df_hist = pd.DataFrame(st.session_state.historial)
    st.table(df_hist)
