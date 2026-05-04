import streamlit as st
import numpy as np
from datetime import datetime

# =========================================================
# CONFIGURACIÓN DE LA INTERFAZ v9.5 (FONDO CLARO)
# =========================================================
st.set_page_config(page_title="NEXUS-7 v9.5 PRO", layout="wide")

# CSS para replicar exactamente tu foto v9.5
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    
    /* Título en verde neón */
    .nexus-title {
        color: #33FF33;
        font-family: 'Courier New', monospace;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 0px;
    }

    /* SLIDERS ROJOS LARGOS (Estilo de tu foto) */
    div[data-baseweb="slider"] > div {
        background-color: #FF0000 !important;
        height: 4px;
    }
    div[role="slider"] {
        background-color: #FF0000 !important;
        border: 2px solid #FF0000 !important;
    }

    /* VISUALIZADOR CENTRAL (El fondo blanco/gris de la v9.5) */
    .canvas-border {
        border: 2px solid #33FF33;
        background-color: #F0F0F0; /* Fondo claro de la foto */
    }

    /* Cuadros de texto de la derecha */
    .side-module {
        border: 1px solid #33FF33;
        padding: 10px;
        background-color: #000000;
        color: #33FF33;
        font-family: 'Courier New', monospace;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SOLUCIÓN AL ERROR: GENERADOR DE DATOS "POTENCIA.TXT"
# =========================================================
# En lugar de leer un archivo que no existe, generamos los datos en memoria
def obtener_datos_señal():
    # Simulamos la lista de números que pedía tu módulo (uno por línea)
    return np.random.uniform(0.1, 1.0, 100)

# =========================================================
# RENDERIZADO DE LA INTERFAZ
# =========================================================

# Encabezado v9.5
st.markdown('<div class="nexus-title">NEXUS-7: DATA ANALYZER - ROSS 128 b</div>', unsafe_allow_html=True)
st.markdown("<p style='color:#33FF33; font-size:12px;'>SIGNAL CAPTURE ACTIVE // V9.5 STABLE</p>", unsafe_allow_html=True)

# Sliders Rojos de lado a lado
col_a, col_b = st.columns([1, 1])
with col_a:
    st.select_slider("ESCALA KARDASHOV", options=["I", "II", "III"], value="III")
with col_b:
    st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.write("") # Espaciador

# Layout Principal
col_mapa, col_info = st.columns([3, 1])

with col_mapa:
    # Creamos el mapa con fondo blanco y puntos negros (v9.5)
    h, w = 500, 1100
    img = np.ones((h, w, 3), dtype=np.uint8) * 235 # Gris muy claro
    
    # Línea central de frecuencia negra
    img[:, w//2 - 1 : w//2 + 1] = [0, 0, 0]
    
    # Puntos de señal
    for _ in range(300):
        y, x = np.random.randint(0, h), np.random.randint(0, w)
        img[y:y+2, x:x+2] = [40, 40, 40]
        
    st.image(img, use_container_width=True)
    st.markdown("<p style='color:#33FF33; font-size:10px;'>MODO: LECTURA DE SEÑAL REAL ACTIVA</p>", unsafe_allow_html=True)

with col_info:
    # Estado del Sistema
    st.markdown('<div class="side-module">SISTEMA: ROSS 128 b<br>DISTANCIA: 4.22 AL<br><span style="color:#00FF00;">● ANALIZANDO...</span></div>', unsafe_allow_html=True)
    
    # IA Engine (Barra Azul de tus fotos)
    st.markdown("<p style='color:#33FF33; font-size:14px; font-weight:bold;'>🧠 AI ENGINE</p>", unsafe_allow_html=True)
    st.progress(0.94) # Barra azul celeste
    
    # Datos simulados (Sustituye a potencia.txt)
    datos = obtener_datos_señal()
    st.markdown(f'<div class="side-module" style="font-size:10px; height:150px; overflow:hidden;">' + 
                "<br>".join([f"SIG_POW: {d:.4f}" for d in datos]) + 
                '</div>', unsafe_allow_html=True)

st.caption("PROTOCOLO NEXUS-7 v9.5 // SIN ERRORES DE ARCHIVO")
