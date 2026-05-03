import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Alien Hunter IA", page_icon="👽")

st.title("📡 Detector de Tecnofirmas IA")

# --- NUEVO: Selector de Objetivos Reales ---
objetivos = {
    "Próxima Centauri b": "4.2 años luz",
    "Estrella de Tabby (KIC 8462852)": "1,470 años luz",
    "TRAPPIST-1e": "40 años luz",
    "Kepler-186f": "582 años luz",
    "Centro Galáctico (Sagitario A*)": "26,000 años luz"
}

target = st.sidebar.selectbox("Seleccionar Objetivo", list(objetivos.keys()))
distancia = objetivos[target]

st.sidebar.write(f"**Distancia:** {distancia}")
st.write(f"### Escaneando actualmente: **{target}**")
# ------------------------------------------

sensibilidad = st.sidebar.slider("Potencia de la Señal (SNR)", 1, 100, 25)

if st.button("Iniciar Escaneo"):
    with st.spinner(f"Sincronizando con el radiotelescopio hacia {target}..."):
        t_steps = 64
        f_chans = 1024
        data = np.random.exponential(scale=1.0, size=(t_steps, f_chans))
        
        # Simulamos la señal
        start_chan = random.randint(200, 800)
        drift_rate = random.uniform(-1.0, 1.0) # Deriva Doppler variable
        
        for i in range(t_steps):
            center = int(start_chan + i * drift_rate)
            lanes = np.arange(f_chans)
            data[i] += (sensibilidad / 5) * np.exp(-((lanes - center)**2) / (2 * 3**2))

        fig, ax = plt.subplots(figsize=(10, 6))
        img = ax.imshow(data, aspect='auto', cmap='magma', origin='lower')
        plt.colorbar(img, label='Intensidad de Radio')
        ax.set_title(f"Espectrograma: Datos de {target}")
        ax.set_xlabel("Frecuencia (Canales)")
        ax.set_ylabel("Tiempo (Pasos)")
        
        st.pyplot(fig)
        st.success(f"✅ ¡Detección en {target} confirmada!")
