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
        
        # Fases del menú: "INICIO", "SELECCION_P1", "CONFIRMAR_P1", "SELECCION_P2", "CONFIRMAR_P2", "LISTOS", "MAPA"
        self.fase_actual = "INICIO"
        
        # Animación global
        self.tiempo_global = 0.0
        self.tiempo_seleccion = 0.0 

        # Posiciones en el mapa
        self.p1_pos = [-2.0, 0.0, 2.0]
        self.p2_pos = [2.0, 0.0, 2.0]
        self.p1_rot = 0.0
        self.p2_rot = 0.0
        
        # Teclas presionadas
        self.teclas = set()

        # --- SISTEMA DE ESCENARIOS ---
        self.current_scenario_idx = 0
        self.scenarios = [
            {
                "name": "Pradera Verde",
                "floor_color": (0.1, 0.3, 0.1),
                "grid_color": (0.2, 0.5, 0.2),
                "obstacles": [
                    {"x": 5, "z": 5, "radius": 1.5, "type": "ROCK"},
                    {"x": -5, "z": -8, "radius": 2.0, "type": "TREE"},
                    {"x": 8, "z": -3, "radius": 1.2, "type": "ROCK"}
                ],
                "portal": {"x": 0, "z": -15, "radius": 2.0}
            },
            {
                "name": "Desierto Rojo",
                "floor_color": (0.4, 0.1, 0.0),
                "grid_color": (0.6, 0.2, 0.1),
                "obstacles": [
                    {"x": -10, "z": 5, "radius": 2.5, "type": "CACTUS"},
                    {"x": 3, "z": -4, "radius": 1.8, "type": "CACTUS"},
                    {"x": -2, "z": -12, "radius": 3.0, "type": "ROCK"}
                ],
                "portal": {"x": 15, "z": 0, "radius": 2.0}
            },
            {
                "name": "Noche Azul",
                "floor_color": (0.02, 0.02, 0.1),
                "grid_color": (0.1, 0.1, 0.3),
                "obstacles": [
                    {"x": 10, "z": -10, "radius": 4.0, "type": "MONUMENT"}, # Movido para no estorbar el spawn
                    {"x": 10, "z": 10, "radius": 1.5, "type": "ROCK"}
                ],
                "portal": {"x": -15, "z": -15, "radius": 2.0}
            }
        ]
        self.map_limit = 20.0
