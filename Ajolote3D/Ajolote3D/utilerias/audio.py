import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sonido_habilitado = True # Este es el interruptor maestro
        self.efectos = {}
        
        rutas = {
            "enojo": "utilerias/enojo.mp3",
            "triste": "utilerias/triste.mp3",
            "guino": "utilerias/guino.mp3",
            "sorpresa": "utilerias/sorpresa.mp3",
            "pasos": "utilerias/pasos.mp3",
            "salto": "utilerias/salto.mp3",
            "saludo": "utilerias/saludo.mp3",
            "giro": "utilerias/giro.mp3"
        }

        for nombre, ruta in rutas.items():
            if os.path.exists(ruta):
                self.efectos[nombre] = pygame.mixer.Sound(ruta)

        self.ruta_fondo = "utilerias/musica_fondo.mp3"

    def reproducir_fondo(self):
        # Solo suena si el usuario no dio "Mute" con la N
        if self.sonido_habilitado and os.path.exists(self.ruta_fondo):
            pygame.mixer.music.load(self.ruta_fondo)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

    def detener_musica(self):
        pygame.mixer.music.stop()

    def reproducir_efecto(self, nombre):
        # CRUCIAL: Solo suena si el sonido NO está muteado
        if self.sonido_habilitado and nombre in self.efectos:
            self.detener_musica() 
            self.efectos[nombre].play()

    def toggle_mute(self):
        self.sonido_habilitado = not self.sonido_habilitado
        if not self.sonido_habilitado:
            pygame.mixer.music.pause()
            pygame.mixer.stop() # Detiene efectos que estén sonando
        else:
            pygame.mixer.music.unpause()