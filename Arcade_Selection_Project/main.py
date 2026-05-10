# main.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

from estados.game_state import GameState

try:
    import personajes.ajolote as ajolote
    import personajes.chef as chef
    import personajes.knuckles as knuckles
    import personajes.mapache as mapache
    import personajes.pinguino as pinguino
    import personajes.robot as robot
    from personajes.manager import manager
    from sonidos.sound_manager import sound_manager
except ImportError as e:
    print(f"Advertencia al importar: {e}")


estado = GameState()

# =====================================================================
# 🛠️ PANEL MAESTRO DE AJUSTES 🛠️
# =====================================================================
ESCALAS = {
    0: (1.5, 1.5, 1.5),     # Ajolote
    1: (0.6, 0.45, 0.6),    # Chef 
    2: (0.9, 0.75, 0.9),    # Knuckles
    3: (1.5, 1.5, 1.5),     # Mapache
    4: (1.5, 1.5, 1.5),     # Pinguino
    5: (1.5, 1.5, 1.5)      # Robot
}

ALTURAS = {
    0: -0.5,  # Ajolote
    1: -1.7,  # Chef
    2: -0.3,  # Knuckles
    3: -0.9,  # Mapache
    4: -0.9,  # Pinguino
    5: -1.2   # Robot
}

ROTACIONES_Y = {
    0: 0.0,   
    1: 180.0, 
    2: 0.0,   
    3: 0.0,   
    4: 0.0,   
    5: 0.0    
}

INFO_PERSONAJES = {
    0: ["Lumi el Ajolote", "Acuatico / Curacion", "Mascota Tierna", "W,A,S,D: Movimiento", "1-5: Expresiones Faciales"],
    1: ["Chef Soma", "Fuego / Cocina", "Humano Agil", "W,A,S,D: Mover en cocina", "E: Cocinar / X: Expresion"],
    2: ["Knuckles", "Fuerza / Tierra", "Guerrero Echidna", "Z,X: Caminar y Saltar", "B: Golpear / C: Brazos arriba"],
    3: ["Miko el Mapache", "Agilidad / Bosque", "Bailarin Experto", "Flechas: Caminar", "Z,X,C: Acciones / 1-7: Caras"],
    4: ["Pinguino Bebe", "Hielo / Nieve", "Resistencia Fria", "W: Caminar / J: Saltar", "S: Temblar / Y,T,U: Caras"],
    5: ["Robot Espacial", "Metal / Energia", "Explorador", "W: Caminar / J: Saltar", "E,X: Mover brazos / Saludar"]
}
# =====================================================================

def init():
    glClearColor(0.02, 0.02, 0.05, 1.0) # Fondo ligeramente más azulado/oscuro
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 5.0, 10.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

def dibujar_modelo(indice):
    """Dibuja el modelo del personaje usando los wrappers neutrales de cada módulo."""
    try:
        if indice == 0: ajolote.draw_axolotl_full(ajolote.state)
        elif indice == 1: chef.get_chef().draw()
        elif indice == 2: 
            # Dibujar a Knuckles con animación de golpes y caminata
            p = manager.knuckles_anim["punch"]
            wc = manager.knuckles_anim["walk_cycle"]
            rot_b = math.sin(p) * 60 if p > 0 else 0
            rot_p = math.sin(wc) * 30
            knuckles.draw_knuckles_full(
                rot_brazo_i=rot_b, rot_brazo_d=-rot_b, 
                rot_pierna_i=rot_p, rot_pierna_d=-rot_p,
                expresion=manager.knuckles_anim["expresion"]
            )
        elif indice == 3: mapache.draw_miko(mapache.state)
        elif indice == 4: pinguino.draw_penguin_full()
        elif indice == 5: robot.draw_robot_full()
    except Exception as e:
        print(f"Error dibujando personaje {indice}: {e}")
        glutSolidTeapot(1.0)

