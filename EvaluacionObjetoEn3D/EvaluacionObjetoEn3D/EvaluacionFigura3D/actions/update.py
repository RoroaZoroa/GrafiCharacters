# ============================================================
# update.py - Lógica de actualización por frame (~60fps)
# ============================================================
# Actualiza animaciones, reacciones, movimiento, y límites.
# Se llama cada 16ms via glutTimerFunc.
# ============================================================

from OpenGL.GLUT import *
import math
from actions import state
from utils import sounds

def check_collisions():
    """Verifica colisiones entre el robot y los 3 objetos interactivos."""
    rx, rz = state.robot_x, state.robot_z
    radius = 0.9
    
    # 1. Cubo Energía Cyan (3, 3)
    if math.dist((rx, rz), (3, 3)) < radius:
        if state.reaction_type != "nod":
            if not hasattr(state, 'prev_expr'): state.prev_expr = state.expression
            state.reaction_type = "nod"
            state.reaction_timer = 0
            state.color_override = (0.2, 1.0, 1.0)
            state.color_override_timer = 60
            sounds.play_sound("nod")
            
    # 2. Cristal Rombo Espinoso (-4, 3)
    elif math.dist((rx, rz), (-4, 3)) < radius:
        if state.expression != "scared" or state.reaction_type != "shake":
            if not hasattr(state, 'prev_expr'): state.prev_expr = state.expression
            state.expression = "scared"
            state.reaction_type = "shake"
            state.reaction_timer = 0
            state.color_override = (1.0, 0.3, 0.3)
            state.color_override_timer = 60
            sounds.play_sound("scared")
            
    # 3. Trampolín (0, 3)
    elif math.dist((rx, rz), (0, 3)) < radius:
        if state.reaction_type != "jump":
            if not hasattr(state, 'prev_expr'): state.prev_expr = state.expression
            state.expression = "surprised"
            state.reaction_type = "jump"
            state.reaction_timer = 0
            sounds.play_sound("jump")


def enforce_scene_bounds():
    """Limita la posición del robot dentro de los bordes de la escena."""
    x_min, x_max = state.scene_bounds["x"]
    z_min, z_max = state.scene_bounds["z"]
    state.robot_x = max(x_min, min(x_max, state.robot_x))
    state.robot_z = max(z_min, min(z_max, state.robot_z))


def update(value):
    """Función principal de update, llamada cada 16ms."""

    # ─── Animación de caminar ───
    if state.walking:
        state.animation_angle += 0.15
        state.tail_angle += 0.08

    # ─── Parpadeo siempre activo ───
    state.blink_timer += 0.05

    # ─── Reacciones con temporizador ───
    if state.reaction_type:
        state.reaction_timer += 1
        if state.reaction_timer >= state.reaction_duration:
            state.reaction_type = None
            state.reaction_timer = 0
            if hasattr(state, 'prev_expr'):
                state.expression = state.prev_expr
                del state.prev_expr

    # ─── Movimiento continuo con teclas presionadas ───
    if state.key_up:
        state.robot_z -= state.robot_speed
    if state.key_down:
        state.robot_z += state.robot_speed
    if state.key_left:
        state.robot_x -= state.robot_speed
    if state.key_right:
        state.robot_x += state.robot_speed

    # ─── Limitar posición e interactuar ───
    enforce_scene_bounds()
    check_collisions()
    
    if hasattr(state, 'color_override') and state.color_override_timer > 0:
        state.color_override_timer -= 1
        if state.color_override_timer <= 0:
            state.color_override = None

    # ─── Redibujar y programar siguiente update ───
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)