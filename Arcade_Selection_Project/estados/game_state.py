# estados/game_state.py
import random

# Catálogo de objetos para contar (variedad para que no sea repetitivo)
CATALOGO_OBJETOS = [
    {"nombre": "MANZANAS",   "color": (1.0, 0.1, 0.1),  "forma": "esfera"},
    {"nombre": "NARANJAS",   "color": (1.0, 0.5, 0.0),  "forma": "esfera"},
    {"nombre": "CUBOS",      "color": (0.2, 0.5, 1.0),  "forma": "cubo"},
    {"nombre": "ESTRELLAS",  "color": (1.0, 1.0, 0.0),  "forma": "estrella"},
    {"nombre": "DONAS",      "color": (1.0, 0.3, 0.7),  "forma": "dona"},
    {"nombre": "PLATANOS",   "color": (1.0, 0.9, 0.2),  "forma": "platano"},
    {"nombre": "DIAMANTES",  "color": (0.0, 1.0, 0.9),  "forma": "diamante"},
    {"nombre": "CORAZONES",  "color": (1.0, 0.0, 0.4),  "forma": "esfera"},
    {"nombre": "ZAPATOS",    "color": (0.5, 0.3, 0.1),  "forma": "cubo"},
    {"nombre": "MONEDAS",    "color": (1.0, 0.8, 0.0),  "forma": "dona"},
]

class GameState:
    def __init__(self):
        # Lista de personajes disponibles
        self.personajes_disponibles = ["Lumi el Ajolote", "Chef Soma", "Knuckles", "Miko el Mapache", "Pinguino Bebe", "Robot Espacial"]
        
        # Índice del personaje que está resaltado actualmente (el cursor)
        self.cursor_index = 0
        self.cursor_index_p2 = 0
        
        # Selección de jugadores
        self.jugador1_seleccion = None
        self.jugador2_seleccion = None
        
        # Empezamos en la Pantalla de Título
        # Fases: "TITULO", "SELECCION_P1", "CONFIRMAR_P1", "SELECCION_P2", "CONFIRMAR_P2", "LISTOS", "MAPA"
        self.fase_actual = "TITULO"
        
        # Animación global
        self.tiempo_global = 0.0
        self.tiempo_seleccion = 0.0 

        # Posiciones en el mapa
        self.p1_pos = [-3.0, 0.0, 8.0]
        self.p2_pos = [3.0, 0.0, 8.0]
        self.p1_rot = 0.0
        self.p2_rot = 0.0
        
        # Teclas presionadas
        self.teclas = set()
        self.map_limit = 20.0

        # ==========================================
        # 🎮 SISTEMA DE NIVELES Y PUNTAJES 
        # ==========================================
        self.p1_score = 0
        self.p2_score = 0
        self.meta_puntos = 3  # El primero en hacer 3 puntos, gana el Nivel
        
        # Variables Nivel 1 (Colisión de Cómputo)
        self.n1_target = 0
        self.n1_objetos = []
        self.n1_bloques = []
        self.n1_tipo_objeto = None  # Tipo de objeto actual del catálogo
        self.generar_nivel_1()

        # ==========================================
        # 🎮 NUEVO: VARIABLES DEL NIVEL 2 (SUMAS)
        # ==========================================
        self.n2_num1 = 0
        self.n2_num2 = 0
        self.n2_target = 0
        self.n2_bloques = []
        
        # Temporizadores de congelamiento (3 segundos de castigo)
        self.p1_stun = 0.0  
        self.p2_stun = 0.0  

    def generar_nivel_1(self):
        """Genera un nuevo acertijo matemático aleatorio con objetos variados"""
        # 1. Elegir un tipo de objeto aleatorio del catálogo
        self.n1_tipo_objeto = random.choice(CATALOGO_OBJETOS)
        
        # 2. El número que los niños deben contar (1 al 9)
        self.n1_target = random.randint(1, 9)
        
        # 3. Generar posiciones dispersas por TODO el mapa (evitando zona de cajas y spawn)
        self.n1_objetos = []
        for _ in range(self.n1_target):
            intentos = 0
            while intentos < 50:
                x = random.uniform(-15, 15)
                z = random.uniform(-8, 6)
                # Evitar zona de cajas (z < -10) y zona de spawn (z > 6)
                if z > -9 and z < 5:
                    # Evitar que queden demasiado juntos
                    demasiado_cerca = False
                    for ox, oz in self.n1_objetos:
                        if abs(x - ox) < 2.0 and abs(z - oz) < 2.0:
                            demasiado_cerca = True
                            break
                    if not demasiado_cerca:
                        self.n1_objetos.append((x, z))
                        break
                intentos += 1
            else:
                # Si no encuentra posición, poner donde se pueda
                self.n1_objetos.append((random.uniform(-14, 14), random.uniform(-7, 4)))
        
        # 4. Crear las 3 cajas de respuesta (1 correcta, 2 incorrectas)
        opciones = [self.n1_target]
        while len(opciones) < 3:
            falso = random.randint(1, 9)
            if falso not in opciones:
                opciones.append(falso)
        random.shuffle(opciones)
        
        self.n1_bloques = [
            {"x": -8, "z": -14, "val": opciones[0]},
            {"x": 0,  "z": -14, "val": opciones[1]},
            {"x": 8,  "z": -14, "val": opciones[2]}
        ]
        
        # Reposicionar jugadores a la línea de salida
        self.p1_pos = [-3.0, 0.0, 8.0]
        self.p2_pos = [3.0, 0.0, 8.0]

    def generar_nivel_2(self):
        """Genera la suma y las 3 plataformas puente para el Nivel 2"""
        self.n2_num1 = random.randint(1, 10)
        self.n2_num2 = random.randint(1, 10)
        self.n2_target = self.n2_num1 + self.n2_num2 # La respuesta correcta
        
        opciones = [self.n2_target]
        while len(opciones) < 3:
            falso = random.randint(2, 20) # Respuestas trampa
            if falso not in opciones:
                opciones.append(falso)
        random.shuffle(opciones)
        
        # Posición de las plataformas (Están más cerca para simular un puente)
        self.n2_bloques = [
            {"x": -6, "z": -5, "val": opciones[0]}, # Plataforma Izquierda
            {"x": 0,  "z": -5, "val": opciones[1]}, # Plataforma Centro
            {"x": 6,  "z": -5, "val": opciones[2]}  # Plataforma Derecha
        ]
        
        # Línea de salida para el Nivel 2
        self.p1_pos = [-3.0, 0.0, 8.0]
        self.p2_pos = [3.0, 0.0, 8.0]
