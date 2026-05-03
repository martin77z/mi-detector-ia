import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN NEXUS-7 ULTIMATE v7.1
st.set_page_config(page_title="NEXUS-7 ULTIMATE v7.1", page_icon="📡", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #010a01; color: #00FF41; font-family: 'Courier New', monospace; }
    .stSelectbox, .stSlider { background-color: #051505; border-radius: 5px; padding: 10px; border: 1px solid #00FF41; }
    .stButton>button { 
        border: 2px solid #00FF41; background-color: #000; color: #00FF41; 
        font-weight: bold; height: 3.5em; width: 100%; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 50px #00FF41; }
    .detail-card { background-color: #051505; border: 1px solid #00FF41; padding: 20px; border-radius: 5px; }
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Tipo": "Rocoso", "Nota": "Candidato cercano."},
    "Ross 128 b": {"Dist": 11.0, "Tipo": "Templado", "Nota": "Estrella estable."},
    "K2-18b": {"Dist": 124.0, "Tipo": "Hicéano", "Nota": "Vapor de agua detectado."},
    "Sector Wow!": {"Dist": 1800.0, "Tipo": "Histórico", "Nota": "Señal de 1977."},
    "Andrómeda": {"Dist": 2500000.0, "Tipo": "Galaxia", "Nota": "Búsqueda Extragaláctica."}
}

st.title("📡 NEXUS-7: ULTIMATE CONTACT v7.1")

# --- PANEL DE CONTROL (Nuevos parámetros) ---
c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    objetivo = st.selectbox("🎯 DESTINO GALÁCTICO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 ESCALA DE KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])
with c2:
    # AÑADIDO: Potencia de Antena
    potencia_mw = st.slider("⚡ POTENCIA DE ANTENA (MW)", 10, 1000, 500)
    ganancia = st.slider("📶 GANANCIA SENSORIAL (dB)", 150, 400, 250)
with c3:
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <b>SISTEMA:</b> {objetivo} | <b>CIVILIZACIÓN:</b> {k_scale}<br>
        <b>DISTANCIA BASE:</b> {data['Dist']:,} AL<br>
        <b>POTENCIA EMISIÓN:</b> {potencia_mw} Megavatios<br>
        <b>ESTADO:</b> ANTENA ALINEADA AL 98.4%
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col_main, col_decoder = st.columns([2, 1])
with col_main:
    v_cascada = st.empty()
    v_potencia = st.empty()
with col_decoder:
    st.subheader("📟 TELEMETRÍA DE CAMPO")
    v_dist_live = st.empty()
    v_terminal = st.empty()
    v_alerta = st.empty()

if st.button("🚀 INICIAR ESCANEO PROFUNDO"):
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    
    prob_map = {"Tipo I": 0.7, "Tipo II": 0.5, "Tipo III": 0.3}
    es_alien = random.random() > prob_map[k_scale]
    
    distancia_base = info_objetivos[objetivo]["Dist"]

    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.05)
        
        # AÑADIDO: Lógica de potencia vs distancia
        # A más potencia de antena, el pico de señal es más limpio
        factor_potencia = potencia_mw / 100
        
        if 0 <= centro < 400:
            if es_alien:
                pico = (ganancia / 5) * factor_potencia
                ruido[centro] += pico
            else:
                ruido[centro-5:centro+6] += (ganancia / 20)
            
        matriz[t] = ruido
        
        # Simulación de distancia variando por el movimiento orbital
        dist_variacion = distancia_base + (np.sin(t/10) * (distancia_base * 0.001))
        
        # Visualización
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        v_dist_live.metric("DISTANCIA ACTUAL (AL)", f"{dist_variacion:,.4f}")
        v_terminal.code(f"📡 POTENCIA ANTENA: {potencia_mw} MW\n📈 SNR: {np.max(ruido)/1.5:.2f} dB\n🛰️ RASTREO: {t}%")
        time.sleep(0.01)

    if es_alien:
        v_alerta.success(f"¡CONTACTO EN {objetivo.upper()}!")
        st.session_state.historial.append({
            "Fecha": datetime.now().strftime("%H:%M"), 
            "Origen": objetivo, 
            "Distancia": f"{distancia_base} AL",
            "Potencia": f"{potencia_mw} MW"
        })
    else:
        v_alerta.error("SCAN COMPLETO: Sin señales inteligentes.")

# BITÁCORA ACTUALIZADA
if st.session_state.historial:
    st.divider()
    st.subheader("📂 LOG DE CIVILIZACIONES (v7.1)")
    st.table(pd.DataFrame(st.session_state.historial))
