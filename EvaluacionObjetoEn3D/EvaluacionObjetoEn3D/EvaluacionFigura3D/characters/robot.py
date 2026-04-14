# ============================================================
# robot.py - Modelo 3D de un Robot con expresiones y movimientos
# ============================================================

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from actions import state

# ─── Paleta de colores ───
WHITE       = (0.95, 0.95, 0.97)
CYAN        = (0.10, 0.70, 0.80)
GLOW_CYAN   = (0.30, 0.90, 1.00)
DARK_BLUE   = (0.05, 0.15, 0.40)
DARKER_BLUE = (0.02, 0.05, 0.20)
BLACK       = (0.05, 0.05, 0.05)
GRAY        = (0.50, 0.50, 0.55)

def get_white_color():
    if hasattr(state, 'color_override') and state.color_override:
        return state.color_override
    return WHITE

# ═══════════════════════════════════════════
# PARTES DEL CUERPO
# ═══════════════════════════════════════════

def draw_head():
    """Cabeza flotante blanca con pantalla azul."""
    glPushMatrix()
    glTranslatef(0, 0.85, 0.0)
    
    # Cabeza blanca esférica
    glPushMatrix()
    glScalef(1.2, 1.0, 1.1)
    glColor3f(*get_white_color())
    glutSolidSphere(0.4, 32, 32)
    glPopMatrix()
    
    # Pantalla frontal (azul oscuro)
    glPushMatrix()
    glTranslatef(0, 0.0, 0.30)
    glScalef(0.9, 0.65, 0.4)
    glColor3f(*DARK_BLUE)
    glutSolidSphere(0.42, 32, 32)
    glPopMatrix()

    # Ojos digitales en la pantalla
    draw_eyes()

    # Auriculares / Antenas laterales
    draw_ears()

    # Antena superior mecánica
    glPushMatrix()
    glTranslatef(0, 0.38, 0.0)
    
    # Base oscura de la antena
    glPushMatrix()
    glScalef(1.0, 0.2, 1.0)
    glColor3f(*DARK_BLUE)
    glutSolidSphere(0.15, 16, 16)
    glPopMatrix()
    
    # Palo de la antena
    glPushMatrix()
    glTranslatef(0, 0.15, 0.0)
    glScalef(0.1, 1.0, 0.1)
    glColor3f(*GRAY)
    glutSolidCube(0.25)
    glPopMatrix()
    
    # Foco brillante superior
    glPushMatrix()
    glTranslatef(0, 0.28, 0.0)
    glColor3f(*GLOW_CYAN)
    glutSolidSphere(0.04, 12, 12)
    glPopMatrix()
    
    glPopMatrix()

    glPopMatrix()

def draw_ears():
    """Auriculares flotantes a los lados de la cabeza."""
    for dx in [-0.52, 0.52]:
        glPushMatrix()
        glTranslatef(dx, 0.0, 0.0)
        
        # Base del auricular (blanco)
        glPushMatrix()
        glScalef(0.25, 0.5, 0.5)
        glColor3f(*get_white_color())
        glutSolidSphere(0.3, 16, 16)
        glPopMatrix()
        
        # Núcleo magnético oscuro interno
        glPushMatrix()
        if dx < 0:
            glTranslatef(0.08, 0.0, 0.0)
        else:
            glTranslatef(-0.08, 0.0, 0.0)
        glScalef(0.1, 0.4, 0.4)
        glColor3f(*DARKER_BLUE)
        glutSolidSphere(0.28, 16, 16)
        glPopMatrix()
        
        # Antena/Detalle cyan
        glPushMatrix()
        if dx < 0:
            glTranslatef(-0.06, 0.15, 0.0)
            glRotatef(15, 0, 0, 1)
        else:
            glTranslatef(0.06, 0.15, 0.0)
            glRotatef(-15, 0, 0, 1)
        
        glScalef(0.15, 0.6, 0.2)
        glColor3f(*CYAN)
        glutSolidCube(0.3)
        glPopMatrix()
        
        glPopMatrix()

