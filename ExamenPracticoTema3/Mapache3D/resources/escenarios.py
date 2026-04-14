from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def draw_cube_sc(x, y, z, sx, sy, sz, r, g, b):
    glColor3f(r, g, b)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glutSolidCube(1.0)
    glPopMatrix()

# --- Funciones Auxiliares para Detalles ---
def draw_detail_flower_sc(x, y, z, r, g, b):
    # Un "píxel" central amarillo
    draw_cube_sc(x, y, z, 0.15, 0.15, 0.15, 1.0, 1.0, 0.0)
    # 4 pétalos de color
    for p in [(0.12,0), (-0.12,0), (0,0.12), (0,-0.12)]:
        draw_cube_sc(x + p[0], y + p[1], z, 0.1, 0.1, 0.1, r, g, b)


def escenario_cerezos():
    # Suelo Rosa 
    draw_cube_sc(0, -1, 0, 20, 0.2, 20, 1.0, 0.6, 0.8)
    
    #Árboles 
    for pos in [(-4, -5), (4, -6), (-3, -8), (5, -9)]:
        draw_cube_sc(pos[0], 0, pos[1], 0.4, 2, 0.4, 0.5, 0.3, 0.2) # Tronco
        # Copas Fucsia y Rosa 
        draw_cube_sc(pos[0], 1.5, pos[1], 1.8, 1.8, 1.8, 1.0, 0.3, 0.7) 
        draw_cube_sc(pos[0] + 0.3, 2.0, pos[1] - 0.2, 1.5, 1.5, 1.5, 1.0, 0.5, 0.8) 

    # Flores pequeñas en el suelo
    for pos in [(-2,1), (2,-1), (-1,-3), (1,3), (0,2)]:
        draw_detail_flower_sc(pos[0], -0.85, pos[1], 1.0, 1.0, 0.2) # Flores Amarillas
        draw_detail_flower_sc(pos[0] * -1, -0.85, pos[1] * -1, 0.2, 0.8, 1.0) # Flores Cian


def escenario_picnic_armonioso():
    # Césped verde 
    draw_cube_sc(0, -1, 0, 20, 0.2, 20, 0.4, 0.9, 0.5) 
    # Mantel 
    draw_cube_sc(0, -0.85, -1, 2.5, 0.05, 2.5, 1.0, 0.3, 0.5)
    # Comida
    draw_cube_sc(0.6, -0.7, -1, 0.5, 0.35, 0.15, 1.0, 0.1, 0.1)
    # Cubo central blanco de la sandía
    draw_cube_sc(0.6, -0.65, -1, 0.4, 0.2, 0.1, 1.0, 1.0, 1.0)
    draw_cube_sc(-0.6, -0.7, -1, 0.3, 0.45, 0.3, 0.2, 0.8, 1.0)
    # Una "Tarta" 
    draw_cube_sc(0, -0.7, -1.8, 0.6, 0.4, 0.6, 1.0, 0.6, 0.2) # Base Naranja
    draw_cube_sc(0, -0.5, -1.8, 0.4, 0.2, 0.4, 1.0, 0.9, 0.7) # Crema
    draw_cube_sc(0, -0.3, -1.8, 0.1, 0.1, 0.1, 1.0, 0.1, 0.1) # Guinda roja
    # Flores en el suelo
    for pos in [(-2,-3), (2,1), (0,-4), (-3,2)]:
        draw_detail_flower_sc(pos[0], -0.85, pos[1], 1.0, 0.6, 0.2) # Flores Naranjas



def escenario_dulces_armonioso():
    # Suelo 
    draw_cube_sc(0, -1, 0, 20, 0.2, 20, 1.0, 0.6, 0.8) 
    # Bastones
    for x in [-5, 5]:
        glDisable(GL_LIGHTING) # Rayas puras
        draw_cube_sc(x, 1, -3, 0.5, 4, 0.5, 1.0, 1.0, 1.0) # Blanco
        for i in range(8):
            draw_cube_sc(x, 1.1 + (i*0.4), -3, 0.55, 0.2, 0.55, 1.0, 0.1, 0.1) # Rayas rojas 
        glEnable(GL_LIGHTING)
    # Paleta
    for pos in [(-7,-4), (7,-5)]:
        draw_cube_sc(pos[0], 2, pos[1], 0.15, 6, 0.15, 1.0, 1.0, 0.0) # Palo Amarillo
        # Caramelo 
        glDisable(GL_LIGHTING)
        for i in range(5):
             draw_cube_sc(pos[0], 4.5, pos[1], 1.2 - (i*0.15), 1.2 - (i*0.15), 0.05, 1.0, 0.3, 1.0) # Espiral Fucsia
        glEnable(GL_LIGHTING)
    # Caramelo extra
    glDisable(GL_LIGHTING)
    for p in [(-3,3,-2), (3,4,-1), (0,5,-4)]:
        draw_cube_sc(p[0], p[1], p[2], 0.2, 0.2, 0.2, 0.2, 0.8, 1.0) # Caramelos Cian
    glEnable(GL_LIGHTING)



