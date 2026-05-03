import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN NEXUS-7
st.set_page_config(page_title="NEXUS-7 CONTACT", page_icon="👽", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO VISUAL MEJORADO (CON BOTÓN DE MENÚ SIEMPRE VISIBLE)
st.markdown("""
    <style>
    .stApp { background-color: #020502; color: #00FF41; font-family: 'Courier New', monospace; }
    
    /* Forzar visibilidad del botón para abrir el Sidebar */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #00FF41 !important;
        color: #000 !important;
        border-radius: 5px;
        left: 10px;
        top: 10px;
    }

    .stButton>button { 
        border: 2px solid #00FF41; 
        background-color: #000; 
        color: #00FF41; 
        font-weight: bold; 
        width: 100%; 
        height: 3.5em; 
    }
    .stButton>button:hover { 
        background-color: #00FF41; 
        color: #000; 
        box-shadow: 0 0 30px #00FF41; 
    }
    .info-card { 
        background-color: #0a1a0a; 
        border: 1px solid #1a3a1a; 
        padding: 15px; 
        border-radius: 5px; 
        margin-bottom: 10px; 
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Tipo": "Rocoso", "Nota": "Señal corta, mucha deriva Doppler."},
    "Ross 128 b": {"Dist": 11.0, "Tipo": "Habitable", "Nota": "Estrella enana roja muy estable."},
    "TRAPPIST-1e": {"Dist": 40.0, "Tipo": "Rocoso", "Nota": "Posible red de comunicaciones entre planetas."},
    "K2-18b": {"Dist": 124.0, "Tipo": "Hicéano", "Nota": "Mundo oceánico. Señal muy clara."},
    "Estrella de Tabby": {"Dist": 1470.0, "Tipo": "Anómala", "Nota": "¿Megaestructura detectada?"},
    "Sector Wow!": {"Dist": 1800.0, "Tipo": "Histórico", "Nota": "Alta probabilidad de re-detección."},
    "Sagitario A*": {"Dist": 26000.0, "Tipo": "Agujero Negro", "Nota": "Mucho ruido de fondo, difícil filtrar."},
    "Cúmulo M13": {"Dist": 25000.0, "Tipo": "Cúmulo Estelar", "Nota": "300.000 estrellas emitiendo."}
}

st.title("📡 NEXUS-7: FIRST CONTACT v5.7.2")

# --- SIDEBAR ---
st.sidebar.title("🎛️ PANEL DE CONTROL")
objetivo = st.sidebar.selectbox("Seleccionar Objetivo", list(info_objetivos.keys()))
ganancia = st.sidebar.slider("Ganancia de Antena (dB)", 80, 200, 140)

data = info_objetivos[objetivo]
st.sidebar.markdown(f"""
<div class="info-card">
    <p><b>INFO DE SECTOR:</b></p>
    <p>🔭 {data['Tipo']}</p>
    <p>📏 {data['Dist']} Años Luz</p>
    <p>📝 {data['Nota']}</p>
</div>
""", unsafe_allow_html=True)

# --- ESPACIO DE TRABAJO ---
col_radar, col_log = st.columns([2, 1])

with col_radar:
    v_cascada = st.empty()
    v_potencia = st.empty() 

with col_log:
    st.subheader("📟 STATUS LOG")
    v_terminal = st.empty()
    v_resultado = st.empty()

if st.button("🚀 INICIAR ESCANEO DE BANDA ESTRECHA"):
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    
    # PROBABILIDAD DE ÉXITO (60%)
    es_alien = random.random() > 0.4 
    
    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.08)
        
        if 0 <= centro < 400:
            if es_alien:
                # SEÑAL ALIEN: Banda Estrecha Pura
                intensidad = ganancia / 6
                ruido[centro] += intensidad
            else:
                # INTERFERENCIA: Banda Ancha
                intensidad = ganancia / 12
                ruido[centro-6:centro+7] += intensidad
            
        matriz[t] = ruido
        
        # 1. Render Cascada
        fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        # 2. Render Potencia (Fijado para evitar errores)
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 50) 
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        
        v_terminal.code(f"MUESTRA: {t}/{pasos}\nSNR: {np.max(ruido):.1f}\nANALIZANDO...")
        time.sleep(0.01)

    # RESULTADO FINAL
    if es_alien:
        v_resultado.success("🎯 ¡TECNOSÍGNAL DETECTADA!")
        v_resultado.write(f"Coherencia artificial confirmada en {objetivo}.")
        if st.button("💾 GUARDAR CONTACTO"):
            st.session_state.historial.append({"Fecha": datetime.now().strftime("%H:%M"), "Lugar": objetivo, "Tipo": "INTELIGENTE"})
            st.rerun()
    else:
        v_resultado.error("❌ INTERFERENCIA DETECTADA")
        v_resultado.write("Señal demasiado ancha. Clasificada como RFI.")

# HISTORIAL
if st.session_state.historial:
    st.divider()
    st.subheader("📂 ARCHIVO FIRST CONTACT")
    st.table(st.session_state.historial)
