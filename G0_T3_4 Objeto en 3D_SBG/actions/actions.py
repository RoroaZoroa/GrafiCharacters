import math
from audio import audio
from states import state

def actualizar_animacion(estado, app, ventana):
    estado.tiempo += 0.1

    # 1. CAMINAR — bucle continuo
    if estado.animacion_actual == "caminar":
        estado.tilt_brazo_actual = 45
        estado.pos_y_knuckles    = abs(math.sin(estado.tiempo * 2)) * 0.1
        estado.brazo_izq  = -math.sin(estado.tiempo) * 45
        estado.brazo_der  = -math.sin(estado.tiempo) * 45
        estado.pierna_izq = -math.sin(estado.tiempo) * 30
        estado.pierna_der =  math.sin(estado.tiempo) * 30

    # 2. SALTAR — un solo rebote
    elif estado.animacion_actual == "saltar":
        estado.tilt_brazo_actual = 45
        estado.tiempo_anim += 0.1
        estado.pos_y_knuckles = abs(math.sin(estado.tiempo_anim * 1.5)) * 1.8
        estado.brazo_izq = -25;  estado.brazo_der  = -25
        estado.pierna_izq = 15;  estado.pierna_der = 15
        if estado.tiempo_anim >= math.pi / 1.5:
            estado.animacion_actual = "ninguna"
            estado.expresion_actual = 0

    # 3. BRAZOS ARRIBA — celebración (bucle continuo)
    elif estado.animacion_actual == "brazos":
        estado.tilt_brazo_actual = -90 + math.sin(estado.tiempo * 2) * 10
        estado.pos_y_knuckles = 0.0
        estado.brazo_izq = estado.brazo_der = estado.pierna_izq = estado.pierna_der = 0.0

    # 4. GIRO DE CABEZA — terror (bucle continuo)
    elif estado.animacion_actual == "agacharse":
        estado.tilt_brazo_actual = 45
        estado.pos_y_knuckles = 0.0
        estado.brazo_izq = estado.brazo_der = estado.pierna_izq = estado.pierna_der = 0.0
        estado.rot_cabeza = (estado.rot_cabeza + 3) % 360

    # 5. GOLPEAR — dos trancazos
    elif estado.animacion_actual == "golpear":
        estado.tilt_brazo_actual = 45
        estado.tiempo_anim += 0.1
        estado.pos_y_knuckles = estado.pierna_izq = estado.pierna_der = 0.0
        medio = math.pi / 4
        if estado.tiempo_anim < medio:
            estado.brazo_der = -math.sin(estado.tiempo_anim / medio * math.pi) * 70
            estado.brazo_izq = 0.0
        else:
            estado.brazo_der = 0.0
            estado.brazo_izq = math.sin((estado.tiempo_anim - medio) / medio * math.pi) * 70
        if estado.tiempo_anim >= math.pi / 2:
            estado.animacion_actual = "ninguna"
            estado.expresion_actual = 0

    # 0. NINGUNA — pose en T
    else:
        estado.tilt_brazo_actual = 45
        estado.rot_cabeza = 0.0
        estado.pos_y_knuckles = estado.brazo_izq = estado.brazo_der = estado.pierna_izq = estado.pierna_der = 0.0

    app.tkExpose(None)                          # Solicita redibujado
    ventana.after(16, actualizar_animacion, estado, app, ventana)

def set_animacion(estado, anim):
    estado.animacion_actual = anim
    estado.tiempo_anim = 0.0
    estado.rot_cabeza  = 0.0
    # Expresión automática según animación
    expresion_map = {
        "caminar":   3,
        "saltar":    3,
        "brazos":    3,
        "agacharse": 5,
        "golpear":   2,
        "ninguna":   0,
    }
    estado.expresion_actual = expresion_map.get(anim, 0)
    if anim == "ninguna":
        audio.detener_efectos()
    else:
        audio.play_accion(anim)

def set_expresion(estado, exp):
    estado.expresion_actual = exp
    audio.play_expresion(exp)

def set_escenario(estado, esc):
    estado.escenario_actual = esc
    audio.cambiar_bgm(esc)

def toggle_sonido():
    audio.toggle_mute()

def teclado(event, estado, app, ventana):
    tecla = event.keysym.lower()

    # Cámara
    if   tecla == 'up':    estado.target_y -= 0.2
    elif tecla == 'down':  estado.target_y += 0.2
    elif tecla == 'left':  estado.target_x += 0.2
    elif tecla == 'right': estado.target_x -= 0.2
    elif tecla in ('plus', 'equal'): estado.radio = max(2.0, estado.radio - 0.5)
    elif tecla == 'minus':           estado.radio += 0.5
    elif tecla == 'r':
        estado.radio = 8.0; estado.theta = 0.0; estado.phi = math.pi / 2.0
        estado.target_x = estado.target_y = estado.target_z = 0.0

    # Atajos de animación
    elif tecla == 'z': set_animacion(estado, "caminar")
    elif tecla == 'x': set_animacion(estado, "saltar")
    elif tecla == 'c': set_animacion(estado, "brazos")
    elif tecla == 'v': set_animacion(estado, "agacharse")
    elif tecla == 'b': set_animacion(estado, "golpear")
    elif tecla == 'n': set_animacion(estado, "ninguna")

    # Atajos de expresión
    elif tecla in [str(i) for i in range(6)]:
        set_expresion(estado, int(tecla))

    # Escenario
    elif tecla == 't':
        set_escenario(estado, (estado.escenario_actual + 1) % 6)

    # Audio
    elif tecla == 'm': toggle_sonido()

    # Salir
    elif tecla == 'escape': ventana.quit()

    app.tkExpose(None)

def raton_presionar(event, estado):
    estado.mouse_down = True
    estado.last_x = event.x; estado.last_y = event.y

def raton_soltar(event, estado):
    estado.mouse_down = False

def raton_arrastrar(event, estado, app):
    if estado.mouse_down:
        estado.theta += (event.x - estado.last_x) * 0.01
        estado.phi   -= (event.y - estado.last_y) * 0.01
        estado.phi = max(0.1, min(math.pi - 0.1, estado.phi))
        estado.last_x = event.x; estado.last_y = event.y
        app.tkExpose(None)

def raton_rueda(event, estado, app):
    if event.delta > 0:
        estado.radio = max(2.0, estado.radio - 0.4)
    else:
        estado.radio += 0.4
    app.tkExpose(None)
