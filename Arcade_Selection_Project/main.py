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
            # Dibujar a Knuckles con animación de golpes si está activa
            p = manager.knuckles_anim["punch"]
            rot_b = math.sin(p) * 60 if p > 0 else 0
            knuckles.draw_knuckles_full(rot_brazo_i=rot_b, rot_brazo_d=-rot_b, expresion=manager.knuckles_anim["expresion"])
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
        # Carrusel Jugador 2
        idx_izq = (idx_p2 - 1) % 6
        idx_der = (idx_p2 + 1) % 6
        
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
        draw_text_centered(50, "Presiona [ ESC ] para reiniciar", GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()

def teclado_normal(key, x, y):
    key = key.lower()
    if key == b'\r': # Enter
        if estado.fase_actual == "SELECCION_P1":
            manager.trigger_characteristic_anim(estado.cursor_index)
            estado.fase_actual = "CONFIRMAR_P1"
        elif estado.fase_actual == "CONFIRMAR_P1":
            manager.stop_characteristic_anim(estado.cursor_index)
            estado.jugador1_seleccion = estado.cursor_index
            estado.fase_actual = "SELECCION_P2"
        elif estado.fase_actual == "SELECCION_P2":
            manager.trigger_characteristic_anim(estado.cursor_index_p2)
            estado.fase_actual = "CONFIRMAR_P2"
        elif estado.fase_actual == "CONFIRMAR_P2":
            manager.stop_characteristic_anim(estado.cursor_index_p2)
            estado.jugador2_seleccion = estado.cursor_index_p2
            estado.fase_actual = "LISTOS"
            
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

    # Controles de navegación P1 (WASD)
    if estado.fase_actual == "SELECCION_P1":
        if key == b'a':
            estado.cursor_index = (estado.cursor_index - 1) % 6
            estado.tiempo_seleccion = 0.0
        elif key == b'd':
            estado.cursor_index = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0

    # Teclas de animación universales (1-4)
    if key in [b'1', b'2', b'3', b'4']:
        val = int(key.decode())
        curr_char = estado.cursor_index if "P1" in estado.fase_actual else estado.cursor_index_p2
        manager.set_expression(curr_char, val)
            
    glutPostRedisplay()

def teclado_especial(key, x, y):
    # Controles de navegación P2 (Arrows)
    if estado.fase_actual == "SELECCION_P2":
        if key == GLUT_KEY_LEFT:
            estado.cursor_index_p2 = (estado.cursor_index_p2 - 1) % 6
            estado.tiempo_seleccion = 0.0 
        elif key == GLUT_KEY_RIGHT:
            estado.cursor_index_p2 = (estado.cursor_index_p2 + 1) % 6
            estado.tiempo_seleccion = 0.0 
    
    # También permitir flechas para P1 si está en su fase
    elif estado.fase_actual == "SELECCION_P1":
        if key == GLUT_KEY_LEFT:
            estado.cursor_index = (estado.cursor_index - 1) % 6
            estado.tiempo_seleccion = 0.0 
        elif key == GLUT_KEY_RIGHT:
            estado.cursor_index = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0 
            
    glutPostRedisplay()

def animacion():
    dt = 0.016
    estado.tiempo_global += dt
    manager.update(dt)
    
    if estado.tiempo_seleccion <= 1.0:
        estado.tiempo_seleccion += 0.007
    else:
        estado.tiempo_seleccion = 1.01 
        
    glutPostRedisplay()

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
    glutCreateWindow(b"Arcade - Seleccion de Personajes")
    
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado_normal)
    glutSpecialFunc(teclado_especial)
    glutIdleFunc(animacion)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
