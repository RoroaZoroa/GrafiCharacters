# main.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import random

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

# === DATOS DE ESTRELLAS PARA PANTALLA DE TÍTULO ===
random.seed(42)  # Semilla fija para que siempre se vean igual
title_stars = []
for _ in range(150):
    title_stars.append({
        "x": random.uniform(0, 1),    # Posición normalizada (0-1)
        "y": random.uniform(0, 1),
        "speed": random.uniform(0.02, 0.12),  # Velocidad de movimiento
        "size": random.uniform(1.0, 3.5),      # Tamaño del punto
        "brightness": random.uniform(0.3, 1.0) # Brillo
    })

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

def draw_arrow_keys(cx, cy):
    """Dibuja 4 teclas de flechas como iconos en 2D"""
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w_win, 0, h_win)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    s = 20  # Tamaño de cada tecla
    gap = 4  # Espacio entre teclas
    
    # Posiciones: arriba-centro, izq-abajo, centro-abajo, der-abajo
    keys = [
        (cx + s + gap, cy + s + gap, "up"),
        (cx,           cy,           "left"),
        (cx + s + gap, cy,           "down"),
        (cx + (s + gap) * 2, cy,     "right"),
    ]
    
    for kx, ky, direction in keys:
        # Fondo de la tecla
        glColor3f(0.15, 0.15, 0.25)
        glBegin(GL_QUADS)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Borde de la tecla
        glColor3f(0.4, 0.7, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Flecha (triángulo grande y visible)
        mx = kx + s / 2
        my = ky + s / 2
        a = 6
        
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        if direction == "up":
            glVertex2f(mx, my + a)
            glVertex2f(mx - a, my - a)
            glVertex2f(mx + a, my - a)
        elif direction == "down":
            glVertex2f(mx, my - a)
            glVertex2f(mx - a, my + a)
            glVertex2f(mx + a, my + a)
        elif direction == "left":
            glVertex2f(mx - a, my)
            glVertex2f(mx + a, my + a)
            glVertex2f(mx + a, my - a)
        elif direction == "right":
            glVertex2f(mx + a, my)
            glVertex2f(mx - a, my + a)
            glVertex2f(mx - a, my - a)
        glEnd()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_wasd_keys(cx, cy):
    """Dibuja 4 teclas WASD como iconos en 2D"""
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w_win, 0, h_win)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    s = 20  # Tamaño de cada tecla
    gap = 4  # Espacio entre teclas
    
    # Posiciones: W arriba-centro, A izq-abajo, S centro-abajo, D der-abajo
    keys = [
        (cx + s + gap, cy + s + gap, "W"),
        (cx,           cy,           "A"),
        (cx + s + gap, cy,           "S"),
        (cx + (s + gap) * 2, cy,     "D"),
    ]
    
    for kx, ky, letra in keys:
        # Fondo de la tecla
        glColor3f(0.15, 0.15, 0.25)
        glBegin(GL_QUADS)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Borde de la tecla
        glColor3f(0.2, 1.0, 0.4)
        glBegin(GL_LINE_LOOP)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Letra centrada dentro de la tecla
        glColor3f(1.0, 1.0, 1.0)
        letra_w = glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(letra))
        lx = kx + (s - letra_w) / 2
        ly = ky + (s - 14) / 2  # 14 aprox alto de Helvetica 18
        glRasterPos2f(lx, ly)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(letra))
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

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
    
    # Ancho real del texto sumando cada carácter
    ancho_real = sum(glutBitmapWidth(font, ord(c)) for c in text)
    x = (w_win - ancho_real) / 2
    
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
    if estado.fase_actual == "TITULO":
        draw_start_screen()
    elif estado.fase_actual == "RONDA_INTRO":
        draw_ronda_intro()
    elif estado.fase_actual == "MAPA":
        pass  # La cámara se configura más abajo en el bloque de dibujo
    else:
        # Cámara de selección
        gluLookAt(0.0, 1.5, 9.0,   
                  0.0, 0.0, 0.0,    
                  0.0, 1.0, 0.0)    
              
    idx_p1 = estado.cursor_index
    idx_p2 = estado.cursor_index_p2
    
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    if estado.fase_actual in ["SELECCION_P1", "SELECCION_P2"]:
        # === MODO CARRUSEL ===
        if estado.fase_actual == "SELECCION_P1":
            idx_actual = idx_p1
            datos = INFO_PERSONAJES[idx_p1]
        else:
            idx_actual = idx_p2
            datos = INFO_PERSONAJES[idx_p2]
        
        idx_izq = (idx_actual - 1) % 6
        idx_der = (idx_actual + 1) % 6
        
        # Si es P2, saltar el personaje del P1 en las siluetas
        if estado.fase_actual == "SELECCION_P2":
            if idx_izq == estado.jugador1_seleccion:
                idx_izq = (idx_izq - 1) % 6
            if idx_der == estado.jugador1_seleccion:
                idx_der = (idx_der + 1) % 6
        
        dibujar_personaje(idx_izq, "silueta", -6.0, -3.0)
        dibujar_personaje(idx_der, "silueta", 6.0, -3.0)
        dibujar_personaje(idx_actual, "centro", 0.0, 0.0)
        
        # Indicador de turno (¡Súper importante para los niños!)
        if estado.fase_actual == "SELECCION_P1":
            glColor3f(0.0, 1.0, 0.0) # Verde para P1
            draw_text_centered(h - 40, "TURNO DEL JUGADOR 1", GLUT_BITMAP_TIMES_ROMAN_24)
        else:
            glColor3f(1.0, 0.0, 0.0) # Rojo para P2
            draw_text_centered(h - 40, "TURNO DEL JUGADOR 2", GLUT_BITMAP_TIMES_ROMAN_24)

        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 80, f"> {datos[0].upper()} <", GLUT_BITMAP_TIMES_ROMAN_24)
        
        glColor3f(0.7, 0.7, 0.7)
        draw_text_centered(30, "Usa Flechas <- -> para navegar  |  [ENTER] Seleccionar", GLUT_BITMAP_HELVETICA_18)
        
    elif estado.fase_actual in ["CONFIRMAR_P1", "CONFIRMAR_P2"]:
        # === MODO VENTANA DE CONFIRMACIÓN ===
        if estado.fase_actual == "CONFIRMAR_P1":
            idx_actual = idx_p1
            datos = INFO_PERSONAJES[idx_p1]
        else:
            idx_actual = idx_p2
            datos = INFO_PERSONAJES[idx_p2]
        
        dibujar_personaje(idx_actual, "centro", 0.0, 0.0)
        
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h - 60, f"¿ELEGIR A {datos[0].upper()}?", GLUT_BITMAP_TIMES_ROMAN_24)

        glColor3f(0.0, 0.9, 1.0)
        draw_text_centered(h - 130, f"CLASE: {datos[1]}  |  ESTILO: {datos[2]}", GLUT_BITMAP_HELVETICA_18)
        
        glColor3f(1.0, 1.0, 1.0)
        if estado.fase_actual == "CONFIRMAR_P1":
            draw_text_centered(h - 190, "CONTROLES:", GLUT_BITMAP_HELVETICA_18)
            draw_wasd_keys(w // 2 + 50, h - 210)
        else:
            draw_text_centered(h - 190, "CONTROLES:", GLUT_BITMAP_HELVETICA_18)
            draw_arrow_keys(w // 2 + 50, h - 210)

        # Botones dinámicos según de quién sea el turno
        jugador_txt = "JUGADOR 1" if estado.fase_actual == "CONFIRMAR_P1" else "JUGADOR 2"
        glColor3f(0.2, 1.0, 0.2)
        draw_text_centered(100, f"[ ENTER ] CONFIRMAR {jugador_txt}", GLUT_BITMAP_TIMES_ROMAN_24)
        glColor3f(1.0, 0.2, 0.2)
        draw_text_centered(50, "[ ESC ] VOLVER AL MENU", GLUT_BITMAP_HELVETICA_18)

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
        # Cámara más alta para ver toda la arena de competencia
        mid_x = (estado.p1_pos[0] + estado.p2_pos[0]) / 2
        mid_z = (estado.p1_pos[2] + estado.p2_pos[2]) / 2
        gluLookAt(mid_x, 15.0, mid_z + 18.0,   
                  mid_x, 0.0, mid_z,    
                  0.0, 1.0, 0.0)
                  
        draw_nivel_1()
        
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

        # ==================== UI DE PUNTAJES ====================
        nombre_obj = estado.n1_tipo_objeto["nombre"] if estado.n1_tipo_objeto else "OBJETOS"
        r_obj, g_obj, b_obj = estado.n1_tipo_objeto["color"] if estado.n1_tipo_objeto else (1,1,1)
        
        # Pregunta con color del objeto
        # Si el objeto es oscuro, lo aclaramos un poco
        brightness = r_obj * 0.3 + g_obj * 0.59 + b_obj * 0.11
        if brightness < 0.4:
            color_pregunta = (1.0, 1.0, 1.0) # Blanco
        else:
            color_pregunta = (r_obj, g_obj, b_obj)
            
        # Texto principal
        glColor3f(*color_pregunta)
        draw_text_centered(h - 35, f"¿CUANTAS {nombre_obj} HAY?", GLUT_BITMAP_TIMES_ROMAN_24)
        
        glColor3f(0.0, 1.0, 0.0)
        draw_text_centered(h - 70, f"JUGADOR 1: {estado.p1_score} / {estado.meta_puntos} PTS", GLUT_BITMAP_HELVETICA_18)
        
        glColor3f(1.0, 0.3, 0.3)
        draw_text_centered(h - 95, f"JUGADOR 2: {estado.p2_score} / {estado.meta_puntos} PTS", GLUT_BITMAP_HELVETICA_18)

    elif estado.fase_actual == "NIVEL_2":
        # Cámara para el Nivel 2
        mid_x = (estado.p1_pos[0] + estado.p2_pos[0]) / 2
        gluLookAt(mid_x, 15.0, 18.0,   
                  mid_x, 0.0, 0.0,    
                  0.0, 1.0, 0.0)
                  
        draw_nivel_2()
        
        # LÓGICA DE DIBUJO CON EFECTO DE "CONGELADO" (ROJO)
        glPushMatrix()
        glTranslatef(estado.p1_pos[0], estado.p1_pos[1], estado.p1_pos[2])
        glRotatef(estado.p1_rot, 0, 1, 0)
        if estado.p1_stun > 0 and math.sin(estado.tiempo_global * 15) > 0:
            glColor3f(1.0, 0.0, 0.0) # Parpadeo rojo si J1 está aturdido
        else:
            glColor3f(1.0, 1.0, 1.0)
        dibujar_modelo_en_mapa(estado.jugador1_seleccion)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(estado.p2_pos[0], estado.p2_pos[1], estado.p2_pos[2])
        glRotatef(estado.p2_rot, 0, 1, 0)
        if estado.p2_stun > 0 and math.sin(estado.tiempo_global * 15) > 0:
            glColor3f(1.0, 0.0, 0.0) # Parpadeo rojo si J2 está aturdido
        else:
            glColor3f(1.0, 1.0, 1.0)
        dibujar_modelo_en_mapa(estado.jugador2_seleccion)
        glPopMatrix()

        # ==================== UI DEL NIVEL 2 ====================
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h - 35, f"¿CUÁNTO ES {estado.n2_num1} + {estado.n2_num2}?", GLUT_BITMAP_TIMES_ROMAN_24)
        
        # Textos de Puntajes y Estados

        color_p1 = [1.0, 0.0, 0.0] if estado.p1_stun > 0 else [0.0, 1.0, 0.0]
        glColor3f(*color_p1)
        txt_p1 = "CONGELADO" if estado.p1_stun > 0 else f"{estado.p1_score} / {estado.meta_puntos} PTS"
        draw_text_centered(h - 70, f"JUGADOR 1: {txt_p1}", GLUT_BITMAP_HELVETICA_18)
        
        color_p2 = [1.0, 0.0, 0.0] if estado.p2_stun > 0 else [1.0, 0.3, 0.3]
        glColor3f(*color_p2)
        txt_p2 = "CONGELADO" if estado.p2_stun > 0 else f"{estado.p2_score} / {estado.meta_puntos} PTS"
        draw_text_centered(h - 95, f"JUGADOR 2: {txt_p2}", GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()

def draw_start_screen():
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    t = estado.tiempo_global
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    # =========================================================
    # PARTE 1: FONDO 3D - Rejilla Neon estilo Tron/Retrowave
    # =========================================================
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(60, w / max(h, 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 3, 8,  0, 0, -5,  0, 1, 0)
    
    # Fondo gradiente (dibujar un quad gigante lejos)
    glBegin(GL_QUADS)
    glColor3f(0.02, 0.0, 0.08)  # Púrpura oscuro abajo
    glVertex3f(-50, -5, -50)
    glVertex3f(50, -5, -50)
    glColor3f(0.0, 0.02, 0.12)   # Azul oscuro arriba
    glVertex3f(50, 15, -50)
    glVertex3f(-50, 15, -50)
    glEnd()
    
    # Rejilla neon en el suelo (se mueve hacia la cámara)
    grid_offset = (t * 2.0) % 2.0  # Movimiento continuo
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Blend aditivo para neon
    
    # Líneas horizontales (Z)
    for i in range(-20, 5):
        z = float(i) + grid_offset
        alpha = max(0.0, 1.0 - abs(z + 5) / 20.0) * 0.6
        glColor4f(0.0, 0.8, 1.0, alpha)
        glBegin(GL_LINES)
        glVertex3f(-25, -0.5, z)
        glVertex3f(25, -0.5, z)
        glEnd()
    
    # Líneas verticales (X)
    for i in range(-12, 13):
        x = float(i) * 2
        glColor4f(0.0, 0.5, 1.0, 0.3)
        glBegin(GL_LINES)
        glVertex3f(x, -0.5, -20)
        glVertex3f(x, -0.5, 5)
        glEnd()
    
    # Línea de horizonte brillante
    glLineWidth(2.0)
    glow = 0.7 + 0.3 * math.sin(t * 3.0)
    glColor4f(0.0, glow, 1.0, 0.9)
    glBegin(GL_LINES)
    glVertex3f(-30, -0.5, -20)
    glVertex3f(30, -0.5, -20)
    glEnd()
    glLineWidth(1.0)
    
    # Partículas flotantes (cubitos neon volando)
    for i in range(20):
        px = math.sin(t * 0.3 + i * 1.7) * 12
        py = (math.sin(t * 0.5 + i * 2.3) + 1.0) * 3.0 + 1.0
        pz = ((t * 0.8 + i * 3.0) % 25.0) - 20.0
        size = 0.08 + 0.05 * math.sin(t * 2 + i)
        
        # Color alternando entre cian, magenta, y amarillo
        if i % 3 == 0:
            glColor4f(0.0, 1.0, 1.0, 0.7)
        elif i % 3 == 1:
            glColor4f(1.0, 0.0, 1.0, 0.5)
        else:
            glColor4f(1.0, 1.0, 0.0, 0.5)
        
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(t * 100 + i * 45, 1, 1, 0)
        glutSolidCube(size)
        glPopMatrix()
    
    glDisable(GL_BLEND)
    
    # Restaurar la proyección 3D
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # =========================================================
    # PARTE 2: OVERLAY 2D - Estrellas, Título, Textos
    # =========================================================
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # --- ESTRELLAS ANIMADAS (Titilando) ---
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_POINT_SMOOTH)
    
    for star in title_stars:
        # Mover estrella hacia abajo (efecto de caída)
        sy = (star["y"] - t * star["speed"]) % 1.0
        sx = star["x"]
        
        # Titileo suave
        twinkle = 0.5 + 0.5 * math.sin(t * 4.0 + sx * 20.0 + sy * 15.0)
        alpha = star["brightness"] * twinkle
        
        glPointSize(star["size"])
        glBegin(GL_POINTS)
        glColor4f(0.7, 0.85, 1.0, alpha)
        glVertex2f(sx * w, sy * h)
        glEnd()
    
    glDisable(GL_POINT_SMOOTH)
    
    # --- BORDES DECORATIVOS NEON ---
    glLineWidth(2.0)
    border_alpha = 0.4 + 0.2 * math.sin(t * 2.0)
    glColor4f(0.0, 0.8, 1.0, border_alpha)
    margin = 15
    glBegin(GL_LINE_LOOP)
    glVertex2f(margin, margin)
    glVertex2f(w - margin, margin)
    glVertex2f(w - margin, h - margin)
    glVertex2f(margin, h - margin)
    glEnd()
    
    # Segundo borde interior
    glColor4f(1.0, 0.0, 0.8, border_alpha * 0.5)
    m2 = 25
    glBegin(GL_LINE_LOOP)
    glVertex2f(m2, m2)
    glVertex2f(w - m2, m2)
    glVertex2f(w - m2, h - m2)
    glVertex2f(m2, h - m2)
    glEnd()
    glLineWidth(1.0)
    
    glDisable(GL_BLEND)
    
    # --- TÍTULO PRINCIPAL: "NUMY PLAY" con efecto glow ---
    # Efecto de color cycling suave en el título
    r_title = 0.5 + 0.5 * math.sin(t * 1.2)
    g_title = 0.8 + 0.2 * math.sin(t * 1.5 + 1.0)
    b_title = 0.5 + 0.5 * math.sin(t * 1.8 + 2.0)
    
    # Capa de "glow" (texto repetido con offsets y menor opacidad)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    
    title_y = h // 2 + 80
    for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2), (0, 3), (0, -3)]:
        glColor4f(r_title * 0.4, g_title * 0.4, b_title * 0.4, 0.3)
        # Dibujamos el glow manualmente usando rasterPos
        title_width = sum(glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ord(c)) for c in "NUMY PLAY")
        glRasterPos2f((w - title_width) / 2 + offset[0], title_y + offset[1])
        for char in "NUMY PLAY":
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    
    glDisable(GL_BLEND)
    
    # Texto principal sólido
    glColor3f(r_title, g_title, b_title)
    draw_text_centered(title_y, "NUMY PLAY", GLUT_BITMAP_TIMES_ROMAN_24)
    
    # --- SUBTÍTULO ---
    glColor3f(0.0, 0.85, 1.0)
    draw_text_centered(h // 2 + 40, "- ARCADE MATEMATICO 3D -", GLUT_BITMAP_HELVETICA_18)
    
    # --- LÍNEA SEPARADORA ANIMADA ---
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    sep_y = h // 2 + 15
    line_w = 200 + 50 * math.sin(t * 2.0)
    cx = w / 2
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor4f(1.0, 0.0, 1.0, 0.8)
    glVertex2f(cx - line_w, sep_y)
    glColor4f(0.0, 1.0, 1.0, 0.0)
    glVertex2f(cx, sep_y)
    glEnd()
    glBegin(GL_LINES)
    glColor4f(0.0, 1.0, 1.0, 0.0)
    glVertex2f(cx, sep_y)
    glColor4f(1.0, 0.0, 1.0, 0.8)
    glVertex2f(cx + line_w, sep_y)
    glEnd()
    glLineWidth(1.0)
    glDisable(GL_BLEND)
    
    # --- TEXTO PARPADEANTE ARCADE ---
    if math.sin(t * 5.0) > 0:
        # Efecto glow amarillo en el texto de enter
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glColor4f(1.0, 0.8, 0.0, 0.3)
        draw_text_centered(h // 2 - 50 + 1, "PRESIONA [ ENTER ] PARA JUGAR", GLUT_BITMAP_HELVETICA_18)
        draw_text_centered(h // 2 - 50 - 1, "PRESIONA [ ENTER ] PARA JUGAR", GLUT_BITMAP_HELVETICA_18)
        glDisable(GL_BLEND)
        
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h // 2 - 50, "PRESIONA [ ENTER ] PARA JUGAR", GLUT_BITMAP_HELVETICA_18)
    
    # --- CRÉDITOS / VERSIÓN ---
    glColor3f(0.3, 0.3, 0.5)
    draw_text_centered(45, "v1.0  |  2 JUGADORES  |  6 PERSONAJES", GLUT_BITMAP_HELVETICA_12)
    
    # Restaurar estados
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_ronda_intro():
    """Pantalla negra antes de iniciar la ronda, muestra el objetivo"""
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    t = estado.tiempo_global
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Fondo negro
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(w, 0)
    glVertex2f(w, h)
    glVertex2f(0, h)
    glEnd()
    
    # Textos
    nombre_obj = estado.n1_tipo_objeto["nombre"] if estado.n1_tipo_objeto else "OBJETOS"
    r_obj, g_obj, b_obj = estado.n1_tipo_objeto["color"] if estado.n1_tipo_objeto else (1,1,1)
    
    glColor3f(1.0, 1.0, 1.0)
    draw_text_centered(h // 2 + 100, "NUEVA RONDA", GLUT_BITMAP_TIMES_ROMAN_24)
    
    # Objetivo con color
    glColor3f(r_obj, g_obj, b_obj)
    draw_text_centered(h // 2 + 30, f"OBJETIVO: CONTAR LOS {nombre_obj}", GLUT_BITMAP_TIMES_ROMAN_24)
    
    # Texto parpadeante
    if math.sin(t * 5.0) > 0:
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h // 2 - 80, "PRESIONA [ ENTER ] PARA COMENZAR", GLUT_BITMAP_HELVETICA_18)
        
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # Dibujar un objeto de muestra girando en el centro
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    # Configurar proyeccion para el objeto 3D
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    gluLookAt(0, 0, 8,  0, 0, 0,  0, 1, 0)
    
    if estado.n1_tipo_objeto:
        forma = estado.n1_tipo_objeto["forma"]
        glPushMatrix()
        glTranslatef(0, -1.0, 0)
        glRotatef(t * 50, 0, 1, 0)  # Rotar
        glScalef(2.0, 2.0, 2.0)     # Hacerlo mas grande
        
        glColor3f(r_obj, g_obj, b_obj)
        
        if forma == "esfera":
            glutSolidSphere(0.5, 16, 16)
        elif forma == "cubo":
            glRotatef(45, 0, 1, 0)
            glutSolidCube(0.8)
        elif forma == "dona":
            glRotatef(90, 1, 0, 0)
            glutSolidTorus(0.15, 0.35, 12, 16)
        elif forma == "diamante":
            glPushMatrix()
            glScalef(0.5, 0.7, 0.5)
            glutSolidSphere(0.7, 4, 4)
            glPopMatrix()
        elif forma == "platano":
            glRotatef(30, 0, 0, 1)
            glPushMatrix()
            glRotatef(-90, 1, 0, 0)
            q2 = gluNewQuadric()
            gluCylinder(q2, 0.15, 0.2, 0.8, 8, 1)
            glPopMatrix()
        elif forma == "estrella":
            glPushMatrix()
            glRotatef(90, 1, 0, 0)
            glutSolidTorus(0.1, 0.4, 5, 5)
            glPopMatrix()
            
        glPopMatrix()
        
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

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

def draw_nivel_1():
    limit = estado.map_limit
    t = estado.tiempo_global
    
    # ========== 1. CIELO DEGRADADO ==========
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.7, 1.0)  # Azul cielo arriba
    glVertex2f(0, 1)
    glVertex2f(1, 1)
    glColor3f(0.7, 0.85, 1.0)  # Celeste claro abajo
    glVertex2f(1, 0.3)
    glVertex2f(0, 0.3)
    glEnd()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    
    # ========== 2. SUELO DE PRADERA ==========
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.55, 0.1)  # Verde pasto claro centro
    glVertex3f(-limit, -2, -limit)
    glVertex3f(limit, -2, -limit)
    glColor3f(0.15, 0.45, 0.08)  # Verde pasto oscuro borde
    glVertex3f(limit, -2, limit)
    glVertex3f(-limit, -2, limit)
    glEnd()
    
    # Camino de tierra hacia las cajas
    glBegin(GL_QUADS)
    glColor3f(0.55, 0.4, 0.2)
    glVertex3f(-2, -1.98, -16)
    glVertex3f(2, -1.98, -16)
    glColor3f(0.6, 0.45, 0.25)
    glVertex3f(2, -1.98, 10)
    glVertex3f(-2, -1.98, 10)
    glEnd()
    glEnable(GL_LIGHTING)
    
    # ========== 3. ARBOLES DECORATIVOS ==========
    arboles_pos = [(-16, -8), (-14, 2), (-17, 8), (15, -5), (16, 4), (17, 9),
                   (-12, -15), (12, -15), (-18, -2), (18, -10)]
    for ax, az in arboles_pos:
        glPushMatrix()
        glTranslatef(ax, -2, az)
        # Tronco
        glColor3f(0.45, 0.25, 0.1)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        q = gluNewQuadric()
        gluCylinder(q, 0.3, 0.25, 3.0, 8, 1)
        glPopMatrix()
        # Copa del arbol
        glColor3f(0.1, 0.55, 0.15)
        glTranslatef(0, 3.0, 0)
        glutSolidSphere(1.8, 12, 12)
        # Copa superior mas chica
        glColor3f(0.15, 0.65, 0.2)
        glTranslatef(0, 1.2, 0)
        glutSolidSphere(1.2, 10, 10)
        glPopMatrix()
    
    # ========== 4. ARBUSTOS Y FLORES ==========
    random.seed(123)  # Semilla fija para decoracion
    for i in range(25):
        fx = random.uniform(-18, 18)
        fz = random.uniform(-10, 9)
        glPushMatrix()
        glTranslatef(fx, -1.8, fz)
        # Arbusto verde
        glColor3f(0.15 + i * 0.01, 0.5 + (i % 5) * 0.05, 0.1)
        glutSolidSphere(0.35, 8, 8)
        glPopMatrix()
    
    # Flores de colores
    colores_flores = [(1.0, 0.3, 0.3), (1.0, 1.0, 0.3), (0.8, 0.3, 1.0), (1.0, 0.6, 0.8)]
    for i in range(15):
        fx = random.uniform(-17, 17)
        fz = random.uniform(-8, 8)
        glPushMatrix()
        glTranslatef(fx, -1.7, fz)
        glColor3f(*colores_flores[i % len(colores_flores)])
        glutSolidSphere(0.15, 6, 6)
        glPopMatrix()
    random.seed()  # Restaurar semilla aleatoria
    
    # ========== 5. NUBES ==========
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)
    nubes = [(-10, 12, -18), (5, 14, -20), (15, 11, -15), (-5, 13, -22), (0, 15, -25)]
    for nx, ny, nz in nubes:
        drift = math.sin(t * 0.15 + nx) * 2  # Movimiento lento
        glPushMatrix()
        glTranslatef(nx + drift, ny, nz)
        glutSolidSphere(2.0, 10, 10)
        glTranslatef(1.8, -0.3, 0)
        glutSolidSphere(1.5, 10, 10)
        glTranslatef(-3.5, 0.2, 0)
        glutSolidSphere(1.7, 10, 10)
        glPopMatrix()
    glEnable(GL_LIGHTING)

    # ========== 6. OBJETOS A CONTAR ==========
    tipo = estado.n1_tipo_objeto
    if tipo:
        r, g, b = tipo["color"]
        forma = tipo["forma"]
        
        for obj in estado.n1_objetos:
            glPushMatrix()
            glTranslatef(obj[0], -1.3, obj[1])
            glColor3f(r, g, b)
            
            if forma == "esfera":
                glutSolidSphere(0.5, 16, 16)
            elif forma == "cubo":
                glRotatef(45, 0, 1, 0)  # Rotacion estetica
                glutSolidCube(0.8)
            elif forma == "dona":
                glRotatef(90, 1, 0, 0)
                glutSolidTorus(0.15, 0.35, 12, 16)
            elif forma == "diamante":
                # Diamante = dos piramides (octaedro aplastado)
                glPushMatrix()
                glScalef(0.5, 0.7, 0.5)
                glutSolidSphere(0.7, 4, 4)  # Esfera con pocos lados = diamante
                glPopMatrix()
            elif forma == "platano":
                # Platano = cilindro curvado
                glRotatef(30, 0, 0, 1)
                glPushMatrix()
                glRotatef(-90, 1, 0, 0)
                q2 = gluNewQuadric()
                gluCylinder(q2, 0.15, 0.2, 0.8, 8, 1)
                glPopMatrix()
            elif forma == "estrella":
                # Estrella = torus aplastado + esfera
                glPushMatrix()
                glRotatef(90, 1, 0, 0)
                glutSolidTorus(0.1, 0.4, 5, 5)
                glPopMatrix()
            
            # Sombra debajo del objeto
            glDisable(GL_LIGHTING)
            glColor4f(0.0, 0.0, 0.0, 0.3)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glPushMatrix()
            glTranslatef(0, -0.25, 0)
            glScalef(1.0, 0.02, 1.0)
            glutSolidSphere(0.5, 8, 8)
            glPopMatrix()
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            
            glPopMatrix()

    # ========== 7. CAJAS DE RESPUESTA ==========
    from OpenGL.GLUT import GLUT_STROKE_ROMAN
    colores_caja = [(0.9, 0.3, 0.2), (0.2, 0.7, 0.3), (0.2, 0.4, 0.9)]
    for i, blk in enumerate(estado.n1_bloques):
        glPushMatrix()
        glTranslatef(blk["x"], -0.5, blk["z"])
        
        # Caja colorida
        glColor3f(*colores_caja[i])
        glutSolidCube(3.0)
        
        # Borde mas oscuro
        glColor3f(colores_caja[i][0] * 0.5, colores_caja[i][1] * 0.5, colores_caja[i][2] * 0.5)
        glutWireCube(3.05)
        
        glPopMatrix()
        
        # NUMERO GIGANTE 3D en la CARA FRONTAL de la caja
        glDisable(GL_LIGHTING)
        num_str = str(blk["val"])
        
        # Centrar horizontalmente usando el ancho estimado
        # Cada caracter de stroke mide aprox 104 unidades de ancho
        escala_texto = 0.012
        text_w = len(num_str) * 104 * escala_texto
        
        # Posición: al frente de la caja (z + 1.51 para que no haya z-fighting)
        # Y un poco más abajo del centro de la caja (y = -1.0)
        pos_x = blk["x"] - (text_w / 2)
        pos_y = -1.2
        pos_z = blk["z"] + 1.52
        
        # Numero blanco grueso y limpio
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(4.0)
        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glScalef(escala_texto, escala_texto, escala_texto)
        for char in num_str:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
        glPopMatrix()
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHTING)

def draw_nivel_2():
    # 1. Dibujar la plataforma base (donde inician)
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2) # Gris oscuro
    glTranslatef(0, -1.0, 8.0)
    glScalef(18.0, 0.5, 4.0)
    glutSolidCube(1.0)
    glPopMatrix()

    # 2. Dibujar las 3 plataformas flotantes (Las respuestas)
    for blk in estado.n2_bloques:
        glPushMatrix()
        glTranslatef(blk["x"], -1.0, blk["z"])
        glColor3f(0.0, 0.5, 0.8) # Azul brillante
        glScalef(4.0, 0.5, 4.0)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # 3. Dibujar la respuesta sobre cada plataforma
        glDisable(GL_LIGHTING)
        num_str = str(blk["val"])
        escala_texto = 0.012
        text_w = len(num_str) * 104 * escala_texto
        
        pos_x = blk["x"] - (text_w / 2)
        pos_y = -0.7 # Ligeramente sobre la plataforma
        pos_z = blk["z"] + 1.0 # Un poco al frente
        
        # Numero blanco grueso y limpio
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(4.0)
        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glScalef(escala_texto, escala_texto, escala_texto)
        for char in num_str:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
        glPopMatrix()
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)