def draw_eyes():
    """Ojos digitales que cambian con la expresión."""
    expr = state.expression
    blink = math.sin(state.blink_timer) > 0.95

    # Si parpadea, son solo líneas delgadas
    if blink:
        for dx in [-0.15, 0.15]:
            glPushMatrix()
            glTranslatef(dx, 0.0, 0.47)
            glScalef(0.2, 0.02, 0.02)
            glColor3f(*GLOW_CYAN)
            glutSolidSphere(0.4, 10, 10)
            glPopMatrix()
        return

    # Expresiones regulares
    for dx in [-0.15, 0.15]:
        glPushMatrix()
        
        if expr == "scared":
            offset = math.sin(state.blink_timer * 20) * 0.02
            glTranslatef(dx + offset, 0.0, 0.47)
        else:
            glTranslatef(dx, 0.0, 0.47)

        glColor3f(*GLOW_CYAN)

        if expr == "happy" or expr == "neutral":
            if expr == "neutral":
                # Ojos neutrales redondos
                glutSolidSphere(0.06, 16, 16)
            else:
                # Ojos felices en forma de ^ (5 círculos)
                for ang in [-40, -20, 0, 20, 40]:
                    glPushMatrix()
                    px = math.sin(math.radians(ang)) * 0.07
                    py = math.cos(math.radians(ang)) * 0.07
                    glTranslatef(px, py - 0.02, 0)
                    glutSolidSphere(0.045, 12, 12)
                    glPopMatrix()
        elif expr == "sad":
            # Ojos tristes (5 círculos)
            for ang in [-40, -20, 0, 20, 40]:
                glPushMatrix()
                px = math.sin(math.radians(ang)) * 0.07
                py = -math.cos(math.radians(ang)) * 0.07
                glTranslatef(px, py + 0.03, 0)
                glutSolidSphere(0.045, 12, 12)
                glPopMatrix()
        elif expr == "surprised":
            # Ojos de sorpresa O O
            for i in range(8):
                ang = i * 45
                glPushMatrix()
                px = math.sin(math.radians(ang)) * 0.06
                py = math.cos(math.radians(ang)) * 0.07
                glTranslatef(px, py, 0)
                glutSolidSphere(0.025, 12, 12)
                glPopMatrix()
        elif expr == "angry":
            # V / (Más largo y grueso)
            glPushMatrix()
            if dx < 0:
                glRotatef(-25, 0, 0, 1)
            else:
                glRotatef(25, 0, 0, 1)
            glScalef(0.20, 0.065, 0.025)
            glutSolidSphere(0.45, 12, 12)
            glPopMatrix()
        elif expr == "scared":
            glScalef(0.10, 0.12, 0.02)
            glutSolidSphere(0.35, 12, 12)
        elif expr == "doubt":
            # Duda: - \
            glPushMatrix()
            if dx < 0:
                # Ojo izquierdo recto
                glScalef(0.18, 0.06, 0.02)
            else:
                # Ojo derecho inclinado
                glRotatef(-25, 0, 0, 1)
                glScalef(0.18, 0.06, 0.02)
            glutSolidSphere(0.45, 12, 12)
            glPopMatrix()

        glPopMatrix()

def draw_body():
    """Cuerpo ovalado blanco con panel cyan."""
    glPushMatrix()
    glTranslatef(0, 0.25, 0.0)
    
    # Cuerpo principal (blanco)
    glPushMatrix()
    glScalef(1.0, 1.2, 0.8)
    glColor3f(*get_white_color())
    glutSolidSphere(0.4, 32, 32)
    glPopMatrix()

    # Placa del pecho (núcleo del reactor)
    glPushMatrix()
    glTranslatef(0, 0.05, 0.3)
    glScalef(0.55, 0.65, 0.2)  # Marco ligeramente más pequeño
    glColor3f(*DARKER_BLUE)  # Borde oscuro
    glutSolidSphere(0.35, 20, 20)
    
    # Núcleo central brillante (ocupa mayor proporción para que el marco se vea delgado)
    glTranslatef(0, 0.0, 0.20)
    glScalef(0.75, 0.75, 1.0)
    glColor3f(*GLOW_CYAN)
    glutSolidSphere(0.30, 16, 16)
    glPopMatrix()
    
    # Junta mecánica del cuello (gris)
    glPushMatrix()
    glTranslatef(0, 0.38, 0.0)
    glScalef(0.5, 0.15, 0.5)
    glColor3f(*GRAY)
    glutSolidSphere(0.35, 16, 16)
    glPopMatrix()
    
    # Propulsor (jetpack) en la espalda, ligeramente más grande
    glPushMatrix()
    glTranslatef(0, 0.0, -0.32)
    glScalef(0.9, 1.15, 0.55)
    glColor3f(*GRAY)
    glutSolidCube(0.4)
    
    # Energía/Flama del jetpack hacia abajo
    glTranslatef(0, -0.22, 0.0)
    glScalef(0.6, 0.4, 0.6)
    glColor3f(*CYAN)
    glutSolidSphere(0.2, 12, 12)
    glPopMatrix()
    
    # Unión oscura en la base
    glPushMatrix()
    glTranslatef(0, -0.35, 0.0)
    glScalef(0.8, 0.15, 0.7)
    glColor3f(*DARK_BLUE)
    glutSolidSphere(0.35, 20, 20)
    glPopMatrix()

    glPopMatrix()

