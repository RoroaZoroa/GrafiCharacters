# ============================================================
# Main.py - Programa principal: Robot Espacial 3D Interactivo
# ============================================================
# Punto de entrada. Inicializa OpenGL, dibuja la escena con
# el Robot Espacial, escenarios, HUD de instrucciones, y conecta
# todos los controles de entrada.
# ============================================================

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

from characters import robot
from actions import camera
from actions import state
from actions import update as update_module
from resources import input_handlers
from resources import grid
from resources import scenarios
from utils import sounds


def init():
    """Inicialización de OpenGL."""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # Fondo inicial
    scenarios.apply_scenario_background()

    # Inicializar sonidos
    sounds.init_sounds()
    
    # Iniciar sonido del escenario por defecto
    sounds.play_scenario_sound(state.current_scenario)

def _apply_projection_with_zoom():
    """Aplica la proyección perspectiva usando state.zoom (scroll = zoom in/out)."""
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    if h == 0:
        h = 1
    aspect = float(w) / float(h)
    # Zoom: valor mayor = FOV más estrecho = acercar; valor menor = alejar
    fov = 45.0 * 10.0 / state.zoom
    fov = max(5.0, min(90.0, fov))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, aspect, 0.5, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_interactive_objects():
    """Dibuja 3 objetos interactivos para colisiones."""
    import math
    
    # Objeto 1: Cubo de Energía Azul/Cyan (3, 3) Flotando
    glPushMatrix()
    float_y1 = math.sin(state.blink_timer * 3) * 0.15
    glTranslatef(3, 0.0 + float_y1, 3)
    glRotatef(state.blink_timer * 60, 0, 1, 0)
    glRotatef(45, 1, 1, 0)  # Rotación fija para que flote inclinado
    glColor3f(0.2, 0.9, 0.9)
    glutSolidCube(0.5)
    glPopMatrix()
    
    # Objeto 2: Cristal Rojo Rombo/Octaedro (-4, 3) Flotando
    glPushMatrix()
    float_y2 = math.sin(state.blink_timer * 4) * 0.1
    glTranslatef(-4, 0.2 + float_y2, 3)
    glRotatef(state.blink_timer * 40, 0, 1, 0)
    glColor3f(0.9, 0.1, 0.2)
    glScalef(0.35, 0.7, 0.35)
    glutSolidOctahedron()
    glPopMatrix()
    
    # Objeto 3: Plataforma Trampolín (0, 3) en el suelo
    glPushMatrix()
    glTranslatef(0, -0.65, 3)
    glColor3f(0.3, 0.8, 0.3)
    glScalef(1.0, 0.1, 1.0)
    glutSolidSphere(0.8, 16, 16)
    glPopMatrix()

def display():
    """Función de renderizado principal."""
    # Aplicar color de fondo del escenario
    scenarios.apply_scenario_background()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Proyección con zoom (scroll afecta el FOV)
    _apply_projection_with_zoom()
    glLoadIdentity()

    # Aplicar cámara
    camera.apply_camera()

    # Dibujar escenario de fondo
    scenarios.draw_scenario()

    # Dibujar objetos interactivos para colisiones
    draw_interactive_objects()

    # Dibujar el robot
    glPushMatrix()
    glTranslatef(state.robot_x, 0, state.robot_z)
    glRotatef(state.rotate_y, 0, 1, 0)
    glRotatef(state.rotate_x, 1, 0, 0)
    robot.draw_robot_full()
    glPopMatrix()

    # Dibujar HUD (instrucciones o about)
    if state.show_instructions:
        _draw_instructions_hud()
    elif state.show_about:
        _draw_about_hud()

    # Mostrar nombre del escenario brevemente
    _draw_scenario_label()

    glutSwapBuffers()


def reshape(w, h):
    """Redimensionamiento de ventana."""
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    # La proyección con zoom se aplica en display() cada frame
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(w) / float(h)
    fov = 45.0 * 10.0 / state.zoom
    fov = max(5.0, min(90.0, fov))
    gluPerspective(fov, aspect, 0.5, 100.0)
    glMatrixMode(GL_MODELVIEW)


# ═══════════════════════════════════════════
# HUD: Texto 2D superpuesto
# ═══════════════════════════════════════════

