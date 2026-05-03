import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

st.set_page_config(page_title="Alien Hunter IA", page_icon="📡", layout="wide")

# Estilo personalizado
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #2e7bcf; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Detector de Tecnofirmas IA v2.0")

# --- Barra Lateral ---
st.sidebar.header("🕹️ Control de Misión")
objetivos = {
    "Próxima Centauri b": "4.2 años luz",
    "Estrella de Tabby": "1,470 años luz",
    "TRAPPIST-1e": "40 años luz",
    "Kepler-186f": "582 años luz",
    "Centro Galáctico (Sagitario A*)": "26,000 años luz"
}
target = st.sidebar.selectbox("Objetivo de Escaneo", list(objetivos.keys()))
sensibilidad = st.sidebar.slider("Sensibilidad del Sensor", 10, 100, 45)

st.sidebar.info(f"**Destino:** {target}\n\n**Distancia:** {objetivos[target]}")

# --- Espacio de Trabajo ---
st.write(f"### 🔭 Apuntando Antenas hacia: **{target}**")
grafico_placeholder = st.empty()
status_placeholder = st.empty()

if st.button("🚀 INICIAR ESCANEO EN TIEMPO REAL"):
    t_steps = 60  # Segundos de escaneo
    f_chans = 500
    
    # Creamos una matriz vacía que iremos rellenando
    display_data = np.zeros((t_steps, f_chans))
    
    # Parámetros de la señal oculta
    start_chan = random.randint(100, 400)
    drift = random.uniform(-0.8, 0.8)
    
    for t in range(t_steps):
        # 1. Generar ruido de fondo para esta línea
        linea_ruido = np.random.exponential(scale=1.0, size=f_chans)
        
        # 2. Inyectar señal (Tecnofirma)
        center = int(start_chan + t * drift)
        lanes = np.arange(f_chans)
        señal = (sensibilidad / 10) * np.exp(-((lanes - center)**2) / (2 * 2**2))
        
        # 3. Actualizar matriz de datos
        display_data[t] = linea_ruido + señal
        
        # 4. Dibujar dinámicamente
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(display_data, aspect='auto', cmap='magma', origin='lower')
        ax.set_title(f"DATOS EN VIVO: {target}")
        ax.set_xlabel("Frecuencia (MHz)")
        ax.set_ylabel("Tiempo de Integración (s)")
        
        grafico_placeholder.pyplot(fig)
        plt.close(fig) # Limpiar memoria
        
        status_placeholder.text(f"🛰️ Recibiendo paquetes de datos... Segundo {t+1}/60")
        time.sleep(0.05) # Velocidad del escaneo

    # --- ANALIZADOR DE IA AL FINAL ---
    st.divider()
    st.subheader("🧠 Análisis de Inteligencia Artificial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prob = random.randint(75, 99) if sensibilidad > 30 else random.randint(20, 50)
        st.metric("Probabilidad de Origen Artificial", f"{prob}%")
        st.progress(prob / 100)

    with col2:
        if prob > 70:
            st.success("✅ VEREDICTO: TECNOFIRMA DETECTADA")
            st.write("**Tipo de Señal:** Banda estrecha con deriva Doppler coherente.")
            st.write("**Clasificación:** Posible civilización Kardashev Tipo I.")
        else:
            st.warning("⚠️ VEREDICTO: RUIDO CÓSMICO")
            st.write("La señal no presenta patrones de modulación inteligente claros.")

    st.balloons()
