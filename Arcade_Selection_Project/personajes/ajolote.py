from OpenGL.GL import *
from OpenGL.GLUT import *
import math

def draw_cube(x, y, z, sx, sy, sz, r, g, b):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glColor3f(r, g, b)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_axolotl_full(state):
    # Desactivamos iluminación para el look Minecraft
    glDisable(GL_LIGHTING)
    
    rosa_cuerpo = [1.0, 0.75, 0.8]
    rosa_fuerte = [0.85, 0.2, 0.5]
    rosa_boca = [1.0, 0.55, 0.75]
    
    # --- LÓGICA DE EXPRESIONES (Punto 2.1) ---
    color_ojos = [0.4, 0.15, 0.5] # Normal
    if state.expresion == "enojado": color_ojos = [1.0, 0.0, 0.0]
    elif state.expresion == "triste": color_ojos = [0.2, 0.2, 0.4]
    elif state.expresion == "sorprendido": color_ojos = [0.0, 0.0, 0.0]

    glPushMatrix()
    
    # --- MOVIMIENTOS GLOBALES ---
    alt_salto = state.frame_animacion if state.movimiento == "saltando" else 0
    glTranslatef(0, alt_salto, 0)
    
    if state.movimiento == "giro":
        glRotatef(state.frame_animacion * 10, 0, 1, 0)

    # CUERPO Y CABEZA
    draw_cube(0, -0.1, 0, 0.85, 1.1, 0.65, *rosa_cuerpo)
    draw_cube(0, 0.65, 0.1, 1.4, 0.7, 0.9, *rosa_cuerpo)

    # OJOS (con Guiño)
    escala_guiño = 0.2 if state.expresion != "guiño" else 0.02
    draw_cube(-0.55, 0.75, 0.56, 0.2, escala_guiño, 0.05, *color_ojos)
    draw_cube(0.55, 0.75, 0.56, 0.2, 0.2, 0.05, *color_ojos)

    # --- DETALLES DE EXPRESIONES NOTORIAS ---
    if state.expresion == "enojado":
        # Cejas enojadas
        draw_cube(-0.45, 0.92, 0.57, 0.25, 0.05, 0.06, 0.3, 0, 0)
        draw_cube(0.45, 0.92, 0.57, 0.25, 0.05, 0.06, 0.3, 0, 0)
    
    if state.expresion == "triste":
        # Boca triste (hacia abajo)
        draw_cube(0, 0.55, 0.56, 0.3, 0.06, 0.05, *rosa_boca)
    elif state.expresion == "sorprendido":
        # Boca sorpresa (forma de O)
        draw_cube(0, 0.6, 0.56, 0.15, 0.2, 0.05, 0.2, 0.1, 0.1)
    else:
        # Boca normal
        draw_cube(0, 0.65, 0.56, 0.25, 0.12, 0.05, *rosa_boca)

    # BRANQUIAS
    for side in [-1, 1]:
        draw_cube(0.85*side, 1.0, 0.1, 0.3, 0.15, 0.1, *rosa_fuerte)
        draw_cube(1.0*side, 1.15, 0.1, 0.15, 0.2, 0.1, *rosa_fuerte)
        draw_cube(0.95*side, 0.75, 0.1, 0.5, 0.15, 0.1, *rosa_fuerte)
        draw_cube(0.85*side, 0.5, 0.1, 0.3, 0.15, 0.1, *rosa_fuerte)

    # --- BRAZOS (Saludo con agitación) ---
    rot_saludo = 0
    agitacion = 0
    if state.movimiento == "saludo":
        rot_saludo = 60
        agitacion = math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.02) * 15

    glPushMatrix() # Brazo derecho animado
    glTranslatef(0.55, 0.1, 0.2)
    glRotatef(rot_saludo + agitacion, 0, 0, 1)
    draw_cube(0.15, 0, 0, 0.35, 0.12, 0.12, *rosa_cuerpo)
    glPopMatrix()
    
    draw_cube(-0.55, 0.1, 0.2, 0.3, 0.12, 0.12, *rosa_cuerpo) # Brazo izq

    # PATAS (Caminar)
    oscilacion = state.frame_animacion if state.movimiento == "caminando" else 0
    for side in [-1, 1]:
        glPushMatrix()
        glRotatef(oscilacion * side, 1, 0, 0)
        draw_cube(0.35*side, -0.65, 0.2, 0.25, 0.1, 0.4, *rosa_cuerpo)
        glPopMatrix()

    glPopMatrix()
    glEnable(GL_LIGHTING)


# === WRAPPER PARA EL MENÚ DE SELECCIÓN ===
class _NeutralState:
    """Estado neutral mínimo para la pose base del Ajolote."""
    expresion = "normal"
    movimiento = "quieto"
    frame_animacion = 0

def draw_neutral():
    """Dibuja al Ajolote en T-Pose / pose neutral sin depender de su proyecto."""
    draw_axolotl_full(_NeutralState())