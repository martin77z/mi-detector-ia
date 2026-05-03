import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime
import os

# CONFIGURACIÓN
st.set_page_config(page_title="NEXUS-7 PERMANENT v7.9", page_icon="📡", layout="wide")

# ARCHIVO DE REGISTRO
DB_FILE = "registro_civilizaciones.csv"

# --- FUNCIÓN DE CARGA SEGURA ---
def cargar_historial():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE).to_dict('records')
        except:
            return []
    return []

# --- FUNCIÓN DE GUARDADO SEGURO ---
def guardar_hallazgo(nuevo_dato):
    historial_actual = cargar_historial()
    historial_actual.append(nuevo_dato)
    pd.DataFrame(historial_actual).to_csv(DB_FILE, index=False)
    return historial_actual

# Inicializamos el estado de la sesión
if 'historial' not in st.session_state:
    st.session_state['historial'] = cargar_historial()

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .detail-card { background-color: #051205; border: 1px solid #00FF41; padding: 15px; border-radius: 5px; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; font-weight: bold; width: 100%; }
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# (Aquí mantendríamos los diccionarios de info_objetivos que ya tienes)
info_objetivos = {
    "Próxima b": {"Dist": "4.2 AL", "Tipo": "Rocoso", "Nota": "Señal corta."},
    "Estrella de Tabby": {"Dist": "1,470 AL", "Tipo": "Anomalía", "Nota": "¿Dyson?"},
    "Andrómeda": {"Dist": "2.5M AL", "Tipo": "Galaxia", "Nota": "Extragaláctica."}
}

st.title("📡 NEXUS-7: ARCHIVO PERMANENTE v7.9")

# PANEL SUPERIOR
c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    objetivo = st.selectbox("OBJETIVO", list(info_objetivos.keys()))
    k_scale = st.select_slider("K-SCALE", options=["Tipo I", "Tipo II", "Tipo III"])
with c2:
    ganancia = st.slider("GANANCIA (dB)", 100, 500, 200)
    trigger = st.button("🚀 INICIAR ESCANEO")
with c3:
    data = info_objetivos[objetivo]
    st.markdown(f"<div class='detail-card'><b>SISTEMA:</b> {objetivo}<br><b>DISTANCIA:</b> {data['Dist']}<br><i>{data['Nota']}</i></div>", unsafe_allow_html=True)

# VISUALIZACIÓN
v_cascada = st.empty()
v_potencia = st.empty()
v_alerta = st.empty()

if trigger:
    # --- LÓGICA DE ESCANEO SIMPLIFICADA ---
    es_alien = random.random() > 0.5
    for t in range(50): # Versión rápida para probar
        v_cascada.text(f"Escaneando... {t*2}%")
        time.sleep(0.05)
    
    if es_alien:
        v_alerta.success("🎯 ¡CONTACTO CONFIRMADO!")
        nuevo = {
            "Hora": datetime.now().strftime("%H:%M"),
            "Lugar": objetivo,
            "K-Scale": k_scale,
            "Result": "ÉXITO"
        }
        # Guardamos en el archivo y actualizamos la sesión
        st.session_state['historial'] = guardar_hallazgo(nuevo)
    else:
        v_alerta.error("❌ Solo ruido de fondo.")

# --- SECCIÓN DE ARCHIVO (LO QUE BUSCAS) ---
st.write("---")
st.subheader("📂 REGISTRO HISTÓRICO DE CIVILIZACIONES")

if st.session_state['historial']:
    # Convertimos a DataFrame solo para mostrar la tabla
    df_mostrar = pd.DataFrame(st.session_state['historial'])
    st.table(df_mostrar)
    
    # Botón para borrar si hay errores
    if st.button("🗑️ Limpiar Historial"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state['historial'] = []
        st.rerun()
else:
    st.write("No hay hallazgos registrados todavía.")
