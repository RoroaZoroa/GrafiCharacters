# ============================================================
# scenarios.py - 5 Escenarios 3D para el Pingüino
# ============================================================
# Cada escenario dibuja un fondo temático con primitivas OpenGL.
# El fondo (glClearColor) se cambia según el escenario activo.
# ============================================================

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from actions import state

# Colores de fondo por escenario (cielo/ambiente)
SCENARIO_COLORS = {
    1: (0.02, 0.03, 0.12, 1.0),   # Noche Ártica - azul muy oscuro
    2: (0.45, 0.72, 0.92, 1.0),   # Parque - cielo azul suave
    3: (0.25, 0.65, 0.92, 1.0),   # Playa - azul tropical
    4: (0.55, 0.68, 0.82, 1.0),   # Montaña - cielo gris-azulado
    5: (0.15, 0.18, 0.28, 1.0),   # Ciudad - noche urbana
}

SCENARIO_NAMES = {
    1: "Noche Artica",
    2: "Parque",
    3: "Playa",
    4: "Montana Nevada",
    5: "Ciudad",
}


def apply_scenario_background():
    """Aplica el color de fondo según el escenario actual."""
    color = SCENARIO_COLORS.get(state.current_scenario, (0.53, 0.81, 0.98, 1.0))
    glClearColor(*color)


def draw_scenario():
    """Dibuja el escenario actual."""
    s = state.current_scenario
    _draw_ground(s)
    if s == 1:
        _draw_arctic_night()
    elif s == 2:
        _draw_park()
    elif s == 3:
        _draw_beach()
    elif s == 4:
        _draw_mountain()
    elif s == 5:
        _draw_city()


def _draw_ground(scenario):
    """Dibuja el suelo según el escenario (con variación sutil en Parque/Playa)."""
    glPushMatrix()
    glDisable(GL_LIGHTING)

    colors = {
        1: (0.88, 0.93, 0.98),   # Hielo/nieve brillante (Noche Ártica)
        2: (0.22, 0.58, 0.18),   # Pasto verde más vivo (Parque)
        3: (0.94, 0.86, 0.62),   # Arena cálida (Playa)
        4: (0.92, 0.95, 0.98),   # Nieve (Montaña Nevada)
        5: (0.28, 0.28, 0.32),   # Asfalto oscuro (Ciudad)
    }
    glColor3f(*colors.get(scenario, (0.5, 0.5, 0.5)))

    glBegin(GL_QUADS)
    size = 15
    glVertex3f(-size, -0.71, -size)
    glVertex3f( size, -0.71, -size)
    glVertex3f( size, -0.71,  size)
    glVertex3f(-size, -0.71,  size)
    glEnd()

    glEnable(GL_LIGHTING)
    glPopMatrix()


