# estados/game_state.py

class GameState:
    def __init__(self):
        # Lista de personajes disponibles
        self.personajes_disponibles = ["Ajolote", "Chef", "Knuckles", "Mapache", "Pinguino", "Robot"]
        
        # Índice del personaje que está resaltado actualmente (el cursor)
        self.cursor_index = 0
        self.cursor_index_p2 = 0
        
        # Selección de jugadores
        self.jugador1_seleccion = None
        self.jugador2_seleccion = None
        
        # Fases del menú: "SELECCION_P1", "CONFIRMAR_P1", "SELECCION_P2", "CONFIRMAR_P2", "LISTOS"
        self.fase_actual = "SELECCION_P1"
        
        # Animación global para que todos los personajes respiren o se muevan un poco
        self.tiempo_global = 0.0
        self.tiempo_seleccion = 0.0  # <--- NUEVO: Cronómetro para el salto único
