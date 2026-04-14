# ============================================================
# penguin.py - Modelo 3D de un Pingüino Bebé con expresiones y movimientos
# ============================================================
# Primitivas: esferas, conos, cilindros escalados.
# Expresiones: happy, sad, surprised, angry, scared (+neutral)
# Movimientos: walk, jump, spin, shake, wave_arms
# ============================================================

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from actions import state

# ─── Paleta de colores ───
DARK_GRAY   = (0.15, 0.15, 0.20)
WHITE       = (0.95, 0.95, 0.97)
ORANGE      = (0.95, 0.55, 0.10)
BLACK       = (0.05, 0.05, 0.05)
SOFT_GRAY   = (0.55, 0.58, 0.65)
PINK        = (0.95, 0.70, 0.75)
HIGHLIGHT   = (1.0, 1.0, 1.0)
RED         = (0.9, 0.2, 0.2)


# ═══════════════════════════════════════════
# PARTES DEL CUERPO
# ═══════════════════════════════════════════

def draw_body():
    """Cuerpo principal ovalado + panza blanca."""
    glPushMatrix()
    glScalef(1.0, 1.15, 0.9)
    glColor3f(*DARK_GRAY)
    glutSolidSphere(0.55, 32, 32)
    glPopMatrix()

    # Panza blanca
    glPushMatrix()
    glTranslatef(0, -0.05, 0.18)
    glScalef(0.95, 1.1, 0.75)
    glColor3f(*WHITE)
    glutSolidSphere(0.52, 32, 32)
    glPopMatrix()


def draw_head():
    """Cabeza esférica oscura + cara blanca frontal."""
    glPushMatrix()
    glTranslatef(0, 0.72, 0.0)
    glColor3f(*DARK_GRAY)
    glutSolidSphere(0.35, 32, 32)
    glPopMatrix()

    # Cara blanca
    glPushMatrix()
    glTranslatef(0, 0.70, 0.15)
    glScalef(0.8, 0.85, 0.6)
    glColor3f(*WHITE)
    glutSolidSphere(0.30, 32, 32)
    glPopMatrix()


def draw_eyes():
    """Ojos con expresiones dinámicas y parpadeo."""
    blink = math.sin(state.blink_timer) > 0.95
    expr = state.expression

    # Tamaños dinámicos
    sclera_w, sclera_h = 0.07, 0.07
    pupil_w, pupil_h = 0.055, 0.055
    pupil_y_offset = 0.0

    if expr == "sad":
        # Triste: pequeña pupila
        pupil_w, pupil_h = 0.05, 0.05
    elif expr == "angry":
        # Enojado: pupila un poco más pequeña y abajo + cejas furiosas
        pupil_w, pupil_h = 0.045, 0.045
        pupil_y_offset = -0.01
    elif expr == "surprised":
        # Sorpresa: mostrar más esclerótica blanca y pupilas grandes pero que dejen ver el blanco
        sclera_w, sclera_h = 0.08, 0.09
        pupil_w, pupil_h = 0.065, 0.065
    elif expr == "scared":
        # Miedo: pupila más chica para que se note la esclerótica blanca (ojos pelados)
        sclera_w, sclera_h = 0.07, 0.07
        pupil_w, pupil_h = 0.045, 0.045
    elif expr == "happy":
        # Feliz: ojos grandes y algo entrecerrados (sonrisa en los ojos)
        sclera_w, sclera_h = 0.088, 0.078
        pupil_w, pupil_h = 0.068, 0.068
        pupil_y_offset = 0.008

    for dx in [-0.12, 0.12]:
        glPushMatrix()
        # Temblor para miedo
        if expr == "scared":
            offset = math.sin(state.blink_timer * 15) * 0.005
            glTranslatef(offset, 0, 0)
        
        glTranslatef(dx, 0.78, 0.28)

        # Esclerótica (blanco del ojo)
        glPushMatrix()
        if blink:
            glScalef(1.0, 0.15, 1.0)
        else:
            glScalef(sclera_w/0.07, sclera_h/0.07, 1.0)
        glColor3f(*WHITE)
        glutSolidSphere(0.07, 20, 20)
        glPopMatrix()

        # Pupila (negro)
        glPushMatrix()
        glTranslatef(0, pupil_y_offset, 0.04) # Un poco hacia adelante
        if blink:
            glScalef(1.0, 0.15, 1.0)
        else:
            glScalef(pupil_w/0.055, pupil_h/0.055, 1.0)
        glColor3f(*BLACK)
        glutSolidSphere(0.055, 20, 20)
        glPopMatrix()

        # Brillos (solo si no parpadea ni tiene miedo/enojo)
        if not blink and expr not in ("scared", "angry"):
            glPushMatrix()
            glTranslatef(0.02, pupil_y_offset + 0.02, 0.07)
            # Brillo principal más grande si está feliz
            brillo_size = 0.022 if expr == "happy" else 0.015
            glColor3f(*HIGHLIGHT)
            glutSolidSphere(brillo_size, 12, 12)
            glPopMatrix()
            
            # Brillo secundario extra si está feliz
            if expr == "happy":
                glPushMatrix()
                glTranslatef(-0.015, pupil_y_offset - 0.01, 0.07)
                glColor3f(*HIGHLIGHT)
                glutSolidSphere(0.012, 10, 10)
                glPopMatrix()

        glPopMatrix()

    # Cejas dinámicas (solo enojo y tristeza; feliz sin cejas)
    if expr in ("angry", "sad"):
        _draw_eyebrows(expr)