# ─── Escenario 1: Parque ───
def _draw_park():
    """Parque con árboles, nubes, flores, banco, sendero y arbustos."""
    # Sendero (franja de tierra clara) - mucho más largo
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(0.65, 0.52, 0.38)
    glBegin(GL_QUADS)
    glVertex3f(-2, -0.708, -8)
    glVertex3f(2, -0.708, -8)
    glVertex3f(1.5, -0.708, 6)
    glVertex3f(-1.5, -0.708, 6)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Árboles variados (posición x, z, escala copa) - 1.5x más grandes
    trees = [(-3.5, -4, 1.5), (4, -3, 1.275), (-5.5, -6, 1.725), (2, -7, 1.35), (6, -5, 1.5), (-1, -3.5, 1.125)]
    for tx, tz, scale in trees:
        _draw_tree(tx, tz, scale)

    # Sol con halo suave - 1.5x más grande
    glPushMatrix()
    glTranslatef(5, 5.5, -9)
    glColor3f(1.0, 0.92, 0.35)
    glutSolidSphere(1.275, 24, 24)
    glPopMatrix()

    # Nubes (esferas superpuestas, más esponjosas) - 1.5x más grandes
    for cx, cy, cz in [(2, 4.5, -7), (-3, 5, -8), (6, 3.8, -6)]:
        glPushMatrix()
        glTranslatef(cx, cy, cz)
        glColor3f(1.0, 1.0, 1.0)
        glutSolidSphere(0.63, 12, 12)
        glTranslatef(0.57, 0.12, 0)
        glutSolidSphere(0.54, 12, 12)
        glTranslatef(-0.33, 0.33, 0.18)
        glutSolidSphere(0.48, 12, 12)
        glPopMatrix()

    # Flores (menos cantidad, más distribuidas) - 1.5x más grandes
    flower_data = [
        (-1, -2, 1.0, 0.3, 0.4), (1.5, -3, 1.0, 0.5, 0.6), 
        (-2, -5, 1.0, 0.9, 0.3), (3, -1, 0.95, 0.75, 0.85)
    ]
    for fx, fz, r, g, b in flower_data:
        glPushMatrix()
        glTranslatef(fx, -0.65, fz)
        glColor3f(r, g, b)
        glutSolidSphere(0.135, 12, 12)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(fx, -0.70, fz)
        glColor3f(0.15, 0.5, 0.12)
        glScalef(0.12, 0.6, 0.12)
        glutSolidCube(0.4)
        glPopMatrix()

    # Arbustos (menos cantidad) - 1.5x más grandes
    for bx, bz in [(1, -4), (-4.5, -3)]:
        glPushMatrix()
        glTranslatef(bx, -0.55, bz)
        glScalef(0.6, 0.375, 0.6)
        glColor3f(0.18, 0.48, 0.2)
        glutSolidSphere(0.5, 14, 14)
        glPopMatrix()

    # Banco (asiento + respaldo + 4 patas)
    glPushMatrix()
    glTranslatef(-4, -0.35, -2)
    glColor3f(0.4, 0.25, 0.12)
    glScalef(1.2, 0.12, 0.35)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-4, 0.1, -2.18)
    glScalef(1.2, 0.5, 0.08)
    glutSolidCube(1)
    glPopMatrix()
    # Patas del banco (4 cubos)
    leg_y_center = -0.57
    leg_h = 0.26
    leg_w = 0.1
    for lx, lz in [(-4.5, -1.88), (-3.5, -1.88), (-4.5, -2.12), (-3.5, -2.12)]:
        glPushMatrix()
        glTranslatef(lx, leg_y_center, lz)
        glColor3f(0.35, 0.22, 0.1)
        glScalef(leg_w, leg_h, leg_w)
        glutSolidCube(1)
        glPopMatrix()


def _draw_tree(x, z, crown_scale=1.0):
    """Dibuja un árbol con tronco y copa (escala opcional) - 1.5x más grande."""
    glPushMatrix()
    glTranslatef(x, -0.1, z)
    glColor3f(0.42, 0.28, 0.12)
    glScalef(0.21, 1.65, 0.21)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, 0.45, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.12, 0.48, 0.14)
    glScalef(crown_scale, crown_scale, crown_scale)
    glutSolidCone(0.825, 1.725, 16, 8)
    glPopMatrix()


