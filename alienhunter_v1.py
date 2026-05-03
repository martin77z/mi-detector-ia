import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Configuración básica para evitar errores de visualización
st.set_page_config(page_title="DEEP SPACE RADAR", page_icon="📡", layout="wide")

# Estilo Negro "NASA"
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stApp { background-color: #000000; color: #00FF41; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 NEXUS-7: ANALIZADOR TÁCTICO")

# --- BARRA LATERAL ---
target = st.sidebar.selectbox("Objetivo", ["Próxima b", "Estrella de Tabby", "Sagitario A*"])
ganancia = st.sidebar.slider("Potencia de Antena", 10, 100, 80)

# --- PANEL DE CONTROL ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📡 ESCANEANDO: {target}")
    pantalla = st.empty()

with col2:
    st.subheader("📊 TELEMETRÍA")
    consola = st.empty()

if st.button("INICIAR BÚSQUEDA DE SEÑAL"):
    filas = 50
    columnas = 300
    datos = np.zeros((filas, columnas))
    
    # Posición de la señal alienígena
    pos = random.randint(50, 250)
    
    for i in range(filas):
        # Crear ruido y añadir señal
        linea = np.random.normal(0.5, 0.1, columnas)
        # La señal se mueve un poco (Efecto Doppler)
        centro = pos + int(i * 0.2)
        if 0 <= centro < columnas:
            linea[centro-2:centro+3] += (ganancia / 10)
            
        datos[i] = linea
        
        # Dibujar gráfico
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='black')
        ax.imshow(datos, aspect='auto', cmap='magma', origin='lower')
        ax.axis('off')
        pantalla.pyplot(fig)
        plt.close(fig)
        
        # Texto de consola
        consola.code(f"SYNC_STREAM... OK\nFREQ_LOCKED: {centro} MHz\nSNR: {ganancia}dB")
        time.sleep(0.05)

    st.success(f"Escaneo de {target} completado. Análisis de IA: SEÑAL INTELIGENTE DETECTADA.")
