import streamlit as st
import numpy as np
from datetime import datetime

# =========================================================
# CONFIGURACIÓN Y CSS PARA REPLICAR LA VERSIÓN 9.5
# =========================================================
st.set_page_config(page_title="NEXUS-7: DEEP SPACE ANALYZER", layout="wide")

st.markdown("""
<style>
    /* Fondo negro absoluto para la aplicación */
    .stApp {
        background-color: #000000;
    }
    
    /* Textos en verde neón brillante */
    h1, h2, h3, p, span, label, div[data-testid="stMarkdownContainer"] {
        color: #33FF33 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* LOS SLIDERS ROJOS (Lo más distintivo de tu foto) */
    div[data-baseweb="slider"] > div > div {
        background-color: #FF0000 !important; /* Línea del slider */
    }
    div[role="slider"] {
        background-color: #FF0000 !important; /* El botón del slider */
        border: 2px solid #AA0000 !important;
    }

    /* Cuadros laterales con borde verde neón */
    .module-box {
        border: 2px solid #33FF33;
        padding: 15px;
        background-color: #000000;
        margin-bottom: 20px;
        border-radius: 4px;
    }

    /* Progress Bar en azul cielo */
    .stProgress > div > div > div > div {
        background-color: #33CCFF;
    }

    /* Terminal de logs */
    .terminal-output {
        color: #33FF33;
        font-family: 'Courier New', monospace;
        font-size: 11px;
        line-height: 1.2;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# GENERADOR DEL MAPA ESTELAR (FONDO CLARO / PUNTOS NEGROS)
# =========================================================
def generar_mapa_estelar_v95():
    # Creamos una base clara (gris muy claro/blanco) como se ve en el centro de tu monitor
    h, w = 500, 1000
    img = np.ones((h, w, 3), dtype=np.uint8) * 230 
    
    # Añadimos "estrellas" o ruido de señal (puntos negros/grises)
    num_puntos = 300
    for _ in range(num_puntos):
        y, x = np.random.randint(0, h), np.random.randint(0, w)
        img[y:y+2, x:x+2] = [40, 40, 40] # Puntos oscuros
    
    # Línea de señal Doppler (la traza central)
    for i in range(h):
        centro = 450 + int(i * 0.05)
        if centro < w:
            img[i, centro-1:centro+2] = [20, 20, 20]
            
    return img

# =========================================================
# ESTRUCTURA DE LA INTERFAZ
# =========================================================

# Título Principal
st.markdown("<h1>NEXUS-7: DEEP SPACE ANALYZER v9.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top:-25px; font-size: 14px;'>HEURISTIC CORE ENABLED // SIGNAL CAPTURE ACTIVE</p>", unsafe_allow_html=True)

# Controles Superiores con sliders ROJOS
c1, c2, c3 = st.columns([2, 3, 3])
with c1:
    target = st.selectbox("OBJETIVO", ["Ross 128 b", "Próxima b", "Andrómeda"])
with c2:
    st.select_slider("ESCALA KARDASHOV", options=["Tipo I", "Tipo II", "Tipo III"], value="Tipo III")
with c3:
    st.slider("GANANCIA SENSORIAL (dB)", 0, 500, 300)

st.markdown("<hr style='border: 1px solid #33FF33;'>", unsafe_allow_html=True)

# Layout: Visualizador | Panel de IA
col_viz, col_ia = st.columns([2.5, 1])

with col_viz:
    # Generamos el mapa estelar invertido
    data_mapa = generar_mapa_estelar_v95()
    st.image(data_mapa, use_container_width=True)
    st.markdown("<p style='font-size: 10px; color: #33FF33;'>BARRIDO DE FRECUENCIA ACTIVO | SENSOR: VLA-ARRAY 4</p>", unsafe_allow_html=True)

with col_ia:
    # Cuadro de Estado del Sistema
    st.markdown(f"""
    <div class="module-box">
        SISTEMA: {target} | DISTANCIA: 4.22 AL<br>
        ZONA: Habitable | ESTRELLA: Enana Roja<br>
        <span style="color: #00FF00;">● ANALIZANDO...</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧠 AI HEURISTIC ENGINE")
    st.write("CONFIANZA DE LA IA: 94.8%")
    st.progress(0.94)
    
    # Mensaje del Operador (Cuadro con fondo verde oscuro)
    st.markdown("""
    <div style="background-color: #001100; border-left: 3px solid #33FF33; padding: 10px; font-style: italic; font-size: 12px; margin-bottom: 20px;">
        "Operador, la señal detectada es de origen tecnológico. Coherencia confirmada en la línea de Hidrógeno."
    </div>
    """, unsafe_allow_html=True)
    
    # Log de Terminal
    st.markdown(f"""
    <div class="module-box terminal-output">
        [{datetime.now().strftime('%H:%M:%S')}] Iniciando escaneo sector Ross...<br>
        [00:23:50] Confirmado: Drift doppler detectado.<br>
        [00:21:43] Anomalía de banda estrecha en 1420MHz.<br>
        -------------------------------------------<br>
        ◆ SISTEMA NEXUS-7 INICIALIZADO...<br>
        ◆ IA HEURÍSTICA: BUSCANDO PATRONES...
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("SISTEMA DE SEGURIDAD NEXUS-7 v9.5 | PROTOCOLO DE RADIOASTRONOMÍA ACTIVO")