# ─── Escenario 2: Noche Ártica ───
def _draw_arctic_night():
    """Noche ártica con aurora, estrellas, luna, iglú y bloques de hielo."""
    import random
    random.seed(42)

    glDisable(GL_LIGHTING)

    # Aurora boreal (bandas largas que cruzan todo el cielo)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    # Banda verde principal (más larga en X y en altura)
    glColor4f(0.25, 0.82, 0.55, 0.28)
    glVertex3f(-18, 3.5, -14)
    glVertex3f(18, 4.5, -14)
    glVertex3f(16, 7.5, -14)
    glVertex3f(-16, 6.5, -14)
    # Banda verde secundaria (ondulada)
    glColor4f(0.15, 0.7, 0.45, 0.22)
    glVertex3f(-17, 4.2, -13)
    glVertex3f(17, 5.2, -13)
    glVertex3f(15, 8.2, -13)
    glVertex3f(-15, 7.2, -13)
    # Banda azul-verde
    glColor4f(0.12, 0.55, 0.72, 0.2)
    glVertex3f(-16, 5.0, -12)
    glVertex3f(16, 6.0, -12)
    glVertex3f(14, 8.5, -12)
    glVertex3f(-14, 7.5, -12)
    # Banda azul tenue (más alta)
    glColor4f(0.08, 0.4, 0.65, 0.15)
    glVertex3f(-15, 5.8, -11)
    glVertex3f(15, 6.8, -11)
    glVertex3f(13, 9.0, -11)
    glVertex3f(-13, 8.0, -11)
    glEnd()
    glDisable(GL_BLEND)

    # Estrellas (varios tamaños)
    for size, n in [(2.0, 40), (3.5, 25), (5.0, 10)]:
        glPointSize(size)
        glBegin(GL_POINTS)
        glColor3f(1, 0.98, 0.95)
        for _ in range(n):
            sx = random.uniform(-12, 12)
            sy = random.uniform(2, 8)
            sz = random.uniform(-12, -2)
            glVertex3f(sx, sy, sz)
        glEnd()

    # Luna llena con brillo
    glPushMatrix()
    glTranslatef(-4.5, 5.2, -8)
    glColor3f(0.98, 0.98, 0.9)
    glutSolidSphere(0.65, 24, 24)
    glPopMatrix()

    glEnable(GL_LIGHTING)

    # Iglú más grande (cúpula + entrada definida) - 1.5x más grande
    glPushMatrix()
    glTranslatef(3, -0.71, -4)
    glColor3f(0.88, 0.92, 0.97)
    glutSolidSphere(2.325, 24, 12)
    glTranslatef(0, -0.35, 1.2)
    glColor3f(0.2, 0.25, 0.35)
    glScalef(1.05, 1.275, 0.45)
    glutSolidCube(1)
    glPopMatrix()

    # Bloques de hielo / nieve amontonada (varios tamaños) - 1.5x más grandes
    for hx, hz, sx, sy, sz in [
        (-4, -3, 1.05, 0.675, 0.75), (-2, -6, 0.75, 0.525, 0.9), (5, -5, 0.9, 0.75, 0.6),
        (-6, -4, 0.6, 0.45, 0.525), (1, -7, 0.825, 0.6, 0.675), (3.5, -6.5, 0.675, 0.525, 0.6),
    ]:
        glPushMatrix()
        glTranslatef(hx, -0.71 + sy / 2, hz)
        glColor3f(0.72, 0.88, 0.98)
        glScalef(sx, sy, sz)
        glutSolidCube(1)
        glPopMatrix()

    # Muñeco de nieve (3 esferas, más grande) - 1.5x más grande, cerca del pingüino
    glPushMatrix()
    glTranslatef(-1.5, -0.71, -1.5)
    glColor3f(0.96, 0.98, 1.0)
    glutSolidSphere(0.57, 14, 14)
    glTranslatef(0, 0.63, 0)
    glutSolidSphere(0.42, 14, 14)
    glTranslatef(0, 0.525, 0)
    glutSolidSphere(0.3, 12, 12)
    glPopMatrix()


