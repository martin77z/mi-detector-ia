import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- GESTIÓN DE BASE DE DATOS (NEXUS-7 Local) ---
DB_FILE = "registro_civilizaciones.csv"

def cargar_db():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["Hora", "Lugar", "Escala K", "Result"])
    return pd.DataFrame(columns=["Hora", "Lugar", "Escala K", "Result"])

# --- CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="NEXUS-7 v9.8 SETI Console", layout="wide", page_icon="📡")

if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# --- ESTILO CSS PERSONALIZADO (RESTORED BLUE/CYAN THEME) ---
# Hemos modificado el CSS para usar el tono cian de tu foto en los acentos
st.markdown("""
<style>
    /* Fondo negro Matrix */
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    
    /* Acentos Cyan de tu foto original */
    h1, h2, h3, h4 { color: #00FFFF !important; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Paneles */
    .stAlert { background-color: rgba(0, 20, 20, 0.7); border: 1px solid #00FFFF; color: #00FFFF; }
    
    /* Botones */
    .stButton>button { 
        border: 2px solid #00FFFF; background-color: #000; color: #00FFFF; 
        font-weight: bold; text-transform: uppercase; border-radius: 0;
    }
    .stButton>button:hover { background-color: #00FFFF; color: #000; box-shadow: 0 0 20px #00FFFF; }
    
    /* Inputs */
    .stSelectbox>div>div, .stSlider>div { background-color: #111; border: 1px solid #00FFFF; color: #00FFFF; }
    [data-testid="stHeader"], [data-testid="stSidebar"], footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- CATÁLOGO ESTELAR (NEXUS-7) ---
objetivos_db = {
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000.0 AL", "retraso": "26,000.0 años", "emision": "Edad de Hielo", "info": "Centro galáctico. Agujero negro masivo."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470.0 AL", "retraso": "1,470.0 años", "emision": "Año 556", "info": "¿Megaestructura extraterrestre?"},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "retraso": "4.2 años", "emision": "Hace 4 años", "info": "Planeta rocoso en zona habitable."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000.0 AL", "retraso": "25,000.0 años", "emision": "Pre-historia", "info": "Objetivo del Mensaje de Arecibo."}
}

st.title("📡 NEXUS-7 OMNIBUS: RESTORED BLUE Console v9.8")

# --- PANEL DE CONTROL ---
ctrl_col, gap_col, tele_col = st.columns([1, 0.1, 1.4])

with ctrl_col:
    st.subheader("🧭 NAVEGACIÓN")
    target_sel = st.selectbox("OBJETIVO", list(objetivos_db.keys()))
    k_level = st.select_slider("ESCALA K", options=["Tipo I", "Tipo II", "Tipo III"], value="Tipo II")
    gain_db = st.slider("GANANCIA SENSOR (dB)", 100, 500, 200)
    btn_scan = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with tele_col:
    t = objetivos_db[target_sel]
    # Usamos acentos cian aquí también
    st.markdown(f"""
    <div style="border: 2px solid #00FFFF; padding: 20px; background-color: rgba(0, 30, 30, 0.5);">
        <h4 style="color: #00FFFF; margin-top: 0;">📊 TELEMETRÍA AUTOMÁTICA</h4>
        <b>OBJETIVO:</b> {target_sel.upper()} | <b>CATÁLOGO:</b> {t['cat']}<br>
        <b>DISTANCIA:</b> {t['dist']} | <b>RETRASO LUZ:</b> {t['retraso']}<br>
        <b>LA LUZ QUE VES ES DE:</b> {t['emision']}<br>
        <hr style="border: 0.5px solid #00FFFF;">
        <b>INFO:</b> <i>{t['info']}</i>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- ÁREA DE VISUALIZACIÓN DE CAMPO (RADAR + IA) ---
radar_col, ia_col = st.columns([2, 1])

with radar_col:
    st.subheader("🛰️ ESPECTROGRAMA DE CAMPO")
    v_water = st.empty() # Contenedor para el gráfico de cascada
    v_spec = st.empty()  # Contenedor para el gráfico de picos

with ia_col:
    st.subheader("📟 ANÁLISIS IA")
    v_alert = st.empty()
    v_log = st.empty()

# --- LÓGICA DE ESCANEO SETI ---
if btn_scan:
    # 1. Preparar datos (simulación)
    data_radar = np.random.rand(40, 100)
    is_hit = random.random() > 0.4
    
    # 2. Simulación de IA analizando frecuencias
    log_messages = [
        "Ajustando parábola...", "Filtrando ruidos de púlsares...", 
        "Analizando línea de hidrógeno...", "Buscando patrones binarios...",
        "Calculando Doppler..."
    ]

    # 3. Bucle de renderizado dinámico (Simulando tiempo real)
    for i in range(60):
        # Generar ruido de fondo
        frame = np.random.rand(100)
        
        # Insertar señal artificial si hay "Éxito"
        if is_hit: frame[50] += (gain_db / 150)
        
        # Desplazar la cascada hacia arriba
        data_radar = np.roll(data_radar, -1, axis=0)
        data_radar[-1] = frame
        
        # --- EL CAMBIO CRÍTICO: cmap='cool' para el tono cian original ---
        # 4. Renderizar Gráfico de Cascada (Waterfall)
        fig_w, ax_w = plt.subplots(figsize=(10, 5), facecolor='black')
        # cmap='cool' replica el color azul/cian eléctrico de tu foto
        ax_w.imshow(data_radar, aspect='auto', cmap='cool', vmin=0, vmax=1.8)
        ax_w.axis('off') # Consola limpia
        v_water.pyplot(fig_w)
        plt.close(fig_w)
        
        # 5. Renderizar Gráfico de Picos (Spectrum)
        fig_s, ax_s = plt.subplots(figsize=(10, 1), facecolor='black')
        ax_s.plot(frame, color='#00FFFF' if not is_hit else '#FF3131') # Cian o Rojo SETI
        ax_s.set_facecolor('black')
        ax_s.set_ylim(0, 3)
        ax_s.axis('off')
        v_spec.pyplot(fig_s)
        plt.close(fig_s)
        
        # 6. Actualizar Log de IA
        v_log.code(f"PROGRESO: {i*1.6:.1f}%\nINTENSIDAD: {np.max(frame):.2f} Jy\nESTADO: {random.choice(log_messages)}")
        time.sleep(0.05)

    # 4. Resultado final
    if is_hit:
        st.balloons()
        v_alert.success(f"⚠️ ¡ALERTA SETI! CONTACTO COHERENTE CONFIRMADO EN {target_sel.upper()}")
        # Guardar en Base de Datos
        new_row = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Lugar": target_sel, "Escala K": k_level, "Result": "ÉXITO"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_row], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
    else:
        v_alert.error("FIN DE ESCANEO. Solo ruido de fondo detectado.")

# --- HISTORIAL DE DESCUBRIMIENTOS ---
st.write("---")
st.subheader("📂 ARCHIVO DE CIVILIZACIONES (EVIDENCIA B)")
if len(st.session_state.historial_df) > 0:
    st.dataframe(st.session_state.historial_df, use_container_width=True)
else:
    st.info("No hay registros en la base de datos.")
