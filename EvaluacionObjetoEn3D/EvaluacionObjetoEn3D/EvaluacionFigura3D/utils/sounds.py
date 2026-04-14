# ============================================================
# sounds.py - Sistema de sonido con pygame.mixer
# ============================================================
# Genera tonos WAV programáticamente y los reproduce.
# Si pygame no está disponible, el programa funciona sin audio.
# ============================================================

import os
import struct
import wave
import math

# Intentar importar pygame para audio
_pygame_available = False
try:
    import pygame
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    _pygame_available = True
except Exception:
    print("[sounds] pygame no disponible - audio desactivado")

from actions import state

# Directorio donde se guardan los WAVs generados y los MP3 del usuario
_SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "utils", "sounds")

# Cache de sonidos cargados
_sound_cache = {}

# Sonido de escenario actual
_current_scenario_sound = None


def _ensure_dir():
    """Crea el directorio de sonidos si no existe."""
    os.makedirs(_SOUNDS_DIR, exist_ok=True)


def _generate_tone(filename, frequency, duration_ms, volume=0.5, wave_type="sine"):
    """Genera un archivo WAV con un tono simple.

    Args:
        filename: Nombre del archivo (sin ruta)
        frequency: Frecuencia en Hz
        duration_ms: Duración en milisegundos
        volume: Volumen 0.0 a 1.0
        wave_type: 'sine', 'square', 'triangle'
    """
    _ensure_dir()
    filepath = os.path.join(_SOUNDS_DIR, filename)
    if os.path.exists(filepath):
        return filepath

    sample_rate = 22050
    n_samples = int(sample_rate * duration_ms / 1000)
    amplitude = int(32767 * volume)

    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate
            if wave_type == "sine":
                val = math.sin(2 * math.pi * frequency * t)
            elif wave_type == "square":
                val = 1.0 if math.sin(2 * math.pi * frequency * t) >= 0 else -1.0
            elif wave_type == "triangle":
                val = 2 * abs(2 * (t * frequency - math.floor(t * frequency + 0.5))) - 1
            else:
                val = math.sin(2 * math.pi * frequency * t)

            # Fade in/out para evitar clicks
            fade_samples = int(sample_rate * 0.01)
            if i < fade_samples:
                val *= i / fade_samples
            elif i > n_samples - fade_samples:
                val *= (n_samples - i) / fade_samples

            sample = int(val * amplitude)
            wf.writeframes(struct.pack('<h', max(-32768, min(32767, sample))))

    return filepath


def _generate_multi_tone(filename, tones, duration_ms, volume=0.4):
    """Genera un WAV con múltiples tonos secuenciales.

    Args:
        filename: Nombre del archivo
        tones: Lista de (frequency, duration_fraction)
        duration_ms: Duración total en ms
        volume: Volumen
    """
    _ensure_dir()
    filepath = os.path.join(_SOUNDS_DIR, filename)
    if os.path.exists(filepath):
        return filepath

    sample_rate = 22050
    n_total = int(sample_rate * duration_ms / 1000)
    amplitude = int(32767 * volume)

    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        sample_idx = 0
        for freq, frac in tones:
            n_samples = int(n_total * frac)
            for i in range(n_samples):
                t = i / sample_rate
                val = math.sin(2 * math.pi * freq * t)
                fade = min(1.0, i / 200, (n_samples - i) / 200)
                sample = int(val * amplitude * fade)
                wf.writeframes(struct.pack('<h', max(-32768, min(32767, sample))))
                sample_idx += 1

    return filepath