def dibujar_personaje(indice, tipo_vista, x, z):
    glPushMatrix()
    glTranslatef(x, 0.0, z)

    if tipo_vista == "centro":
        # 1. PLATAFORMA NEON
        glPushMatrix()
        glColor3f(0.0, 0.8, 1.0) 
        glTranslatef(0, -2.0, 0) 
        glScalef(3.5, 0.2, 3.5)
        glutSolidCube(1.0)
        glPopMatrix()

        # 2. ANIMACIÓN DE ENTRADA
        if estado.tiempo_seleccion <= 1.0:
            progreso = estado.tiempo_seleccion
            salto = math.sin(progreso * math.pi) * 2.5
            giro_animacion = progreso * 360
        else:
            salto = 0.0 
            giro_animacion = 0.0

        glTranslatef(0, salto, 0)
        glRotatef(giro_animacion, 0, 1, 0)

        # 3. ILUMINACIÓN Y COLOR FULL
        glEnable(GL_LIGHTING)
        glTranslatef(0, ALTURAS[indice], 0)
        glRotatef(ROTACIONES_Y[indice], 0, 1, 0)
        
        sx, sy, sz = ESCALAS[indice]
        glScalef(sx, sy, sz)

        glColor3f(1.0, 1.0, 1.0)
        # El ajolote necesita lighting OFF para su look Minecraft plano
        if indice == 0:
            glDisable(GL_LIGHTING)
        dibujar_modelo(indice)
        if indice == 0:
            glEnable(GL_LIGHTING)

    else:
        # 4. MODO SILUETA: Lighting ON pero luz a CERO + COLOR_MATERIAL OFF
        #    Así los glColor3f internos de cada módulo NO afectan el resultado.
        glDisable(GL_COLOR_MATERIAL)  # glColor ya no cambia materiales
        
        # Guardar luz original y poner todo a negro
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
        
        # Material: todo negro con emisión mínima para ver la forma
        negro = [0.0, 0.0, 0.0, 1.0]
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, negro)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, negro)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, negro)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.04, 0.04, 0.08, 1.0])
        
        glPushMatrix()
        glTranslatef(0, -1.5 + ALTURAS[indice], 0) 
        glRotatef(ROTACIONES_Y[indice], 0, 1, 0)
        
        sx, sy, sz = ESCALAS[indice]
        glScalef(sx * 0.7, sy * 0.7, sz * 0.7)
        
        glColor3f(0.03, 0.03, 0.06)
        dibujar_modelo(indice)
        glPopMatrix()
        
        # Restaurar luz y estado OpenGL
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_LIGHTING)

    glPopMatrix()

