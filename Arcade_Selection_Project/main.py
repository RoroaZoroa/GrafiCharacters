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
    try:
        if indice == 0: ajolote.draw_axolotl_full(estado) 
        elif indice == 1: chef.draw()
        elif indice == 2: knuckles.draw_knuckles_full()
        elif indice == 3: mapache.draw_miko(estado)
        elif indice == 4: pinguino.draw_penguin_full()
        elif indice == 5: robot.draw_robot_full()
    except Exception:
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
        dibujar_modelo(indice)

    else:
        # 4. MODO SILUETA (Oscuro total)
        glDisable(GL_LIGHTING) # Sin luces para las siluetas
        glPushMatrix()
        glTranslatef(0, -1.5 + ALTURAS[indice], 0) 
        glRotatef(ROTACIONES_Y[indice], 0, 1, 0)
        
        sx, sy, sz = ESCALAS[indice]
        glScalef(sx * 0.7, sy * 0.7, sz * 0.7)
        
        glColor3f(0.0, 0.0, 0.0) # Negro absoluto
        dibujar_modelo(indice)
        glPopMatrix()
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
              
    idx_centro = estado.cursor_index
    idx_izq = (estado.cursor_index - 1) % 6
    idx_der = (estado.cursor_index + 1) % 6

    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    datos = INFO_PERSONAJES[idx_centro]

    if estado.fase_actual == "SELECCION_P1":
        # Carrusel con siluetas laterales
        dibujar_personaje(idx_izq, "silueta", -6.0, -3.0)
        dibujar_personaje(idx_der, "silueta", 6.0, -3.0)
        dibujar_personaje(idx_centro, "centro", 0.0, 0.0)
        
        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 60, f"> {datos[0].upper()} <", GLUT_BITMAP_TIMES_ROMAN_24)
        
        glColor3f(0.7, 0.7, 0.7)
        draw_text_centered(30, "Usa Flechas <- -> para navegar  |  [ENTER] Seleccionar", GLUT_BITMAP_HELVETICA_18)
        
    elif estado.fase_actual == "CONFIRMAR_P1":
        dibujar_personaje(idx_centro, "centro", 0.0, 0.0)
        
        # Panel centrado arriba
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h - 60, f"¿ELEGIR A {datos[0].upper()}?", GLUT_BITMAP_TIMES_ROMAN_24)

        # Características (Izquierda)
        glColor3f(0.0, 0.9, 1.0)
        draw_text_centered(h - 130, f"CLASE: {datos[1]}  |  ESTILO: {datos[2]}", GLUT_BITMAP_HELVETICA_18)
        
        # Controles (Abajo del nombre)
        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 170, f"CONTROLES: {datos[3]} y {datos[4]}", GLUT_BITMAP_HELVETICA_12)

        # Botones de Acción
        glColor3f(0.2, 1.0, 0.2)
        draw_text_centered(100, "[ ENTER ] CONFIRMAR JUGADOR 1", GLUT_BITMAP_TIMES_ROMAN_24)
        glColor3f(1.0, 0.2, 0.2)
        draw_text_centered(50, "[ ESC ] VOLVER AL MENU", GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()

def teclado_normal(key, x, y):
    if key == b'\r': # Enter
        if estado.fase_actual == "SELECCION_P1":
            estado.fase_actual = "CONFIRMAR_P1"
        elif estado.fase_actual == "CONFIRMAR_P1":
            print(f"J1 CONFIRMADO: {INFO_PERSONAJES[estado.cursor_index][0]}")
            estado.fase_actual = "SELECCION_P1" 
            
    elif key == b'\x1b': # Esc
        if estado.fase_actual == "CONFIRMAR_P1":
            estado.fase_actual = "SELECCION_P1"
            
    glutPostRedisplay()

def teclado_especial(key, x, y):
    if estado.fase_actual == "SELECCION_P1":
        if key == GLUT_KEY_LEFT:
            estado.cursor_index = (estado.cursor_index - 1) % 6
            estado.tiempo_seleccion = 0.0 
        elif key == GLUT_KEY_RIGHT:
            estado.cursor_index = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0 
            
    glutPostRedisplay()

def animacion():
    estado.tiempo_global += 0.016
    
    if estado.tiempo_seleccion <= 1.0:
        # ANIMACIÓN MAJESTUOSA (0.007 es la clave para que se vea lento y fluido)
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
