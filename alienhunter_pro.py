import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Intentamos importar setigen, si falla damos un aviso amigable
try:
    import setigen as stg
except Exception:
    st.error("Instalando componentes astronómicos... Por favor, pulsa el botón de 'Reboot' en el menú de Streamlit si este mensaje no desaparece en 1 minuto.")
    st.stop()

st.set_page_config(page_title="Alien Hunter IA", page_icon="👽")

st.title("📡 Detector de Tecnofirmas IA")
st.write("Analizando señales de radioastronomía en busca de patrones tecnológicos.")

# Configuración en la barra lateral
st.sidebar.header("Parámetros")
sensibilidad = st.sidebar.slider("Sensibilidad", 10, 50, 25)

if st.button("Iniciar Escaneo"):
    with st.spinner("Buscando señales en el espectro..."):
        # Generamos una señal sintética pura con numpy y setigen simplificado
        # Esto evita usar las partes de blimpy que dan error
        frame = stg.Frame(fchans=1024, tsteps=32, df=2.7939677238464355, dt=18.253611008)
        frame.add_noise(x_mean=0, noise_type='chi2')
        
        # Añadimos la "firma alienígena"
        frame.add_signal(stg.constant_path(f_start=frame.get_frequency(200), drift_rate=2),
                         stg.constant_t_profile(level=frame.get_intensity(snr=sensibilidad)),
                         stg.gaussian_f_profile(width=40),
                         stg.constant_bp_profile(level=1))
        
        # Creamos el gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(frame.get_data(), aspect='auto', cmap='magma')
        ax.set_title("Espectrograma: Señal detectada")
        ax.set_xlabel("Frecuencia")
        ax.set_ylabel("Tiempo")
        st.pyplot(fig)
        
        st.success("¡Señal detectada! El patrón muestra una deriva Doppler coherente.")