def _draw_eyebrows(mood):
    r"""Cejas. Angry: hacia adentro (/ \). Sad: hacia afuera (\ /)."""
    if mood == "angry":
        left_rot, right_rot = -25, 25
        y_offset = -0.015
    else:  # sad
        left_rot, right_rot = 20, -20
        y_offset = 0.01

    for dx, rot in [(-0.12, left_rot), (0.12, right_rot)]:
        glPushMatrix()
        glTranslatef(dx, 0.88 + y_offset, 0.32)
        glRotatef(rot, 0, 0, 1)
        glScalef(1.8, 0.3, 0.5)
        glColor3f(0.65, 0.65, 0.70)
        glutSolidSphere(0.04, 12, 12)
        glPopMatrix()


def draw_beak():
    """Pico naranja con boca expresiva."""
    # Pico superior
    glPushMatrix()
    glTranslatef(0, 0.72, 0.33)
    glScalef(1.0, 0.6, 1.0)
    glColor3f(*ORANGE)
    glutSolidSphere(0.07, 16, 16)
    glPopMatrix()

    # Pico inferior / boca
    expr = state.expression
    if expr == "happy":
        # Boca abierta feliz en forma de D girada (curva arriba, abierta)
        # Interior de la boca (forma de D: ancha, curva al techo)
        glPushMatrix()
        glTranslatef(0, 0.665, 0.38)
        glRotatef(-25, 1, 0, 0)
        glScalef(1.25, 0.5, 0.45)
        glColor3f(0.82, 0.28, 0.28)
        glutSolidSphere(0.065, 20, 20)
        glPopMatrix()
        # Borde superior del pico (curva de la D, sonrisa)
        glPushMatrix()
        glTranslatef(0, 0.71, 0.355)
        glScalef(1.15, 0.22, 0.5)
        glColor3f(0.92, 0.5, 0.1)
        glutSolidSphere(0.055, 16, 16)
        glPopMatrix()
    elif expr == "surprised":
        # Boca abierta (círculo)
        glPushMatrix()
        glTranslatef(0, 0.67, 0.38)
        glScalef(0.6, 0.8, 0.6)
        glColor3f(0.80, 0.30, 0.20)
        glutSolidSphere(0.05, 16, 16)
        glPopMatrix()
    else:
        # Punta del pico normal
        glPushMatrix()
        glTranslatef(0, 0.71, 0.38)
        glScalef(0.8, 0.4, 1.0)
        glColor3f(0.90, 0.45, 0.05)
        glutSolidSphere(0.05, 16, 16)
        glPopMatrix()


def draw_cheeks():
    """Mejillas sonrojadas (más intensas cuando está happy o scared)."""
    expr = state.expression
    if expr == "happy":
        color = (1.0, 0.48, 0.55)
        scale = 1.45
    elif expr == "scared":
        color = (0.85, 0.85, 0.95)  # Pálido
        scale = 1.1
    else:
        color = PINK
        scale = 1.0

    for dx in [-0.18, 0.18]:
        glPushMatrix()
        glTranslatef(dx, 0.68, 0.28)
        glScalef(scale, 0.7, 0.5)
        glColor3f(*color)
        glutSolidSphere(0.06, 16, 16)
        glPopMatrix()


