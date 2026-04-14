# ============================================================
# scenarios.py - 7 Escenarios 3D para Robot Espacial
# ============================================================

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from actions import state

# Colores de fondo por escenario (cielo/ambiente)
SCENARIO_COLORS = {
    1: (0.1, 0.2, 0.4, 1.0),      # Bio-Parque (Cielo alienígena)
    2: (0.01, 0.01, 0.05, 1.0),   # Base Neon (Aurora oscura)
    3: (0.8, 0.3, 0.1, 1.0),      # Costa Cyber (Atardecer rojo/naranja)
    4: (0.2, 0.05, 0.3, 1.0),     # Montañas de Cristal (Planeta violeta)
    5: (0.05, 0.0, 0.08, 1.0),    # Ciudad Cyberpunk
    6: (0.02, 0.0, 0.05, 1.0),    # Espacio - negro profundo
    7: (0.08, 0.0, 0.15, 1.0),    # Bosque Mágico - morado nocturno
}

SCENARIO_NAMES = {
    1: "Bio-Parque Tecnologico",
    2: "Base Glaciar",
    3: "Costa Cibernetica",
    4: "Planeta Cristal",
    5: "Ciudad Cyberpunk",
    6: "Espacio Exterior",
    7: "Bosque Magico",
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
        _draw_sci_park()
    elif s == 2:
        _draw_neon_arctic()
    elif s == 3:
        _draw_cyber_beach()
    elif s == 4:
        _draw_crystal_mountain()
    elif s == 5:
        _draw_cyber_city()
    elif s == 6:
        _draw_space()
    elif s == 7:
        _draw_magic_forest()


def _draw_ground(scenario):
    """Dibuja el suelo temático para el robot."""
    glPushMatrix()
    glDisable(GL_LIGHTING)

    colors = {
        1: (0.1, 0.35, 0.25),    # Césped digital / Metálico oscuro
        2: (0.6, 0.7, 0.9),      # Nieve azulada brillante
        3: (0.15, 0.1, 0.1),     # Arena oscura / rojiza
        4: (0.15, 0.1, 0.25),    # Suelo árido violeta
        5: (0.1, 0.1, 0.12),     # Asfalto cibernético
        6: (0.18, 0.18, 0.20),   # Suelo lunar gris (Espacio)
        7: (0.15, 0.08, 0.20),   # Suelo violeta (Bosque Magico)
    }
    # Patrón de rejilla (wireframe grid) en ciudad cibernética y costa
    base_color = colors.get(scenario, (0.5, 0.5, 0.5))
    glColor3f(*base_color)

    glBegin(GL_QUADS)
    size = 15
    glVertex3f(-size, -0.71, -size)
    glVertex3f( size, -0.71, -size)
    glVertex3f( size, -0.71,  size)
    glVertex3f(-size, -0.71,  size)
    glEnd()
    
    # Añadir red de neon (grid line) en playa y ciudad
    if scenario in [3, 5]:
        glColor3f(0.8, 0.1, 0.5) if scenario == 5 else glColor3f(0.9, 0.5, 0.1)
        glBegin(GL_LINES)
        for i in range(-15, 16, 2):
            glVertex3f(i, -0.70, -15)
            glVertex3f(i, -0.70, 15)
            glVertex3f(-15, -0.70, i)
            glVertex3f(15, -0.70, i)
        glEnd()

    glEnable(GL_LIGHTING)
    glPopMatrix()


# ─── Escenario 1: Bio-Parque ───
def _draw_sci_park():
    """Parque tecnológico con árboles metálicos y flores holográficas."""
    # Sendero metálico
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(0.3, 0.4, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-2, -0.708, -8)
    glVertex3f(2, -0.708, -8)
    glVertex3f(1.5, -0.708, 6)
    glVertex3f(-1.5, -0.708, 6)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Árboles alienígenas
    trees = [(-3.5, -4, 1.5), (4, -3, 1.2), (-5.5, -6, 1.7), (2, -7, 1.3), (6, -5, 1.5), (-1, -3.5, 1.1)]
    for tx, tz, scale in trees:
        glPushMatrix()
        glTranslatef(tx, -0.1, tz)
        glColor3f(0.4, 0.45, 0.5)  # Tronco gris
        glScalef(0.2, 1.6, 0.2)
        glutSolidCube(1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(tx, 1.8, tz)
        glColor3f(0.2, 0.8, 0.6)  # Corona aqua
        glScalef(scale, scale * 1.5, scale)
        glutWireSphere(0.8, 12, 12)  # Árbol holográfico o wireframe
        glPopMatrix()

    # Monolitos Gigantes de Fondo
    for mx, mz in [(-12, -15), (10, -14)]:
        glPushMatrix()
        glTranslatef(mx, -0.7, mz)
        glColor3f(0.15, 0.25, 0.3)
        glScalef(3.0, 15.0, 3.0)
        glutSolidCube(1)
        glPopMatrix()

    # Soles gemelos
    glPushMatrix()
    glTranslatef(3, 5.5, -9)
    glColor3f(1.0, 0.3, 0.6)
    glutSolidSphere(0.8, 20, 20)
    glTranslatef(1.5, 0.5, 0)
    glColor3f(0.9, 0.7, 0.2)
    glutSolidSphere(0.5, 15, 15)
    glPopMatrix()

    # Flores / Nodos de energía
    for fx, fz in [(-1, -2), (1.5, -3), (-2, -5), (3, -1)]:
        glPushMatrix()
        glTranslatef(fx, -0.5, fz)
        glColor3f(0.1, 0.9, 0.8)
        glutSolidSphere(0.15, 12, 12)
        glutWireCube(0.4)
        glPopMatrix()

    # Banco flotante (holo)
    glPushMatrix()
    glTranslatef(-4, -0.2, -2)
    glColor3f(0.5, 0.5, 0.6)
    glScalef(1.2, 0.1, 0.35)
    glutSolidCube(1)
    glPopMatrix()
    # Pata central luminosa
    glPushMatrix()
    glTranslatef(-4, -0.5, -2)
    glColor3f(0.2, 0.8, 0.9)
    glScalef(0.1, 0.5, 0.1)
    glutSolidCube(1)
    glPopMatrix()


# ─── Escenario 2: Base Glaciar Neon ───
def _draw_neon_arctic():
    """Auroras intensas y módulos geodésicos en lugar de campo nevado clásico."""
    import random
    random.seed(42)

    glDisable(GL_LIGHTING)
    # Aurora agresiva (Cyan y Magenta)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glColor4f(0.9, 0.2, 0.7, 0.3)
    glVertex3f(-18, 3.5, -14)
    glVertex3f(18, 4.5, -14)
    glVertex3f(16, 7.5, -14)
    glVertex3f(-16, 6.5, -14)
    glColor4f(0.1, 0.8, 0.9, 0.25)
    glVertex3f(-17, 4.2, -13)
    glVertex3f(17, 5.2, -13)
    glVertex3f(15, 8.2, -13)
    glVertex3f(-15, 7.2, -13)
    glEnd()
    glDisable(GL_BLEND)

    # Estrellas de colores
    glPointSize(3.0)
    glBegin(GL_POINTS)
    for _ in range(40):
        glColor3f(random.uniform(0.5,1), random.uniform(0.5,1), 1)
        glVertex3f(random.uniform(-12, 12), random.uniform(2, 8), random.uniform(-12, -2))
    glEnd()
    glEnable(GL_LIGHTING)

    # Iceberg Gigante en la lejanía
    glPushMatrix()
    glTranslatef(-8, -0.71, -18)
    glRotatef(25, 0, 1, 0)
    glColor3f(0.2, 0.5, 0.8)
    glScalef(10.0, 25.0, 5.0)
    glutSolidCube(1)
    glPopMatrix()

    # Domo Metálico / Base (en vez del iglú)
    glPushMatrix()
    glTranslatef(3, -0.7, -4)
    glColor3f(0.4, 0.45, 0.5)
    glutWireSphere(2.3, 15, 10)
    # Núcleo interior del domo
    glColor3f(0.1, 0.8, 0.9)
    glutSolidSphere(1.8, 15, 15)
    # Entrada/Tubo
    glTranslatef(0, 0, 1.5)
    glColor3f(0.2, 0.25, 0.35)
    glScalef(0.8, 1.0, 1.5)
    glutSolidCube(1)
    glPopMatrix()

    # Bloques cristalinos esparcidos
    for hx, hz, sx, sy, sz in [
        (-4, -3, 1.0, 1.2, 0.7), (-2, -6, 0.5, 1.5, 0.5), (5, -5, 0.9, 0.8, 0.6),
    ]:
        glPushMatrix()
        glTranslatef(hx, -0.7 + sy/2, hz)
        glColor3f(0.3, 0.5, 0.9)
        glScalef(sx, sy, sz)
        glutSolidCube(1)
        glPopMatrix()

    # Antena repetidora rota (Robo Muñeco)
    glPushMatrix()
    glTranslatef(-1.5, -0.3, -1.5)
    glColor3f(0.5, 0.5, 0.5)
    glScalef(0.2, 1.0, 0.2)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-1.5, 0.3, -1.5)
    glColor3f(1.0, 0.2, 0.2)
    glutSolidSphere(0.15, 10, 10)
    glPopMatrix()


# ─── Escenario 3: Costa Cibernética ───
def _draw_cyber_beach():
    """Mar de neon, palmeras sintéticas y sol gigante rojizo."""
    # Mar de neon (Grid encima del suelo plano oscuro)
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 0.2, 0.1)  # Sol gigante de atardecer synthwave
    glTranslatef(0, 3.0, -14)
    glutSolidSphere(4.0, 30, 30)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Palmeras Sintéticas
    def _synth_palm(x, z):
        glPushMatrix()
        glTranslatef(x, 0.5, z)
        glColor3f(0.2, 0.2, 0.25)
        glScalef(0.15, 2.5, 0.15)
        glutSolidCube(1)
        glPopMatrix()
        # Hojas triangulares / neón
        for ang in range(0, 360, 90):
            glPushMatrix()
            glTranslatef(x, 1.8, z)
            glRotatef(ang, 0, 1, 0)
            glTranslatef(0.8, -0.2, 0)
            glRotatef(20, 0, 0, 1)
            glScalef(1.5, 0.1, 0.4)
            glColor3f(0.1, 0.9, 0.3)
            glutSolidCube(1)
            glPopMatrix()

    _synth_palm(-4, -3)
    _synth_palm(3.5, -5)
    _synth_palm(-6, -6)
    _synth_palm(5, -2.5)

    # Panel solar / antena de comunicaciones (Sombrilla)
    glPushMatrix()
    glTranslatef(2, 0.5, -3)
    glColor3f(0.2, 0.2, 0.2)
    glScalef(0.1, 2.0, 0.1)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(2, 1.5, -3)
    glColor3f(0.4, 0.6, 0.9)
    glScalef(1.5, 0.05, 1.5)
    glutSolidCube(1)
    glPopMatrix()

    # Rocas escoria de metal
    for rx, rz, scale in [(-2, -2.5, 0.5), (1, -1.8, 0.3), (-4, -3, 0.4), (5, -4, 0.6)]:
        glPushMatrix()
        glTranslatef(rx, -0.65, rz)
        glColor3f(0.1, 0.1, 0.15)
        glScalef(scale, scale*0.6, scale)
        glutSolidSphere(0.5, 10, 10)
        glPopMatrix()

    # Ascensor orbital cibernético (Gigaestructura al fondo)
    glPushMatrix()
    glTranslatef(12, -0.65, -18)
    glColor3f(0.05, 0.05, 0.08)
    glScalef(2.0, 40.0, 2.0)
    glutSolidCube(1)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(12, 15.0, -18)
    glColor3f(0.1, 0.8, 0.9)
    glScalef(4.0, 0.5, 4.0)
    glutSolidCube(1)
    glPopMatrix()