def escenario_luciernagas_armonioso():
    # Suelo 
    draw_cube_sc(0, -1, 0, 20, 0.2, 20, 0.02, 0.05, 0.02) 
    
    # Árboles
    for i in range(6):
        draw_cube_sc(-6 + i*2.5, 2, -5, 0.4, 6, 0.4, 0.1, 0.05, 0.01) # Tronco Oscuro
        # Copas de Hojas
        draw_cube_sc(-6 + i*2.5, 4.5, -5, 1.2, 1.2, 1.2, 0.1, 0.6, 0.1)

    # Luciérnagas amarillas
    glDisable(GL_LIGHTING) 
    for i in range(15):
        r = 3 + (i * 0.15)
        angle = (i * 0.6)
        px = r * math.cos(angle)
        py = 1.0 + (i * 0.1)
        pz = -3 + r * math.sin(angle)
        draw_cube_sc(px, py, pz, 0.1, 0.1, 0.1, 1.0, 1.0, 0.1) # Amarillas
    glEnable(GL_LIGHTING)



def escenario_concierto():
    # Suelo 
    draw_cube_sc(0, -1, 0, 20, 0.2, 20, 0.05, 0.05, 0.1) 
    # Dibujamos una cuadrícula en el suelo
    for i in range(-5, 6, 2):
        draw_cube_sc(i, -0.85, 0, 0.05, 0.02, 20, 0.0, 1.0, 1.0) # Líneas Cian
        draw_cube_sc(0, -0.85, i, 20, 0.02, 0.05, 1.0, 0.0, 1.0) # Líneas Fucsia
    # Altavoces / Luces
    for x in [-6, -3, 3, 6]:
        # Estructura base
        draw_cube_sc(x, 1, -6, 1, 4, 1, 0.1, 0.1, 0.1)
        # Focos de colores 
        glDisable(GL_LIGHTING)
        colores_foco = [[1,0,0], [0,1,0], [0,0,1], [1,1,0]]
        for j in range(4):
            c = colores_foco[j % 4]
            draw_cube_sc(x, 0 + (j*0.8), -5.4, 0.6, 0.4, 0.2, *c)
        glEnable(GL_LIGHTING)
    # Pantalla gigante al fondo
    draw_cube_sc(0, 3, -8, 10, 6, 0.1, 0.0, 0.05, 0.0) # Fondo pantalla
    for k in range(15):
        # "Píxeles" verdes flotando
        px = -4 + (k * 0.6)
        py = 1 + (math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.01 + k) * 2)
        draw_cube_sc(px, py + 2, -7.8, 0.15, 0.15, 0.05, 0.0, 1.0, 0.2)
    # Máquina de Humo 
    draw_cube_sc(-2, -0.5, -3, 0.8, 0.8, 0.8, 0.3, 0.3, 0.3)
    draw_cube_sc(-2, 0.2, -3, 1.2, 0.5, 1.2, 0.8, 0.8, 0.9)#humo



def escenario_bosque_lindo():
    # Suelo 
    draw_cube_sc(0, -1, 0, 20, 0.2, 20, 0.2, 0.9, 0.2)
    # Árboles 
    for pos in [(-5, -4), (5, -3), (-6, -8), (2, -7)]:
        # Tronco café 
        draw_cube_sc(pos[0], 0, pos[1], 0.5, 2.5, 0.5, 0.5, 0.3, 0.1)
        # Hojas verde 
        draw_cube_sc(pos[0], 2, pos[1], 2, 2, 2, 0.0, 0.8, 0.0)
        # Manzanitas rojas 
        draw_cube_sc(pos[0]+0.5, 1.8, pos[1]+0.8, 0.2, 0.2, 0.2, 1.0, 0.0, 0.0)
        draw_cube_sc(pos[0]-0.6, 2.2, pos[1]-0.5, 0.2, 0.2, 0.2, 1.0, 0.0, 0.0)
    # Flores 
    for x in range(-8, 9, 4):
        for z in range(-8, 9, 4):
            draw_detail_flower_sc(x, -0.85, z, 1.0, 0.5, 0.0) # Naranjas
            draw_detail_flower_sc(x+1, -0.85, z+1, 1.0, 0.2, 0.8) # Fucsias


def escenario_lago():
    # Agua
    draw_cube_sc(0, -1, 0, 20, 0.2, 20, 0.0, 1.0, 1.0) 
    #Hojas
    for i in range(5):
        # Color Verde 
        draw_cube_sc(-4 + i*2, -0.9, -2 + i, 1.4, 0.15, 1.4, 0.1, 1.0, 0.1)
    # Flores amarillas
    for pos in [(-2,-2), (2,-1), (0,0), (-3,1)]:
        draw_detail_flower_sc(pos[0], -0.6, pos[1], 1.0, 1.0, 0.0) # Flores
    # Y unas luciérnagas
    for p in [(-1,0.5,-1), (1,1,0), (0,0.8,-2)]:
        draw_cube_sc(p[0], p[1], p[2], 0.1, 0.1, 0.1, 1.0, 1.0, 0.0)