def draw_wings():
    """Alas/aletas con animación de wave_arms."""
    for i, dx in enumerate([-0.50, 0.50]):
        glPushMatrix()
        glTranslatef(dx, 0.05, 0.0)

        # Animación de mover brazos
        if state.reaction_type == "wave_arms":
            wave = math.sin(state.reaction_timer * 0.3) * 45
            if dx < 0:
                glRotatef(wave, 0, 0, 1)
            else:
                glRotatef(-wave, 0, 0, 1)
        elif state.walking:
            swing = math.sin(state.animation_angle + (i * math.pi)) * 15
            glRotatef(swing, 1, 0, 0)

        # Ala principal
        glPushMatrix()
        glScalef(0.18, 0.85, 0.40)
        glColor3f(0.10, 0.10, 0.12)
        glutSolidSphere(0.45, 24, 24)
        glPopMatrix()

        # Punta inferior
        glPushMatrix()
        glTranslatef(0, -0.27, 0.0)
        glScalef(0.15, 0.45, 0.35)
        glColor3f(0.08, 0.08, 0.10)
        glutSolidSphere(0.38, 20, 20)
        glPopMatrix()

        glPopMatrix()


def draw_feet():
    """Patas naranjas con animación de caminar."""
    for i, dx in enumerate([-0.18, 0.18]):
        glPushMatrix()
        glTranslatef(dx, -0.65, 0.12)

        # Animación de caminar
        if state.walking:
            swing = math.sin(state.animation_angle + (i * math.pi)) * 20
            glRotatef(swing, 1, 0, 0)

        # Pie ovalado
        glPushMatrix()
        glScalef(1.3, 0.3, 1.5)
        glColor3f(*ORANGE)
        glutSolidSphere(0.12, 20, 20)
        glPopMatrix()

        # Dedos
        for ddx in [-0.05, 0.0, 0.05]:
            glPushMatrix()
            glTranslatef(ddx, -0.02, 0.14)
            glScalef(0.6, 0.25, 1.0)
            glColor3f(0.90, 0.45, 0.05)
            glutSolidSphere(0.05, 12, 12)
            glPopMatrix()

        glPopMatrix()


def draw_tail():
    """Colita pequeña trasera."""
    glPushMatrix()
    glTranslatef(0, -0.15, -0.45)

    # Mover cola si está caminando
    if state.walking:
        wag = math.sin(state.tail_angle) * 10
        glRotatef(wag, 0, 1, 0)

    glScalef(0.6, 0.5, 0.8)
    glColor3f(*DARK_GRAY)
    glutSolidSphere(0.15, 16, 16)
    glPopMatrix()


def draw_head_fluff():
    """Plumón de bebé en la cabeza."""
    for dx, dy in [(0, 0.12), (-0.06, 0.10), (0.06, 0.10)]:
        glPushMatrix()
        glTranslatef(dx, 1.02 + dy, -0.02)
        glScalef(0.3, 1.0, 0.3)
        glColor3f(*SOFT_GRAY)
        glutSolidSphere(0.04, 12, 12)
        glPopMatrix()


# ═══════════════════════════════════════════
# FUNCIÓN PRINCIPAL - DIBUJA AL PINGÜINO COMPLETO
# ═══════════════════════════════════════════

def draw_penguin_full():
    """Dibuja al pingüino bebé completo con expresiones y movimientos."""
    glPushMatrix()

    # ─── Aplicar movimientos/reacciones globales ───
    if state.reaction_type == "jump":
        progress = state.reaction_timer / state.reaction_duration
        y_offset = math.sin(math.pi * progress) * 0.5
        glTranslatef(0, y_offset, 0)

    elif state.reaction_type == "spin":
        progress = state.reaction_timer / state.reaction_duration
        angle = 360 * progress
        glRotatef(angle, 0, 1, 0)

    elif state.reaction_type == "shake":
        x_offset = math.sin(state.reaction_timer * 0.5 * math.pi) * 0.15
        glTranslatef(x_offset, 0, 0)

    # Expresión scared → temblor sutil constante
    if state.expression == "scared":
        tremor = math.sin(state.blink_timer * 15) * 0.02
        glTranslatef(tremor, 0, tremor)

    # ─── Dibujar todas las partes ───
    draw_body()
    draw_head()
    draw_eyes()
    draw_cheeks()
    draw_beak()
    draw_wings()
    draw_feet()
    draw_tail()
    draw_head_fluff()

    glPopMatrix()