import pygame
import os
import sys

def ruta_absoluta(ruta_relativa):
    """Obtiene la ruta absoluta correcta para el .exe"""
    try:
        # PyInstaller crea una carpeta temporal _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no estamos en el .exe, subimos un nivel para estar en la raíz de NumyPlay
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, ruta_relativa)

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
        # Obtener la ruta absoluta de la carpeta 'sonidos' (donde está este script)
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Mapeo de personajes a sus carpetas
        self.char_folders = {
            0: "ajolote",
            1: "chef",
            2: "knuckles",
            3: "mapache",
            4: "pinguino",
            5: "robot"
        }
        
        # Mapeo de alias para nombres inconsistentes
        self.aliases = {
            "walk": ["walk", "pasos", "caminar", "caminar_loop", "walking"],
            "happy": ["happy", "saludo", "sonrisa", "feliz", "victoria", "giro", "smile"],
            "surprised": ["surprised", "sorpresa", "shock", "sorprendido"],
            "sad": ["sad", "triste", "llanto", "llorar"],
            "bgm": ["scenario", "musica_fondo", "bgm", "theme", "scenario_1", "bgm_aula"]
        }
        
    def load_char_sound(self, char_idx, sound_name):
        folder = self.char_folders.get(char_idx)
        if not folder: return None
        
        # Generar lista de posibles nombres (el original + sus alias)
        possible_names = [sound_name] + self.aliases.get(sound_name, [])
        
        for name in possible_names:
            for ext in [".wav", ".mp3"]:
                # Generar la ruta usando la nueva función ruta_absoluta
                path = ruta_absoluta(os.path.join("sonidos", folder, name + ext))
                
                if os.path.exists(path):
                    key = f"{folder}_{name}_{ext}"
                    if key not in self.sounds:
                        try:
                            self.sounds[key] = pygame.mixer.Sound(path)
                            print(f"INFO: Sonido cargado: {path}")
                        except Exception as e:
                            print(f"Error cargando {path}: {e}")
                            continue
                    return self.sounds[key]
        return None

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
            
        path = ruta_absoluta(os.path.join("sonidos", folder, "scenario.wav"))
        if not os.path.exists(path):
            # Fallback por si acaso
            path = os.path.join(self.base_path, folder, "scenario.wav")
            
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

    def play_global_bgm(self, name, loop=-1):
        """Reproduce música desde la carpeta base de sonidos/"""
        for ext in [".wav", ".mp3"]:
            path = ruta_absoluta(os.path.join("sonidos", name + ext))
            # print(f"DEBUG: Buscando BGM global en: {path}")
            if os.path.exists(path):
                if self.current_bgm == path: return
                try:
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.set_volume(1.0) # Volumen máximo para los nuevos temas
                    pygame.mixer.music.play(loop)
                    self.current_bgm = path
                    print(f"INFO: Muscia iniciada -> {os.path.basename(path)}")
                    return
                except Exception as e:
                    print(f"Error BGM global {path}: {e}")
                    pass
        # print(f"DEBUG: No se encontró BGM global para: {name}")

    def play_global_sound(self, name, volume=0.5):
        """Reproduce un efecto desde la carpeta base de sonidos/"""
        for ext in [".wav", ".mp3"]:
            path = ruta_absoluta(os.path.join("sonidos", name + ext))
            if os.path.exists(path):
                try:
                    s = pygame.mixer.Sound(path)
                    s.set_volume(volume)
                    s.play()
                    return
                except Exception as e:
                    print(f"Error sonido global {path}: {e}")
                    pass

    def is_busy(self):
        """Devuelve True si algún efecto de sonido está sonando (no incluye música)"""
        return pygame.mixer.get_busy()

sound_manager = SoundManager()