# ─── Escenario 3: Playa ───
def _draw_beach():
    """Playa con mar, palmeras, sombrilla, rocas, conchas y sol."""
    # Mar (con tono más profundo cerca del horizonte)
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor4f(0.08, 0.35, 0.72, 0.75)
    glBegin(GL_QUADS)
    glVertex3f(-15, -0.68, -15)
    glVertex3f(15, -0.68, -15)
    glVertex3f(15, -0.68, -4)
    glVertex3f(-15, -0.68, -4)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Palmeras - 4 bien distribuidas en toda la arena
    _draw_palm_tree(-4, -3, 1.1)
    _draw_palm_tree(3.5, -5, 0.9)
    _draw_palm_tree(-6, -6, 1.2)
    _draw_palm_tree(5, -2.5, 0.85)

    # Sombrilla (poste + cono como sombrilla) - 1.5x más grande
    glPushMatrix()
    glTranslatef(2, -0.1, -3)
    glColor3f(0.25, 0.25, 0.3)
    glScalef(0.06, 1.5, 0.06)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(2, 0.55, -3)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1.0, 0.35, 0.4)
    glutSolidCone(0.75, 0.6, 12, 4)
    glPopMatrix()

    # Rocas en la orilla - 1.5x más grandes
    for rx, rz, scale in [(-2, -2.5, 0.525), (1, -1.8, 0.375), (-4, -3, 0.45), (5, -4, 0.6), (-1, -5, 0.33)]:
        glPushMatrix()
        glTranslatef(rx, -0.65, rz)
        glColor3f(0.5, 0.48, 0.45)
        glScalef(scale, scale * 0.6, scale)
        glutSolidSphere(0.5, 10, 10)
        glPopMatrix()

    # Toalla (plano en la arena) - más grande y extendida
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(-2.5, -0.69, -2)
    glRotatef(15, 0, 1, 0)
    glColor3f(1.0, 0.4, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-0.8, 0, -0.5)
    glVertex3f(0.8, 0, -0.5)
    glVertex3f(0.8, 0, 0.5)
    glVertex3f(-0.8, 0, 0.5)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Conchas y caracoles (esferas aplastadas, distintos tonos) - 1.5x más grandes
    for sx, sz, r, g, b in [
        (1, -2, 0.95, 0.88, 0.75), (-1.5, -1.5, 0.9, 0.82, 0.78),
        (-3, -4, 0.92, 0.85, 0.72), (3.5, -2.5, 0.97, 0.9, 0.8), (0, -3.5, 0.9, 0.85, 0.78),
    ]:
        glPushMatrix()
        glTranslatef(sx, -0.68, sz)
        glScalef(1.0, 0.25, 1.0)
        glColor3f(r, g, b)
        glutSolidSphere(0.18, 12, 12)
        glPopMatrix()

    # Sol - 1.5x más grande
    glPushMatrix()
    glTranslatef(0, 5.8, -10)
    glColor3f(1.0, 0.9, 0.25)
    glutSolidSphere(1.425, 24, 24)
    glPopMatrix()


def _draw_palm_tree(x, z, scale=1.0):
    """Palmera con tronco y hojas (escala opcional) - más alta y hojas más grandes."""
    glPushMatrix()
    glTranslatef(x, -0.1, z)
    glColor3f(0.5, 0.32, 0.18)
    glScalef(0.165 * scale, 3.0 * scale, 0.165 * scale)
    glutSolidCube(1)
    glPopMatrix()
    for angle in range(0, 360, 60):
        glPushMatrix()
        glTranslatef(x, 1.2, z)
        glRotatef(angle, 0, 1, 0)
        glTranslatef(0.76 * scale, 0, 0)
        glRotatef(28, 0, 0, 1)
        glScalef(2.8 * scale, 0.28, 1.0 * scale)
        glColor3f(0.08, 0.52, 0.12)
        glutSolidSphere(0.35, 12, 12)
        glPopMatrix()


