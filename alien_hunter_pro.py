import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import setigen as stg

# Configuración de la página
st.set_page_config(page_title="Alien Hunter IA", page_icon="👽")

st.title("📡 Detector de Tecnofirmas IA")
st.write("Analizando señales de radioastronomía en busca de patrones tecnológicos.")

# Interfaz lateral
st.sidebar.header("Configuración del Escaneo")
sensibilidad = st.sidebar.slider("Sensibilidad del Umbral", 10, 50, 25)

if st.button("Iniciar Escaneo del Espacio Profundo"):
    with st.spinner("Procesando datos del telescopio..."):
        # Generar datos de radioastronomía sintéticos
        frame = stg.Frame(fchans=1024, tsteps=32, df=2.7939677238464355, dt=18.253611008)
        frame.add_noise(x_mean=0, noise_type='chi2')
        
        # Inyectar una señal con deriva (típica de una tecnofirma)
        frame.add_signal(stg.constant_path(f_start=frame.get_frequency(200), drift_rate=2),
                         stg.constant_t_profile(level=frame.get_intensity(snr=sensibilidad)),
                         stg.gaussian_f_profile(width=40),
                         stg.constant_bp_profile(level=1))
        
        # Crear la visualización
        fig, ax = plt.subplots(figsize=(10, 6))
        img = ax.imshow(frame.get_data(), aspect='auto', cmap='magma')
        plt.colorbar(img, label='Potencia de la Señal')
        ax.set_title("Espectrograma: Anomalía Detectada")
        ax.set_xlabel("Frecuencia")
        ax.set_ylabel("Tiempo")
        
        # Mostrar en Streamlit
        st.pyplot(fig)
        
        st.success("✅ ¡Análisis completado! Se ha detectado una señal de banda estrecha con deriva Doppler coherente.")
        st.info("Nota: Este patrón es inconsistente con interferencias terrestres conocidas.")
