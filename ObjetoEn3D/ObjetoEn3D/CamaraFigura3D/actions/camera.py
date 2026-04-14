# ============================================================
# camera.py - Control de cámara FPS en OpenGL
# ============================================================
# 7 movimientos de cámara:
# 1. Flechas arriba/abajo → mover adelante/atrás
# 2. Flechas izq/der → paneo lateral
# 3. Scroll → zoom in/out (via state.zoom)
# 4. Click+drag → rotar vista (yaw/pitch)
# 5. PageUp/PageDown → mover arriba/abajo en Y
# 6. Home → reset a posición inicial
# ============================================================

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from actions import state

# ─── Variables de estado de la cámara ───
cam_pos = [0.0, 1.5, 6.0]
yaw = 0.0
pitch = 0.0

cam_speed = 0.2
mouse_down = False
last_mouse_x = 0
last_mouse_y = 0

# Valores iniciales para reset
_INITIAL_POS = [0.0, 1.5, 6.0]
_INITIAL_YAW = 0.0
_INITIAL_PITCH = 0.0


def apply_camera():
    """Aplica las transformaciones de la cámara a la escena."""
    global cam_pos, yaw, pitch
    glRotatef(-pitch, 1.0, 0.0, 0.0)
    glRotatef(-yaw, 0.0, 1.0, 0.0)
    glTranslatef(-cam_pos[0], -cam_pos[1], -cam_pos[2])


def handle_special_keys(key, x, y):
    """Flechas del teclado para mover la cámara."""
    global cam_pos, yaw

    forward = [
        math.sin(math.radians(yaw)),
        0,
        -math.cos(math.radians(yaw))
    ]
    right = [
        math.cos(math.radians(yaw)),
        0,
        math.sin(math.radians(yaw))
    ]

    if key == GLUT_KEY_UP:
        cam_pos[0] += forward[0] * cam_speed
        cam_pos[2] += forward[2] * cam_speed
    elif key == GLUT_KEY_DOWN:
        cam_pos[0] -= forward[0] * cam_speed
        cam_pos[2] -= forward[2] * cam_speed
    elif key == GLUT_KEY_LEFT:
        cam_pos[0] -= right[0] * cam_speed
        cam_pos[2] -= right[2] * cam_speed
    elif key == GLUT_KEY_RIGHT:
        cam_pos[0] += right[0] * cam_speed
        cam_pos[2] += right[2] * cam_speed

    glutPostRedisplay()


def mouse(button, button_state, x, y):
    """Click izquierdo para activar rotación con arrastre."""
    global mouse_down, last_mouse_x, last_mouse_y

    if button == GLUT_LEFT_BUTTON:
        mouse_down = (button_state == GLUT_DOWN)
        last_mouse_x = x
        last_mouse_y = y


def motion(x, y):
    """Rotar cámara arrastrando con click izquierdo."""
    global yaw, pitch, last_mouse_x, last_mouse_y

    if not mouse_down:
        return

    dx = x - last_mouse_x
    dy = y - last_mouse_y

    yaw += dx * 0.2
    pitch += dy * 0.2
    pitch = max(-89, min(89, pitch))

    last_mouse_x = x
    last_mouse_y = y

    glutPostRedisplay()


def move_vertical(amount):
    """Mueve la cámara arriba/abajo en el eje Y.

    Args:
        amount: Positivo sube, negativo baja.
    """
    global cam_pos
    cam_pos[1] += amount
    glutPostRedisplay()


def reset_camera():
    """Restaura la cámara a su posición y orientación inicial."""
    global cam_pos, yaw, pitch
    cam_pos = list(_INITIAL_POS)
    yaw = _INITIAL_YAW
    pitch = _INITIAL_PITCH
    glutPostRedisplay()
