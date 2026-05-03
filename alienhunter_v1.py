import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN PRO
st.set_page_config(page_title="NEXUS-7 EXPLORER", page_icon="🔭", layout="wide")

# Inicializar sesión
if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO "DEEP SPACE" MEJORADO
st.markdown("""
    <style>
    .stApp { background-color: #020202; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; border-radius: 0px; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 30px #00FF41; }
    .data-card { background-color: #0a0a0a; border: 1px solid #1a1a1a; padding: 20px; border-radius: 5px; margin-bottom: 10px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# BASE DE DATOS DE OBJETIVOS REALES
info_objetivos = {
    "Próxima b": {"Distancia": "4.24 AL", "Estrella": "Enana Roja (M)", "Coordenadas": "14h 29m / -62°"},
    "Kepler-186f": {"Distancia": "582 AL", "Estrella": "Enana K", "Coordenadas": "19h 54m / +43°"},
    "TRAPPIST-1e": {"Distancia": "40.7 AL", "Estrella": "Enana ultrafría", "Coordenadas": "23h 06m / -05°"},
    "Estrella de Tabby": {"Distancia": "1,470 AL", "Estrella": "Tipo F", "Coordenadas": "20h 06m / +44°"},
    "Sagitario A*": {"Distancia": "26,670 AL", "Estrella": "Agujero Negro Supermasivo", "Coordenadas": "17h 45m / -29°"}
}

st.title("📟 NEXUS-7: EXPLORER EDITION v4.0")
st.write("---")

# --- BARRA LATERAL (CONTROL DE MISIÓN) ---
st.sidebar.title("🎮 MÓDULO DE CONTROL")
target = st.sidebar.selectbox("Fijar Objetivo Galáctico", list(info_objetivos.keys()))
sensibilidad = st.sidebar.select_slider("Sensibilidad de Recepción", options=["BAJA", "MEDIA", "ALTA", "MÁXIMA"], value="ALTA")
potencia_map = {"BAJA": 40, "MEDIA": 60, "ALTA": 85, "MÁXIMA": 110}

# Mostrar Info del Objetivo en la Sidebar
st.sidebar.markdown(f"""
<div class="data-card">
    <p><b>INFO DE SECTOR:</b></p>
    <p>Distancia: {info_objetivos[target]['Distancia']}</p>
    <p>Estrella: {info_objetivos[target]['Estrella']}</p>
    <p>Coord: {info_objetivos[target]['Coordenadas']}</p>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL ---
col_radar, col_analisis = st.columns([2, 1])

with col_radar:
    st.subheader(f"📡 RADAR DE CASCADA: {target}")
    radar_plot = st.empty()
    st.subheader("📉 ESPECTRO DE POTENCIA (Power Spectrum)")
    power_plot = st.empty()

with col_analisis:
    st.subheader("📟 TELEMETRÍA")
    consola = st.empty()
    alertas = st.empty()

# LÓGICA DE ESCANEO
if st.button("🚀 INICIAR ESCANEO DE ESPACIO PROFUNDO"):
    filas, columnas = 70, 500
    matriz = np.zeros((filas, columnas))
    pos_señal = random.randint(150, 350)
    deriva = random.uniform(-0.6, 0.6)
    
    for t in range(filas):
        # Ruido y Señal
        ruido = np.random.normal(0.5, 0.2, columnas)
        centro = int(pos_señal + t * deriva)
        if 0 <= centro < columnas:
            p_val = potencia_map[sensibilidad]
            ruido[centro-2:centro+3] += (p_val / 10)
        
        matriz[t] = ruido
        
        # 1. Gráfico de Radar (Cascada)
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma', origin='lower')
        ax1.axis('off')
        radar_plot.pyplot(fig1)
        plt.close(fig1)
        
        # 2. Gráfico de Potencia (Línea)
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 15)
        ax2.axis('off')
        power_plot.pyplot(fig2)
        plt.close(fig2)
        
        # Consola
        consola.code(f"SCANNING_{target.upper()}...\nFREQ_LOCKED: {centro}MHz\nNOISE_FLOOR: -110dBm\nSIG_STRENGTH: {np.max(ruido):.2f}")
        time.sleep(0.03)

    # RESULTADOS DE IA
    score = random.randint(85, 99) if potencia_map[sensibilidad] > 50 else random.randint(10, 40)
    
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("PROBABILIDAD IA", f"{score}%")
    c2.metric("ORIGEN", "ARTIFICIAL" if score > 75 else "ESTELAR")
    
    if score > 75:
        st.success(f"💥 ¡TECNOSÍGNAL CONFIRMADA EN {target}!")
        with st.expander("🔓 DESBLOQUEAR MENSAJE DECODIFICADO"):
            msg = random.choice(["SEC_PRIMOS_DETECTADA", "PATRON_MATEMATICO_PI", "BINARIO_REPETITIVO", "MAPA_ESTELAR_EXTERNO"])
            st.code(f"DECODE_RESULT: {msg}")
            
        # BOTÓN GUARDAR
        if st.button("📥 REGISTRAR EN EL ARCHIVO"):
            hallazgo = {"Fecha": datetime.now().strftime("%H:%M"), "Sector": target, "Prob": f"{score}%", "Info": info_objetivos[target]['Estrella']}
            st.session_state.historial.append(hallazgo)
            st.toast("Hallazgo guardado correctamente.")

# --- HISTORIAL Y EXPORTACIÓN (Punto B mejorado) ---
if st.session_state.historial:
    st.divider()
    st.subheader("📂 REGISTRO DE HALLAZGOS NEXUS-7")
    df = pd.DataFrame(st.session_state.historial)
    st.table(df)
    
    # Botón para descargar los datos (Punto Profesional)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 DESCARGAR REGISTRO (CSV)", csv, "nexus7_logs.csv", "text/csv")
    
    if st.button("🗑️ RESETEAR ARCHIVO"):
        st.session_state.historial = []
        st.rerun()