def draw_text_centered(y, text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    """Dibuja texto centrado horizontalmente de forma automática"""
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w_win, 0, h_win)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Estimación de ancho para centrar (aprox 15px por letra en Times 24)
    ancho_aprox = len(text) * 14
    x = (w_win - ancho_aprox) / 2
    
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
        
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_LIGHTING)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    if estado.fase_actual == "INICIO":
        draw_start_screen()
    elif estado.fase_actual == "MAPA":
        # Cámara que sigue el punto medio entre ambos jugadores
        mid_x = (estado.p1_pos[0] + estado.p2_pos[0]) / 2
        mid_z = (estado.p1_pos[2] + estado.p2_pos[2]) / 2
        
        # Limitamos la distancia de la cámara para no perder de vista el mapa
        cam_y = 12.0
        cam_z = mid_z + 18.0
        
        gluLookAt(mid_x, cam_y, cam_z,   
                  mid_x, 0.0, mid_z,    
                  0.0, 1.0, 0.0)
    else:
        # Cámara de selección
        gluLookAt(0.0, 1.5, 9.0,   
                  0.0, 0.0, 0.0,    
                  0.0, 1.0, 0.0)    
              
    idx_p1 = estado.cursor_index
    idx_p2 = estado.cursor_index_p2
    
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    if estado.fase_actual in ["SELECCION_P1", "CONFIRMAR_P1"]:
        datos = INFO_PERSONAJES[idx_p1]
        # Carrusel Jugador 1
        idx_izq = (idx_p1 - 1) % 6
        idx_der = (idx_p1 + 1) % 6
        
        dibujar_personaje(idx_izq, "silueta", -6.0, -3.0)
        dibujar_personaje(idx_der, "silueta", 6.0, -3.0)
        dibujar_personaje(idx_p1, "centro", 0.0, 0.0)
        
        glColor3f(1.0, 1.0, 1.0)
        txt = f"JUGADOR 1: {datos[0].upper()}" if estado.fase_actual == "SELECCION_P1" else f"¿ELEGIR A {datos[0].upper()}?"
        draw_text_centered(h - 60, txt, GLUT_BITMAP_TIMES_ROMAN_24)
        
        if estado.fase_actual == "CONFIRMAR_P1":
            glColor3f(0.0, 0.9, 1.0)
            draw_text_centered(h - 110, f"{datos[1]} | {datos[2]}", GLUT_BITMAP_HELVETICA_18)
            glColor3f(0.2, 1.0, 0.2)
            draw_text_centered(100, "[ ENTER ] PARA CONFIRMAR JUGADOR 1", GLUT_BITMAP_TIMES_ROMAN_24)

    elif estado.fase_actual in ["SELECCION_P2", "CONFIRMAR_P2"]:
        datos = INFO_PERSONAJES[idx_p2]
        # Carrusel Jugador 2 (Saltando al P1)
        idx_izq = (idx_p2 - 1) % 6
        if idx_izq == estado.jugador1_seleccion:
            idx_izq = (idx_izq - 1) % 6
            
        idx_der = (idx_p2 + 1) % 6
        if idx_der == estado.jugador1_seleccion:
            idx_der = (idx_der + 1) % 6
        
        dibujar_personaje(idx_izq, "silueta", -6.0, -3.0)
        dibujar_personaje(idx_der, "silueta", 6.0, -3.0)
        dibujar_personaje(idx_p2, "centro", 0.0, 0.0)
        
        glColor3f(1.0, 1.0, 1.0)
        txt = f"JUGADOR 2: {datos[0].upper()}" if estado.fase_actual == "SELECCION_P2" else f"¿ELEGIR A {datos[0].upper()}?"
        draw_text_centered(h - 60, txt, GLUT_BITMAP_TIMES_ROMAN_24)
        
        if estado.fase_actual == "CONFIRMAR_P2":
            glColor3f(0.0, 0.9, 1.0)
            draw_text_centered(h - 110, f"{datos[1]} | {datos[2]}", GLUT_BITMAP_HELVETICA_18)
            glColor3f(0.2, 1.0, 0.2)
            draw_text_centered(100, "[ ENTER ] PARA CONFIRMAR JUGADOR 2", GLUT_BITMAP_TIMES_ROMAN_24)

    elif estado.fase_actual == "LISTOS":
        # Mostrar ambos personajes seleccionados
        p1_idx = estado.jugador1_seleccion
        p2_idx = estado.jugador2_seleccion
        
        dibujar_personaje(p1_idx, "centro", -3.0, 0.0)
        dibujar_personaje(p2_idx, "centro", 3.0, 0.0)
        
        glColor3f(0.2, 1.0, 0.2)
        draw_text_centered(h - 100, "¡AMBOS JUGADORES LISTOS!", GLUT_BITMAP_TIMES_ROMAN_24)
        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 150, "Presiona [ ENTER ] para jugar en el mapa", GLUT_BITMAP_HELVETICA_18)
        draw_text_centered(50, "Presiona [ ESC ] para reiniciar", GLUT_BITMAP_HELVETICA_18)

    elif estado.fase_actual == "MAPA":
        draw_map()
        
        # Dibujar Jugador 1
        glPushMatrix()
        glTranslatef(estado.p1_pos[0], estado.p1_pos[1], estado.p1_pos[2])
        glRotatef(estado.p1_rot, 0, 1, 0)
        dibujar_modelo_en_mapa(estado.jugador1_seleccion)
        glPopMatrix()
        
        # Dibujar Jugador 2
        glPushMatrix()
        glTranslatef(estado.p2_pos[0], estado.p2_pos[1], estado.p2_pos[2])
        glRotatef(estado.p2_rot, 0, 1, 0)
        dibujar_modelo_en_mapa(estado.jugador2_seleccion)
        glPopMatrix()

    glutSwapBuffers()

