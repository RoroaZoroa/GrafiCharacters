from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
from characters import miko 
from actions.state import State
from actions.camera import Camera
from resources import escenarios
from utilerias.sonido import SonidoManager
from utilerias.colisiones import ColisionManager

# Inicialización de objetos
state = State()
camara = Camera()
sonido = SonidoManager()
colisiones = ColisionManager()

def draw_text(x, y, text):
    glDisable(GL_LIGHTING)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    glEnable(GL_LIGHTING)

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
        glColor3f(1.0, 1.0, 1.0)
        draw_text(10, 580, "----- INSTRUCCIONES -----")
        draw_text(10, 560, "MOVIMIENTOS: W: Caminar | A: Giro | S: Saltar | Z: Saludar | X: Bailar | C: Aplaudir | Q: Quieto")
        draw_text(10, 540, "E: Cambiar Escenario (7 disponibles)  | D: Resetear")
        draw_text(10, 520, "EXPRESIONES: Teclas 1 al 7 (Normal, Enojo, Triste, Guiño, Sorpresa, Llanto, Sueño)")
        draw_text(10, 500, "CAMARA: I,O: Zoom | J,L: Paneo | K,U: Altura | R: Reset Camara")
        draw_text(10, 480, "SISTEMA: H: Ocultar Ayuda | V: Acerca de... | M: Mute ")

    if state.mostrar_acerca_de:
        glColor3f(0.6, 0.0, 0.5) 
        draw_text(450, 110, "--- INFORMACION DEL PROYECTO ---")
        draw_text(450, 90, "PERSONAJE: Miko el Mapache")
        draw_text(450, 70, "DESARROLLADOR: Laura Alicia Morales Medina")
        draw_text(450, 50, "MATERIA: Graficacion  |  PERIODO: Enero - Junio")
        draw_text(450, 30, "PROFESOR: Rocio Elizabeth Pulido Alba")

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_LIGHTING)

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0) # Fondo oscuro para que resalten los colores
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    # Luz posicionada para resaltar el antifaz
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 2.0, 5.0, 1.0])
    state.mostrar_instrucciones = True

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camara.update()
    # Renderizado de los 7 Escenarios Propios de Miko
    if state.escenario_actual == 0: escenarios.escenario_cerezos()
    elif state.escenario_actual == 1: escenarios.escenario_picnic_armonioso()
    elif state.escenario_actual == 2: escenarios.escenario_bosque_lindo()
    elif state.escenario_actual == 3: escenarios.escenario_lago()
    elif state.escenario_actual == 4: escenarios.escenario_dulces_armonioso()
    elif state.escenario_actual == 5: escenarios.escenario_luciernagas_armonioso()
    elif state.escenario_actual == 6: escenarios.escenario_concierto()
    #Objetos de colision
    colisiones.dibujar_objetos()
    # Renderizado de Miko
    glDisable(GL_LIGHTING)
    glPushMatrix()

    glTranslatef(state.pos_x, state.pos_y, state.pos_z) #mueve posisicon con flechas
    # TRASLACIÓN DE SALTO
    if state.movimiento == "saltando":
        # Crea una curva de salto usando el tiempo
        salto = abs(math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.005)) * 1.5
        glTranslatef(0, salto, 0)
    # ROTACIÓN DE GIRO 
    if state.movimiento == "giro":
        # Gira sobre su propio eje Y
        angulo_giro = (glutGet(GLUT_ELAPSED_TIME) * 0.5) % 360
        glRotatef(angulo_giro, 0, 1, 0)

    glRotatef(10, 0, 1, 0) 
    miko.draw_miko(state) 
    glPopMatrix()
    glEnable(GL_LIGHTING)

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
    sonido.update()
    glutPostRedisplay()

def specialKeys(key, x, y):
    paso = 0.25  # Velocidad de movimiento
    
    if key == GLUT_KEY_UP:
        state.pos_z -= paso
        state.movimiento = "caminando"
        sonido.reproducir_efecto("caminando")
        
    elif key == GLUT_KEY_DOWN:
        state.pos_z += paso
        state.movimiento = "caminando"
        sonido.reproducir_efecto("caminando")
        
    elif key == GLUT_KEY_LEFT:
        state.pos_x -= paso
        state.movimiento = "caminando"
        sonido.reproducir_efecto("caminando")
        
    elif key == GLUT_KEY_RIGHT:
        state.pos_x += paso
        state.movimiento = "caminando"
        sonido.reproducir_efecto("caminando")

    # Verificamos si al movernos chocamos con algo
    colisiones.verificar_colisiones(state.pos_x, state.pos_z, state, sonido)
    glutPostRedisplay()

def keyPressed(key, x, y):
    # Expresiones
    if key in [b'1', b'2', b'3', b'4', b'5', b'6', b'7']:
        expresiones = ["normal", "enojado", "triste", "guino", "sorprendido", "llorando", "dormido"]
        idx = int(key.decode()) - 1
        state.expresion = expresiones[idx]
        nombre_expresion = expresiones[idx]
        sonido.reproducir_efecto(nombre_expresion)
    #Acciones
    elif key == b'w': 
        state.movimiento = "caminando"
        sonido.reproducir_efecto("caminando")
    elif key == b'q': 
        state.movimiento = "quieto"
        sonido.reproducir_efecto("quieto")
    elif key == b'a': 
        state.movimiento = "giro"
        sonido.reproducir_efecto("giro")
    elif key == b's': 
        state.movimiento = "saltando"
        sonido.reproducir_efecto("saltando")
    elif key == b'z': 
        state.movimiento = "saludo"
        sonido.reproducir_efecto("saludo")
    elif key == b'x': 
        state.movimiento = "bailar"
        sonido.reproducir_efecto("bailar")
    elif key == b'c': 
        state.movimiento = "aplaudir"
        sonido.reproducir_efecto("aplaudir")
    # Sistema y Escenarios
    elif key == b'e': 
        state.escenario_actual = (state.escenario_actual + 1) % 7
        sonido.cambiar_musica_escenario(state.escenario_actual)
    elif key == b'h': 
        state.mostrar_instrucciones = not state.mostrar_instrucciones
    elif key == b'v': 
        state.mostrar_acerca_de = not state.mostrar_acerca_de
    elif key == b'd': 
        state.reset()
        colisiones.reset_objetos()
        sonido.detener_todo()
    # Controles de Cámara
    elif key == b'i': camara.zoom_in()
    elif key == b'o': camara.zoom_out()
    elif key == b'j': camara.pan_left()
    elif key == b'l': camara.pan_right()
    elif key == b'k': camara.move_up()
    elif key == b'u': camara.move_down()
    elif key == b'r': camara.reset_view()
    # --- SISTEMA DE SONIDO ---
    elif key == b'n':
        sonido.reiniciar_fondo()
    elif key == b'm':
        sonido.toggle_mute()

    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Mapache 3D - Miko")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(specialKeys)
    glutIdleFunc(animacion)
    glutMainLoop()

if __name__ == "__main__":
    main()