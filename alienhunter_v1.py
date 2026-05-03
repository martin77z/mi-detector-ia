import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- 1. NÚCLEO DE DATOS RESISTENTE ---
DB_FILE = "registro_misiones.csv"
def cargar_db():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Hora", "Sector", "K-Scale", "Status", "Frecuencia"])
    return pd.DataFrame(columns=["Hora", "Sector", "K-Scale", "Status", "Frecuencia"])

st.set_page_config(page_title="NEXUS-7 MASTER v15.0", layout="wide")
if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# --- 2. INTERFAZ TÁCTICA (CIAN / NEÓN) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .card { 
        border: 2px solid #00FF41; padding: 25px; 
        background: rgba(0, 40, 40, 0.3); border-radius: 10px; 
        box-shadow: inset 0 0 15px rgba(0, 255, 65, 0.1);
    }
    .stButton>button { 
        border: 2px solid #00FF41; background: #000; color: #00FF41; 
        font-weight: bold; height: 4.5em; width: 100%;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { background: #00FF41; color: #000; box-shadow: 0 0 25px #00FF41; }
    [data-testid="stHeader"], footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE CONOCIMIENTO (10 OBJETIVOS BLINDADOS) ---
objetivos_db = {
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000.0 AL", "retraso": "26,000 años", "emision": "Edad de Hielo", "info": "Centro Galáctico. Agujero negro masivo."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470.0 AL", "retraso": "1,470 años", "emision": "Año 556 D.C.", "info": "Anomalía de luz. Posible Enjambre de Dyson."},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.24 AL", "retraso": "4.24 años", "emision": "Hace 4 años", "info": "Zona habitable. Objetivo Tipo I prioritario."},
    "Ross 128 b": {"cat": "Ross 128", "dist": "11.03 AL", "retraso": "11.03 años", "emision": "Hace 11 años", "info": "Exoplaneta templado en enana roja inactiva."},
    "Gliese 581g": {"cat": "GJ 581", "dist": "20.2 AL", "retraso": "20.2 años", "emision": "Hace 20 años", "info": "Mundo rocoso con potencial de atmósfera estable."},
    "TRAPPIST-1e": {"cat": "2MASS J2306", "dist": "39.6 AL", "retraso": "39.6 años", "emision": "Hace 40 años", "info": "Mundo oceánico. Sistema de 7 planetas hermanos."},
    "K2-18b": {"cat": "EPIC 20191", "dist": "124.0 AL", "retraso": "124 años", "emision": "Año 1902", "info": "Presencia de moléculas biogénicas detectadas."},
    "Sector Wow!": {"cat": "7UC Sgr", "dist": "1,800.0 AL", "retraso": "1,800 años", "emision": "Año 226 D.C.", "info": "Origen de la señal de banda estrecha de 1977."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000.0 AL", "retraso": "25,000 años", "emision": "Pre-historia", "info": "Destino del Mensaje de Arecibo."},
    "Andrómeda": {"cat": "M31", "dist": "2.53M AL", "retraso": "2.5M años", "emision": "Plioceno", "info": "Búsqueda de civilizaciones Tipo III masivas."}
}

st.title("📡 NEXUS-7 OMNIBUS | TITAN RESTORATION v15.0")

# --- 4. PANEL DE MANDO Y TELEMETRÍA ---
col_ctrl, _, col_tele = st.columns([1, 0.1, 1.3])
with col_ctrl:
    st.subheader("🕹️ SISTEMAS DE NAVEGACIÓN")
    t_key = st.selectbox("DESTINO ESTELAR", list(objetivos_db.keys()))
    k_level = st.select_slider("ESCALA KARDASHOV", options=["Tipo I (Planetaria)", "Tipo II (Estelar)", "Tipo III (Galáctica)"], value="Tipo II (Estelar)")
    gain_db = st.slider("SENSIBILIDAD RECEPTOR (dB)", 100, 500, 250)
    btn_scan = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with col_tele:
    t = objetivos_db[t_key]
    st.markdown(f"""
    <div class="card">
        <h4>📊 TELEMETRÍA DE SECTOR: {t_key.upper()}</h4>
        <b>CATÁLOGO:</b> {t['cat']} | <b>DISTANCIA:</b> {t['dist']}<br>
        <b>RETRASO SEÑAL:</b> {t['retraso']} | <b>FOTONES DE:</b> {t['emision']}<br>
        <hr style='border:0.5px solid #00FF41'>
        <b>CONFIGURACIÓN:</b> Escaneo activo para civilización {k_level}<br>
        <b>NOTAS DE CAMPO:</b> <i>{t['info']}</i>
    </div>
    """, unsafe_allow_html=True)

# --- 5. VISUALIZADORES ---
st.write("---")
col_vis, col_ia = st.columns([2, 1])

with col_vis:
    st.subheader("🛰️ ESPECTRO ELECTROMAGNÉTICO (AZUL CIAN)")
    v_water = st.empty()
    v_spec = st.empty()

with col_ia:
    st.subheader("📟 ANALIZADOR IA")
    v_msg = st.empty()
    v_log = st.empty()

# --- 6. PROCESAMIENTO DE SEÑAL ---
if btn_scan:
    radar_buffer = np.random.rand(40, 100) * 0.4
    is_hit = random.random() > 0.4
    
    frases_ia = [
        "Ajustando parábola de 70m...", "Filtrando estática estelar...",
        "Calculando desplazamiento Doppler...", "Buscando secuencias Prime...",
        "Analizando línea de 21cm...", "Estabilizando receptor criogénico..."
    ]

    for i in range(65):
        frame = np.random.rand(100) * 0.3
        if is_hit:
            pico = 50
            frame[pico] += (gain_db / 105)
            frame[pico-1] += (gain_db / 250) # Armónicos
            frame[pico+1] += (gain_db / 250)
        
        radar_buffer = np.roll(radar_buffer, -1, axis=0)
        radar_buffer[-1] = frame
        
        # RADAR CIAN
        fig_w, ax_w = plt.subplots(figsize=(10, 5), facecolor='black')
        ax_w.imshow(radar_buffer, aspect='auto', cmap='cool', vmin=0, vmax=1.8)
        ax_w.axis('off')
        v_water.pyplot(fig_w)
        plt.close(fig_w)
        
        # ESPECTRO
        fig_s, ax_s = plt.subplots(figsize=(10, 1.2), facecolor='black')
        ax_s.plot(frame, color='#00FF41' if not is_hit else '#FF3131', linewidth=1.8)
        ax_s.set_facecolor('black')
        ax_s.set_ylim(0, 4)
        ax_s.axis('off')
        v_spec.pyplot(fig_s)
        plt.close(fig_s)
        
        v_msg.info(f"IA: {random.choice(frases_ia)}")
        v_log.code(f"PROGRESO: {i*1.54:.1f}%\nSNR: {np.max(frame)*6:.2f} dB\nDEST: {t_key}")
        time.sleep(0.04)

    if is_hit:
        v_msg.success(f"¡CONTACTO! Señal coherente detectada. Parámetros compatibles con civilización {k_level}.")
        new_row = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Sector": t_key, "K-Scale": k_level, "Status": "ÉXITO", "Frecuencia": "1420.4 MHz"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_row], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
    else:
        v_msg.error("SIN RESULTADOS. El sector analizado solo muestra ruido de fondo térmico.")

# --- 7. ARCHIVO HISTÓRICO ---
st.write("---")
st.subheader("📂 BITÁCORA DE DESCUBRIMIENTOS")
st.dataframe(st.session_state.historial_df, use_container_width=True)