def draw_start_screen():
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST) # Asegurar que el fondo 2D se vea siempre
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w_win, 0, h_win)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Fondo
    glBegin(GL_QUADS)
    glColor3f(0.02, 0.02, 0.08)
    glVertex2f(0, 0)
    glVertex2f(w_win, 0)
    glVertex2f(w_win, h_win)
    glVertex2f(0, h_win)
    glEnd()
    
    # Texto
    glColor3f(1.0, 1.0, 1.0)
    # Título solicitado: Numy Play
    draw_text_centered(h_win // 2 + 50, "NUMY PLAY", GLUT_BITMAP_TIMES_ROMAN_24)
    
    if int(estado.tiempo_global * 2) % 2 == 0:
        glColor3f(0.0, 0.8, 1.0)
        draw_text_centered(h_win // 2 - 50, "Presiona [ ENTER ] para comenzar", GLUT_BITMAP_HELVETICA_18)
    
    # Restaurar estados
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def dibujar_modelo_en_mapa(indice):
    glPushMatrix()
    glTranslatef(0, ALTURAS[indice], 0)
    glRotatef(ROTACIONES_Y[indice], 0, 1, 0)
    sx, sy, sz = ESCALAS[indice]
    glScalef(sx, sy, sz)
    if indice == 0: glDisable(GL_LIGHTING)
    dibujar_modelo(indice)
    if indice == 0: glEnable(GL_LIGHTING)
    glPopMatrix()

def draw_map():
    scenario = estado.scenarios[estado.current_scenario_idx]
    
    # Suelo dinámico
    glDisable(GL_LIGHTING)
    glBegin(GL_QUADS)
    glColor3f(*scenario["floor_color"])
    limit = estado.map_limit
    glVertex3f(-limit, -2, -limit)
    glVertex3f(limit, -2, -limit)
    glVertex3f(limit, -2, limit)
    glVertex3f(-limit, -2, limit)
    glEnd()
    
    # Cuadrícula dinámica
    glColor3f(*scenario["grid_color"])
    glBegin(GL_LINES)
    for i in range(-int(limit), int(limit) + 1):
        glVertex3f(i, -1.99, -limit)
        glVertex3f(i, -1.99, limit)
        glVertex3f(-limit, -1.99, i)
        glVertex3f(limit, -1.99, i)
    glEnd()
    glEnable(GL_LIGHTING)
    
    # Dibujar Obstáculos
    for obs in scenario["obstacles"]:
        dibujar_obstaculo(obs)
        
    # Dibujar Portal
    dibujar_portal(scenario["portal"])

def dibujar_obstaculo(obs):
    glPushMatrix()
    glTranslatef(obs["x"], -2.0, obs["z"])
    
    if obs["type"] == "ROCK":
        glColor3f(0.4, 0.4, 0.4)
        glScalef(1.0, 0.8, 1.0)
        glutSolidSphere(obs["radius"], 16, 16)
    elif obs["type"] == "TREE" or obs["type"] == "CACTUS":
        # Tronco / Base
        glColor3f(0.4, 0.2, 0.0) if obs["type"] == "TREE" else glColor3f(0.0, 0.5, 0.0)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        q = gluNewQuadric()
        gluCylinder(q, 0.5, 0.5, 3.0, 16, 1)
        glPopMatrix()
        # Copa / Ramas
        if obs["type"] == "TREE":
            glColor3f(0.1, 0.5, 0.1)
            glTranslatef(0, 3.0, 0)
            glutSolidSphere(obs["radius"], 16, 16)
    elif obs["type"] == "MONUMENT":
        glColor3f(0.6, 0.6, 0.7)
        glPushMatrix()
        glScalef(1.0, 4.0, 1.0)
        glutSolidCube(obs["radius"])
        glPopMatrix()
        
    glPopMatrix()

def dibujar_portal(portal):
    glPushMatrix()
    glTranslatef(portal["x"], -1.9, portal["z"])
    
    # Efecto de portal giratorio
    glRotatef(estado.tiempo_global * 100, 0, 1, 0)
    
    # Borde exterior
    glColor3f(0.5, 0.0, 1.0)
    glutSolidTorus(0.2, portal["radius"], 16, 32)
    
    # Núcleo brillante
    glDisable(GL_LIGHTING)
    glColor3f(0.8, 0.5, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(37):
        ang = math.radians(i * 10)
        glVertex3f(math.sin(ang) * portal["radius"], 0, math.cos(ang) * portal["radius"])
    glEnd()
    glEnable(GL_LIGHTING)
    
    glPopMatrix()

def teclado_normal(key, x, y):
    key = key.lower()
    if key == b'\r': # Enter
        if estado.fase_actual == "INICIO":
            estado.fase_actual = "SELECCION_P1"
            sound_manager.play_sound(0, "happy") # Sonido de inicio
        elif estado.fase_actual == "SELECCION_P1":
            manager.trigger_characteristic_anim(estado.cursor_index)
            estado.fase_actual = "CONFIRMAR_P1"
            sound_manager.play_sound(estado.cursor_index, "happy")
        elif estado.fase_actual == "CONFIRMAR_P1":
            manager.stop_characteristic_anim(estado.cursor_index)
            estado.jugador1_seleccion = estado.cursor_index
            estado.fase_actual = "SELECCION_P2"
            # Si el cursor de P2 cae en la selección de P1, saltar al siguiente
            if estado.cursor_index_p2 == estado.jugador1_seleccion:
                estado.cursor_index_p2 = (estado.cursor_index_p2 + 1) % 6
            sound_manager.play_sound(estado.jugador1_seleccion, "surprised")
        elif estado.fase_actual == "SELECCION_P2":
            manager.trigger_characteristic_anim(estado.cursor_index_p2)
            estado.fase_actual = "CONFIRMAR_P2"
            sound_manager.play_sound(estado.cursor_index_p2, "happy")
        elif estado.fase_actual == "CONFIRMAR_P2":
            manager.stop_characteristic_anim(estado.cursor_index_p2)
            estado.jugador2_seleccion = estado.cursor_index_p2
            estado.fase_actual = "LISTOS"
            sound_manager.play_sound(estado.jugador2_seleccion, "happy")
        elif estado.fase_actual == "LISTOS":
            estado.fase_actual = "MAPA"
            # Iniciar música de fondo (usamos la del P1 por ejemplo)
            sound_manager.play_bgm(estado.jugador1_seleccion)
            
    elif key == b'\x1b': # Esc
        if estado.fase_actual == "CONFIRMAR_P1":
            manager.stop_characteristic_anim(estado.cursor_index)
            estado.fase_actual = "SELECCION_P1"
        elif estado.fase_actual == "SELECCION_P2":
            estado.fase_actual = "SELECCION_P1"
        elif estado.fase_actual == "CONFIRMAR_P2":
            manager.stop_characteristic_anim(estado.cursor_index_p2)
            estado.fase_actual = "SELECCION_P2"
        elif estado.fase_actual == "LISTOS":
            estado.fase_actual = "SELECCION_P1"
            sound_manager.stop_bgm()
        elif estado.fase_actual == "MAPA":
            estado.fase_actual = "SELECCION_P1"
            sound_manager.stop_bgm()
            # Resetear posiciones
            estado.p1_pos = [-2.0, 0.0, 0.0]
            estado.p2_pos = [2.0, 0.0, 0.0]

    # Controles de navegación P1 (WASD)
    if estado.fase_actual == "SELECCION_P1":
        if key == b'a':
            estado.cursor_index = (estado.cursor_index - 1) % 6
            estado.tiempo_seleccion = 0.0
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)
        elif key == b'd':
            estado.cursor_index = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)

    if estado.fase_actual == "MAPA":
        estado.teclas.add(key)
            
    glutPostRedisplay()

def teclado_arriba(key, x, y):
    key = key.lower()
    if estado.fase_actual == "MAPA":
        if key in estado.teclas:
            estado.teclas.remove(key)
    glutPostRedisplay()

def teclado_especial(key, x, y):
    # Controles de navegación P2 (Arrows)
    if estado.fase_actual == "SELECCION_P2":
        if key == GLUT_KEY_LEFT:
            estado.cursor_index_p2 = (estado.cursor_index_p2 - 1) % 6
            # Saltar personaje de P1
            if estado.cursor_index_p2 == estado.jugador1_seleccion:
                estado.cursor_index_p2 = (estado.cursor_index_p2 - 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index_p2, "walk", volume=0.3)
        elif key == GLUT_KEY_RIGHT:
            estado.cursor_index_p2 = (estado.cursor_index_p2 + 1) % 6
            # Saltar personaje de P1
            if estado.cursor_index_p2 == estado.jugador1_seleccion:
                estado.cursor_index_p2 = (estado.cursor_index_p2 + 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index_p2, "walk", volume=0.3)
    
    # También permitir flechas para P1 si está en su fase
    elif estado.fase_actual == "SELECCION_P1":
        if key == GLUT_KEY_LEFT:
            estado.cursor_index = (estado.cursor_index - 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)
        elif key == GLUT_KEY_RIGHT:
            estado.cursor_index = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)
    
    if estado.fase_actual == "MAPA":
        estado.teclas.add(key)
            
    glutPostRedisplay()