def teclado_normal(key, x, y):
    key = key.lower()
    if key == b'\r': # Enter
        if estado.fase_actual == "TITULO":
            estado.fase_actual = "SELECCION_P1"
            sound_manager.play_sound(0, "happy") # Sonido de inicio
        elif estado.fase_actual == "SELECCION_P1":
            manager.trigger_characteristic_anim(estado.cursor_index)
            estado.fase_actual = "CONFIRMAR_P1"
            sound_manager.play_sound(estado.cursor_index, "happy")
        elif estado.fase_actual == "CONFIRMAR_P1":
            manager.stop_characteristic_anim(estado.cursor_index)
            # ¡Guardamos la selección del J1 y pasamos al J2!
            estado.jugador1_seleccion = estado.cursor_index
            estado.fase_actual = "SELECCION_P2"
            # Movemos el cursor para que no empiece en el mismo personaje
            estado.cursor_index_p2 = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0
            sound_manager.play_sound(estado.jugador1_seleccion, "surprised")
        elif estado.fase_actual == "SELECCION_P2":
            # Validar que el J2 NO elija el mismo del J1
            if estado.cursor_index_p2 == estado.jugador1_seleccion:
                print("¡Personaje ya ocupado por el J1!")
                # Aquí podríamos poner un sonido de error luego
            else:
                manager.trigger_characteristic_anim(estado.cursor_index_p2)
                estado.fase_actual = "CONFIRMAR_P2"
                sound_manager.play_sound(estado.cursor_index_p2, "happy")
        elif estado.fase_actual == "CONFIRMAR_P2":
            manager.stop_characteristic_anim(estado.cursor_index_p2)
            # ¡Ambos listos!
            estado.jugador2_seleccion = estado.cursor_index_p2
            print(f"¡BATALLA LISTA! J1:{estado.jugador1_seleccion} vs J2:{estado.jugador2_seleccion}")
            estado.fase_actual = "LISTOS"
            sound_manager.play_sound(estado.jugador2_seleccion, "happy")
        elif estado.fase_actual == "LISTOS":
            estado.fase_actual = "RONDA_INTRO"
            # Iniciar música de fondo (usamos la del P1 por ejemplo)
            sound_manager.play_bgm(estado.jugador1_seleccion)
        elif estado.fase_actual == "RONDA_INTRO":
            estado.fase_actual = "MAPA"
            
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
            # Resetear puntajes y posiciones
            estado.p1_score = 0
            estado.p2_score = 0
            estado.generar_nivel_1()

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

    if estado.fase_actual in ["MAPA", "NIVEL_2"]:
        estado.teclas.add(key)
            
    glutPostRedisplay()

