import pygame

# Control general de sonido
sonido_activado = True

# Diccionarios de sonidos en memoria
sfx_acciones    = {}
sfx_expresiones = {}
bgm_escenarios  = {}

def init_audio():
    """Inicializa pygame.mixer."""
    try:
        pygame.mixer.init()
        pygame.mixer.set_num_channels(4)
        cargar_archivos()
        print("Motor de audio avanzado inicializado.")
    except Exception as e:
        print("Nota: pygame.mixer no se inició correctamente.", e)

def cargar_archivos():
    """Carga efectos y rutas de BGM. Fallas silenciosas si faltan archivos."""
    if not pygame.mixer.get_init():
        return

    # Efectos de acciones
    for accion, ruta in {
        "caminar": "sonidos/caminar.mp3",
        "saltar":  "sonidos/saltar.mp3",
        "brazos":  "sonidos/brazos.mp3",
        "agacharse": "sonidos/cabeza.mp3",
        "golpear": "sonidos/golpear.mp3",
    }.items():
        try: sfx_acciones[accion] = pygame.mixer.Sound(ruta)
        except: pass

    # Efectos de expresiones (1-5)
    for exp, ruta in {
        1: "sonidos/guino.mp3",
        2: "sonidos/ira.mp3",
        3: "sonidos/sonrisa.mp3",
        4: "sonidos/triste.mp3",
        5: "sonidos/sorpresa.mp3",
    }.items():
        try: sfx_expresiones[exp] = pygame.mixer.Sound(ruta)
        except: pass

    # Rutas de música de fondo por escenario
    global bgm_escenarios
    bgm_escenarios = {
        0: "sonidos/bgm_vacio.mp3",
        1: "sonidos/bgm_parque.mp3",
        2: "sonidos/bgm_callejon.mp3",
        3: "sonidos/bgm_batalla.mp3",
        4: "sonidos/bgm_aula.mp3",
        5: "sonidos/bgm_teatro.mp3",
    }

def detener_efectos():
    """Para todos los Sound (efectos), sin tocar la música de fondo."""
    if pygame.mixer.get_init():
        pygame.mixer.stop()

def play_accion(accion):
    """Reproduce el efecto de una acción (para el anterior primero)."""
    if not sonido_activado or not pygame.mixer.get_init():
        return
    detener_efectos()
    if accion in sfx_acciones:
        sfx_acciones[accion].play()

def play_expresion(expresion):
    """Reproduce el efecto de una expresión (para el anterior primero)."""
    if not sonido_activado or not pygame.mixer.get_init():
        return
    detener_efectos()
    if expresion in sfx_expresiones:
        sfx_expresiones[expresion].play()

def cambiar_bgm(escenario_id):
    """Carga y pone en loop la música del escenario indicado."""
    if not pygame.mixer.get_init():
        return
    ruta = bgm_escenarios.get(escenario_id)
    if ruta:
        try:
            pygame.mixer.music.load(ruta)
            if sonido_activado:
                pygame.mixer.music.play(-1)
        except: pass

def toggle_mute():
    """Alterna silencio global (efectos + fondo)."""
    global sonido_activado
    sonido_activado = not sonido_activado
    if not pygame.mixer.get_init():
        return
    if sonido_activado:
        pygame.mixer.music.unpause()
    else:
        detener_efectos()
        pygame.mixer.music.pause()
