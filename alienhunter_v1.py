import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
import time

# =========================================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Estética Profesional 9.5)
# =========================================================
st.set_page_config(
    page_title="Monitor SETI - Deep Space Analysis",
    page_icon="🌌",
    layout="wide"
)

# Estilo visual "Modo Científico"
st.markdown("""
<style>
    .main { background-color: #050505; }
    .stMetric { background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #222; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. MOTOR DE IA Y DATOS DE OBJETIVOS REALES
# =========================================================
class MotorSETI:
    def __init__(self):
        self.objetivos = {
            "Ross 128 b": {"freq": 1420.4, "tipo": "Exoplaneta", "anomalia": True},
            "Andrómeda (M31)": {"freq": 1665.4, "tipo": "Galaxia", "anomalia": False},
            "Sagitario A*": {"freq": 1420.4, "tipo": "Agujero Negro Supermasivo", "anomalia": False},
            "Espacio Profundo": {"freq": 0.0, "tipo": "Vacío", "anomalia": False}
        }

    def generar_espectro(self, nombre_obj):
        obj = self.objetivos[nombre_obj]
        longitud = 250
        freq_eje = np.linspace(obj["freq"] - 5, obj["freq"] + 5, longitud)
        ruido = np.random.normal(0.2, 0.1, longitud)
        
        if obj["anomalia"]:
            pico = np.zeros(longitud)
            pico[longitud//2] = 3.5 
            datos = ruido + pico
            veredicto = "ANOMALÍA DETECTADA"
            confianza = np.random.uniform(98.2, 99.9)
        else:
            curva_natural = np.exp(-np.power(np.linspace(-5, 5, longitud), 2) / 2) * 0.4
            datos = ruido + curva_natural
            veredicto = "EMISIÓN NATURAL / RUIDO"
            confianza = np.random.uniform(0.5, 4.0)
            
        df = pd.DataFrame({'Frecuencia (MHz)': freq_eje, 'Potencia (Jy)': datos})
        return df, veredicto, confianza, obj

# =========================================================
# 3. INTERFAZ DE USUARIO (STREAMLIT)
# =========================================================
seti = MotorSETI()

st.title("🛰️ Deep Space Signal Detector v3.0")
st.write(f"**Telemetría activa:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

# --- Barra Lateral ---
with st.sidebar:
    st.header("Control de Antena")
    target = st.selectbox("Seleccionar Objetivo:", list(seti.objetivos.keys()))
    modo_ia = st.toggle("Activar Procesador IA Heurístico", value=True)
    st.divider()
    st.write("📡 **Estado:** Online")

# --- Cuerpo Principal ---
col1, col2 = st.columns([3, 1])

df_datos, veredicto_ia, prob, info_obj = seti.generar_espectro(target)

with col1:
    st.subheader(f"Análisis Espectral: {target}")
    
    chart = alt.Chart(df_datos).mark_area(
        color='#00FF41',
        opacity=0.3,
        line={'color': '#00FF41'}
    ).encode(
        x=alt.X('Frecuencia (MHz):Q', scale=alt.Scale(zero=False)),
        y=alt.Y('Potencia (Jy):Q')
    ).properties(height=400)
    
    # --- LA CORRECCIÓN ESTÁ AQUÍ ---
    # Hemos vuelto a True para que tu servidor lo entienda, 
    # pero el resto del código está optimizado para que no falle.
    st.altair_chart(chart, use_container_width=True)
    
    st.write("🌊 **Historial de Cascada (Waterfall)**")
    waterfall = np.random.rand(10, 100)
    st.image(waterfall, use_container_width=True, clamp=True)

with col2:
    st.subheader("🤖 Diagnóstico IA")
    if modo_ia:
        st.metric("Confianza", f"{prob:.2f}%")
        if veredicto_ia == "ANOMALÍA DETECTADA":
            st.error(f"⚠️ {veredicto_ia}")
            st.write(f"**Tipo:** {info_obj['tipo']}")
        else:
            st.success(f"✅ {veredicto_ia}")
    else:
        st.info("IA en espera.")

st.divider()
st.caption("SETI-NET v3.0 | Protocolo de Radioastronomía Avanzada")
