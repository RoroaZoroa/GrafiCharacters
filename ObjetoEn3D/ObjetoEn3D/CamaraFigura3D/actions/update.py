# ============================================================
# update.py - Lógica de actualización por frame (~60fps)
# ============================================================
# Actualiza animaciones, reacciones, movimiento, y límites.
# Se llama cada 16ms via glutTimerFunc.
# ============================================================

from OpenGL.GLUT import *
from actions import state


def enforce_scene_bounds():
    """Limita la posición del pingüino dentro de los bordes de la escena."""
    x_min, x_max = state.scene_bounds["x"]
    z_min, z_max = state.scene_bounds["z"]
    state.penguin_x = max(x_min, min(x_max, state.penguin_x))
    state.penguin_z = max(z_min, min(z_max, state.penguin_z))


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

    # ─── Movimiento continuo con teclas presionadas ───
    if state.key_up:
        state.penguin_z -= state.penguin_speed
    if state.key_down:
        state.penguin_z += state.penguin_speed
    if state.key_left:
        state.penguin_x -= state.penguin_speed
    if state.key_right:
        state.penguin_x += state.penguin_speed

    # ─── Limitar posición ───
    enforce_scene_bounds()

    # ─── Redibujar y programar siguiente update ───
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)