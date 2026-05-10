import pygame
import os

class SoundManager:
    def __init__(self):
        try:
            # Inicialización robusta
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.init()
            pygame.mixer.init()
            print("INFO: Pygame Mixer inicializado correctamente.")
        except Exception as e:
            print(f"ERROR: No se pudo inicializar el mezclador de audio: {e}")
            
        self.sounds = {}
        self.current_bgm = None
        
        # Mapeo de personajes a sus carpetas
        self.char_folders = {
            0: "ajolote",
            1: "chef",
            2: "knuckles",
            3: "mapache",
            4: "pinguino",
            5: "robot"
        }
        
    def load_char_sound(self, char_idx, sound_name):
        folder = self.char_folders.get(char_idx)
        if not folder:
            return None
        
        path = os.path.join("sonidos", folder, f"{sound_name}.wav")
        # Intentar ruta absoluta si relativa falla?
        if not os.path.exists(path):
            # Probar subiendo un nivel si se ejecuta desde subcarpeta
            path = os.path.join("..", "sonidos", folder, f"{sound_name}.wav")
            if not os.path.exists(path):
                return None
            
        key = f"{folder}_{sound_name}"
        if key not in self.sounds:
            try:
                self.sounds[key] = pygame.mixer.Sound(path)
                print(f"INFO: Sonido cargado: {path}")
            except Exception as e:
                print(f"ERROR cargando sonido {path}: {e}")
                return None
        return self.sounds[key]

    def play_sound(self, char_idx, sound_name, volume=0.5, loops=0):
        sound = self.load_char_sound(char_idx, sound_name)
        if sound:
            sound.set_volume(volume)
            sound.play(loops=loops)

    def play_bgm(self, char_idx):
        """Usa scenario.wav de un personaje como música de fondo"""
        folder = self.char_folders.get(char_idx)
        if not folder:
            return
            
        path = os.path.join("sonidos", folder, "scenario.wav")
        if not os.path.exists(path):
            path = os.path.join("..", "sonidos", folder, "scenario.wav")
            
        if os.path.exists(path):
            if self.current_bgm == path:
                return
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                self.current_bgm = path
                print(f"INFO: Música de fondo iniciada: {path}")
            except Exception as e:
                print(f"ERROR iniciando música {path}: {e}")

    def stop_bgm(self):
        pygame.mixer.music.stop()
        self.current_bgm = None

sound_manager = SoundManager()