# ─── Escenario 4: Montaña Nevada ───
def _draw_mountain():
    """Montañas con nieve, pinos, refugio y lago helado."""
    # Montañas (conos con tonos ligeramente distintos) - 1.5x más grandes
    mountains = [
        (-5, -8, 4.5, 6.0, (0.52, 0.48, 0.44)),
        (0, -10, 6.0, 8.25, (0.58, 0.53, 0.48)),
        (6, -7, 3.75, 5.25, (0.50, 0.47, 0.42)),
        (-7, -5, 3.0, 4.2, (0.55, 0.51, 0.46)),
    ]
    for mx, mz, radius, height, color in mountains:
        glPushMatrix()
        glTranslatef(mx, -0.71, mz)
        glRotatef(-90, 1, 0, 0)
        glColor3f(*color)
        glutSolidCone(radius, height, 24, 12)
        glPopMatrix()

        # Nieve en la cima - 1.5x más grande
        glPushMatrix()
        glTranslatef(mx, -0.71 + height * 0.72, mz)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.96, 0.98, 1.0)
        glutSolidCone(radius * 0.4, height * 0.28, 16, 6)
        glPopMatrix()

    # Lago helado (plano bajo entre montañas)
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(0.75, 0.88, 0.95)
    glBegin(GL_QUADS)
    glVertex3f(-2, -0.70, -6)
    glVertex3f(3, -0.70, -6)
    glVertex3f(3, -0.70, -3)
    glVertex3f(-2, -0.70, -3)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Refugio / cabaña (cuerpo + techo + chimenea) - 4x más grande detrás del pingüino
    glPushMatrix()
    glTranslatef(-3, -0.71, -3)
    glColor3f(0.45, 0.28, 0.18)
    glScalef(2.4, 2.0, 2.0)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-3, 0.29, -3)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.35, 0.22, 0.12)
    glutSolidCone(1.8, 1.4, 8, 4)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-3.15, 0.05, -3.2)
    glColor3f(0.5, 0.32, 0.2)
    glScalef(0.48, 1.0, 0.48)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-3.15, 0.2, -3.2)
    glColor3f(0.4, 0.15, 0.1)
    glutSolidSphere(0.24, 8, 8)
    glPopMatrix()

    # Rocas pequeñas al pie de montañas - 1.5x más grandes
    for rxx, rzz in [(-2, -4), (1, -3), (4, -5)]:
        glPushMatrix()
        glTranslatef(rxx, -0.68, rzz)
        glColor3f(0.48, 0.45, 0.42)
        glScalef(0.3, 0.18, 0.3)
        glutSolidSphere(0.5, 10, 10)
        glPopMatrix()

    # Pinos (más y con tamaños variados) - 1.5x más grandes
    for px, pz, tree_scale in [
        (-3, -3, 1.5), (2, -2, 1.35), (5, -4, 1.65), (-6, -2, 1.275),
        (0, -5, 1.125), (4, -1, 1.425), (-2, -7, 1.2),
    ]:
        glPushMatrix()
        glTranslatef(px, -0.2, pz)
        glColor3f(0.32, 0.20, 0.12)
        glScalef(0.105 * tree_scale, 1.125 * tree_scale, 0.105 * tree_scale)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(px, 0.28, pz)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.08, 0.32, 0.10)
        glScalef(tree_scale, tree_scale, 1.0)
        glutSolidCone(0.51, 1.125, 12, 6)
        glPopMatrix()