def init_sounds():
    """Genera y carga todos los sonidos al inicio."""
    if not _pygame_available:
        return

    sounds = {
        # Movimientos (7) - cada uno con carácter único
        "jump":      lambda: _generate_multi_tone("jump.wav", [(350, 0.2), (500, 0.2), (700, 0.2), (900, 0.2), (1100, 0.2)], 350),          # Escala rápida ascendente = impulso
        "walk":      lambda: _generate_multi_tone("walk.wav", [(250, 0.2), (150, 0.15), (250, 0.2), (150, 0.15), (300, 0.15), (180, 0.15)], 400, 0.9),                                   # Pasos mecánicos rítmicos
        "spin":      lambda: _generate_multi_tone("spin.wav", [(300, 0.1), (450, 0.1), (600, 0.1), (800, 0.1), (1000, 0.1), (1200, 0.1), (1400, 0.1), (1600, 0.15), (1800, 0.15)], 500), # Espiral acelerando
        "shake":     lambda: _generate_multi_tone("shake.wav", [(500, 0.1), (200, 0.1), (500, 0.1), (200, 0.1), (500, 0.1), (200, 0.1), (500, 0.15), (200, 0.15)], 400, 0.6),          # Zigzag rápido = vibración
        "wave_arms": lambda: _generate_multi_tone("wave_arms.wav", [(800, 0.15), (600, 0.15), (800, 0.15), (600, 0.15), (900, 0.2), (700, 0.2)], 450),                                 # Vaivén animado
        "nod":       lambda: _generate_multi_tone("nod.wav", [(700, 0.3), (500, 0.3), (700, 0.4)], 350, 0.7),                                   # Cabeceo amigable
        "crouch":    lambda: _generate_multi_tone("crouch.wav", [(400, 0.3), (250, 0.3), (150, 0.4)], 400, 0.5),                             # Descenso grave = agacharse
        # Expresiones (7) - emociones contrastantes
        "happy":     lambda: _generate_multi_tone("happy.wav", [(523, 0.15), (659, 0.15), (784, 0.2), (1047, 0.2), (1318, 0.3)], 600),       # Escala mayor brillante = alegría
        "sad":       lambda: _generate_multi_tone("sad.wav", [(440, 0.25), (370, 0.25), (311, 0.25), (261, 0.25)], 800, 0.7),                # Descenso lento y suave = tristeza
        "surprised": lambda: _generate_multi_tone("surprised.wav", [(600, 0.15), (1400, 0.5), (1200, 0.35)], 350, 0.6),                      # Salto agudo repentino = sorpresa
        "angry":     lambda: _generate_multi_tone("angry.wav", [(200, 0.15), (350, 0.1), (150, 0.15), (400, 0.1), (120, 0.2), (500, 0.15), (100, 0.15)], 600, 0.8),  # Gruñido intenso
        "scared":    lambda: _generate_multi_tone("scared.wav", [(800, 0.1), (1100, 0.1), (900, 0.1), (1300, 0.1), (1000, 0.1), (1500, 0.15), (1800, 0.15), (2000, 0.2)], 550, 0.6),  # Escalofrío tembloroso
        "neutral":   lambda: _generate_tone("neutral.wav", 440, 400, 0.7, "triangle"),                                                      # Tono plano neutro
        "doubt":     lambda: _generate_multi_tone("doubt.wav", [(400, 0.3), (500, 0.3), (450, 0.4)], 450, 0.75),                             # Tono indeciso sube/baja
    }

    for name, gen_func in sounds.items():
        try:
            filepath = gen_func()
            _sound_cache[name] = pygame.mixer.Sound(filepath)
        except Exception as e:
            print(f"[sounds] Error generando {name}: {e}")

    # ─── Cargar MP3 de escenarios desde carpeta sounds/ ───
    # Coloca archivos: scenario_1.mp3, scenario_2.mp3, ... scenario_7.mp3
    _ensure_dir()
    for i in range(1, 8):
        mp3_name = f"scenario_{i}.mp3"
        mp3_path = os.path.join(_SOUNDS_DIR, mp3_name)
        if os.path.exists(mp3_path):
            try:
                _sound_cache[f"scenario_{i}"] = pygame.mixer.Sound(mp3_path)
                print(f"[sounds] Cargado: {mp3_name}")
            except Exception as e:
                print(f"[sounds] Error cargando {mp3_name}: {e}")
        else:
            print(f"[sounds] No encontrado: {mp3_name} (coloca en utils/sounds/)")


def play_sound(name):
    """Reproduce un sonido por nombre si el sonido está habilitado."""
    if not _pygame_available or not state.sound_enabled:
        return
    sound = _sound_cache.get(name)
    if sound:
        sound.play()


def play_scenario_sound(scenario_idx):
    """Reproduce el sonido del escenario actual de forma continua."""
    global _current_scenario_sound
    if not _pygame_available:
        return
        
    # Detener el sonido actual si existe
    if _current_scenario_sound:
        _current_scenario_sound.stop()
        
    name = f"scenario_{scenario_idx}"
    sound = _sound_cache.get(name)
    if sound:
        _current_scenario_sound = sound
        if state.sound_enabled:
            sound.play(loops=-1)


def toggle_sound():
    """Activa/desactiva el sonido global."""
    global _current_scenario_sound
    state.sound_enabled = not state.sound_enabled
    status = "activado" if state.sound_enabled else "desactivado"
    print(f"[sounds] Sonido {status}")
    
    if _pygame_available and _current_scenario_sound:
        if state.sound_enabled:
            _current_scenario_sound.play(loops=-1)
        else:
            _current_scenario_sound.stop()
