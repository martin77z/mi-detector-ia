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
    .css-10trblm { color: #00FF41; } /* Color verde Matrix */
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. MOTOR DE IA Y DATOS DE OBJETIVOS REALES
# =========================================================
class MotorSETI:
    def __init__(self):
        # Base de datos con información científica real
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
        
        # Ruido cósmico base
        ruido = np.random.normal(0.2, 0.1, longitud)
        
        # Lógica de detección de anomalías
        if obj["anomalia"]:
            # Inyección de Tecnofirma de banda estrecha
            pico = np.zeros(longitud)
            pico[longitud//2] = 3.5 # Señal potente y fina
            datos = ruido + pico
            veredicto = "ANOMALÍA DETECTADA"
            confianza = np.random.uniform(98.2, 99.9)
        else:
            # Emisión natural (curva ancha)
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
    st.image("https://img.icons8.com/nolan/128/satellite-dish.png", width=80)
    st.header("Control de Antena")
    target = st.selectbox("Seleccionar Objetivo:", list(seti.objetivos.keys()))
    modo_ia = st.toggle("Activar Procesador IA Heurístico", value=True)
    st.divider()
    st.write("📡 **Estado del Hardware:** Online")
    st.write("🌍 **Ubicación:** Estación Terrena Alpha")

# --- Cuerpo Principal ---
col1, col2 = st.columns([3, 1])

df_datos, veredicto_ia, prob, info_obj = seti.generar_espectro(target)

with col1:
    st.subheader(f"Análisis Espectral: {target}")
    
    # Gráfica de alta resolución corregida para evitar el error de la consola
    chart = alt.Chart(df_datos).mark_area(
        color='#00FF41',
        opacity=0.3,
        line={'color': '#00FF41'}
    ).encode(
        x=alt.X('Frecuencia (MHz):Q', scale=alt.Scale(zero=False)),
        y=alt.Y('Potencia (Jy):Q', title='Densidad de Flujo (Jy)')
    ).properties(height=400)
    
    # IMPORTANTE: use_container_width='always' elimina el aviso amarillo de tu consola
    st.altair_chart(chart, use_container_width='always')
    
    # Mini-Waterfall simulado (Esencia del 9.5)
    st.write("🌊 **Historial de Cascada (Waterfall)**")
    waterfall = np.random.rand(10, 100)
    st.image(waterfall, use_container_width=True, clamp=True)

with col2:
    st.subheader("🤖 Diagnóstico IA")
    
    if modo_ia:
        # Simulación de carga
        with st.spinner('Analizando paquetes de datos...'):
            time.sleep(0.5)
            
        # Métricas de detección
        st.metric("Confianza", f"{prob:.2f}%")
        
        if veredicto_ia == "ANOMALÍA DETECTADA":
            st.error(f"⚠️ {veredicto_ia}")
            st.warning("Señal de banda estrecha artificial identificada.")
            st.write(f"**Tipo de Objeto:** {info_obj['tipo']}")
            st.write("**Recomendación:** Iniciar protocolo de contacto y re-orientar matriz de antenas.")
        else:
            st.success(f"✅ {veredicto_ia}")
            st.write("No se encontraron patrones inteligentes en esta frecuencia.")
    else:
        st.info("Procesador IA en espera. Active el interruptor lateral.")

# Pie de página técnico
st.divider()
st.caption("Cifrado de datos: AES-256 | Protocolo: SETI-NET | Proyecto de Radioastronomía Avanzada")
