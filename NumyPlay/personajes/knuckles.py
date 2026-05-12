from OpenGL.GL import *
from OpenGL.GLU import *

# ---------------------------------------------------------------------------
# HELPERS: reemplazan glutSolidSphere / glutSolidCone con GLU puro.
# Estas funciones son compatibles con cualquier contexto OpenGL (GLUT, pyopengltk, etc.)
# ---------------------------------------------------------------------------
def solid_sphere(radius, slices=24, stacks=24):
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, radius, slices, stacks)
    gluDeleteQuadric(q)

def solid_cone(base, height, slices=16, stacks=16):
    """Cono apuntando en +Z, igual que glutSolidCone."""
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluCylinder(q, base, 0.0, height, slices, stacks)  # base→0 = cono
    gluDeleteQuadric(q)

# ---------------------------------------------------------------------------

def draw_body():
    glPushMatrix()
    glColor3f(0.8, 0.1, 0.1) 
    solid_sphere(1.0, 32, 32)
    
    # Panza blanca redonda
    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.88)  
    glColor3f(1.0, 1.0, 1.0)
    solid_sphere(0.45, 24, 24) 
    glPopMatrix()
    glPopMatrix()

def draw_head_and_dreadlocks(expresion, rot_cabeza=0):
    glPushMatrix()
    glTranslatef(0.0, 1.4, 0.0)
    glRotatef(rot_cabeza, 0, 1, 0)  # Giro completo de cabeza (eje Y)
    
    # Cabeza principal
    glColor3f(0.8, 0.1, 0.1)
    solid_sphere(0.8, 32, 32)
    
    # Hocico
    glPushMatrix()
    glTranslatef(0.0, -0.2, 0.7)
    glColor3f(1.0, 0.6, 0.2)
    solid_sphere(0.4, 16, 16)
    
    # Nariz negra
    glTranslatef(0.0, 0.1, 0.4)
    glColor3f(0.0, 0.0, 0.0)
    solid_sphere(0.1, 16, 16)
    glPopMatrix()

    # --- SISTEMA DE EXPRESIONES FACIALES ---
    # 0:Normal, 1:Guiño, 2:Ira, 3:Sonrisa, 4:Tristeza, 5:Admiración
    for i, dx in enumerate([-0.25, 0.25]):
        glPushMatrix()
        glTranslatef(dx, 0.2, 0.75)
        
        # 1. Guiño (Cierra el ojo izquierdo i==0)
        if expresion == 1 and i == 0:
            glScalef(1.0, 0.1, 1.0)
            glColor3f(0.0, 0.0, 0.0) 
            solid_sphere(0.15, 16, 16)
        
        # 3. Sonrisa (Ojos cerrados felices ^ ^)
        elif expresion == 3:
            glTranslatef(0.0, 0.0, 0.1)
            glRotatef(45 if i == 0 else -45, 0, 0, 1)
            glScalef(1.5, 0.2, 0.2)
            glColor3f(0.0, 0.0, 0.0)
            solid_sphere(0.1, 8, 8)
            
        else:
            # Ojo abierto normal
            glColor3f(1.0, 1.0, 1.0) 
            solid_sphere(0.15, 16, 16)
            
            # Pupila
            glPushMatrix()
            glTranslatef(0.0, 0.02, 0.13)
            glColor3f(0.0, 0.0, 0.0)
            
            # 5. Admiración (Pupilas gigantes)
            if expresion == 5:
                solid_sphere(0.11, 8, 8) 
            else:
                solid_sphere(0.06, 8, 8)
            glPopMatrix()
            
            # Cejas para Ira (2) o Tristeza (4)
            if expresion == 2 or expresion == 4:
                glPushMatrix()
                glTranslatef(0.0, 0.15, 0.1)
                angulo_ceja = -30 if expresion == 2 else 30
                glRotatef(angulo_ceja if i == 0 else -angulo_ceja, 0, 0, 1) 
                glColor3f(0.0, 0.0, 0.0)
                glScalef(2.0, 0.3, 0.5)
                solid_sphere(0.08, 8, 8)
                glPopMatrix()
                
        glPopMatrix()

    # Rastas
    for rot_y in [-60, 0, 60]:
        glPushMatrix()
        glRotatef(rot_y, 0, 1, 0)
        glTranslatef(0.0, 0.2, -0.5)
        glRotatef(135, 1, 0, 0) 
        glColor3f(0.8, 0.1, 0.1)
        solid_cone(0.3, 1.2, 16, 16)
        glPopMatrix()
        
    glPopMatrix()

def draw_arms_and_fists(rot_izq, rot_der, tilt_v=45):
    for i, dx in enumerate([-1, 1]): 
        rot_actual = rot_izq if dx == -1 else rot_der
        
        glPushMatrix()
        glTranslatef(dx * 0.9, 0.1, 0.0) 
        glRotatef(90 * dx, 0, 1, 0) 
        glRotatef(tilt_v, 1, 0, 0)
        glRotatef(rot_actual, 0, 1, 0)
        
        glColor3f(0.8, 0.1, 0.1)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.15, 0.15, 0.6, 16, 16)
        gluDeleteQuadric(quad)
        
        glTranslatef(0.0, 0.0, 0.6) 
        glColor3f(1.0, 1.0, 1.0)
        solid_sphere(0.35, 32, 32)
        
        for desp_z in [-0.15, 0.15]:
            glPushMatrix()
            glTranslatef(dx * 0.35, 0.0, desp_z) 
            glRotatef(90 * dx, 0, 1, 0)
            glColor3f(0.7, 0.7, 0.7) 
            solid_cone(0.08, 0.25, 16, 16)
            glPopMatrix()
            
        glPopMatrix()

def draw_legs_and_shoes(rot_izq, rot_der):
    for i, dx in enumerate([-0.4, 0.4]):
        rot_actual = rot_izq if dx == -0.4 else rot_der
        
        glPushMatrix()
        glTranslatef(dx, -0.6, 0.0)
        glRotatef(rot_actual, 1, 0, 0)
        
        # Piernas
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glColor3f(0.8, 0.1, 0.1)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.15, 0.15, 0.6, 16, 16)
        gluDeleteQuadric(quad)
        glPopMatrix()
        
        # Zapatos
        glTranslatef(0.0, -0.7, 0.2) 
        
        glColor3f(0.9, 0.1, 0.1)
        glPushMatrix()
        glScalef(1.0, 0.5, 1.5)
        solid_sphere(0.35, 24, 24)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.0, 0.15, -0.1) 
        glScalef(1.0, 0.5, 0.8)       
        glColor3f(0.9, 0.9, 0.0)      
        solid_sphere(0.25, 16, 16)
        glPopMatrix()
        
        glPopMatrix()

def draw_knuckles_full(rot_brazo_i=0, rot_brazo_d=0, rot_pierna_i=0, rot_pierna_d=0, expresion=0, tilt_brazos=45, rot_cabeza=0):
    glPushMatrix()
    draw_body()
    draw_head_and_dreadlocks(expresion, rot_cabeza)
    draw_arms_and_fists(rot_brazo_i, rot_brazo_d, tilt_brazos)
    draw_legs_and_shoes(rot_pierna_i, rot_pierna_d)
    glPopMatrix()