def teclado_especial_arriba(key, x, y):
    if estado.fase_actual == "MAPA":
        if key in estado.teclas:
            estado.teclas.remove(key)
    glutPostRedisplay()

def animacion():
    dt = 0.016
    estado.tiempo_global += dt
    manager.update(dt)
    
    if estado.tiempo_seleccion <= 1.0:
        estado.tiempo_seleccion += 0.007
    else:
        estado.tiempo_seleccion = 1.01 
    
    if estado.fase_actual == "MAPA":
        mover_jugadores(dt)
        
    glutPostRedisplay()

def mover_jugadores(dt):
    # Velocidad reducida considerablemente (era 5.0 * dt)
    vel = 3.5 * dt
    radio_col = 1.2
    
    # Player 1 (WASD)
    moliendo_p1 = False
    next_p1 = list(estado.p1_pos)
    
    if b'w' in estado.teclas:
        next_p1[2] -= vel
        estado.p1_rot = 180
        moliendo_p1 = True
    if b's' in estado.teclas:
        next_p1[2] += vel
        estado.p1_rot = 0
        moliendo_p1 = True
    if b'a' in estado.teclas:
        next_p1[0] -= vel
        estado.p1_rot = 270
        moliendo_p1 = True
    if b'd' in estado.teclas:
        next_p1[0] += vel
        estado.p1_rot = 90
        moliendo_p1 = True
        
    if not check_collision(next_p1, radio_col):
        estado.p1_pos = next_p1
        check_portal(estado.p1_pos)
        
    manager.set_walking(estado.jugador1_seleccion, moliendo_p1)
    
    # Player 2 (Arrows)
    moliendo_p2 = False
    next_p2 = list(estado.p2_pos)
    
    if GLUT_KEY_UP in estado.teclas:
        next_p2[2] -= vel
        estado.p2_rot = 180
        moliendo_p2 = True
    if GLUT_KEY_DOWN in estado.teclas:
        next_p2[2] += vel
        estado.p2_rot = 0
        moliendo_p2 = True
    if GLUT_KEY_LEFT in estado.teclas:
        next_p2[0] -= vel
        estado.p2_rot = 270
        moliendo_p2 = True
    if GLUT_KEY_RIGHT in estado.teclas:
        next_p2[0] += vel
        estado.p2_rot = 90
        moliendo_p2 = True

    if not check_collision(next_p2, radio_col):
        estado.p2_pos = next_p2
        check_portal(estado.p2_pos)

    manager.set_walking(estado.jugador2_seleccion, moliendo_p2)

