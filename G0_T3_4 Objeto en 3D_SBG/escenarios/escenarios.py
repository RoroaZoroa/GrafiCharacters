from OpenGL.GL import *
from OpenGL.GLU import *

# ---------------------------------------------------------------------------
# HELPERS: reemplazan glutSolidSphere / glutSolidCube con GL/GLU puro.
# Compatibles con cualquier contexto OpenGL (GLUT, pyopengltk, etc.)
# ---------------------------------------------------------------------------
def solid_sphere(radius, slices=16, stacks=16):
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, radius, slices, stacks)
    gluDeleteQuadric(q)

def solid_cube(size):
    """Cubo centrado en el origen con lado = size, equivalente a glutSolidCube."""
    h = size / 2.0
    glBegin(GL_QUADS)
    # Frente
    glNormal3f( 0,  0,  1); glVertex3f(-h,-h, h); glVertex3f( h,-h, h); glVertex3f( h, h, h); glVertex3f(-h, h, h)
    # Atrás
    glNormal3f( 0,  0, -1); glVertex3f( h,-h,-h); glVertex3f(-h,-h,-h); glVertex3f(-h, h,-h); glVertex3f( h, h,-h)
    # Izquierda
    glNormal3f(-1,  0,  0); glVertex3f(-h,-h,-h); glVertex3f(-h,-h, h); glVertex3f(-h, h, h); glVertex3f(-h, h,-h)
    # Derecha
    glNormal3f( 1,  0,  0); glVertex3f( h,-h, h); glVertex3f( h,-h,-h); glVertex3f( h, h,-h); glVertex3f( h, h, h)
    # Arriba
    glNormal3f( 0,  1,  0); glVertex3f(-h, h, h); glVertex3f( h, h, h); glVertex3f( h, h,-h); glVertex3f(-h, h,-h)
    # Abajo
    glNormal3f( 0, -1,  0); glVertex3f(-h,-h,-h); glVertex3f( h,-h,-h); glVertex3f( h,-h, h); glVertex3f(-h,-h, h)
    glEnd()

# ---------------------------------------------------------------------------

def dibujar_piso(r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex3f(-10.0, -1.5, -10.0)
    glVertex3f(-10.0, -1.5,  10.0)
    glVertex3f( 10.0, -1.5,  10.0)
    glVertex3f( 10.0, -1.5, -10.0)
    glEnd()

def escenario_parque():
    # Piso de pasto verde
    dibujar_piso(0.2, 0.6, 0.2)
    
    # Árboles simples (cilindro marrón + esfera verde)
    posiciones_arboles = [(-4, -1.5, -5), (5, -1.5, -3), (-6, -1.5, 2)]
    for x, y, z in posiciones_arboles:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.5, 0.3, 0.1)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.4, 0.4, 2.0, 16, 16)
        glTranslatef(0.0, 0.0, 2.0)
        glColor3f(0.1, 0.8, 0.1)
        solid_sphere(1.2, 16, 16)
        gluDeleteQuadric(quad)
        glPopMatrix()

def escenario_callejon():
    # Piso de asfalto oscuro
    dibujar_piso(0.2, 0.2, 0.2)
    
    # Paredes laterales grises
    glColor3f(0.3, 0.3, 0.3)
    for x in [-5.0, 5.0]:
        glPushMatrix()
        glTranslatef(x, 1.0, 0.0)
        glScalef(1.0, 5.0, 20.0)
        solid_cube(1.0)
        glPopMatrix()

def escenario_batalla():
    # Piso de tierra rojiza
    dibujar_piso(0.6, 0.2, 0.1)
    
    # Rocas irregulares esparcidas
    posiciones_rocas = [(3, -1.2, -4), (-4, -1.0, -2), (2, -1.4, 3), (-2, -1.3, 5)]
    glColor3f(0.4, 0.4, 0.4)
    for x, y, z in posiciones_rocas:
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(1.5, 0.8, 1.2)
        solid_sphere(0.8, 8, 8)
        glPopMatrix()

def escenario_aula():
    # Piso de madera / loseta
    dibujar_piso(0.8, 0.7, 0.5)
    
    # Pizarrón verde al fondo
    glColor3f(0.1, 0.5, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-4.0, 0.0, -6.0)
    glVertex3f(-4.0, 4.0, -6.0)
    glVertex3f( 4.0, 4.0, -6.0)
    glVertex3f( 4.0, 0.0, -6.0)
    glEnd()
    
    # Escritorios marrones
    glColor3f(0.6, 0.4, 0.2)
    for x in [-2.0, 2.0]:
        glPushMatrix()
        glTranslatef(x, -0.5, -3.0)
        glScalef(2.0, 1.0, 1.0)
        solid_cube(1.0)
        glPopMatrix()

def escenario_teatral():
    # Piso negro
    dibujar_piso(0.05, 0.05, 0.05)
    
    # Spotlight pintado en el suelo bajo Knuckles
    glColor3f(1.0, 1.0, 0.8)
    glPushMatrix()
    glTranslatef(0.0, -1.49, 0.0)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluDisk(quad, 0.0, 2.5, 32, 1)
    gluDeleteQuadric(quad)
    glPopMatrix()

def dibujar(tipo):
    if   tipo == 1: escenario_parque()
    elif tipo == 2: escenario_callejon()
    elif tipo == 3: escenario_batalla()
    elif tipo == 4: escenario_aula()
    elif tipo == 5: escenario_teatral()
    # tipo == 0: fondo vacío, no dibuja nada