def teclado_arriba(key, x, y):
    key = key.lower()
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
    
    if estado.fase_actual in ["MAPA", "NIVEL_2"]:
        estado.teclas.add(key)
            
    glutPostRedisplay()

def teclado_especial_arriba(key, x, y):
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
        
    if estado.p1_stun > 0: estado.p1_stun -= dt
    if estado.p2_stun > 0: estado.p2_stun -= dt
    
    if estado.fase_actual in ["MAPA", "NIVEL_2"]:
        mover_jugadores(dt)
        
    glutPostRedisplay()

def mover_jugadores(dt):
    vel = 3.5 * dt
    
    # Player 1 (WASD)
    moliendo_p1 = False
    if estado.p1_stun <= 0:
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
            
        if not check_limites(next_p1):
            estado.p1_pos = next_p1
            verificar_respuesta(estado.p1_pos, "J1")
        
    manager.set_walking(estado.jugador1_seleccion, moliendo_p1)
    
    # Player 2 (Arrows)
    moliendo_p2 = False
    if estado.p2_stun <= 0:
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

        if not check_limites(next_p2):
            estado.p2_pos = next_p2
            verificar_respuesta(estado.p2_pos, "J2")

    manager.set_walking(estado.jugador2_seleccion, moliendo_p2)

def check_limites(pos):
    """Evita que los niños se salgan del mapa"""
    limit = estado.map_limit - 1.0
    if abs(pos[0]) > limit or abs(pos[2]) > limit:
        return True
    return False

