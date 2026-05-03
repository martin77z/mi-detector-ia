import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from datetime import datetime

# CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="NEXUS-7 PRO", page_icon="📡", layout="wide")

# Inicializar Base de Datos en la sesión (Punto B)
if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO "NASA DARK MODE"
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 20px #00FF41; }
    .stMetric { border: 1px solid #111; background-color: #0a0a0a; padding: 10px; border-radius: 5px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("📟 NEXUS-7: DEEP SPACE ANALYZER v3.0")
st.write("---")

# --- BARRA LATERAL ---
st.sidebar.header("🕹️ CONTROL DE MISIÓN")
objetivo = st.sidebar.selectbox("Fijar Objetivo", ["Próxima b", "Kepler-186f", "TRAPPIST-1e", "Estrella de Tabby", "Sagitario A*"])
potencia = st.sidebar.slider("Potencia de Antena (dB)", 20, 100, 85)

# --- PANEL PRINCIPAL ---
col_radar, col_telemetria = st.columns([2, 1])

with col_radar:
    st.subheader(f"📡 SECTOR: {objetivo.upper()}")
    pantalla = st.empty()
    progreso = st.empty()

with col_telemetria:
    st.subheader("📊 DATOS EN VIVO")
    consola = st.empty()
    stats = st.empty()

# Lógica del Escaneo
if st.button("EJECUTAR ESCANEO TÁCTICO"):
    filas, columnas = 60, 400
    matriz = np.zeros((filas, columnas))
    pos_señal = random.randint(100, 300)
    deriva = random.uniform(-0.4, 0.4)

    for t in range(filas):
        ruido = np.random.normal(0.5, 0.15, columnas)
        centro = int(pos_señal + t * deriva)
        if 0 <= centro < columnas:
            # Inyectar señal según potencia
            ruido[centro-2:centro+3] += (potencia / 12)
        
        matriz[t] = ruido
        
        # Renderizado de Radar
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='black')
        ax.imshow(matriz, aspect='auto', cmap='magma', origin='lower')
        ax.axis('off')
        pantalla.pyplot(fig)
        plt.close(fig)
        
        progreso.progress((t+1)/filas)
        consola.code(f"SYNC_OK..{random.random()}\nFREQ_LOCK: {centro}MHz\nGAIN: +{potencia}dB")
        time.sleep(0.04)

    # --- RESULTADOS ---
    score = random.randint(88, 99) if potencia > 70 else random.randint(10, 45)
    
    st.write("---")
    res1, res2, res3 = st.columns(3)
    res1.metric("CONFIDENCIALIDAD IA", f"{score}%")
    res2.metric("TIPO DE SEÑAL", "BANDA ESTRECHA" if score > 70 else "RUIDO TÉRMICO")
    
    # PUNTO A: DECODIFICADOR DE MENSAJES
    if score > 90:
        st.warning("⚠️ ¡SEÑAL DE ALTA INTENSIDAD DETECTADA! INICIANDO DECODIFICACIÓN...")
        mensajes_alien = [
            "2-3-5-7-11-13-17-19-23 (SEC. PRIMOS)",
            "01001000 01001111 01001100 01000001",
            "COORDINADAS: 14.242n, 10.121e",
            "PATRÓN MATEMÁTICO: FIBONACCI DETECTADO",
            "ALERTA: SEÑAL DE ORIGEN ARTIFICIAL CONFIRMADA"
        ]
        with st.expander("🔓 VER MENSAJE DECODIFICADO"):
            st.code(random.choice(mensajes_alien))
    
    # PUNTO B: REGISTRO DE HALLAZGOS
    nuevo_hallazgo = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Objetivo": objetivo,
        "Probabilidad": f"{score}%",
        "Veredicto": "EXITOSO" if score > 70 else "FALLIDO"
    }
    
    if st.button("💾 GUARDAR EN BASE DE DATOS"):
        st.session_state['historial'].append(nuevo_hallazgo)
        st.success("Registro guardado en el Archivo Nexus-7.")

# --- SECCIÓN DE HISTORIAL (Punto B) ---
if st.session_state['historial']:
    st.write("---")
    st.subheader("📂 ARCHIVO HISTÓRICO DE HALLAZGOS")
    st.table(st.session_state['historial'])
    if st.button("🗑️ LIMPIAR REGISTROS"):
        st.session_state['historial'] = []
        st.rerun()