# ─── Escenario 5: Ciudad ───
def _draw_city():
    """Ciudad con edificios, calle, faroles y detalles."""
    # Calle (franja oscura) y aceras (gris claro)
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(0.22, 0.22, 0.25)
    glBegin(GL_QUADS)
    glVertex3f(-15, -0.705, -1.5)
    glVertex3f(15, -0.705, -1.5)
    glVertex3f(15, -0.705, -2.8)
    glVertex3f(-15, -0.705, -2.8)
    glEnd()
    glColor3f(0.4, 0.4, 0.42)
    glBegin(GL_QUADS)
    glVertex3f(-15, -0.704, -2.85)
    glVertex3f(15, -0.704, -2.85)
    glVertex3f(15, -0.704, -3.5)
    glVertex3f(-15, -0.704, -3.5)
    glVertex3f(-15, -0.704, -1.45)
    glVertex3f(15, -0.704, -1.45)
    glVertex3f(15, -0.704, -0.8)
    glVertex3f(-15, -0.704, -0.8)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Edificios 1.5x más grandes (sx, sy, sz)
    buildings = [
        (-5.5, -5, 2.03, 5.1, 1.65, (0.48, 0.48, 0.52)),
        (-3.2, -6, 1.73, 7.05, 1.43, (0.38, 0.42, 0.52)),
        (-1, -5, 2.25, 4.35, 1.95, (0.52, 0.42, 0.38)),
        (2, -6, 1.88, 8.25, 1.62, (0.42, 0.48, 0.52)),
        (4.2, -4, 2.1, 5.7, 1.73, (0.48, 0.38, 0.42)),
        (6.2, -7, 1.43, 6.6, 1.23, (0.40, 0.46, 0.50)),
        (-7, -4, 1.38, 3.9, 1.28, (0.45, 0.48, 0.50)),
    ]
    for bx, bz, sx, sy, sz, color in buildings:
        glPushMatrix()
        glTranslatef(bx, -0.71 + sy / 2, bz)
        glColor3f(*color)
        glScalef(sx, sy, sz)
        glutSolidCube(1)
        glPopMatrix()

        # Ventanas iluminadas (cuadros más grandes en la fachada)
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 0.88, 0.35)
        n_rows = max(2, int(sy * 1.8))
        n_cols = 2 if sx < 1 else 3
        win_w, win_h = 0.14, 0.18
        win_z = bz + sz / 2 + 0.02
        glBegin(GL_QUADS)
        for row in range(1, n_rows):
            for col in range(n_cols):
                wx = bx + (col / max(1, n_cols - 1) - 0.5) * sx * 0.5
                wy_pos = -0.71 + row * (sy / n_rows) + 0.15
                if wy_pos < -0.71 + sy - 0.15:
                    hw, hh = win_w / 2, win_h / 2
                    glVertex3f(wx - hw, wy_pos - hh, win_z)
                    glVertex3f(wx + hw, wy_pos - hh, win_z)
                    glVertex3f(wx + hw, wy_pos + hh, win_z)
                    glVertex3f(wx - hw, wy_pos + hh, win_z)
        glEnd()
        glEnable(GL_LIGHTING)

    # Faroles rediseñados: poste alto + brazo curvo + pantalla + luz - 1.5x más grandes
    post_height = 3.0
    post_thick = 0.105
    base_y = -0.71
    top_y = base_y + post_height
    for lx in [-2.5, 0.5, 3.5, 5.5]:
        # Poste principal (más alto y delgado)
        glPushMatrix()
        glTranslatef(lx, base_y, -2.1)
        glColor3f(0.22, 0.22, 0.26)
        glScalef(post_thick, post_height, post_thick)
        glutSolidCube(1)
        glPopMatrix()
        # Base del poste (bloque bajo)
        glPushMatrix()
        glTranslatef(lx, base_y + 0.08, -2.1)
        glColor3f(0.2, 0.2, 0.24)
        glScalef(0.21, 0.15, 0.21)
        glutSolidCube(1)
        glPopMatrix()
        # Brazo horizontal (soporte del faro)
        glPushMatrix()
        glTranslatef(lx, top_y - 0.05, -2.1)
        glColor3f(0.24, 0.24, 0.28)
        glScalef(0.375, 0.075, 0.075)
        glutSolidCube(1)
        glPopMatrix()
        # Pantalla del faro (cubo pequeño que envuelve la luz)
        glPushMatrix()
        glTranslatef(lx, top_y - 0.18, -2.1)
        glColor3f(0.35, 0.35, 0.4)
        glScalef(0.18, 0.21, 0.15)
        glutSolidCube(1)
        glPopMatrix()
        # Luz (esfera amarilla dentro de la pantalla)
        glPushMatrix()
        glTranslatef(lx, top_y - 0.18, -2.1)
        glColor3f(1.0, 0.95, 0.6)
        glutSolidSphere(0.0825, 12, 12)
        glPopMatrix()


def get_scenario_name():
    """Retorna el nombre del escenario actual."""
    return SCENARIO_NAMES.get(state.current_scenario, "Desconocido")
