import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# --- 1. CONFIGURACIÓN E HISTORIAL ---
DB_FILE = "registro_civilizaciones.csv"
def cargar_db():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Hora", "Lugar", "Escala K", "Result", "Frecuencia"])
    return pd.DataFrame(columns=["Hora", "Lugar", "Escala K", "Result", "Frecuencia"])

st.set_page_config(page_title="NEXUS-7 MASTER v14.0", layout="wide")
if 'historial_df' not in st.session_state:
    st.session_state.historial_df = cargar_db()

# --- 2. ESTILO VISUAL (EL CIAN ELÉCTRICO ORIGINAL) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .telemetria-card { 
        border: 2px solid #00FF41; 
        padding: 20px; 
        background: rgba(0, 30, 30, 0.4); 
        border-radius: 10px; 
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stButton>button { 
        border: 2px solid #00FF41; 
        background: #000; 
        color: #00FF41; 
        font-weight: bold; 
        height: 4em;
        text-transform: uppercase;
    }
    .stButton>button:hover { background: #00FF41; color: #000; box-shadow: 0 0 20px #00FF41; }
    [data-testid="stHeader"], footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 3. CATÁLOGO MAESTRO (10 DESTINOS CON DATOS CRÍTICOS) ---
objetivos_db = {
    "Sagitario A*": {"cat": "Sgr A*", "dist": "26,000 AL", "retraso": "26,000 años", "emision": "Edad de Hielo", "info": "Centro Galáctico. Agujero negro masivo."},
    "Estrella de Tabby": {"cat": "KIC 8462852", "dist": "1,470 AL", "retraso": "1,470 años", "emision": "Año 556", "info": "Anomalía de luz. Posible Megaestructura."},
    "Próxima b": {"cat": "Alpha Cen Cb", "dist": "4.2 AL", "retraso": "4.2 años", "emision": "Hace 4 años", "info": "Zona habitable. Candidato cercano."},
    "Ross 128 b": {"cat": "Ross 128", "dist": "11.0 AL", "retraso": "11.0 años", "emision": "Hace 11 años", "info": "Mundo templado orbitando estrella estable."},
    "Gliese 581g": {"cat": "GJ 581", "dist": "20.0 AL", "retraso": "20.0 años", "emision": "Hace 20 años", "info": "Super-Tierra con potencial atmosférico."},
    "TRAPPIST-1e": {"cat": "2MASS J2306", "dist": "40.0 AL", "retraso": "40.0 años", "emision": "Hace 40 años", "info": "Mundo oceánico en sistema compacto."},
    "K2-18b": {"cat": "EPIC 20191", "dist": "124.0 AL", "retraso": "124.0 años", "emision": "Siglo XIX", "info": "Firma química de Dimetilsulfuro (Vida)."},
    "Sector Wow!": {"cat": "7UC Sgr", "dist": "1,800 AL", "retraso": "1,800 años", "emision": "Año 226", "info": "Origen de la señal de 1977."},
    "Cúmulo M13": {"cat": "NGC 6205", "dist": "25,000 AL", "retraso": "25,000 años", "emision": "Pre-historia", "info": "Objetivo del mensaje de Arecibo."},
    "Andrómeda": {"cat": "M31", "dist": "2.5M AL", "retraso": "2.5M años", "emision": "Plioceno", "info": "Civilizaciones extragalácticas masivas."}
}

st.title("📡 NEXUS-7 OMNIBUS | FINAL ABSOLUTE v14.0")

# --- 4. CENTRO DE MANDO ---
c1, _, c2 = st.columns([1, 0.1, 1.3])
with c1:
    st.subheader("🎯 CONTROL DE NAVEGACIÓN")
    target_sel = st.selectbox("DESTINO", list(objetivos_db.keys()))
    k_level = st.select_slider("ESCALA KARDASHOV", options=["Tipo I (Planetaria)", "Tipo II (Estelar)", "Tipo III (Galáctica)"], value="Tipo II (Estelar)")
    gain_db = st.slider("SENSIBILIDAD (dB)", 100, 500, 200)
    btn_scan = st.button("🚀 INICIAR ESCANEO PROFUNDO")

with c2:
    t = objetivos_db[target_sel]
    st.markdown(f"""
    <div class="telemetria-card">
        <h4>📊 ANÁLISIS DE TELEMETRÍA: {target_sel.upper()}</h4>
        <b>SISTEMA:</b> {t['cat']} | <b>DISTANCIA:</b> {t['dist']}<br>
        <b>RETRASO LUZ:</b> {t['retraso']} | <b>ORIGEN TEMPORAL:</b> {t['emision']}<br>
        <hr style='border:0.5px solid #00FF41'>
        <b>PROTOCOLO DE BÚSQUEDA:</b> {k_level}<br>
        <b>DESCRIPCIÓN:</b> <i>{t['info']}</i>
    </div>
    """, unsafe_allow_html=True)

# --- 5. ÁREA DE RADAR Y ANALIZADOR ---
st.write("---")
col_rad, col_ia = st.columns([2, 1])

with col_rad:
    st.subheader("🛰️ ESPECTRÓMETRO EN TIEMPO REAL")
    v_water = st.empty()
    v_spec = st.empty()

with col_ia:
    st.subheader("📟 ANALIZADOR ORIENTATIVO")
    v_narrativa = st.empty()
    v_log = st.empty()
    v_gauge = st.empty()

# --- 6. PROCESAMIENTO DE SEÑAL ---
if btn_scan:
    data_radar = np.random.rand(40, 100) * 0.5
    is_hit = random.random() > 0.4
    
    frases_ia = [
        "Sintonizando antena de 70m...", "Escaneando 'Línea de Hidrógeno'...",
        "Filtrando radiación estelar...", "Analizando picos de energía coherente...",
        "Calculando desplazamiento Doppler...", "Buscando patrones matemáticos..."
    ]

    for i in range(60):
        frame = np.random.rand(100) * 0.4
        if is_hit: 
            frame[50] += (gain_db / 110)
            frame[49] += (gain_db / 220) # Armónicos para realismo
            frame[51] += (gain_db / 220)
        
        data_radar = np.roll(data_radar, -1, axis=0)
        data_radar[-1] = frame
        
        # Waterfall Plot (AZUL CIAN)
        fig_w, ax_w = plt.subplots(figsize=(10, 5), facecolor='black')
        ax_w.imshow(data_radar, aspect='auto', cmap='cool', vmin=0, vmax=1.8)
        ax_w.axis('off')
        v_water.pyplot(fig_w)
        plt.close(fig_w)
        
        # Spectrum Plot
        fig_s, ax_s = plt.subplots(figsize=(10, 1.2), facecolor='black')
        ax_s.plot(frame, color='#00FF41' if not is_hit else '#FF3131', linewidth=1.5)
        ax_s.set_facecolor('black')
        ax_s.set_ylim(0, 4)
        ax_s.axis('off')
        v_spec.pyplot(fig_s)
        plt.close(fig_s)
        
        # IA Orientativa
        v_narrativa.info(f"IA: {random.choice(frases_ia)}")
        v_log.code(f"PROGRESO: {i*1.6:.1f}%\nSNR: {np.max(frame)*6:.2f} dB\nRAD: {target_sel}")
        time.sleep(0.04)

    if is_hit:
        v_narrativa.success(f"¡CONFIRMADO! Señal inteligente detectada. Los patrones coinciden con civilización {k_level} en {target_sel}.")
        new_row = pd.DataFrame([{"Hora": datetime.now().strftime("%H:%M"), "Lugar": target_sel, "Escala K": k_level, "Result": "ÉXITO", "Frecuencia": "1420 MHz"}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, new_row], ignore_index=True)
        st.session_state.historial_df.to_csv(DB_FILE, index=False)
    else:
        v_narrativa.error(f"RESULTADO: Solo se ha detectado ruido térmico. El sector {target_sel} permanece en silencio.")

# --- 7. ARCHIVO HISTÓRICO ---
st.write("---")
st.subheader("📂 BITÁCORA DE SEÑALES DETECTADAS")
st.dataframe(st.session_state.historial_df, use_container_width=True)