# ─── Escenario 4: Montañas Cristalinas ───
def _draw_crystal_mountain():
    """Montañas delgadas como cristal en un planeta inhóspito."""
    # Picos principales (Cristales puntiagudos magenta-azulados)
    mountains = [
        (-5, -8, 2.5, 8.0, (0.4, 0.1, 0.6)),
        (1, -10, 3.0, 9.5, (0.5, 0.1, 0.7)),
        (6, -7, 2.0, 6.5, (0.3, 0.1, 0.5)),
        (-7, -5, 1.8, 5.0, (0.6, 0.1, 0.8)),
    ]
    for mx, mz, rad, h, color in mountains:
        glPushMatrix()
        glTranslatef(mx, -0.71, mz)
        glRotatef(-90, 1, 0, 0)
        glColor3f(*color)
        glutSolidCone(rad, h, 8, 4)  # 8 caras, aspecto filoso
        glPopMatrix()
        # Pico brillante
        glPushMatrix()
        glTranslatef(mx, -0.71 + h*0.8, mz)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.9, 0.8, 1.0)
        glutSolidCone(rad * 0.2, h*0.2, 8, 2)
        glPopMatrix()

    # Base alienígena (Pirámide de metal en lugar de cabaña)
    glPushMatrix()
    glTranslatef(-3, -0.71, -3)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.2, 0.2, 0.25)
    glutSolidCone(2.0, 3.0, 4, 2) # Pirámide
    glPopMatrix()
    
    # Formaciones de cristales pequeños (en lugar de Pinos)
    for px, pz, s in [(-3,-5,1.5), (2,-2,1.3), (5,-4,1.6), (-6,-2,1.2), (4,-1,1.4), (-2,-7,1.2)]:
        glPushMatrix()
        glTranslatef(px, -0.71, pz)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.1, 0.8, 1.0)
        glutSolidCone(0.3*s, 1.5*s, 6, 2)
        glPopMatrix()

    # Planeta satélite gigante visible en cielo
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(-12, 15, -25)
    glColor3f(0.4, 0.2, 0.5)
    glutSolidSphere(8.0, 30, 30)
    # Anillo vertical gigante en el fondo (centrado en el planeta)
    glRotatef(45, 1, 1, 0)
    glColor3f(0.8, 0.2, 0.6)
    glutSolidTorus(0.2, 12.0, 10, 30)
    glEnable(GL_LIGHTING)
    glPopMatrix()


