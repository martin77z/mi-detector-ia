import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- 1. GESTIÓN DE BASE DE DATOS ---
DB_FILE = "registro_civilizaciones.csv"
def cargar_db():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Hora", "Lugar", "Escala K", "Result"])
    return pd.DataFrame(columns=["Hora", "Lugar", "Escala K", "Result"])

st.set_page_config(page_title="NEXUS-7 FINAL v12.0", layout="wide")
if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# --- 2. ESTILO VISUAL (RECUERDO AZUL) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .telemetria-card { border: 2px solid #00FF41; padding: 20px; background: rgba(0, 50, 50, 0.2); border-radius: 5px; }
    .stButton>button { border: 2px solid #00FF41; background: #000; color: #00FF41; width: 100%; font-weight: bold; height: 3em;}
    .stButton>button:hover { background: #00FF41; color: #000; box-shadow: 0 0 15px #00FF41; }
    [data-testid="stHeader"], footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 3. CATÁLOGO ESTELAR COMPLETO (10 OBJETIVOS) ---
objetivos_db = {
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000 AL", "retraso": "26,000 años", "emision": "Edad de Hielo", "info": "Centro Galáctico. Agujero negro masivo."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470 AL", "retraso": "1,470 años", "emision": "Año 556", "info": "Anomalía de luz. ¿Enjambre de Dyson?"},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "retraso": "4.2 años", "emision": "Hace 4 años", "info": "Zona habitable. Candidato Tipo I cercano."},
    "Ross 128 b": {"cat": "Ross 128", "dist": "11.0 AL", "retraso": "11.0 años", "emision": "Hace 11 años", "info": "Mundo templado orbitando estrella estable."},
    "Gliese 581g": {"cat": "GJ 581", "dist": "20.0 AL", "retraso": "20.0 años", "emision": "Hace 20 años", "info": "Super-Tierra con potencial atmosférico."},
    "TRAPPIST-1e": {"cat": "2MASS J2306", "dist": "40.0 AL", "retraso": "40.0 años", "emision": "Hace 40 años", "info": "Mundo oceánico en sistema compacto."},
    "K2-18b": {"cat": "EPIC 20191", "dist": "124.0 AL", "retraso": "124.0 años", "emision": "Siglo XIX", "info": "Detección de firmas químicas biogénicas."},
    "Sector Wow!": {"cat": "7UC Sgr", "dist": "1,800 AL", "retraso": "1,800 años", "emision": "Año 226", "info": "Coordenadas de la señal captada en 1977."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000 AL", "retraso": "25,000 años", "emision": "Pre-historia", "info": "Objetivo del mensaje codificado de Arecibo."},
    "Andrómeda": {"cat": "M31", "dist": "2.5M AL", "retraso": "2.5M años", "emision": "Plioceno", "info": "Análisis de señales extragalácticas masivas."}
}

st.title("📡 NEXUS-7 OMNIBUS | FULL RESTORATION v12.0")

# --- 4. PANEL DE CONTROL ---
c1, _, c2 = st.columns([1, 0.1, 1.3])
with c1:
    st.subheader("🧭 NAVEGACIÓN")
    target_sel = st.selectbox("OBJETIVO ESTELAR", list(objetivos_db.keys()))
    k_level = st.select_slider("ESCALA KARDASHOV", options=["Tipo I (Planetaria)", "Tipo II (Estelar)", "Tipo III (Galáctica)"], value="Tipo II (Estelar)")
    gain_db = st.slider("SENSIBILIDAD (dB)", 100, 500, 200)
    btn_scan = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with c2:
    t = objetivos_db[target_sel]
    st.markdown(f"""
    <div class="telemetria-card">
        <h4>📊 TELEMETRÍA: {target_sel}</h4>
        <b>CATÁLOGO:</b> {t['cat']} | <b>DISTANCIA:</b> {t['dist']}<br>
        <b>RETRASO DE LUZ:</b> {t['retraso']} | <b>ORIGEN:</b> {t['emision']}<br>
        <hr style='border:0.5px solid #00FF41'>
        <b>OBJETIVO:</b> Búsqueda de civilización {k_level}.<br>
        <b>NOTAS:</b> <i>{t['info']}</i>
    </div>
    """, unsafe_allow_html=True)

# --- 5. VISUALIZACIÓN E IA ---
st.write("---")
col_rad, col_ia = st.columns([2, 1])

with col_rad:
    st.subheader("🛰️ ESPECTRO EN TIEMPO REAL")
    v_water = st.empty()
    v_spec = st.empty()

with col_ia:
    st.subheader("📟 ANALIZADOR ORIENTATIVO")
    v_narrativa = st.empty()
    v_log = st.empty()

# --- 6. PROCESAMIENTO ---
if btn_scan:
    data_radar = np.random.rand(40, 100) * 0.5
    is_hit = random.random() > 0.4
    
    def explicar_k(k):
        if "Tipo I" in k: return "Buscando radiofrecuencias de baja intensidad..."
        if "Tipo II" in k: return "Detectando firmas de calor de megaestructuras..."
        return "Analizando distorsiones de energía galáctica..."

    for i in range(60):
        frame = np.random.rand(100) * 0.4
        if is_hit: frame[50] += (gain_db / 110)
        
        data_radar = np.roll(data_radar, -1, axis=0)
        data_radar[-1] = frame
        
        # Waterfall Azul Cian Original
        fig_w, ax_w = plt.subplots(figsize=(10, 5), facecolor='black')
        ax_w.imshow(data_radar, aspect='auto', cmap='cool', vmin=0, vmax=1.5)
        ax_w.axis('off')
        v_water.pyplot(fig_w)
        plt.close(fig_w)
        
        # Espectro
        fig_s, ax_s = plt.subplots(figsize=(10, 1), facecolor='black')
        ax_s.plot(frame, color='#00FF41' if not is_hit else '#FF3131', linewidth=1.5)
        ax_s.set_facecolor('black')
        ax_s.set_ylim(0, 3.5)
        ax_s.axis('off')
        v_spec.pyplot(fig_s)
        plt.close(fig_s)
        
        v_narrativa.info(f"SISTEMA {t['cat']}: {explicar_k(k_level)}")
        v_log.code(f"SCAN: {i*1.6:.1f}%\nSNR: {np.max(frame)*6:.2f} dB\nRAD: {target_sel}")
        time.sleep(0.04)

    if is_hit:
        v_narrativa.success(f"¡CONTACTO! Señal coherente en {target_sel}. Los patrones indican actividad artificial {k_level}.")
        new_row = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Lugar": target_sel, "Escala K": k_level, "Result": "ÉXITO"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_row], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
    else:
        v_narrativa.error(f"SCAN COMPLETO: No se detectó presencia de nivel {k_level}. Solo ruido estelar.")

st.write("---")
st.subheader("📂 BITÁCORA HISTÓRICA")
st.dataframe(st.session_state.historial_df, use_container_width=True)
