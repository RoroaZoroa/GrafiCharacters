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
    {"nombre": "CORAZONES",  "color": (1.0, 0.0, 0.4),  "forma": "corazon"},
    {"nombre": "ZAPATOS",    "color": (0.5, 0.3, 0.1),  "forma": "zapato"},
    {"nombre": "MONEDAS",    "color": (1.0, 0.8, 0.0),  "forma": "moneda"},
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
        # Fases: "TITULO", "SELECCION_P1", "CONFIRMAR_P1", "SELECCION_P2", "CONFIRMAR_P2", "LISTOS", "MAPA", "NIVEL_2", "PODIO"
        self.fase_actual = "TITULO"
        
        # Variables de PODIO
        self.ganador_nivel_actual = None
        self.siguiente_fase = None
        
        # Animación global
        self.tiempo_global = 0.0
        self.tiempo_seleccion = 0.0 

        # Posiciones en el mapa
        self.p1_pos = [-3.0, 0.0, 8.0]
        self.p2_pos = [3.0, 0.0, 8.0]
        self.p1_rot = 0.0
        self.p2_rot = 0.0
        self.map_limit = 20.0
        
        # --- SISTEMA DE PUNTUACIÓN GLOBAL ---
        self.wins_j1 = 0
        self.wins_j2 = 0
        
        # --- MEMORIA NIVEL 1 ---
        self.n1_objetos_usados = []
        
        # --- MENSAJES TEMPORALES NIVEL 3 ---
        self.n3_msg_j1 = ""
        self.n3_msg_timer_j1 = 0.0
        self.n3_msg_j2 = ""
        self.n3_msg_timer_j2 = 0.0
        
        # Teclas presionadas
        self.teclas = set()
        
        # Audio
        self.bgm_canal = None
        self.musica_actual = ""

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
        # 🎮 VARIABLES DEL NIVEL 2 (CARRERA DE SUMAS)
        # ==========================================
        self.n2_pasos_p1 = 0 # En qué paso va el jugador 1
        self.n2_pasos_p2 = 0 # En qué paso va el jugador 2
        self.n2_meta_pasos = 5 # Tienen que pasar 5 plataformas para ganar
        self.n2_pista_p1 = [] 
        self.n2_pista_p2 = []
        
        self.p1_stun = 0.0  
        self.p2_stun = 0.0  
        
        # Agrega esto donde tienes tus tiempos globales
        self.tiempo_versus = 0.0 
        
        # ==========================================
        # 🎮 VARIABLES DEL NIVEL 3 (ATRAPAR Y PICAR)
        # ==========================================
        self.n3_receta = {"Jitomate": 0, "Lechuga": 0, "Queso": 0}
        self.n3_receta_problemas = {} 
        
        # Inventarios separados: Crudos (recién atrapados) y Picados (listos para olla)
        self.n3_p1_hand = None         # Ingrediente en mano J1: None, "Jitomate", "Lechuga", "Queso", "Pollo", "Vaca"
        self.n3_p1_hand_state = "crudo" # "crudo" o "picado"
        self.n3_olla_p1 = {"Jitomate": 0, "Lechuga": 0, "Queso": 0, "Pollo": 0, "Vaca": 0, "Leche": 0}

        self.n3_p2_hand = None         # Ingrediente en mano J2
        self.n3_p2_hand_state = "crudo"
        self.n3_olla_p2 = {"Jitomate": 0, "Lechuga": 0, "Queso": 0, "Pollo": 0, "Vaca": 0, "Leche": 0}

        # Coordenadas de las zonas (Cocinas al frente, Granja al fondo)
        self.n3_tabla_p1 = {"x": -14.0, "z": 12.0}   
        self.n3_cacerola_p1 = {"x": -8.0, "z": 12.0} 
        
        self.n3_tabla_p2 = {"x": 14.0, "z": 12.0}    
        self.n3_cacerola_p2 = {"x": 8.0, "z": 12.0}  

        self.n3_p1_cooldown = 0.0
        self.n3_p2_cooldown = 0.0
        self.generar_nivel_3()

    def generar_nivel_1(self):
        """Genera un nuevo acertijo matemático aleatorio con objetos variados (sin repetir)"""
        # 1. Filtrar objetos no usados
        disponibles = [obj for obj in CATALOGO_OBJETOS if obj["nombre"] not in self.n1_objetos_usados]
        
        # Si se acabaron los objetos o queda 1 solo, reiniciar memoria
        if len(disponibles) <= 1:
            self.n1_objetos_usados = []
            disponibles = CATALOGO_OBJETOS
            
        # Elegir uno y guardarlo en memoria
        self.n1_tipo_objeto = random.choice(disponibles)
        self.n1_objetos_usados.append(self.n1_tipo_objeto["nombre"])
        
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
        """Genera una pista de 5 filas de plataformas. Cada fila es una suma."""
        self.n2_pasos_p1 = 0
        self.n2_pasos_p2 = 0
        self.n2_pista_p1 = []
        self.n2_pista_p2 = []
        
        # Generar pista para P1
        for i in range(self.n2_meta_pasos):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            target = num1 + num2
            opciones = [target]
            while len(opciones) < 3:
                falso = random.randint(2, 20)
                if falso not in opciones: opciones.append(falso)
            random.shuffle(opciones)
            self.n2_pista_p1.append({
                "n1": num1, "n2": num2, "ans": target,
                "z": 2.0 - (i * 10.0),
                "opciones": opciones
            })
            
        # Generar pista para P2 (diferente)
        for i in range(self.n2_meta_pasos):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            target = num1 + num2
            opciones = [target]
            while len(opciones) < 3:
                falso = random.randint(2, 20)
                if falso not in opciones: opciones.append(falso)
            random.shuffle(opciones)
            self.n2_pista_p2.append({
                "n1": num1, "n2": num2, "ans": target,
                "z": 2.0 - (i * 10.0),
                "opciones": opciones
            })
            
        # Línea de salida: En pantalla dividida, ambos pueden estar centrados en X=0
        self.p1_pos = [0.0, 0.0, 8.0]
        self.p2_pos = [0.0, 0.0, 8.0]
        self.p1_stun = 0.0
        self.p2_stun = 0.0
    def generar_nivel_3(self):
        # =========================================================
        # 🥛 NUEVO SISTEMA DE RECETA CON MATEMÁTICAS (RESTAS)
        # =========================================================
        tipos_disponibles = ["Jitomate", "Lechuga", "Queso", "Pollo", "Vaca", "Leche"]
        seleccionados = random.sample(tipos_disponibles, 3) # 3 ingredientes al azar
        
        self.n3_receta = {}
        self.n3_receta_problemas = {} # Guardamos: "Jitomate": (5, 3) -> 5 - 3 = 2
        
        for tipo in seleccionados:
            target = random.randint(1, 3)
            val2 = random.randint(1, 4)
            val1 = target + val2 # Así val1 - val2 = target siempre positivo
            self.n3_receta[tipo] = target
            self.n3_receta_problemas[tipo] = (val1, val2)

        # Limpiar manos y ollas
        self.n3_p1_hand = None
        self.n3_p1_hand_state = "crudo"
        self.n3_p2_hand = None
        self.n3_p2_hand_state = "crudo"

        self.n3_olla_p1 = {t: 0 for t in tipos_disponibles}
        self.n3_olla_p2 = {t: 0 for t in tipos_disponibles}
        
        # Generar ingredientes en el suelo (¡VIVOS!)
        self.n3_ingredientes = []
        # Definir zonas de establos: [min_x, max_x]
        # 6 Establos: Jitomate, Lechuga, Queso, Pollo, Vaca, Leche
        self.n3_establous_x = {
            "Jitomate": [-20, -14],
            "Lechuga": [-13, -8],
            "Queso": [-7, -1],
            "Pollo": [1, 7],
            "Vaca": [8, 13],
            "Leche": [14, 20]
        }

        for tipo in ["Jitomate", "Lechuga", "Queso", "Pollo", "Vaca"]:
            for _ in range(4): 
                z_min, z_max = -12, 4
                x_min, x_max = self.n3_establous_x[tipo]
                self.n3_ingredientes.append({
                    "x": random.uniform(x_min, x_max), "y": 0.0, "z": random.uniform(z_min, z_max),
                    "tipo": tipo, "velocidad": random.uniform(0.04, 0.08),
                    "target_x": random.uniform(x_min, x_max), "target_z": random.uniform(z_min, z_max),
                    "cooldown_giro": random.uniform(2.0, 4.0), "activo": True
                })

        # --- VACAS LECHERAS (NPCs que dan leche) ---
        self.n3_vacas_lecheras = []
        for i in range(2):
            x_min, x_max = self.n3_establous_x["Leche"]
            self.n3_vacas_lecheras.append({
                "x": random.uniform(x_min + 1, x_max - 1),
                "z": random.uniform(-10, 0),
                "rot": random.uniform(0, 360)
            })

        self.p1_pos = [-4.0, 0.0, 10.0]
        self.p2_pos = [4.0, 0.0, 10.0]
        self.p1_stun = 0.0
        self.p2_stun = 0.0