# ─── Escenario 5: Ciudad Cyberpunk ───
def _draw_cyber_city():
    """Edificios esbeltos con cuadrículas de neon, cables y anuncios."""
    # Vereda elevada / calle principal
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.1, 0.12)
    glBegin(GL_QUADS)
    glVertex3f(-15, -0.69, -1.5)
    glVertex3f(15, -0.69, -1.5)
    glVertex3f(15, -0.69, -3.5)
    glVertex3f(-15, -0.69, -3.5)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Edificios rascacielos altos
    buildings = [
        (-5.5, -5, 1.5, 7.0, 1.5, (0.1, 0.1, 0.15)),
        (-3.0, -6, 1.2, 9.0, 1.2, (0.05, 0.1, 0.1)),
        (-1, -5, 1.8, 6.5, 1.8, (0.15, 0.1, 0.15)),
        (2.5, -6, 1.6, 9.5, 1.6, (0.1, 0.1, 0.1)),
        (4.5, -4, 1.6, 6.0, 1.6, (0.12, 0.12, 0.15)),
        (6.5, -7, 1.2, 8.0, 1.2, (0.08, 0.08, 0.1)),
    ]
    for bx, bz, sx, sy, sz, color in buildings:
        glPushMatrix()
        glTranslatef(bx, -0.71 + sy/2, bz)
        # Bloque central
        glColor3f(*color)
        glScalef(sx, sy, sz)
        glutSolidCube(1)
        
        # Overlay wireframe neon azul/magenta
        glDisable(GL_LIGHTING)
        glColor3f(0.8, 0.1, 0.5) if bx < 0 else glColor3f(0.1, 0.8, 0.9)
        glutWireCube(1.02)
        
        # Ventanas iluminadas horizontales
        glBegin(GL_LINES)
        num_floors = int(sy * 2)
        for f in range(1, num_floors):
            y_lvl = -0.5 + (f / num_floors)
            # Frente
            glVertex3f(-0.5, y_lvl, 0.51)
            glVertex3f(0.5, y_lvl, 0.51)
            # Costado Izquierdo
            glVertex3f(-0.51, y_lvl, -0.5)
            glVertex3f(-0.51, y_lvl, 0.5)
            # Costado Derecho
            glVertex3f(0.51, y_lvl, -0.5)
            glVertex3f(0.51, y_lvl, 0.5)
        glEnd()
        glEnable(GL_LIGHTING)
        glPopMatrix()

    # Mega-rascacielos colosal de fondo
    glPushMatrix()
    glTranslatef(-2, -0.71, -16)
    glColor3f(0.02, 0.02, 0.05)
    glScalef(15.0, 35.0, 4.0)
    glutSolidCube(1)
    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.8, 0.9)
    glutWireCube(1.01)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Anuncios Holográficos (paneles transparentes)
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for hx, hy, hz, r,g,b in [(-3.0, 3.5, -5.3, 0.9, 0.9, 0.1), (2.5, 5.0, -5.0, 0.1, 0.9, 0.7)]:
        glPushMatrix()
        glTranslatef(hx, hy, hz)
        glColor4f(r, g, b, 0.6)
        glBegin(GL_QUADS)
        glVertex3f(-0.8, -0.5, 0)
        glVertex3f(0.8, -0.5, 0)
        glVertex3f(0.8, 0.5, 0)
        glVertex3f(-0.8, 0.5, 0)
        glEnd()
        glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

    # Postes de luz futuristas (Aros en lugar de faroles anticuados)
    for lx in [-2.5, 0.5, 3.5, 6.0]:
        glPushMatrix()
        glTranslatef(lx, 0.5, -2.1)
        glColor3f(0.3, 0.3, 0.35)
        glScalef(0.1, 2.5, 0.1)
        glutSolidCube(1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(lx, 1.8, -1.8)
        glRotatef(30, 1, 0, 0)
        glColor3f(0.2, 0.9, 0.8)
        glutSolidTorus(0.05, 0.3, 10, 20)
        glPopMatrix()


# ─── Escenario 6: Espacio ───
def _draw_space():
    """Fondo de espacio sideral con satélites, estrellas y suelo lunar."""
    import random
    glDisable(GL_LIGHTING)
    # Campo estelar denso
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    random.seed(6)
    for _ in range(150):
        glVertex3f(random.uniform(-15, 15), random.uniform(0, 12), random.uniform(-15, -5))
    glEnd()

    # Planeta lejano (Neptuno/Saturno)
    glPushMatrix()
    glTranslatef(-5, 6, -6)
    glColor3f(0.5, 0.2, 0.8)
    glutSolidSphere(1.5, 24, 24)
    glPushMatrix()
    glRotatef(45, 1, 0, 0)
    glScalef(1.0, 0.1, 1.0)
    glColor3f(0.3, 0.6, 0.9)
    glutWireSphere(2.2, 16, 16)
    glPopMatrix()
    glPopMatrix()
    
    glEnable(GL_LIGHTING)
    # Suelo lunar (cráteres distribuidos)
    craters = [
        (2, -4, 0.8), (-3, -2, 0.5), (-5, -5, 1.2), (4, -6, 0.6),
        (7, -2, 1.5), (-8, -8, 2.0), (1, -9, 1.0), (-2, -12, 0.7),
        (8, -10, 1.3), (-10, -3, 0.9), (12, -5, 1.1), (5, -12, 1.6),
        (-6, 2, 0.8), (9, 3, 1.2), (-12, -10, 1.4), (0, -15, 2.2)
    ]
    for cx, cz, s in craters:
        glPushMatrix()
        glTranslatef(cx, -0.68, cz)
        glScalef(1.0, 0.1, 1.0)
        glColor3f(0.2, 0.2, 0.22)
        glutSolidSphere(s, 16, 16)
        glPopMatrix()

    # OVNI Lejano / Animación cruzando el cielo
    glPushMatrix()
    ufo_x = math.sin(state.blink_timer * 0.5) * 15.0
    ufo_y = 6.0 + math.cos(state.blink_timer * 2.0) * 0.5
    ufo_z = -12.0 + math.cos(state.blink_timer * 0.5) * 5.0
    glTranslatef(ufo_x, ufo_y, ufo_z)
    glRotatef(state.blink_timer * 60, 0, 1, 0) # Rotar sobre si mismo
    
    # Plato del OVNI
    glPushMatrix()
    glColor3f(0.4, 0.4, 0.45)
    glScalef(1.5, 0.2, 1.5)
    glutSolidSphere(1.0, 20, 20)
    glPopMatrix()
    
    # Cabina de cristal superior del OVNI
    glPushMatrix()
    glTranslatef(0, 0.2, 0)
    glColor3f(0.1, 0.9, 0.8)
    glScalef(0.7, 0.5, 0.7)
    glutSolidSphere(1.0, 15, 15)
    glPopMatrix()
    
    # Luz inferior (motor)
    glPushMatrix()
    glTranslatef(0, -0.15, 0)
    glColor3f(0.9, 0.2, 0.3)
    glScalef(0.4, 0.1, 0.4)
    glutSolidSphere(1.0, 10, 10)
    glPopMatrix()
    glPopMatrix()

    # Agujero de Gusano / Sol Negro gigantesco
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(12, 10, -20)
    glColor3f(0.8, 0.1, 0.2)
    glutSolidTorus(0.5, 6.0, 10, 30)
    glColor3f(0.0, 0.0, 0.0)
    glutSolidSphere(5.5, 30, 30)
    glEnable(GL_LIGHTING)
    glPopMatrix()


# ─── Escenario 7: Bosque Mágico ───
def _draw_magic_forest():
    """Bosque místico con setas gigantes, flores y mariposas neón."""
    import random
    
    # ──── LUNA GIGANTE ────
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(-8, 12, -22)
    glColor3f(0.9, 0.9, 1.0) # Luna blanca brillante
    glutSolidSphere(6.0, 30, 30)
    # Aura sutil
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.5, 0.6, 1.0, 0.2)
    glutSolidSphere(6.5, 20, 20)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    
    # ──── SETAS GIGANTES ────
    mushrooms = [(-4,-5,1.5,(0.8,0.1,0.8)), (0.5,-4,1.2,(0.0,0.8,0.6)), (-6,-2,0.9,(0.9,0.9,0.2)), (5,-6,1.8,(0.2,0.4,0.9))]
    for mx, mz, scale, color in mushrooms:
        # Tronco grueso
        glPushMatrix()
        glTranslatef(mx, -0.71 + (0.75*scale), mz)
        glColor3f(0.8, 0.8, 0.9)
        glScalef(0.65*scale, 1.5*scale, 0.65*scale)
        glutSolidCube(1)
        glPopMatrix()
        
        # Corona pegada al tronco (la base del tronco es -0.71, tope es -0.71 + 1.5*scale)
        glPushMatrix()
        glTranslatef(mx, -0.71 + 1.2*scale, mz)
        glRotatef(-90, 1, 0, 0)
        glColor3f(*color)
        glutSolidCone(1.6*scale, 0.9*scale, 16, 8)
        glPopMatrix()
        
    # ──── FLORES NEÓN ────
    glDisable(GL_LIGHTING)
    random.seed(8)
    for _ in range(15):
        fx, fz = random.uniform(-10, 10), random.uniform(-10, 0)
        glPushMatrix()
        glTranslatef(fx, -0.65, fz)
        glColor3f(random.uniform(0.5, 1.0), random.uniform(0.1, 0.8), random.uniform(0.5, 1.0))
        # Pétalos
        glRotatef(90, 1, 0, 0)
        glutSolidTorus(0.05, 0.15, 5, 8)
        glPopMatrix()
    
    # ──── LUCIÉRNAGAS / MARIPOSAS NEÓN ────
    glPointSize(5.0)
    glBegin(GL_POINTS)
    random.seed(7)
    for _ in range(30):
        fx, fy, fz = random.uniform(-12,12), random.uniform(0,5), random.uniform(-12,-2)
        # Vuelo sinusoidal usando state.blink_timer
        t_offset_y = math.sin(state.blink_timer * random.uniform(1, 4)) * 0.4
        t_offset_x = math.cos(state.blink_timer * random.uniform(1, 3)) * 0.3
        glColor3f(0.1, 0.9, 0.9) if random.random() > 0.5 else glColor3f(0.9, 0.1, 0.9)
        glVertex3f(fx + t_offset_x, fy + t_offset_y, fz)
    glEnd()
    glEnable(GL_LIGHTING)

    # ──── MARGARITA NEÓN GIGANTE ────
    glPushMatrix()
    glTranslatef(8, -0.71, -10)
    # Tallo verde neón
    glPushMatrix()
    glColor3f(0.2, 0.9, 0.3)
    glTranslatef(0, 3.5, 0)
    glScalef(0.3, 7.0, 0.3)
    glutSolidCube(1)
    glPopMatrix()
    
    # Centro naranja/amarillo brillante
    glPushMatrix()
    glTranslatef(0, 7.0, 0)
    # Ligera inclinación hacia la cámara para que se vea
    glRotatef(-15, 1, 0, 0)
    glColor3f(1.0, 0.8, 0.1)
    glutSolidSphere(1.2, 20, 20)
    # Pétalos blancos/cyan luminosos
    glColor3f(0.8, 0.9, 1.0)
    for ang in range(0, 360, 45):
        glPushMatrix()
        glRotatef(ang, 0, 0, 1) # Girar radialmente
        glTranslatef(0, 1.8, 0) 
        glScalef(0.5, 1.5, 0.2)
        glutSolidSphere(1.0, 15, 10)
        glPopMatrix()
    glPopMatrix()
    glPopMatrix()


def get_scenario_name():
    """Retorna el nombre del escenario actual."""
    return SCENARIO_NAMES.get(state.current_scenario, "Desconocido")
