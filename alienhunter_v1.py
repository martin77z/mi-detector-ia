import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime

# =========================================================
# 1. ESTILO DE ALTO IMPACTO (RECUPERANDO LA ESENCIA 9.5)
# =========================================================
st.set_page_config(page_title="SETI CONTROL PANEL v9.5", layout="wide")

# CSS para inyectar el look de "Terminal de Laboratorio"
st.markdown("""
<style>
    body { background-color: #000000; color: #00FF41; }
    .reportview-container { background: #000000; }
    .stMetric { 
        background-color: #0a0a0a; 
        border: 1px solid #00FF41; 
        border-radius: 0px; 
        padding: 10px;
    }
    h1, h2, h3 { color: #00FF41 !important; font-family: 'Courier New', Courier, monospace; }
    .stAlert { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. MOTOR DE DATOS CRUDOS
# =========================================================
class AnalizadorPro:
    def __init__(self):
        self.targets = {
            "ROSS 128 b": {"f": 1420.405, "desc": "Exoplaneta - Zona Habitable", "status": "ANOMALÍA"},
            "ANDRÓMEDA": {"f": 1665.402, "desc": "M31 - Región H II", "status": "NATURAL"}
        }

    def generar_espectro_v95(self, nombre):
        t = self.targets[nombre]
        x = np.linspace(t['f']-2, t['f']+2, 400)
        # Ruido mucho más fino y detallado
        ruido = np.random.normal(0.5, 0.15, 400)
        
        if t['status'] == "ANOMALÍA":
            # La señal ahora es un pulso ultra-fino de alta energía
            pico = np.zeros(400)
            pico[200] = 4.5
            datos = ruido + pico
            color_hex = "#00FF41" # Verde neón
        else:
            datos = ruido + (np.exp(-np.power(x - t['f'], 2) / 0.5) * 0.5)
            color_hex = "#33CCFF" # Azul científico
            
        return pd.DataFrame({'f': x, 'p': datos}), color_hex, t

# =========================================================
# 3. INTERFAZ DE COMANDO (LAYOUT DE INGENIERÍA)
# =========================================================
proc = AnalizadorPro()

# Encabezado técnico
c_head1, c_head2 = st.columns([4, 1])
with c_head1:
    st.title("📟 SETI GLOBAL NETWORK | STATION ALPHA-9")
    st.write(f"SYSTEM_READY // UTC_SYNCHRONIZED: {datetime.datetime.now()}")
with c_head2:
    target_sel = st.selectbox("SELECT_TARGET", list(proc.targets.keys()))

st.divider()

# Grid principal
col_main, col_side = st.columns([3, 1])

df, color_main, info = proc.generar_espectro_v95(target_sel)

with col_main:
    # Gráfica con look de osciloscopio
    chart = alt.Chart(df).mark_line(
        color=color_main, 
        strokeWidth=1.5,
        opacity=0.9
    ).encode(
        x=alt.X('f:Q', title='FREQUENCY (MHz)', scale=alt.Scale(zero=False)),
        y=alt.Y('p:Q', title='INTENSITY (dBm)', scale=alt.Scale(domain=[0, 6]))
    ).properties(height=450)
    
    # Capa de área para dar volumen
    area = chart.mark_area(opacity=0.1, fill=color_main)
    
    st.altair_chart(area + chart, use_container_width=True)
    
    # Telemetría de flujo (Waterfall mejorado)
    st.write("▼ LIVE_WATERFALL_BUFFER_095")
    waterfall = np.random.normal(0.5, 0.2, (15, 100))
    st.image(waterfall, use_container_width=True, clamp=True)

with col_side:
    st.subheader("SYSTEM_LOG")
    st.metric("SIGNAL_STRENGTH", f"{np.max(df['p']):.2f} dB", delta="0.04% ▲")
    st.metric("CONFIDENCE_INDEX", "99.98%" if info['status'] == "ANOMALÍA" else "4.12%")
    
    st.write(f"**OBJECT:** {target_sel}")
    st.write(f"**CLASS:** {info['desc']}")
    
    if info['status'] == "ANOMALÍA":
        st.error("⚠️ TECNOFIRMA DETECTADA")
        st.info("PROBABILITY: EXTRATERRESTRIAL_ORIGIN")
    else:
        st.success("✅ EMISIÓN NATURAL")

st.divider()
st.caption("CORE_VERSION: 9.5_LEGACY | ENCRYPTED_LINK: ACTIVE | NO_ERRORS_DETECTED")
