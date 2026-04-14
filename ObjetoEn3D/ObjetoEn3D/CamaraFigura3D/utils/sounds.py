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

# Directorio donde se guardan los WAVs generados
_SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "utils", "sounds")

# Cache de sonidos cargados
_sound_cache = {}


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
        "jump":     lambda: _generate_multi_tone("jump.wav", [(400, 0.3), (600, 0.3), (800, 0.4)], 300),
        "happy":    lambda: _generate_multi_tone("happy.wav", [(523, 0.25), (659, 0.25), (784, 0.25), (1047, 0.25)], 500),
        "sad":      lambda: _generate_multi_tone("sad.wav", [(400, 0.4), (350, 0.3), (300, 0.3)], 600),
        "walk":     lambda: _generate_tone("walk.wav", 150, 150, 0.3, "square"),
        "scenario": lambda: _generate_multi_tone("scenario.wav", [(600, 0.5), (800, 0.5)], 250),
        "spin":     lambda: _generate_multi_tone("spin.wav", [(300, 0.2), (400, 0.2), (500, 0.2), (600, 0.2), (700, 0.2)], 400),
        "scared":   lambda: _generate_multi_tone("scared.wav", [(800, 0.3), (600, 0.3), (900, 0.4)], 350),
        "angry":    lambda: _generate_tone("angry.wav", 200, 400, 0.5, "square"),
        "surprised": lambda: _generate_multi_tone("surprised.wav", [(400, 0.2), (800, 0.4), (1200, 0.3), (600, 0.2)], 800),
        "neutral":  lambda: _generate_tone("neutral.wav", 440, 200, 0.15, "sine"),
        "shake":    lambda: _generate_multi_tone("shake.wav", [(150, 0.3), (100, 0.4), (200, 0.3)], 600),
        "wave_arms": lambda: _generate_multi_tone("wave_arms.wav", [(300, 0.2), (500, 0.3), (400, 0.2), (600, 0.3)], 700),
    }

    for name, gen_func in sounds.items():
        try:
            filepath = gen_func()
            _sound_cache[name] = pygame.mixer.Sound(filepath)
        except Exception as e:
            print(f"[sounds] Error generando {name}: {e}")


def play_sound(name):
    """Reproduce un sonido por nombre si el sonido está habilitado."""
    if not _pygame_available or not state.sound_enabled:
        return
    sound = _sound_cache.get(name)
    if sound:
        sound.play()


def toggle_sound():
    """Activa/desactiva el sonido global."""
    state.sound_enabled = not state.sound_enabled
    status = "activado" if state.sound_enabled else "desactivado"
    print(f"[sounds] Sonido {status}")
