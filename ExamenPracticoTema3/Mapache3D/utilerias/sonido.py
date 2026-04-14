import pygame
import os

class SonidoManager:
    def __init__(self):
        pygame.mixer.init()
        self.canal_efectos = pygame.mixer.Channel(0) #para efectos
        self.muted = False
        self.ruta = "utilerias/"
        
        #Lista escenarios
        self.fondos_escenarios = [
            "fondo_cerezos.mp3", 
            "fondo_picnic.mp3", 
            "fondo_bosque.mp3", 
            "fondo_lago.mp3", 
            "fondo_dulces.mp3", 
            "fondo_luciernagas.mp3", 
            "fondo_concierto.mp3"
        ]
        # Diccionario para cargar los efectos de sonido
        self.efectos = {}
        self.nombres_archivos = {
            "caminando": "caminar.mp3",
            "saltando": "saltando.mp3",
            "giro": "giro.mp3",
            "saludo": "saludo.mp3",
            "quieto": "quieto.mp3",
            "bailar": "baile.mp3",
            "aplaudir": "aplaudir.mp3",
            "normal": "normal.mp3",
            "enojado": "enojado.mp3",
            "triste": "triste.mp3",
            "sorprendido": "sorprendido.mp3",
            "dormido": "dormido.mp3",
            "guino": "guino.mp3",
            "llorando": "llorando.mp3"
        }
        self.cargar_recursos()
        self.cambiar_musica_escenario(0)


    def cargar_recursos(self):
        for clave, archivo in self.nombres_archivos.items():
            camino = os.path.join(self.ruta, archivo)
            if os.path.exists(camino):
                self.efectos[clave] = pygame.mixer.Sound(camino)


    def cambiar_musica_escenario(self, indice):
        """Carga y reproduce el fondo musical del escenario actual."""
        if self.muted: return
        try:
            archivo = self.fondos_escenarios[indice]
            ruta_completa = os.path.join(self.ruta, archivo)
            
            if os.path.exists(ruta_completa):
                pygame.mixer.music.load(ruta_completa)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1) # Loop infinito
        except Exception as e:
            print(f"No se pudo cargar el fondo {indice}: {e}")


    def reproducir_efecto(self, nombre):
        if self.muted or nombre not in self.efectos:
            return
        # Lógica de pausa: Pausamos la música de fondo
        pygame.mixer.music.pause()
        # Como usamos un canal fijo, se detiene el anterior 
        self.canal_efectos.play(self.efectos[nombre])
        

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.pause()
            pygame.mixer.stop() # Detiene todos los efectos actuales
        else:
            pygame.mixer.music.unpause()


    def update(self):
        if not self.muted:
            # Si no hay ningún canal de efectos sonando, reanudamos el fondo
            if not pygame.mixer.get_busy():
                pygame.mixer.music.unpause()
    

    def detener_todo(self):
        self.canal_efectos.stop() # Detiene el efecto actual
        if not self.muted:
            pygame.mixer.music.unpause()
    
    def reiniciar_fondo(self):
        """Revisa si el canal de efectos terminó para regresar la música de fondo."""
        if not self.muted:
            pygame.mixer.music.play(-1)