def draw_arms():
    """Brazos blancos flotantes."""
    for dx in [-0.55, 0.55]:
        glPushMatrix()
        # Posición base del brazo/hombro
        glTranslatef(dx, 0.3, 0.0)
        
        # Articulación del hombro magnética (estacionaria respecto al cuerpo)
        glPushMatrix()
        glTranslatef(0.1 if dx < 0 else -0.1, 0.15, 0.0)
        glScalef(0.5, 0.5, 0.5)
        glColor3f(*DARKER_BLUE)
        glutSolidSphere(0.18, 12, 12)
        glPopMatrix()

        # Mover el pivote de rotación al hombro (Y = 0.15)
        glTranslatef(0, 0.15, 0)
        
        # Animaciones de los brazos
        if state.reaction_type == "wave_arms":
            # Levantar brazos y agitarlos efusivamente
            wave = math.sin(state.reaction_timer * 0.6) * 30
            if dx < 0:
                glRotatef(-130, 0, 0, 1) # Levantar brazo izq
                glRotatef(wave, 1, 0, 0) # Agitar adelante/atrás
            else:
                glRotatef(130, 0, 0, 1)  # Levantar brazo der
                glRotatef(-wave, 1, 0, 0)
        elif state.walking:
            swing = math.sin(state.animation_angle + (0 if dx < 0 else math.pi)) * 25
            glRotatef(swing, 1, 0, 0) # Balanceo desde el hombro
            
        # Regresar el pivote para dibujar la cápsula hacia abajo
        glTranslatef(0, -0.15, 0)

        # Cápsula del brazo
        glPushMatrix()
        glScalef(0.3, 0.8, 0.3)
        glColor3f(*get_white_color())
        glutSolidSphere(0.25, 20, 20)
        glPopMatrix()
        
        glPopMatrix()

def draw_feet():
    """Pies blancos flotantes debajo del robot."""
    for i, dx in enumerate([-0.25, 0.25]):
        glPushMatrix()
        glTranslatef(dx, -0.45, 0.1)
        
        # Animación de caminar para los pies
        if state.walking:
            swing = math.sin(state.animation_angle + (i * math.pi)) * 25
            glRotatef(swing, 1, 0, 0)
            
        # Pie redondeado
        glPushMatrix()
        glScalef(0.4, 0.3, 0.6)
        glColor3f(*get_white_color())
        glutSolidSphere(0.3, 16, 16)
        glPopMatrix()
        
        glPopMatrix()


# ═══════════════════════════════════════════
# FUNCIÓN PRINCIPAL - DIBUJA AL ROBOT COMPLETO
# ═══════════════════════════════════════════

def draw_robot_full():
    """Dibuja al robot completo aplicando transformaciones globales."""
    glPushMatrix()

    # Efecto sutil de flotar constante
    float_offset = math.sin(state.blink_timer * 2.0) * 0.05
    glTranslatef(0, float_offset, 0)

    # Reacciones globales
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
        
    elif state.reaction_type == "nod":
        progress = state.reaction_timer / state.reaction_duration
        angle = math.sin(math.pi * progress) * 25
        glRotatef(angle, 1, 0, 0)

    if state.expression == "scared":
        tremor = math.sin(state.blink_timer * 15) * 0.02
        glTranslatef(tremor, 0, tremor)

    # Balanceo al caminar
    if state.walking:
        wobble = math.sin(state.animation_angle * 2) * 5
        glRotatef(wobble, 0, 0, 1)

    # El cuerpo baja para juntarse con los pies
    glPushMatrix()
    if state.reaction_type == "crouch":
        progress = state.reaction_timer / state.reaction_duration
        y_offset = math.sin(math.pi * progress) * -0.55
        glTranslatef(0, y_offset, 0)
        
    draw_body()
    draw_head()
    draw_arms()
    
    if state.expression == "doubt":
        glPushMatrix()
        float_y = math.sin(state.blink_timer * 4.0) * 0.1
        glTranslatef(-0.06, 1.5 + float_y, 0.0)
        glScalef(0.004, 0.004, 0.004)
        glLineWidth(3.0)
        glColor3f(*GLOW_CYAN)
        for char in "?":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
        glLineWidth(1.0)
        glPopMatrix()
        
    glPopMatrix()
    
    # Los pies se quedan atorados en el suelo y se achatan
    glPushMatrix()
    if state.reaction_type == "crouch":
        progress = state.reaction_timer / state.reaction_duration
        scale_y_feet = 1.0 - math.sin(math.pi * progress) * 0.4
        glTranslatef(0, -0.65, 0)
        glScalef(1.0, scale_y_feet, 1.0)
        glTranslatef(0, 0.65, 0)
        
    draw_feet()
    glPopMatrix()

    glPopMatrix()
