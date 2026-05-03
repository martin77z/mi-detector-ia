import os
import subprocess
import sys

# PARCHE DE EMERGENCIA: Instala setuptools si falta pkg_resources
try:
    import pkg_resources
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
    import pkg_resources

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Importaciones de astronomía con manejo de errores
try:
    import setigen as stg
except ImportError:
    st.error("Todavía se están cargando las librerías científicas. Espera un momento y refresca la página.")
    st.stop()

st.set_page_config(page_title="Alien Hunter IA", page_icon="👽")

st.title("📡 Detector de Tecnofirmas IA")
st.write("Analizando señales de radioastronomía en busca de patrones no naturales.")

sensibilidad = st.slider("Sensibilidad del Detector", 10, 50, 25)

if st.button("Simular Escaneo de Cielo"):
    with st.spinner("Escaneando coordenadas..."):
        # Crear señal sintética
        frame = stg.Frame(fchans=1024, tsteps=32, df=2.7939677238464355, dt=18.253611008)
        frame.add_noise(x_mean=0, noise_type='chi2')
        
        # Añadir señal alienígena
        frame.add_signal(stg.constant_path(f_start=frame.get_frequency(200), drift_rate=2),
                         stg.constant_t_profile(level=frame.get_intensity(snr=sensibilidad)),
                         stg.gaussian_f_profile(width=40),
                         stg.constant_bp_profile(level=1))
        
        # Mostrar gráfico
        fig = plt.figure(figsize=(10, 6))
        plt.imshow(frame.get_data(), aspect='auto', cmap='viridis')
        plt.colorbar(label='Intensidad')
        plt.title("Espectrograma: Posible Tecnofirma Detectada")
        plt.xlabel("Frecuencia (Canales)")
        plt.ylabel("Tiempo (Pasos)")
        st.pyplot(fig)
        
        st.success("¡Patrón detectado! La señal muestra una deriva coherente compatible con origen tecnológico.")