def check_collision(pos, radius):
    limit = estado.map_limit - 1.0
    # Límites del mapa
    if abs(pos[0]) > limit or abs(pos[2]) > limit:
        return True
        
    # Obstáculos del escenario actual
    scenario = estado.scenarios[estado.current_scenario_idx]
    for obs in scenario["obstacles"]:
        dx = pos[0] - obs["x"]
        dz = pos[2] - obs["z"]
        dist = math.sqrt(dx*dx + dz*dz)
        if dist < (radius + obs["radius"]):
            return True
    return False

def check_portal(pos):
    scenario = estado.scenarios[estado.current_scenario_idx]
    portal = scenario["portal"]
    dx = pos[0] - portal["x"]
    dz = pos[2] - portal["z"]
    dist = math.sqrt(dx*dx + dz*dz)
    
    if dist < portal["radius"]:
        # Cambiar de escenario
        estado.current_scenario_idx = (estado.current_scenario_idx + 1) % len(estado.scenarios)
        # Reposicionar jugadores en una zona segura (un poco lejos del centro para evitar colisión con posibles monumentos)
        estado.p1_pos = [-5.0, 0.0, 5.0]
        estado.p2_pos = [5.0, 0.0, 5.0]
        # Sonido de "portal"
        sound_manager.play_sound(estado.jugador1_seleccion, "surprised")
        sound_manager.play_bgm(estado.jugador1_seleccion) # Reiniciar música

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1280, 720) 
    glutCreateWindow(b"Numy Play - Arcade Selection")
    
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado_normal)
    glutKeyboardUpFunc(teclado_arriba)
    glutSpecialFunc(teclado_especial)
    glutSpecialUpFunc(teclado_especial_arriba)
    glutIdleFunc(animacion)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
