import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE BASE DE DATOS FÍSICA
DB_FILE = "registro_civilizaciones.csv"

def cargar_datos_seguros():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Hora", "Lugar", "K-Scale", "Result"])

# 2. CONFIGURACIÓN DE INTERFAZ
st.set_page_config(page_title="NEXUS-7 OMNIBUS v8.2", page_icon="📡", layout="wide")

if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_datos_seguros()

# Estilos visuales
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .detail-card { background-color: #051205; border: 1px solid #00FF41; padding: 20px; border-radius: 5px; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; font-weight: bold; }
    .alert-active { color: #ff0000; animation: blink 1s infinite; font-weight: bold; text-align: center; border: 2px solid #ff0000; padding: 10px; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 3. DATOS DE TELEMETRÍA (Punto B: Distancia y Retraso)
info_objetivos = {
    "Estrella de Tabby": {"Dist": "1,470 AL", "Tipo": "Anomalía KIC 8462852", "Retraso": "1,470 años", "Nota": "Oscurecimientos masivos."},
    "Próxima b": {"Dist": "4.2 AL", "Tipo": "Rocoso", "Retraso": "4.2 años", "Nota": "Vecino cercano."},
    "Andrómeda": {"Dist": "2.5M AL", "Tipo": "Galaxia", "Retraso": "2.5M años", "Nota": "Extragaláctica."}
}

st.title("📡 NEXUS-7 OMNIBUS: FIRST CONTACT v8.2")

# 4. PANEL DE CONTROL (Punto C: Potencia de Antena y Kardashov)
c1, c2, c3 = st.columns([1.5, 1.5, 3])

with c1:
    st.subheader("🎯 NAVEGACIÓN")
    objetivo = st.selectbox("OBJETIVO", list(info_objetivos.keys()))
    k_scale = st.select_slider("🌌 ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"])

with c2:
    st.subheader("📶 ANTENA")
    ganancia = st.slider("AMPLIFICACIÓN (dB)", 100, 500, 250)
    trigger = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with c3:
    data = info_objetivos[objetivo]
    st.markdown(f"""
    <div class="detail-card">
        <h3 style='margin:0; color:#00FF41;'>📊 TELEMETRÍA</h3>
        <p><b>SISTEMA:</b> {objetivo} | <b>DISTANCIA:</b> {data['Dist']}</p>
        <p><b>RETRASO LUZ:</b> {data['Retraso']} | <b>NOTA:</b> {data['Nota']}</p>
    </div>
    """, unsafe_allow_html=True)

# 5. ÁREA DE VISUALIZACIÓN
v_cascada = st.empty()
v_potencia = st.empty()
v_alerta = st.empty()
v_matrix = st.empty()

if trigger:
    pasos = 100
    matriz = np.zeros((pasos, 400))
    pos_x = random.randint(150, 250)
    es_alien = random.random() > 0.4
    
    for t in range(pasos):
        ruido = np.random.normal(0.5, 0.2, 400)
        centro = int(pos_x + t * 0.05)
        if 0 <= centro < 400:
            if es_alien:
                ruido[centro] += (ganancia / 5)
            else:
                ruido[centro-5:centro+6] += (ganancia / 20)
        
        matriz[t] = ruido
        
        # Gráficos
        fig1, ax1 = plt.subplots(figsize=(10, 3), facecolor='black')
        ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
        ax1.axis('off')
        v_cascada.pyplot(fig1)
        plt.close(fig1)
        
        fig2, ax2 = plt.subplots(figsize=(10, 1.5), facecolor='black')
        ax2.plot(ruido, color='#00FF41' if not es_alien else '#ff0000')
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 150)
        ax2.axis('off')
        v_potencia.pyplot(fig2)
        plt.close(fig2)
        time.sleep(0.01)

    if es_alien:
        v_alerta.markdown('<p class="alert-active">⚠️ CONTACTO INTELIGENTE CONFIRMADO ⚠️</p>', unsafe_allow_html=True)
        # Guardar éxito (Evidencia B)
        nueva_fila = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Lugar": objetivo, "K-Scale": k_scale, "Result": "ÉXITO"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, nueva_fila], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
        
        # Punto D: Decodificación
        msg = np.random.choice([0, 1], size=(8, 8))
        v_matrix.write("🔢 MATRIZ BINARIA DECODIFICADA:")
        v_matrix.table(msg)
    else:
        v_alerta.error("SCAN COMPLETO: Ruido cósmico detectado.")

# 6. ARCHIVO DE CIVILIZACIONES (CORREGIDO)
st.write("---")
st.subheader("📂 ARCHIVO DE CIVILIZACIONES")

# Corrección de la línea 151: comprobación segura de longitud
if len(st.session_state.historial_df) > 0:
    st.table(st.session_state.historial_df)
    csv = st.session_state.historial_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Archivo para Análisis", csv, "nexus7_log.csv", "text/csv")
else:
    st.info("No hay registros de civilizaciones en la base de datos.")
