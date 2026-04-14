# ============================================================
# input_handlers.py - Manejo centralizado de entrada del usuario
# ============================================================
# Teclas de expresiones, movimientos, escenarios, sonido, etc.
# ============================================================

from OpenGL.GLUT import *
from actions import state
from actions import camera
from utils import sounds
import sys


def keyboard(key, x, y):
    """Maneja teclas normales del teclado."""
    b = key

    # ─── Movimientos del personaje ───
    if b == b'w':                          # Caminar on/off
        state.walking = not state.walking
        if state.walking:
            sounds.play_sound("walk")
    elif b == b'j':                        # Saltar
        state.reaction_type = "jump"
        state.reaction_timer = 0
        sounds.play_sound("jump")
    elif b == b'k':                        # Girar (spin)
        state.reaction_type = "spin"
        state.reaction_timer = 0
        sounds.play_sound("spin")
    elif b == b's':                        # Temblar (shake)
        state.reaction_type = "shake"
        state.reaction_timer = 0
        sounds.play_sound("shake")
    elif b == b'e':                        # Mover brazos (wave)
        state.reaction_type = "wave_arms"
        state.reaction_timer = 0
        sounds.play_sound("wave_arms")

    # ─── Expresiones ───
    elif b == b'y':                        # Happy / Feliz
        state.expression = "happy"
        sounds.play_sound("happy")
    elif b == b't':                        # Sad / Triste
        state.expression = "sad"
        sounds.play_sound("sad")
    elif b == b'u':                        # Surprised / Sorpresa
        state.expression = "surprised"
        sounds.play_sound("surprised")
    elif b == b'g':                        # Angry / Enojado
        state.expression = "angry"
        sounds.play_sound("angry")
    elif b == b'v':                        # Scared / Miedo
        state.expression = "scared"
        sounds.play_sound("scared")
    elif b == b'n':                        # Neutral
        state.expression = "neutral"
        sounds.play_sound("neutral")

    # ─── Escenarios (teclas 1-5) ───
    elif b == b'1':
        state.current_scenario = 1
        sounds.play_sound("scenario")
    elif b == b'2':
        state.current_scenario = 2
        sounds.play_sound("scenario")
    elif b == b'3':
        state.current_scenario = 3
        sounds.play_sound("scenario")
    elif b == b'4':
        state.current_scenario = 4
        sounds.play_sound("scenario")
    elif b == b'5':
        state.current_scenario = 5
        sounds.play_sound("scenario")

    # ─── Sonido on/off ───
    elif b == b'm':
        sounds.toggle_sound()

    # ─── HUD ───
    elif b == b'h':                        # Instrucciones
        state.show_instructions = not state.show_instructions
        state.show_about = False
    elif b == b'a':                        # Acerca de
        state.show_about = not state.show_about
        state.show_instructions = False

    # ─── Cámara follow toggle ───
    elif b == b'f':
        state.camera_follow = not state.camera_follow
        print("Camara sigue al personaje:", state.camera_follow)

    # ─── Reset ───
    elif b == b'r':
        state.penguin_x = 0.0
        state.penguin_z = 0.0
        state.rotate_x = 0.0
        state.rotate_y = 0.0
        state.zoom = 10.0
        camera.reset_camera()

    # ─── Salir ───
    elif b == b'\x1b':                     # ESC
        glutLeaveMainLoop()

    glutPostRedisplay()


def mouse(button, state_btn, x, y):
    """Maneja eventos del ratón: clicks y scroll."""
    # Scroll (zoom)
    if button == 3 and state_btn == GLUT_DOWN:
        state.zoom -= 1.0
        if state.zoom < 2:
            state.zoom = 2
        glutPostRedisplay()
        return
    elif button == 4 and state_btn == GLUT_DOWN:
        state.zoom += 1.0
        if state.zoom > 60:
            state.zoom = 60
        glutPostRedisplay()
        return

    # Click normal - delegar a cámara
    camera.mouse(button, state_btn, x, y)
    glutPostRedisplay()


def motion(x, y):
    """Maneja movimiento del ratón con botón presionado."""
    camera.motion(x, y)
    glutPostRedisplay()


def special_keys(key, x, y):
    """Maneja teclas especiales (flechas, PageUp, Home, etc.)."""
    # Flechas → mover pingüino
    if key == GLUT_KEY_UP:
        state.key_up = True
        state.penguin_z -= state.penguin_speed
    elif key == GLUT_KEY_DOWN:
        state.key_down = True
        state.penguin_z += state.penguin_speed
    elif key == GLUT_KEY_LEFT:
        state.key_left = True
        state.penguin_x -= state.penguin_speed
    elif key == GLUT_KEY_RIGHT:
        state.key_right = True
        state.penguin_x += state.penguin_speed

    # PageUp/PageDown → cámara arriba/abajo
    elif key == GLUT_KEY_PAGE_UP:
        camera.move_vertical(0.3)
    elif key == GLUT_KEY_PAGE_DOWN:
        camera.move_vertical(-0.3)

    # Home → reset cámara
    elif key == GLUT_KEY_HOME:
        camera.reset_camera()

    # Mover cámara con flechas también
    camera.handle_special_keys(key, x, y)

    glutPostRedisplay()


def special_keys_up(key, x, y):
    """Maneja cuando se sueltan teclas especiales."""
    if key == GLUT_KEY_UP:
        state.key_up = False
    elif key == GLUT_KEY_DOWN:
        state.key_down = False
    elif key == GLUT_KEY_LEFT:
        state.key_left = False
    elif key == GLUT_KEY_RIGHT:
        state.key_right = False
