import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE LA ACADEMIA NEXUS
st.set_page_config(page_title="NEXUS-7 ACADEMY", page_icon="🎓", layout="wide")

# Inicializar historial
if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO VISUAL PROFESIONAL
st.markdown("""
    <style>
    .stApp { background-color: #020502; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; font-weight: bold; width: 100%; height: 3.5em; }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 30px #00FF41; }
    .info-card { background-color: #0a1a0a; border: 1px solid #1a3a1a; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# BASE DE DATOS GALÁCTICA EXTENDIDA
info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Tipo": "Rocoso", "Nota": "El planeta más cercano a la Tierra."},
    "Ross 128 b": {"Dist": 11.0, "Tipo": "Habitable", "Nota": "Estrella enana roja muy estable."},
    "Gliese 581g": {"Dist": 20.0, "Tipo": "Super-Tierra", "Nota": "Primer candidato a mundo habitable."},
    "TRAPPIST-1e": {"Dist": 40.0, "Tipo": "Rocoso", "Nota": "Sistema con siete planetas hermanos."},
    "K2-18b": {"Dist": 124.0, "Tipo": "Hicéano", "Nota": "Mundo con océanos y atmósfera de hidrógeno."},
    "Estrella de Tabby": {"Dist": 1470.0, "Tipo": "Anómala", "Nota": "Famosa por sus bajadas de luz inexplicables."},
    "Sector Wow!": {"Dist": 1800.0, "Tipo": "Histórico", "Nota": "Donde se captó la famosa señal en 1977."},
    "Sagitario A*": {"Dist": 26000.0, "Tipo": "Agujero Negro", "Nota": "El corazón masivo de nuestra galaxia."},
    "Cúmulo M13": {"Dist": 25000.0, "Tipo": "Cúmulo Estelar", "Nota": "300.000 estrellas. Enviamos un mensaje aquí en 1974."}
}

st.title("📡 NEXUS-7: DEEP SPACE ACADEMY v5.1")

# --- PANEL EDUCATIVO ---
with st.expander("📖 GUÍA DE INTERPRETACIÓN DE DATOS"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Gráfico Superior (Cascada):** Muestra cómo cambia la señal con el tiempo. Si la línea es recta, el objeto es estable. Si se inclina, es por el movimiento del planeta.")
    with col_b:
        st.write("**Gráfico Inferior (Potencia):** Muestra la fuerza de la señal. Un pico muy estrecho significa tecnología artificial. Un bulto ancho es solo ruido natural.")

# --- SIDEBAR DE CONTROL ---
st.sidebar.title("🎛️ PANEL DE CONTROL")
objetivo = st.sidebar.selectbox("Seleccionar Objetivo", list(info_objetivos.keys()))
modo = st.sidebar.radio("Precisión de Escaneo", ["Táctica (Rápida)", "Científica (Lenta)"])
ganancia = st.sidebar.slider("Potencia de Antena (dB)", 50, 150, 110)

# Mostrar Info del Objetivo
data = info_objetivos[objetivo]
st.sidebar.markdown(f"""
<div class="info-card">
    <p><b>DETALLES DEL SECTOR:</b></p>
    <p>🔭 Tipo: {data['Tipo']}</p>
    <p>📏 Distancia: {data['Dist']} años luz</p>
    <p>⏳ Retraso de señal: {data['Dist']} años</p>
    <p>📝 {data['Nota']}</p>
</div>
""", unsafe_allow_html=True)

# --- ESPACIO DE TRABAJO ---
col_radar, col_log = st.columns([2, 1])

with col_radar:
    v_cascada = st.empty()
    v_potencia = st.empty()

with col_log:
    st.subheader("📟 INFORME DE IA")
    v_terminal = st.empty()
    v_resultado = st.empty()

if st.button("🚀 INICIAR ESCANEO CUÁNTICO"):
    pasos = 120 if modo == "Científica (Lenta)" else 60
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    es_alien = random.random() > 0.6 # 40% de probabilidad de éxito
    
    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.05)
        
        if 0 <= centro < 400:
            intensidad = (ganancia / 10) + (2 if es_alien else 8)
            ancho = 1 if es_alien else 6
            ruido[centro-ancho:centro+ancho+1] += intensidad
            
        matriz[t] = ruido
        
        # Render Cascada
        fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        # Render Potencia
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(ruido, color='#00FF41', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 25)
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        
        v_terminal.code(f"REC_SIG: {t}/{pasos}\nVELOCIDAD: 300,000 km/s\nESTADO: ANALIZANDO FRECUENCIAS...")
        time.sleep(0.01)

    # RESULTADO FINAL
    with v_resultado:
        if es_alien:
            st.success("🎯 ¡TECNOSÍGNAL DETECTADA!")
            st.write(f"Esta señal es de 'Banda Estrecha'. Solo una civilización con transmisores de radio podría emitir algo tan preciso desde {objetivo}.")
            if st.button("💾 REGISTRAR HALLAZGO"):
                st.session_state.historial.append({"Fecha": datetime.now().strftime("%H:%M"), "Lugar": objetivo, "Tipo": "INTELIGENTE"})
        else:
            st.error("📡 INTERFERENCIA TERRESTRE")
            st.write("Señal demasiado ancha. Detectada colisión con satélites locales o ruido térmico estelar.")

# HISTORIAL
if st.session_state.historial:
    st.divider()
    st.subheader("📂 ARCHIVO HISTÓRICO")
    st.table(st.session_state.historial)