def _setup_2d():
    """Configura proyección 2D para dibujar HUD."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    glOrtho(0, w, 0, h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)


def _restore_3d():
    """Restaura proyección 3D después de dibujar HUD."""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


def _draw_text(x, y, text, font=GLUT_BITMAP_9_BY_15):
    """Dibuja texto bitmap en posición (x, y) de pantalla."""
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))


def _draw_instructions_hud():
    """Dibuja el panel de instrucciones detalladas."""
    _setup_2d()
    h = glutGet(GLUT_WINDOW_HEIGHT)

    # Fondo semi-transparente
    glColor4f(0.0, 0.0, 0.0, 0.75)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glVertex2f(10, h - 10)
    glVertex2f(420, h - 10)
    glVertex2f(420, h - 560)
    glVertex2f(10, h - 560)
    glEnd()
    glDisable(GL_BLEND)

    lines = [
        "=== CAMARA ===",
        " Arrastrar Horiz. : Paneo Izq/Der",
        " Arrastrar Vert.  : Paneo Arriba/Abajo",
        " Pg Up            : Mover Arriba",
        " Pg Dn            : Mover Abajo",
        " Tecla F          : Seguir Robot (ON/OFF)",
        " Scroll Mouse     : Zoom In/Out",
        " Tecla Home      : Vista Normal (Reset)",
        "",
        "=== MOVIMIENTOS E INTERACCION ===",
        " W : Caminar ON/OFF    J : Saltar",
        " K : Girar             S : Temblar",
        " E : Mover Brazos      X : Saludar",
        " C : Agacharse",
        " FLECHAS : Mover a Robot",
        "",
        "=== EXPRESIONES ===",
        " Y : Feliz    T : Triste",
        " U : Sorpresa G : Enojado",
        " V : Miedo    N : Neutral",
        " D : Duda",
        "",
        "=== ESCENARIOS Y SONIDO ===",
        " 1-7 : Cambiar Escenario",
        " M   : Sonido Global ON/OFF",
        "",
        "=== OTROS ===",
        " R : Resetear Posicion",
        " H : Mostrar/Ocultar Instrucciones",
        " A : Mostrar/Ocultar Acerca De",
        " ESC : Salir"
    ]

    y_start = h - 30
    for i, line in enumerate(lines):
        if line.startswith("===") or line.startswith("---"):
            glColor3f(1.0, 1.0, 0.3)
        else:
            glColor3f(0.9, 0.9, 0.9)
        _draw_text(20, y_start - i * 16, line)

    _restore_3d()


def _draw_about_hud():
    """Panel 'Acerca de'."""
    _setup_2d()
    h = glutGet(GLUT_WINDOW_HEIGHT)

    # Fondo
    glColor4f(0.0, 0.0, 0.0, 0.75)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glVertex2f(10, h - 10)
    glVertex2f(380, h - 10)
    glVertex2f(380, h - 160)
    glVertex2f(10, h - 160)
    glEnd()
    glDisable(GL_BLEND)

    glColor3f(1.0, 1.0, 0.3)
    _draw_text(20, h - 30, "=== ACERCA DEL PERSONAJE ===")
    glColor3f(0.9, 0.9, 0.9)
    _draw_text(20, h - 55, "Personaje: Robot Espacial")
    _draw_text(20, h - 75, "Alumna: Samantha Gonzalez C")
    _draw_text(20, h - 95, "Materia: Graficacion")
    _draw_text(20, h - 115, "Periodo Escolar: Ciclo 2026")
    _draw_text(20, h - 135, "Profesor: Rocio Elizabeth Pulido Alba")

    _restore_3d()


def _draw_scenario_label():
    """Muestra el nombre del escenario en la esquina."""
    _setup_2d()
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    name = scenarios.get_scenario_name()
    label = f"Escenario: {name}"

    glColor3f(1.0, 1.0, 1.0)
    _draw_text(w - len(label) * 9 - 15, h - 20, label)

    # Indicador de sonido
    sound_label = "[Sonido ON]" if state.sound_enabled else "[Sonido OFF]"
    glColor3f(0.5, 1.0, 0.5) if state.sound_enabled else glColor3f(1.0, 0.5, 0.5)
    _draw_text(w - len(sound_label) * 9 - 15, h - 35, sound_label)

    # Hint
    glColor3f(1.0, 1.0, 1.0)
    _draw_text(10, 15, "H: Instrucciones | A: Acerca de")

    _restore_3d()


# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

def main():
    """Función principal: configura GLUT y ejecuta el bucle."""
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 700)
    glutCreateWindow(b"Robot Espacial 3D - Evaluacion G2_T3")

    init()

    # Callbacks de renderizado
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    # Input centralizado
    glutKeyboardFunc(input_handlers.keyboard)
    glutMouseFunc(input_handlers.mouse)
    glutMotionFunc(input_handlers.motion)
    glutSpecialFunc(input_handlers.special_keys)
    glutSpecialUpFunc(input_handlers.special_keys_up)

    # Timer de actualización (~60 FPS)
    glutTimerFunc(16, update_module.update, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()