def verificar_respuesta(pos, jugador):
    """Verifica si un jugador chocó contra una de las cajas/plataformas"""
    radio_caja = 2.0
    
    if estado.fase_actual == "MAPA": # Nivel 1
        for blk in estado.n1_bloques:
            dx = pos[0] - blk["x"]
            dz = pos[2] - blk["z"]
            dist = math.sqrt(dx*dx + dz*dz)
            
            if dist < radio_caja:
                if blk["val"] == estado.n1_target:
                    sound_manager.play_sound(0, "happy")
                    if jugador == "J1": estado.p1_score += 1
                    else: estado.p2_score += 1
                    
                    if estado.p1_score >= estado.meta_puntos or estado.p2_score >= estado.meta_puntos:
                        print(f"¡GANÓ {jugador} EL NIVEL 1!")
                        estado.p1_score = 0
                        estado.p2_score = 0
                        estado.generar_nivel_2()
                        estado.fase_actual = "NIVEL_2"
                        estado.teclas.clear()
                    else:
                        estado.generar_nivel_1()
                        estado.fase_actual = "RONDA_INTRO"
                        estado.teclas.clear()
                else:
                    sound_manager.play_sound(0, "angry")
                    pos[2] += 4.0
                break

    elif estado.fase_actual == "NIVEL_2":
        radio_plataforma = 2.5
        for blk in estado.n2_bloques:
            dx = pos[0] - blk["x"]
            dz = pos[2] - blk["z"]
            dist = math.sqrt(dx*dx + dz*dz)
            
            if dist < radio_plataforma:
                if blk["val"] == estado.n2_target:
                    sound_manager.play_sound(0, "happy")
                    if jugador == "J1": estado.p1_score += 1
                    else: estado.p2_score += 1
                    
                    if estado.p1_score >= estado.meta_puntos or estado.p2_score >= estado.meta_puntos:
                        print(f"¡EL {jugador} HA GANADO EL JUEGO!")
                        estado.fase_actual = "TITULO"
                        estado.teclas.clear()
                        estado.p1_score = 0
                        estado.p2_score = 0
                    else:
                        estado.generar_nivel_2()
                        # Aquí no cambiamos de fase, solo regeneramos, pero podemos limpiar por si acaso
                        estado.teclas.clear()
                else:
                    sound_manager.play_sound(0, "angry")
                    pos[2] += 4.0
                    if jugador == "J1": estado.p1_stun = 3.0
                    else: estado.p2_stun = 3.0
                break

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
