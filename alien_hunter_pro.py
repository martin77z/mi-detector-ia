
import streamlit as st
import numpy as np
import setigen as stg

# Configuración de la página
st.set_page_config(page_title="Alien Hunter IA", page_icon="👽")
st.title("🚀 Alien Hunter Pro v1.0")
st.markdown("Analizador de señales de radioastronomía.")

# Control de la IA
sensibilidad = st.slider("Sensibilidad de la IA (Umbral)", 1.0, 5.0, 2.0)

if st.button("Escanear Espacio"):
    # Creamos el mapa del cielo
    frame = stg.Frame(fchans=1024, tchans=32)
    frame.add_noise(x_mean=10)
    
    # Inyectamos una señal para probar
    frame.add_signal(stg.constant_path(f_start=frame.get_frequency(index=500), drift_rate=2),
                     stg.constant_t_profile(level=frame.get_intensity(snr=25)),
                     stg.gaussian_f_profile(width=40),
                     stg.constant_bp_profile(level=1))
    
    data = frame.get_data()
    
    # Lógica de detección
    if np.max(data) > (np.mean(data) * sensibilidad):
        st.error("🚨 ¡CONTACTO DETECTADO! SEÑAL INTELIGENTE ENCONTRADA")
        st.balloons()
    else:
        st.info("🔭 Escaneo completado: Solo ruido cósmico de fondo.")
        
    # Mostrar el gráfico
    st.image(data / np.max(data), caption="Espectrograma generado por la IA", use_column_width=True)
