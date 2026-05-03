import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE LA ACADEMIA NEXUS
st.set_page_config(page_title="NEXUS-7 ACADEMY", page_icon="🎓", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO VISUAL "RADAR MILITAR" CON EXPLICACIONES
st.markdown("""
    <style>
    .stApp { background-color: #030603; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; border-radius: 0px; height: 3.5em; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41; color: #000; box-shadow: 0 0 40px #00FF41; }
    .data-card { background-color: #091309; border: 1px solid #1a3a1a; padding: 20px; border-radius: 5px; margin-bottom: 10px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#030603, #000); }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# BASE DE DATOS AMPLIADA (V5.5)
info_objetivos = {
    "Próxima b": {"Dist": 4.2, "Tipo": "Rocoso", "Nota": "El planeta más cercano, orbita una enana roja."},
    "TRAPPIST-1e": {"Dist": 40.0, "Tipo": "Rocoso", "Nota": "Sistema con 7 planetas hermanos del tamaño de la Tierra."},
    "Ross 128 b": {"Dist": 11.0, "Tipo": "Habitable", "Nota": "Señal muy silenciosa, excelente para SETI."},
    "Gliese 581g": {"Dist": 20.0, "Tipo": "Super-Tierra", "Nota": "Ubicado en el centro de la zona habitable."},
    "Estrella de Tabby": {"Dist": 1470.0, "Tipo": "Anómala", "Nota": "Cambios de brillo misteriosos (¿megaestructura alienígena?)"},
    "K2-18b": {"Dist": 124.0, "Tipo": "Hicéano", "Nota": "Vapor de agua detectado en la atmósfera por el JWST."},
    "Cúmulo de Hércules M13": {"Dist": 25000.0, "Tipo": "Cúmulo Estelar", "Nota": "Enviamos el mensaje de Arecibo aquí en 1974."},
    "Sector Wow!": {"Dist": "???", "Tipo": "Histórico", "Nota": "De donde vino la señal real de SETI de 1977."},
    "Sagitario A*": {"Dist": 26000.0, "Tipo": "Agujero Negro", "Nota": "El corazón masivo de nuestra galaxia."}
}

st.title("📡 NEXUS-7: DEEP SPACE ACADEMY v5.5")
st.write("---")

# --- BARRA LATERAL ---
st.sidebar.title("🎛️ CONTROL DE MISIÓN")
target = st.sidebar.selectbox("Fijar Objetivo", list(info_objetivos.keys()))
modo_escaneo = st.sidebar.radio("Resolución de Datos", ["Táctica (Rápida)", "Científica (Profunda)"])
ganancia = st.sidebar.slider("Sensibilidad Antena (dB)", 50, 150, 100)

# Mostrar Info del Objetivo
t_data = info_objetivos[target]
st.sidebar.markdown(f"""
<div class="data-card">
    <p><b>DETALLES DEL SECTOR:</b></p>
    <p>🔭 Tipo: {t_data['Tipo']}</p>
    <p>📏 Distancia: {t_data['Dist'] if type(t_data['Dist']) == float else 'TBA'} Años Luz</p>
    <p>⏳ Retraso de señal: {t_data['Dist'] if type(t_data['Dist']) == float else 'TBA'} Años</p>
    <p>📝 {t_data['Nota']}</p>
</div>
""", unsafe_allow_html=True)

# --- PANEL EDUCATIVO INTERACTIVO (Punto A) ---
with st.expander("❓ ¿CÓMO LEER ESTOS GRÁFICOS?"):
    col_edu1, col_edu2 = st.columns(2)
    with col_edu1:
        st.write("**Gráfico Superior (Cascada/Waterfall):** Muestra cómo cambia la señal con el tiempo. El tiempo corre de arriba hacia abajo. Una línea vertical recta es una señal estable; una inclinada muestra movimiento. Los colores cálidos indican más potencia.")
    with col_edu2:
        st.write("**Gráfico Inferior (Espectro de Potencia):** Muestra la intensidad actual de la señal por frecuencia. Un bulto ancho es solo ruido del espacio. Un pico estrecho y alto es un 'puntero láser' tecnológico.")

# --- UI PRINCIPAL ---
c_radar, c_analisis = st.columns([2, 1])

with c_radar:
    st.subheader(f"📡 RADAR DE CASCADA: {target}")
    radar_v = st.empty()
    st.caption("⬆️ El tiempo corre hacia abajo, la frecuencia horizontalmente.")
    v_power = st.empty()
    st.caption("⬆️ Picos altos indican fuerte intensidad actual.")

with c_analisis:
    st.subheader("📟 STATUS LOG")
    v_consola = st.empty()
    v_veredicto = st.empty()

# LÓGICA DE ESCANEO
if st.button("🚀 INICIAR CAPTURA ESPECTRAL"):
    # Configurar según modo
    pasos = 150 if modo_escaneo == "Científica (Profunda)" else 60
    columnas = 400
    datos = np.zeros((pasos, columnas))
    es_alien = random.random() < 0.4 # 40% de éxito
    pos_x = random.randint(150, 250)
    
    for t in range(pasos):
        linea = np.random.normal(0.6, 0.2, columnas)
        centro = int(pos_x + t * 0.05) # Deriva suave
        
        if 0 <= centro < columnas:
            intensidad = ganancia / (10 if es_alien else 15)
            # Señal RFI (ancha) vs Alien (estrecha)
            ancho = 1 if es_alien else 6
            linea[centro-ancho:centro+ancho+1] += intensidad
            
        datos[t] = linea
        
        # Plot Cascada
        fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
        ax1.imshow(datos, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        radar_v.pyplot(fig1)
        plt.close(fig1)
        
        # Plot Potencia
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(linea, color='#00FF41', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 22)
        ax2.axis('off')
        v_power.pyplot(fig2)
        plt.close(fig2)
        
        v_consola.code(f"READ_BLK_{t}..OK\nVEL: 300,000km/s\nTYPE: {modo_escaneo.upper()}\nTARGET: {target.upper()}")
        time.sleep(0.01)

    # --- VEREDICTO DE IA ---
    if es_alien:
        v_veredicto.success("✅ CLASIFICACIÓN: TECNOFIRMA CONFIRMADA")
        v_veredicto.write(f"Patrón de banda estrecha detectado. El origen extra-solar es innegable. ¡NEXUS-7 ha hecho historia!")
        if st.button("💾 REGISTRAR HALLAZGO"):
            st.session_state.historial.append({"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Sector": target, "Estatus": "ÉXITO"})
            st.toast("Hallazgo guardado")
    else:
        v_veredicto.error("❌ CLASIFICACIÓN: RFI (INTERFERENCIA)")
        v_veredicto.write(f"Señal demasiado ancha. Detectada colisión con satélites o ruido estelar térmico de fondo.")

# HISTORIAL
if st.session_state.historial:
    st.write("---")
    st.subheader("📂 ARCHIVO DE HALLAZGOS CONFIRMADOS")
    st.table(st.session_state.historial)
