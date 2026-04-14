from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# Ángulos de cámara
angle_x = 0
angle_y = 0

# Tamaño de ventana
width = 800
height = 600

def init():
    glEnable(GL_DEPTH_TEST)  # Habilitar prueba de profundidad
    glClearColor(0.1, 0.1, 0.1, 1.0)

def draw_axes():
    """Dibuja ejes coordenados XYZ"""
    glBegin(GL_LINES)
    # Eje X - rojo
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(2, 0, 0)

    # Eje Y - verde
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 2, 0)

    # Eje Z - azul
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 2)
    glEnd()

def draw_shapes():
    """Dibuja figuras en distintos modos y posiciones"""
    # ----- Cubo -----
    glPushMatrix()
    glTranslatef(-4, 2, 0)
    glColor3f(1, 0, 0)
    glutSolidCube(1)
    glColor3f(1, 1, 1)
    glutWireCube(1.01)
    glPopMatrix()

    # ----- Pirámide (Tetraedro) -----
    glPushMatrix()
    glTranslatef(-2, 2, 0)
    glColor3f(0.8, 0.5, 0.1)
    glutSolidTetrahedron()
    glColor3f(1, 1, 1)
    glutWireTetrahedron()
    glPopMatrix()

    # ----- Esfera -----
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glColor3f(0, 0.5, 1)
    glutSolidSphere(0.7, 20, 20)
    glColor3f(1, 1, 1)
    glutWireSphere(0.71, 20, 20)
    glPopMatrix()

    # ----- Cilindro -----
    glPushMatrix()
    glTranslatef(2, 2, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.4, 1, 0.4)
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_FILL)
    gluCylinder(quad, 0.4, 0.4, 1, 20, 5)
    glColor3f(1, 1, 1)
    gluQuadricDrawStyle(quad, GLU_LINE)
    gluCylinder(quad, 0.4, 0.4, 1, 20, 5)
    glPopMatrix()

    # ----- Cono -----
    glPushMatrix()
    glTranslatef(4, 2, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 0.4, 0.7)
    glutSolidCone(0.5, 1.2, 20, 10)
    glColor3f(1, 1, 1)
    glutWireCone(0.5, 1.2, 20, 10)
    glPopMatrix()

    # ----- Prisma rectangular (como cubo estirado) -----
    glPushMatrix()
    glTranslatef(-4, 0, 0)
    glScalef(1, 1.5, 0.5)
    glColor3f(0.2, 0.8, 0.9)
    glutSolidCube(1)
    glColor3f(1, 1, 1)
    glutWireCube(1.01)
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Cámara
    glTranslatef(0.0, 0.0, -10.0)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)

    draw_axes()
    draw_shapes()

    glutSwapBuffers()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/float(h), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global angle_x, angle_y
    if key == b'\x1b':  # ESC
        sys.exit()

def special_keys(key, x, y):
    global angle_x, angle_y
    if key == GLUT_KEY_RIGHT:
        angle_y += 5
    elif key == GLUT_KEY_LEFT:
        angle_y -= 5
    elif key == GLUT_KEY_UP:
        angle_x -= 5
    elif key == GLUT_KEY_DOWN:
        angle_x += 5
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Formas 3D: Wireframe y Relleno")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()