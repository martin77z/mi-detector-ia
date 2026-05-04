import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd

# --- CONFIGURACIÓN DE SISTEMA NEXUS-7 v9.0 ---
st.set_page_config(page_title="NEXUS-7 AI v9.0", page_icon="📡", layout="wide")

# Estilo CSS Avanzado (Dark SETI + AI Overlay)
st.markdown("""
    <style>
    .stApp { background-color: #010801; color: #00FF41; font-family: 'Courier New', monospace; }
    .ai-terminal { 
        background-color: rgba(0, 20, 0, 0.8); 
        border: 1px solid #00FF41; 
        padding: 15px; 
        font-size: 0.85rem; 
        height: 300px; 
        overflow-y: auto;
        box-shadow: inset 0 0 10px #00FF41;
    }
    .status-tag { 
        color: #000; background-color: #00FF41; 
        padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 10px;
    }
    .ai-description {
        background: linear-gradient(90deg, rgba(0,255,65,0.1), transparent);
        border-left: 3px solid #00FF41;
        padding: 10px;
        margin: 10px 0;
        font-style: italic;
    }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    .scanning-active { animation: pulse 1.5s infinite; color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS E HISTORIAL ---
if 'ai_log' not in st.session_state:
    st.session_state.ai_log = ["◈ SISTEMA NEXUS-7 INICIALIZADO...", "◈ IA HEURÍSTICA ONLINE."]

def add_log(text):
    t = time.strftime("%H:%M:%S")
    st.session_state.ai_log.insert(0, f"[{t}] {text}")

# --- INTERFAZ SUPERIOR ---
st.title("📡 NEXUS-7: DEEP SPACE ANALYZER v9.0")
st.markdown("<div style='margin-top:-20px; color:#555;'>AI-HEURISTIC CORE ENABLED</div>", unsafe_allow_html=True)

col_ctrl, col_info = st.columns([2, 1])

with col_ctrl:
    c1, c2, c3 = st.columns(3)
    target = c1.selectbox("🎯 OBJETIVO", ["Próxima b", "Ross 128 b", "K2-18b", "Sector Wow!"])
    k_scale = c2.select_slider("🌌 ESCALA KARDASHOV", ["Tipo I", "Tipo II", "Tipo III"])
    gain = c3.slider("📶 GANANCIA SENSORIAL (dB)", 100, 500, 300)

with col_info:
    st.markdown(f"""
    <div style="border: 1px solid #00FF41; padding: 10px; background: rgba(0,30,0,0.5);">
        <b>SISTEMA:</b> {target} | <b>DISTANCIA:</b> 4.22 AL<br>
        <b>ZONA:</b> Habitable | <b>ESTRELLA:</b> Enana Roja<br>
        <span class="status-tag">IA ANALYZING</span>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- FRAGMENTO DE ESCANEO (LA IA EN ACCIÓN) ---
@st.fragment
def start_deep_scan():
    col_main, col_ai = st.columns([2, 1])
    
    with col_main:
        v_waterfall = st.empty()
        v_power = st.empty()
    
    with col_ai:
        st.subheader("🧠 AI HEURISTIC ENGINE")
        v_confidence = st.empty()
        v_description = st.empty()
        v_terminal = st.empty()

    if st.button("🚀 INICIAR PROCESAMIENTO IA"):
        pasos = 80
        matriz = np.random.normal(0, 0.05, (pasos, 400))
        es_alien = random.random() > 0.4
        drift = random.uniform(-0.3, 0.3)
        pos = random.randint(100, 300)
        
        add_log(f"Iniciando barrido en {target}...")
        
        for t in range(pasos):
            # Generar datos
            ruido = np.random.normal(0.1, 0.05, 400)
            if es_alien:
                # Punto 2: Visión de máquina (Simulación de seguimiento de señal)
                centro = int(pos + (t * drift))
                if 0 <= centro < 400:
                    ruido[centro] = (gain / 100) * (1 + random.random()*0.2)
                    ruido[max(0, centro-1)] = ruido[centro] * 0.6
                    ruido[min(399, centro+1)] = ruido[centro] * 0.6
            
            matriz[t] = ruido
            
            # Punto 1 & 5: Heurística y Análisis de Entorno
            conf = min(100, (t * 1.2)) if es_alien else random.randint(5, 15)
            v_confidence.progress(conf/100, text=f"CONFIANZA DE LA IA: {conf}%")
            
            # Punto 3: Log Narrativo Dinámico
            if t == 10: add_log("Detectando anomalía de banda estrecha...")
            if t == 30 and es_alien: add_log("Confirmado: El drift Doppler coincide con rotación planetaria.")
            if t == 60 and es_alien: add_log("Patrón detectado. Extrayendo estructura semántica...")

            # Actualizar Visualización
            fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='black')
            ax1.imshow(matriz, aspect='auto', cmap='magma' if es_alien else 'viridis', origin='lower')
            # Overlay de la IA (Recuadro de seguimiento)
            if es_alien and t > 5:
                rect_pos = pos + (t * drift)
                ax1.axvspan(rect_pos-5, rect_pos+5, color='green', alpha=0.1)
            ax1.axis('off')
            v_waterfall.pyplot(fig1, clear_figure=True)
            plt.close(fig1)

            # Gráfico de Potencia
            fig2, ax2 = plt.subplots(figsize=(10, 2), facecolor='black')
            ax2.plot(ruido, color='#00FF41' if not es_alien else '#ff3300', linewidth=1)
            ax2.set_facecolor('black')
            ax2.set_ylim(0, 6)
            ax2.axis('off')
            v_power.pyplot(fig2, clear_figure=True)
            plt.close(fig2)

            # Mostrar Terminal IA
            v_terminal.markdown(f'<div class="ai-terminal">{"<br>".join(st.session_state.ai_log)}</div>', unsafe_allow_html=True)
            
            # Punto 4: Bio-sensores (Descripción en tiempo real)
            if es_alien:
                v_description.markdown(f"""
                <div class="ai-description">
                    "Operador, la señal en {centro}px es de origen tecnológico. 
                    La entropía está bajando. No es un fenómeno natural. 
                    Coherencia confirmada en la línea de hidrógeno."
                </div>
                """, unsafe_allow_html=True)
            else:
                v_description.markdown("_Analizando ruido de fondo... Sin patrones inteligentes._")

            time.sleep(0.05)

        if es_alien:
            st.balloons()
            st.success(f"TECNOSIGNATURA CONFIRMADA EN {target}")

start_deep_scan()

# --- FOOTER ---
st.write("---")
st.caption("NEXUS-7 v9.0 | AI Heuristic Core | Subsidaria de Deep Space Network")
