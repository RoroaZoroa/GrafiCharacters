from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def draw_cube_miko(x, y, z, sx, sy, sz, r, g, b):
    glColor3f(r, g, b)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_miko(state):
    # Este 'state.color_miko' lo cambiamos en colisiones.py al chocar
    c = state.color_miko 
    gris_claro = [c[0] * 0.8, c[1] * 0.8, c[2] * 0.8] # Color principal (80% brillo)
    gris_oscuro = [c[0] * 0.5, c[1] * 0.5, c[2] * 0.5] # Color de sombra (50% brillo)
    #colores que no cambian
    blanco, negro = [1.0, 1.0, 1.0], [0.05, 0.05, 0.05]
    rosa_tierno, rojo = [1.0, 0.7, 0.8], [0.9, 0.1, 0.1]
    azul_sueno = [0.1, 0.4, 0.9]
    cian_lagrima = [0.6, 0.9, 1.0]

    glPushMatrix()
    
    t_global = glutGet(GLUT_ELAPSED_TIME) * 0.005
    
    alt_salto = abs(math.sin(t_global)) * 0.2 if state.movimiento == "saltando" else 0
    glTranslatef(0, alt_salto, 0)
    
    if state.movimiento == "giro":
        glRotatef(t_global * 100, 0, 1, 0)

    # CUERPO Y CABEZA (Usan el color dinámico)
    draw_cube_miko(0, 0, 0, 0.9, 1.1, 0.8, *gris_claro)  # Cubo principal cuerpo
    draw_cube_miko(0, 0, 0.1, 0.6, 0.8, 0.75, *blanco)     # Pecho (blanco fijo)
    draw_cube_miko(0, 0.9, 0.1, 1.4, 1.0, 1.1, *gris_claro)# Cabeza principal
    
    # CARA BASE (Fija en negro y blanco)
    draw_cube_miko(0.35, 0.9, 0.62, 0.5, 0.4, 0.1, *negro) # Antifaz D
    draw_cube_miko(-0.35, 0.9, 0.62, 0.5, 0.4, 0.1, *negro)# Antifaz I
    draw_cube_miko(0, 0.75, 0.6, 0.4, 0.3, 0.2, *blanco)  # Hocico
    draw_cube_miko(0, 0.82, 0.71, 0.12, 0.1, 0.1, *negro) # Nariz

    # OJOS (Original, colores fijos)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0.35 * side, 0.95, 0.65)
        es_cerrado = (state.expresion == "dormido") or (state.expresion == "guino" and side == 1)
        if es_cerrado:
            draw_cube_miko(0, 0, 0.05, 0.22, 0.05, 0.05, *negro)
        elif state.expresion == "llorando":
            draw_cube_miko(0, 0, 0.02, 0.25, 0.25, 0.02, *blanco)
            draw_cube_miko(0.03 * side, -0.02, 0.05, 0.12, 0.08, 0.05, *negro)
            draw_cube_miko(0.05 * side, -0.18, 0.07, 0.08, 0.08, 0.05, *cian_lagrima)
            draw_cube_miko(-0.02 * side, -0.28, 0.09, 0.06, 0.06, 0.05, *cian_lagrima)
        else:
            draw_cube_miko(0, 0, 0.02, 0.25, 0.25, 0.02, *blanco)
            p_color = rojo if state.expresion == "enojado" else negro
            draw_cube_miko(0.03 * side, -0.02, 0.05, 0.12, 0.12, 0.05, *p_color)
            if state.expresion not in ["enojado", "triste"]:
                draw_cube_miko(0.06 * side, 0.04, 0.07, 0.06, 0.06, 0.05, *blanco)
        glPopMatrix()

    # LA SONRISITA (Original, negro fijo)
    if state.expresion in ["normal", "guino", "dormido"]:
        glPushMatrix()
        glTranslatef(0, 0.7, 0.72)
        draw_cube_miko(0, -0.02, 0, 0.1, 0.03, 0.02, *negro)
        draw_cube_miko(0.06, 0, 0, 0.05, 0.03, 0.02, *negro)
        draw_cube_miko(-0.06, 0, 0, 0.05, 0.03, 0.02, *negro)
        glPopMatrix()
    elif state.expresion == "sorprendido":
        draw_cube_miko(0, 0.68, 0.72, 0.12, 0.12, 0.05, 0.3, 0.1, 0.1) # Boca ooo
    elif state.expresion == "enojado":
        draw_cube_miko(0, 0.7, 0.72, 0.2, 0.04, 0.05, *negro)
    elif state.expresion in ["triste", "llorando"]:
        temblor = math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.02) * 0.005 if state.expresion == "llorando" else 0
        draw_cube_miko(temblor, 0.68, 0.72, 0.15, 0.03, 0.05, *negro)

    # simbolo de sueño
    if state.expresion == "dormido":
        for i in range(2):
            glPushMatrix()
            glTranslatef(0.8, 1.7 + (i*0.4), 0.2)
            draw_cube_miko(0, 0, 0, 0.2, 0.04, 0.05, *azul_sueno)
            glPopMatrix()

    # OREJAS Y COLA (Usan el color dinámico)
    for side in [-1, 1]:
        # Oreja exterior usa Gris Oscuro dinámico
        draw_cube_miko(0.5 * side, 1.5, 0.1, 0.35, 0.35, 0.2, *gris_oscuro)
        draw_cube_miko(0.5 * side, 1.5, 0.15, 0.18, 0.18, 0.15, *rosa_tierno)

    # COLA
    for i in range(5):
        # Franjas dinámicas: Negro alternado con Gris Oscuro dinámico
        c_cola = negro if i % 2 == 0 else gris_oscuro
        draw_cube_miko(0, -0.4, -0.4 - (i*0.25), 0.45, 0.45, 0.25, *c_cola)

    # Extremidades dinamicas
    t = glutGet(GLUT_ELAPSED_TIME) * 0.005 
    mov = state.movimiento
    val_caminar = math.sin(t * 6) * 30
    val_baile = math.sin(t * 3) * 15
    val_comer = math.sin(t * 12) * 20

    # Bracitos
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0.45 * side, 0.1, 0.3) 
        
        if mov == "aplaudir":
            glRotatef(-90 * side, 0, 0, 1) 
            glRotatef(math.sin(t * 10) * 25, 1, 0, 0)
        elif mov == "caminando":
            glRotatef(val_caminar * -side, 1, 0, 0)
        elif mov == "bailar":
            glRotatef(val_baile, 0, 0, 1)
            glRotatef(-30, 1, 0, 0)
        elif mov == "comer":
            glRotatef(-40 + val_comer, 1, 0, 0)
        elif mov == "saludo" and side == 1:
            glRotatef(-150, 1, 0, 0)
            glRotatef(math.sin(t * 10) * 20, 0, 0, 1)
        elif mov == "saltando":
            glRotatef(-110, 1, 0, 0)
        elif mov == "giro":
            glRotatef(-80 * side, 0, 0, 1)
            
        # Las patitas delanteras usan el Gris Oscuro dinámico
        draw_cube_miko(0, -0.2, 0, 0.22, 0.45, 0.22, *gris_oscuro)
        glPopMatrix()

    # Patitas
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0.35 * side, -0.5, 0.1) 
        
        if mov == "caminando":
            glRotatef(val_caminar * side, 1, 0, 0)
        elif mov == "saltando":
            glRotatef(40, 1, 0, 0) 
        elif mov == "bailar":
            glRotatef(val_baile * -0.5, 0, 0, 1)
        elif mov == "aplaudir":
            glRotatef(45, 1, 0, 0)
            
        glRotatef(10 * side, 0, 0, 1) # Pose base
        
        # Mantenemos las patitas traseras en NEGRO fijo
        draw_cube_miko(0, -0.1, 0, 0.28, 0.3, 0.3, *negro)
        glPopMatrix()

    glPopMatrix()


# === WRAPPER PARA EL MENÚ DE SELECCIÓN ===
class _NeutralState:
    """Estado neutral mínimo para la pose base del Mapache."""
    color_miko = [0.65, 0.65, 0.65]   # Gris mapache original
    expresion = "normal"
    movimiento = "quieto"

def draw_neutral():
    """Dibuja al Mapache Miko en pose neutral sin depender de su proyecto."""
    draw_miko(_NeutralState())