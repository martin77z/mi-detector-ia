import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Alien Hunter IA", page_icon="👽")

st.title("📡 Detector de Tecnofirmas IA")
st.write("Analizando señales de radioastronomía en busca de patrones tecnológicos.")

# Configuración lateral
st.sidebar.header("Parámetros del Telescopio")
sensibilidad = st.sidebar.slider("Potencia de la Señal (SNR)", 1, 100, 25)

if st.button("Iniciar Escaneo del Espacio Profundo"):
    with st.spinner("Procesando datos..."):
        # Creamos una matriz de datos (Tiempo vs Frecuencia)
        t_steps = 64
        f_chans = 1024
        
        # 1. Generamos ruido de fondo (como el siseo de una radio)
        data = np.random.exponential(scale=1.0, size=(t_steps, f_chans))
        
        # 2. Inyectamos la "Tecnofirma" (una línea con deriva Doppler)
        # Esto simula un transmisor moviéndose en el espacio
        start_chan = 200
        drift_rate = 0.5  # La inclinación de la línea
        
        for i in range(t_steps):
            center = int(start_chan + i * drift_rate)
            # Dibujamos un pulso gaussiano en cada paso de tiempo
            lanes = np.arange(f_chans)
            data[i] += (sensibilidad / 5) * np.exp(-((lanes - center)**2) / (2 * 3**2))

        # 3. Visualización
        fig, ax = plt.subplots(figsize=(10, 6))
        # Usamos 'magma' que es el color típico de la astronomía
        img = ax.imshow(data, aspect='auto', cmap='magma', origin='lower')
        plt.colorbar(img, label='Intensidad de Radio')
        ax.set_title("Espectrograma: Candidato a Tecnofirma Detectado")
        ax.set_xlabel("Frecuencia (Canales)")
        ax.set_ylabel("Tiempo (Pasos)")
        
        st.pyplot(fig)
        
        st.success("✅ ¡Detección confirmada! Señal de banda estrecha con deriva coherente.")
        st.info("La inclinación de la señal sugiere que el emisor está en un planeta en rotación.")
