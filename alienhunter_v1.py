import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Configuración de página con estilo oscuro inyectado
st.set_page_config(page_title="DEEP SPACE RADAR", page_icon="📡", layout="wide")

st.markdown("""
    <style>
    /* Estética General */
    .main { background-color: #000000; }
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    
    /* Botón Táctico */
    .stButton>button {
        border: 2px solid #00FF41;
        background-color: #000000;
        color: #00FF41;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00FF41;
        color: #000000;
        box-shadow: 0 0 15px #00FF41;
    }
    
    /* Paneles */
    .stMetric { border: 1px solid #333; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("📟 NEXUS-7: DEEP SPACE ANALYZER")
st.write("---")

# --- SIDEBAR PROFESIONAL ---
st.sidebar.header("📡 CONFIGURACIÓN DEL ARRECHO")
objetivos = {
    "Próxima b": "4.2 LY",
    "KIC 8462852 (Tabby)": "1470 LY",
    "TRAPPIST-1e": "40 LY",
    "Sagittarius A*": "26k LY"
}
target = st.sidebar.selectbox("Fijar Objetivo", list(objetivos.keys()))
gain = st.sidebar.slider("Ganancia de Antena (dB)", 0, 100, 75)

st.sidebar.markdown(f"""
---
**COORDINADAS:** FIJADAS  
**ESTADO:** LISTO PARA ESCANEO  
**DISTANCIA:** {objetivos[target]}
""")

# --- PANTALLA PRINCIPAL ---
col_main, col_data = st.columns([2, 1])

with col_main:
    st.write(f"### [ SECTOR: {target.upper()} ]")
    view = st.empty()
    progress_bar = st.empty()

with col_data:
    st.write("### 📜 TELEMETRÍA")
    log = st.empty()
    stats = st.empty()

if st.button("EJECUTAR ESCANEO DE BANDA ESTRECHA"):
    t_steps = 80
    f_chans = 400
    display_data = np.zeros((t_steps, f_chans))
    
    # Parámetros de señal
    start_chan = random.randint(100, 300)
    drift = random.uniform(-0.5, 0.5)

    for t in range(t_steps):
        # Generar línea
        noise = np.random.normal(0.5, 0.2, f_chans)
        center = int(start_chan + t * drift)
        signal = (gain/10) * np.exp(-((np.arange(f_chans) - center)**2) / 4)
        
        display_data[t] = noise + signal
        
        # Renderizado Táctico
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='black')
        ax.imshow(display_data, aspect='auto', cmap='magma', origin='lower')
        ax.axis('off') # Eliminar ejes para modo "radar"
        view.pyplot(fig)
        plt.close(fig)
        
        progress_bar.progress((t + 1) / t_steps)
        log.code(f"DAT_STREAM: {random.random()}\nFREQ_LOCK: {center}MHz\nSIG_STRENGTH: {np.max(signal):.2f}")
        time.sleep(0.03)

    # --- INFORME FINAL ---
    st.write("---")
    res1, res2, res3 = st.columns(3)
    
    score = random.randint(85, 99) if gain > 50 else random.randint(10, 40)
    
    res1.metric("CONFIDENCIALIDAD", f"{score}%")
    res2.metric("TIPO", "BANDA ESTRECHA" if score > 70 else "RUIDO")
    res3.write(f"**VEREDICTO IA:** {'ALERTA DE TECNOFIRMA' if score > 70 else 'SQUELCH ACTIVO'}")
    
    if score > 70:
        st.success(f"¡Atención! Patrón detectado en {target}. La señal muestra coherencia artificial.")
        st.balloons()
