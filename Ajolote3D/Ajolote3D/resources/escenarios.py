from OpenGL.GL import *
from OpenGL.GLUT import *

def draw_cube(x, y, z, sx, sy, sz, r, g, b):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glColor3f(r, g, b)
    glutSolidCube(1.0)
    glPopMatrix()

def escenario_xochimilco():
    """1. Escenario de Agua (Lugar natural)"""
    glClearColor(0.0, 0.3, 0.5, 1.0) # Fondo azul agua
    # Piso de lodo/tierra
    draw_cube(0, -1.5, 0, 15, 1, 15, 0.4, 0.2, 0.0)
    # Algas (Cilindros o cubos largos)
    draw_cube(2, -0.5, -2, 0.2, 2.0, 0.2, 0.0, 0.8, 0.2)
    draw_cube(-3, -0.5, 1, 0.2, 1.5, 0.2, 0.0, 0.6, 0.1)

def escenario_cueva():
    """2. Cueva de Cristales (Misterioso)"""
    glClearColor(0.1, 0.1, 0.1, 1.0) # Fondo oscuro
    # Piso de piedra
    draw_cube(0, -1.5, 0, 15, 1, 15, 0.3, 0.3, 0.3)
    # Cristales brillantes (Pirámides o cubos rotados)
    glPushMatrix()
    glRotatef(45, 1, 1, 1)
    draw_cube(3, 0, -2, 0.5, 2.0, 0.5, 0.0, 1.0, 1.0) # Cristal Cian
    draw_cube(-2, 1, -3, 0.5, 2.0, 0.5, 1.0, 0.0, 1.0) # Cristal Magenta
    glPopMatrix()

def escenario_espacio():
    """3. Espacio Exterior (Surrealista)"""
    glClearColor(0.0, 0.0, 0.0, 1.0) # Negro absoluto
    # Estrellas lejanas (cubos diminutos)
    import random
    random.seed(42) # Para que no parpadeen
    for i in range(20):
        draw_cube(random.uniform(-10,10), random.uniform(-5,10), -5, 0.1, 0.1, 0.1, 1, 1, 1)

def escenario_laboratorio():
    """4. Aula/Laboratorio (Estudiantil)"""
    glClearColor(0.8, 0.8, 0.8, 1.0) # Gris claro
    # Mesa de laboratorio
    draw_cube(0, -1.2, 0, 10, 0.5, 5, 0.5, 0.3, 0.2)
    # Un "vaso de precipitados" (Cilindro blanco)
    draw_cube(2, -0.8, 0, 0.4, 0.6, 0.4, 0.9, 0.9, 1.0)

def escenario_volcan():
    """5. Campo de Batalla / Volcán (Guerrero)"""
    glClearColor(0.4, 0.1, 0.0, 1.0) # Rojo oscuro
    # Piso de lava (Naranja brillante)
    draw_cube(0, -1.5, 0, 15, 1, 15, 1.0, 0.3, 0.0)
    # Rocas de obsidiana
    draw_cube(-4, -0.5, -4, 2, 2, 2, 0.1, 0.1, 0.1)