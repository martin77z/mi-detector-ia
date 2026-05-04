import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# =========================================================
# 1. MOTOR DE PROCESAMIENTO DE OBJETIVOS REALES
# =========================================================
class AnalizadorRadioastronomico:
    def __init__(self):
        # Base de datos de objetivos y sus frecuencias de interés (MHz)
        self.objetivos = {
            "ROSS 128 b": {"freq": 1420.405, "tipo": "Exoplaneta", "anomalia": True},
            "ANDRÓMEDA (M31)": {"freq": 1665.402, "tipo": "Galaxia", "anomalia": True},
            "SGR A* (VÍA LÁCTEA)": {"freq": 1420.405, "tipo": "Centro Galáctico", "anomalia": False}
        }

    def obtener_espectro_real(self, nombre_objetivo):
        obj = self.objetivos.get(nombre_objetivo)
        longitud = 1024
        
        # Generación de ruido cósmico real (Ruido de Johnson-Nyquist)
        base = np.random.normal(0, 0.4, longitud)
        
        # Si el objetivo tiene una anomalía (Tecnofirma detectada en la ficción del proyecto)
        if obj["anomalia"]:
            señal = np.zeros(longitud)
            # Simulación de señal de banda estrecha real
            pos = 512 + np.random.randint(-2, 2)
            señal[pos-2:pos+2] = np.random.uniform(2.8, 4.5)
            datos = base + señal
            estado = "ANOMALÍA DETECTADA"
            confianza = np.random.uniform(98.5, 99.9)
        else:
            # Para objetivos naturales como Sgr A*, solo hay ruido y picos anchos
            pico_natural = np.exp(-np.power(np.linspace(-10, 10, longitud), 2) / (2 * 1))
            datos = base + pico_natural * 0.5
            estado = "EMISIÓN NATURAL"
            confianza = np.random.uniform(1.0, 5.0)
            
        return datos, estado, confianza, obj["freq"], obj["tipo"]

# =========================================================
# 2. INTERFAZ PROFESIONAL (ESTÉTICA 9.5)
# =========================================================
def iniciar_escaneo():
    analizador = AnalizadorRadioastronomico()
    
    # --- CONFIGURACIÓN DEL OBJETIVO ACTUAL ---
    # Cambia este nombre por cualquier de la lista: "ROSS 128 b", "ANDRÓMEDA (M31)", "SGR A* (VÍA LÁCTEA)"
    target_actual = "ROSS 128 b" 
    
    fig = plt.figure(figsize=(14, 9), facecolor='#020202')
    gs = fig.add_gridspec(2, 1, height_ratios=[1.2, 0.8])
    
    # Subplot 1: Espectro de Frecuencia
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor('black')
    
    # Subplot 2: Waterfall (Cascada de Tiempo)
    ax2 = fig.add_subplot(gs[1])
    buffer_waterfall = np.zeros((60, 1024))
    img = ax2.imshow(buffer_waterfall, aspect='auto', cmap='viridis', interpolation='gaussian')
    
    def update(frame):
        ax1.clear()
        ax1.set_facecolor('black')
        
        # Obtener datos procesados
        espectro, status, prob, f_ref, t_obj = analizador.obtener_espectro_real(target_actual)
        
        # 1. Dibujar Espectro
        ax1.plot(espectro, color='#33FF33', linewidth=1, alpha=0.8)
        ax1.fill_between(range(1024), espectro, color='#33FF33', alpha=0.1)
        ax1.set_ylim(-1, 6)
        
        # 2. Actualizar Waterfall
        nonlocal buffer_waterfall
        buffer_waterfall = np.roll(buffer_waterfall, 1, axis=0)
        buffer_waterfall[0, :] = espectro
        img.set_array(buffer_waterfall)
        
        # 3. Elementos Visuales de "9.5" (Telemetría)
        color_status = '#FF0000' if "ANOMALÍA" in status else '#33FF33'
        
        # Encabezado técnico
        header = f"TARGET: {target_actual} | CLASS: {t_obj} | REF_FREQ: {f_ref} MHz"
        ax1.set_title(header, color='white', loc='left', fontsize=12, family='monospace')
        
        # Cuadro de la IA
        telemetria = (f" [ SETI ANALYSIS ]\n"
                      f" ----------------\n"
                      f" VERDICT: {status}\n"
                      f" PROBABILITY: {prob:.4f}%\n"
                      f" GAIN: +24dB | SIG: ACTIVE")
        
        ax1.text(20, 3.8, telemetria, color='white', family='monospace',
                 bbox=dict(facecolor='black', edgecolor=color_status, boxstyle='square,pad=1'))

        # Estética de rejilla y ejes
        ax1.grid(color='#002200', linestyle='-', alpha=0.5)
        ax1.tick_params(colors='white', labelsize=8)
        
        return ax1, img

    ani = animation.FuncAnimation(fig, update, interval=80, cache_frame_data=False)
    
    print(f"Sincronizando con {target_actual}...")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    iniciar_escaneo()
