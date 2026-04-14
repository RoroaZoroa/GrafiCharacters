from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

from characters import ajolote
from actions.state import State
from actions.camera import Camera
from resources import escenarios
from utilerias.audio import AudioManager

state = State()
camara = Camera()
audio = AudioManager()

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def draw_ui():
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1.0, 1.0, 1.0)
    if state.mostrar_instrucciones:
        draw_text(10, 580, "--- CONTROLES DE LUMI ---")
        draw_text(10, 560, "1-5: Expresiones | W,A,S,D: Movimientos")
        draw_text(10, 540, "M: Activar Musica | N: Mute General")
        draw_text(10, 520, "E: Escenario | Q: Quieto | H: Ayuda")
        draw_text(10, 500, "I,O,J,L,K,U: Camara | R: Reset | V: Acerca de") # Cambiado M por U
    else:
        draw_text(10, 580, "Presiona 'H' para ayuda")

    if state.mostrar_acerca_de:
        glColor3f(1.0, 0.8, 0.0)
        draw_text(450, 50, "DESARROLLADO POR: Laura Alicia Morales Medina")
        draw_text(450, 30, "Lumi el Ajolote - Proyecto Final 3D")

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_LIGHTING)

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 5.0, 1.0])
    state.mostrar_instrucciones = True
    audio.reproducir_fondo()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camara.update()

    if state.escenario_actual == 0: escenarios.escenario_xochimilco()
    elif state.escenario_actual == 1: escenarios.escenario_cueva()
    elif state.escenario_actual == 2: escenarios.escenario_espacio()
    elif state.escenario_actual == 3: escenarios.escenario_laboratorio()
    elif state.escenario_actual == 4: escenarios.escenario_volcan()

    glPushMatrix()
    glRotatef(-5, 1, 0, 0)
    glRotatef(20, 0, 1, 0)
    ajolote.draw_axolotl_full(state)
    glPopMatrix()

    draw_ui()
    glutSwapBuffers()

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def animacion():
    t = glutGet(GLUT_ELAPSED_TIME)
    if state.movimiento == "caminando":
        state.frame_animacion = math.sin(t * 0.01) * 25
    elif state.movimiento == "saltando":
        state.frame_animacion = abs(math.sin(t * 0.006)) * 1.8
    elif state.movimiento == "giro":
        state.frame_animacion += 2.0
    glutPostRedisplay()

def keyPressed(key, x, y):
    # EXPRESIONES
    if key == b'1': 
        state.expresion = "normal"
        audio.reproducir_efecto("normal")
    elif key == b'2': 
        state.expresion = "enojado"
        audio.reproducir_efecto("enojo")
    elif key == b'3': 
        state.expresion = "triste"
        audio.reproducir_efecto("triste")
    elif key == b'4': 
        state.expresion = "guiño"
        audio.reproducir_efecto("guino")
    elif key == b'5': 
        state.expresion = "sorprendido"
        audio.reproducir_efecto("sorpresa")

    # MOVIMIENTOS
    elif key == b'w': 
        state.movimiento = "caminando"
        audio.reproducir_efecto("pasos")
    elif key == b's': 
        state.movimiento = "saltando"
        audio.reproducir_efecto("salto")
    elif key == b'a': 
        state.movimiento = "saludo"
        audio.reproducir_efecto("saludo")
    elif key == b'd': 
        state.movimiento = "giro"
        audio.reproducir_efecto("giro")
    elif key == b'q': 
        state.movimiento = "quieto"

    # AUDIO Y SISTEMA
    elif key == b'm': audio.reproducir_fondo()
    elif key == b'n': audio.toggle_mute()
    elif key == b'e': state.escenario_actual = (state.escenario_actual + 1) % 5
    elif key == b'h': state.mostrar_instrucciones = not state.mostrar_instrucciones
    elif key == b'v': state.mostrar_acerca_de = not state.mostrar_acerca_de
    
    # CAMARA (U para bajar, liberando la M)
    elif key == b'i': camara.zoom_in()
    elif key == b'o': camara.zoom_out()
    elif key == b'j': camara.pan_left()
    elif key == b'l': camara.pan_right()
    elif key == b'k': camara.move_up()
    elif key == b'u': camara.move_down() # Nueva tecla
    elif key == b'r': camara.reset_view()

    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Lumi - Proyecto 3D")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    glutIdleFunc(animacion)
    glutMainLoop()

if __name__ == "__main__":
    main()