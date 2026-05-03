import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime
import os # Para manejar archivos reales

# CONFIGURACIÓN
st.set_page_config(page_title="NEXUS-7 ARCHIVE v7.8", page_icon="📡", layout="wide")

# ARCHIVO FÍSICO DONDE SE GUARDARÁ TODO
DB_FILE = "registro_civilizaciones.csv"

# FUNCIÓN PARA CARGAR DATOS GUARDADOS PREVIAMENTE
def cargar_datos():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])

# INICIALIZAR EL HISTORIAL CON LO QUE HAYA EN EL ARCHIVO
if 'historial' not in st.session_state:
    st.session_state['historial'] = cargar_datos()

# --- (Estilos visuales igual que antes) ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .detail-card { background-color: #051205; border: 1px solid #00FF41; padding: 20px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# ... (Aquí iría el resto de tu código de escaneo y telemetría) ...

# --- MODIFICACIÓN EN LA LÓGICA DE ÉXITO ---
# Cuando encuentres una civilización, añade esto:

if es_alien: # Si el escaneo fue un éxito
    nueva_entrada = {
        "Hora": datetime.now().strftime("%H:%M"),
        "Lugar": objetivo,
        "K-Scale": k_scale,
        "Result": "ÉXITO"
    }
    
    # Añadir al historial de la sesión
    st.session_state.historial = pd.concat([st.session_state.historial, pd.DataFrame([nueva_entrada])], ignore_index=True)
    
    # GUARDAR FÍSICAMENTE EN EL DISCO DURO
    st.session_state.historial.to_csv(DB_FILE, index=False)
    st.success("✅ HALLAZGO ARCHIVADO PERMANENTEMENTE")

# --- SECCIÓN DE ARCHIVO PARA VERLO NUEVAMENTE ---
st.divider()
st.subheader("📂 ARCHIVO DE CIVILIZACIONES (REGISTRO PERMANENTE)")

if not st.session_state.historial.empty:
    # Mostramos la tabla que viste en tu foto
    st.table(st.session_state.historial)
    
    # BOTÓN PARA DESCARGAR EL ARCHIVO Y VERLO EN EXCEL
    csv = st.session_state.historial.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DESCARGAR BASE DE DATOS DE CIVILIZACIONES",
        data=csv,
        file_name='archivo_nexus7_seti.csv',
        mime='text/csv',
    )
else:
    st.info("El archivo está vacío. Inicie escaneo para detectar señales.")
