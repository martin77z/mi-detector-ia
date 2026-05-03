import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(page_title="NEXUS-7 ACADEMY", page_icon="🎓", layout="wide")

if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# ESTILO MEJORADO CON TOOLTIPS
st.markdown("""
    <style>
    .stApp { background-color: #040804; color: #00FF41; font-family: 'Courier New', monospace; }
    .info-box { background-color: #0a1a0a; border: 1px solid #00FF41; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 0.9em; }
    .stButton>button { border: 2px solid #00FF41; background-color: #000; color: #00FF41; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #00FF41; color: #000; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 NEXUS-7: ANALIZADOR ACADÉMICO v5.0")

# --- GUÍA RÁPIDA PARA PRINCIPIANTES ---
with st.expander("❓ ¿CÓMO LEER ESTOS GRÁFICOS? (GUÍA DE OPERADOR)"):
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("""
        **1. RADAR DE CASCADA (Waterfall):**
        * **Eje Horizontal:** Frecuencias de radio.
        * **Eje Vertical:** El tiempo. Lo más nuevo aparece abajo.
        * **Interpretación:** Una línea vertical continua indica una fuente estable. Si está inclinada, el objeto se está moviendo (Efecto Doppler).
        """)
    with col_g2:
        st.markdown("""
        **2. ESPECTRO DE POTENCIA:**
        * **Interpretación:** Es un 'corte' de lo que pasa ahora mismo. 
        * **Picos:** Cuanto más alto es el pico, más fuerte es la señal sobre el ruido del espacio. Un pico fino y alto es señal de tecnología.
        """)

# --- SIDEBAR ---
st.sidebar.title("🎛️ CONFIGURACIÓN")
target = st.sidebar.selectbox("Objetivo", ["Próxima b", "TRAPPIST-1e", "Estrella de Tabby", "Sagitario A*"])
ganancia = st.sidebar.slider("Ganancia LNA (Sensibilidad)", 50, 150, 100)

# --- UI PRINCIPAL ---
c_graficos, c_analisis = st.columns([2, 1])

with c_graficos:
    v_waterfall = st.empty()
    st.caption("⬆️ Historial temporal de la señal (Cascada)")
    v_power = st.empty()
    st.caption("⬆️ Intensidad actual por frecuencia (Espectro de Potencia)")

with c_analisis:
    st.subheader("📟 DIAGNÓSTICO IA")
    v_consola = st.empty()
    v_explicacion = st.empty()

if st.button("🚀 INICIAR CAPTURA DE DATOS"):
    pasos, columnas = 80, 400
    datos = np.zeros((pasos, columnas))
    es_rfi = random.random() < 0.3
    pos_x = random.randint(100, 300)
    
    for t in range(pasos):
        linea = np.random.normal(0.5, 0.15, columnas)
        centro = int(pos_x + t * 0.1) # Deriva suave
        
        if 0 <= centro < columnas:
            ancho = 5 if es_rfi else 1
            linea[centro-ancho:centro+ancho+1] += (ganancia / 12)
        
        datos[t] = linea
        
        # Actualizar Waterfall
        fig1, ax1 = plt.subplots(figsize=(10, 4), facecolor='black')
        ax1.imshow(datos, aspect='auto', cmap='magma', origin='lower')
        ax1.axis('off')
        v_waterfall.pyplot(fig1)
        plt.close(fig1)
        
        # Actualizar Power Spectrum
        fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
        ax2.plot(linea, color='#00FF41', linewidth=1)
        ax2.set_facecolor('black')
        ax2.set_ylim(0, 20)
        ax2.axis('off')
        v_power.pyplot(fig2)
        plt.close(fig2)
        
        v_consola.code(f"MUESTREO: {t}/{pasos}\nINTENSIDAD: {np.max(linea):.2f}\nESTADO: ESCANEANDO...")
        time.sleep(0.02)

    # --- EXPLICACIÓN FINAL DE RESULTADOS ---
    with v_explicacion:
        st.markdown("### 📝 INFORME DEL ANALISTA")
        if es_rfi:
            st.error("⚠️ INTERFERENCIA DETECTADA")
            st.write("La señal es demasiado 'ancha'. Esto suele ser causado por satélites humanos o electrónica terrestre. No es de origen extra-solar.")
        else:
            st.success("✨ SEÑAL COHERENTE DETECTADA")
            st.write("Señal de banda estrecha detectada. Esto es como ver un faro en la oscuridad; la naturaleza no crea señales tan finas y precisas. ¡Posible tecnofirma!")
