# src/entities/chef.py
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from engine.geometry import GeometryEngine  # Comentado: módulo del proyecto original

# Stub para GeometryEngine: dibuja una aproximación plana del mandil
class GeometryEngine:
    @staticmethod
    def draw_bezier_surface(ctrl_points, u_steps, v_steps, wireframe=False):
        # Aproximación simple: dibuja un rectángulo representando el delantal
        from OpenGL.GL import glBegin, glEnd, glVertex3f, GL_QUADS
        glBegin(GL_QUADS)
        glVertex3f(-0.85, 0.0, 0.0)
        glVertex3f(0.85, 0.0, 0.0)
        glVertex3f(0.9, -2.0, 0.1)
        glVertex3f(-0.9, -2.0, 0.1)
        glEnd()

class ChefSaiba:
    def __init__(self):
        # --- RÚBRICA: 7 EXPRESIONES ---
        self.expressions = [
            "NORMAL", "OJOS_BLANCOS", "DUDA", 
            "GUIÑO", "SONRISA_CONF", "IRA", "ADMIRACION"
        ]
        self.current_exp_idx = 0
        
        # --- SISTEMA DE ANIMACIÓN ---
        self.actions = ["IDLE", "CAMINAR", "SALTAR", "AGACHARSE", "PICAR", "SALTEAR", "BANDANA", "SALUDAR"]
        self.current_action = "IDLE"
        self.anim_time = 0.0 # Nuestro reloj interno para los frames

        # --- SISTEMA POSICIONAL ---
        self.pos_x = 0.0
        self.pos_z = 8.0  # Spawneamos lejos de los hornos para no quedar atrapados
        self.rot_y = 180.0 # Volteamos hacia la cámara para la intro
        self.visual_rot_y = 0.0 # Gira el cuerpo independientemente de la cámara
        
        # --- ARTICULACIONES (Fase 3: Animación lista) ---
        self.arm_r_pitch = 0.0
        self.arm_l_pitch = 0.0
        self.leg_r_pitch = 0.0
        self.leg_l_pitch = 0.0
        self.body_y_offset = 0.0 # Para saltar o agacharse
        self.body_pitch = 0.0    # Para inclinar el torso al agacharse
        
        self.quadric = gluNewQuadric()

        # Puntos de control Bézier para un delantal que cae con ondas naturales
        self.apron_ctrl_points = [
            [[-0.8, 0.0, 0.0], [-0.3, 0.0, 0.3], [0.3, 0.0, 0.3], [0.8, 0.0, 0.0]],
            [[-0.85, -1.0, 0.1], [-0.4, -1.0, 0.4], [0.4, -1.0, 0.4], [0.85, -1.0, 0.1]],
            [[-0.9, -2.0, 0.0], [-0.5, -2.0, 0.2], [0.5, -2.0, 0.2], [0.9, -2.0, 0.0]]
        ]

    def draw(self):
        self.update_animation() # Llamamos al motor cada vez que se dibuja
        
        glPushMatrix()
        
        # --- NUEVO: APLICAR COORDENADAS GLOBALES DEL CHEF ---
        glTranslatef(self.pos_x, 0.0, self.pos_z)
        # Sumamos rot_y (dirección base de la cámara) + visual_rot_y (para que el cuerpo gire a los lados sin rotar la cámara)
        glRotatef(self.rot_y + self.visual_rot_y, 0.0, 1.0, 0.0)

        glPushMatrix()
        # Aplicamos la altura base MÁS el offset del salto/agacharse
        glTranslatef(0.0, 3.0 + self.body_y_offset, 0.0)
        # Aplicamos la inclinación del torso
        glRotatef(self.body_pitch, 1.0, 0.0, 0.0)

        # 1. Dibujar Torso completo (con cuello y tirantes)
        self.draw_torso()
        
        # --- CABEZA (Ensamblada sobre el torso) ---
        glPushMatrix()
        glTranslatef(0.0, 1.8, 0.0) # Altura relativa del cuello
        self.draw_head()
        glPopMatrix()

        # --- BRAZOS (CORRECCIÓN DE ALTURA: Subimos hombros) ---
        # Antes estaban en Y=1.0 o Y=0.8. Los subimos a Y=1.3 para que encajen mejor.
        self.draw_limb(1.2, 1.3, self.arm_r_pitch, True)   # Derecho
        self.draw_limb(-1.2, 1.3, self.arm_l_pitch, True)  # Izquierdo

        # --- PIERNAS (CORRECCIÓN DE ENSAMBLADO: Subimos piernas) ---
        # Antes estaban en Y=-1.5, dejando hueco. Las subimos a Y=-1.0.
        self.draw_limb(0.5, -1.0, self.leg_r_pitch, False) # Derecha
        self.draw_limb(-0.5, -1.0, self.leg_l_pitch, False)# Izquierda

        # --- NUEVO: DIBUJAR LOS UTENSILIOS (PROPS) ---
        self.draw_props()

        glPopMatrix()
        glPopMatrix()

    def draw_torso(self):
        # 1. Cuello (Color piel)
        glColor3f(0.9, 0.7, 0.6) 
        glPushMatrix()
        glTranslatef(0.0, 1.1, 0.0)
        glRotatef(90, 1.0, 0.0, 0.0)
        gluCylinder(self.quadric, 0.2, 0.2, 0.4, 16, 16)
        glPopMatrix()

        # 2. Chaqueta de Chef (Azul oscuro)
        glColor3f(0.1, 0.2, 0.5)
        glPushMatrix()
        glTranslatef(0.0, 0.2, 0.0) # Bajamos el centro de la chaqueta
        glScalef(0.9, 1.2, 0.5)     # La hacemos anatómica
        glutSolidCube(1.8)
        glPopMatrix()

        # 3. Delantal / Mandil (Bézier - Blanco azulado)
        glColor3f(0.85, 0.85, 0.9) 
        glPushMatrix()
        glTranslatef(0.0, -0.4, 0.5) # Frente del torso
        GeometryEngine.draw_bezier_surface(self.apron_ctrl_points, 15, 15, wireframe=False)
        glPopMatrix()

        # 4. Tirantes (Color del mandil)
        glColor3f(0.85, 0.85, 0.9) 
        
        # Tirante Izquierdo
        glPushMatrix()
        glTranslatef(-0.4, 0.5, 0.46) # Subimos hasta el hombro izquierdo
        glRotatef(-15, 0.0, 0.0, 1.0) # Cruzado
        glScalef(0.15, 0.9, 0.05)     # Plano y largo
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Tirante Derecho
        glPushMatrix()
        glTranslatef(0.4, 0.5, 0.46)  # Subimos hasta el hombro derecho
        glRotatef(15, 0.0, 0.0, 1.0)  # Cruzado
        glScalef(0.15, 0.9, 0.05)
        glutSolidCube(1.0)
        glPopMatrix()

    def draw_head(self):
        # 1. Cabeza base (Escalada para que no sea un globo)
        glColor3f(0.9, 0.7, 0.6)
        glPushMatrix()
        glScalef(0.9, 1.0, 0.9) 
        gluSphere(self.quadric, 1.0, 32, 32)
        glPopMatrix()

        # 2. EL CABELLO MODO SHOKUGEKI (Puro caos geométrico)
        glColor3f(0.0, 0.25, 0.75) # Azul oscuro/brillante
        
        # --- El "Casco" base para que NUNCA se le vea la calva ---
        glPushMatrix()
        glTranslatef(0.0, 0.3, -0.1)
        glScalef(0.92, 0.85, 0.95)
        gluSphere(self.quadric, 1.0, 32, 32)
        glPopMatrix()

        # --- Flequillo (Picos cayendo hacia la frente) ---
        for angle in range(-50, 51, 25):
            glPushMatrix()
            glTranslatef(0.0, 0.6, 0.65) # Al frente
            glRotatef(angle, 0.0, 0.0, 1.0) # Abanico lateral
            glRotatef(50, 1.0, 0.0, 0.0)    # Inclinados hacia la cara
            gluCylinder(self.quadric, 0.15, 0.0, 0.8, 8, 8)
            glPopMatrix()

        # --- Corona y Arriba (La explosión principal) ---
        for angle_y in range(-90, 91, 30): # Girando alrededor de la cabeza
            for angle_x in range(-50, 20, 20): # Diferentes inclinaciones hacia arriba
                glPushMatrix()
                glTranslatef(0.0, 0.7, 0.0) # Centro arriba
                glRotatef(angle_y, 0.0, 1.0, 0.0)
                glRotatef(angle_x - 90, 1.0, 0.0, 0.0) # Apuntando hacia arriba y afuera
                
                # Hacemos los picos centrales más largos que los laterales
                altura = 1.0 if abs(angle_y) < 40 else 0.7
                gluCylinder(self.quadric, 0.2, 0.0, altura, 8, 8)
                glPopMatrix()

        # --- Lados y Nuca (Picos apuntando hacia atrás/abajo) ---
        for angle_y in range(-140, 141, 40): 
            glPushMatrix()
            glTranslatef(0.0, 0.2, -0.3)
            glRotatef(angle_y, 0.0, 1.0, 0.0)
            glRotatef(-110, 1.0, 0.0, 0.0) # Apuntando hacia abajo/atrás
            gluCylinder(self.quadric, 0.22, 0.0, 1.1, 8, 8)
            glPopMatrix()

        # 3. Bandana (Acomodada entre todo el pelo)
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glTranslatef(0.0, 0.45, 0.0)
        glRotatef(90, 1.0, 0.0, 0.0)
        glutSolidTorus(0.08, 0.9, 16, 32)
        glPopMatrix()

        # 4. Cicatriz
        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(4.0)
        glBegin(GL_LINES)
        glVertex3f(-0.3, 0.1, 0.86)
        glVertex3f(-0.6, -0.2, 0.75)
        glEnd()
        glLineWidth(1.0)

        # 5. Rostro
        self.draw_face()

    def draw_face(self):
        glPushMatrix()
        # Ajustamos Z a 0.91 para que no flote, ya que la cabeza ahora mide 0.9 de profundidad
        glTranslatef(0.0, 0.0, 0.91) 
        exp = self.expressions[self.current_exp_idx]
        glColor3f(0.1, 0.1, 0.1) 

        if exp == "NORMAL":
            self.draw_quad(-0.25, 0.1, 0.08) # Ojos 
            self.draw_quad(0.25, 0.1, 0.08)  
            self.draw_rect(0.0, -0.3, 0.3, 0.05) # Boca recta
            
        elif exp == "OJOS_BLANCOS":
            # Shock / Susto perdiendo el color de los ojos
            glColor3f(1.0, 1.0, 1.0) 
            glPushMatrix()
            glTranslatef(-0.2, 0.1, 0.0)
            gluSphere(self.quadric, 0.15, 16, 16) 
            glPopMatrix()
            glPushMatrix()
            glTranslatef(0.2, 0.1, 0.0)
            gluSphere(self.quadric, 0.15, 16, 16) 
            glPopMatrix()
            glColor3f(0.1, 0.1, 0.1)
            self.draw_rect(0.0, -0.35, 0.15, 0.25) # Boca abierta centrada

        elif exp == "DUDA":
            # Ceja levantada, un ojo más pequeño
            self.draw_quad(-0.25, 0.1, 0.08)
            self.draw_quad(0.25, 0.1, 0.04) 
            glLineWidth(2.0)
            glBegin(GL_LINES)
            glVertex3f(0.1, 0.25, 0.0)
            glVertex3f(0.4, 0.35, 0.0) # Ceja derecha alta
            glEnd()
            glLineWidth(1.0)
            self.draw_rect(0.0, -0.3, 0.2, 0.05)

        elif exp == "GUIÑO":
            # Ojo izquierdo normal, derecho cerrado (linea horizontal)
            self.draw_quad(-0.25, 0.1, 0.08)
            self.draw_rect(0.25, 0.1, 0.16, 0.02) # Ojo derecho cerrado
            # Sonrisa de lado
            glLineWidth(3.0)
            glBegin(GL_LINE_STRIP)
            glVertex3f(-0.1, -0.3, 0.0)
            glVertex3f(0.1, -0.3, 0.0)
            glVertex3f(0.2, -0.2, 0.0)
            glEnd()
            glLineWidth(1.0)
            
        elif exp == "SONRISA_CONF":
            # Ojos cerrados felices (arcos hacia arriba) ^ ^
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glVertex3f(-0.35, 0.05, 0.0); glVertex3f(-0.25, 0.15, 0.0)
            glVertex3f(-0.25, 0.15, 0.0); glVertex3f(-0.15, 0.05, 0.0)
            
            glVertex3f(0.15, 0.05, 0.0);  glVertex3f(0.25, 0.15, 0.0)
            glVertex3f(0.25, 0.15, 0.0);  glVertex3f(0.35, 0.05, 0.0)
            glEnd()
            # Sonrisa abierta contenta grande
            self.draw_rect(0.0, -0.25, 0.3, 0.15)
            glColor3f(1.0, 1.0, 1.0) # Dientes blancos mostrando frescura
            self.draw_rect(0.0, -0.2, 0.25, 0.05)
            glLineWidth(1.0)

        elif exp == "IRA":
            # Escena de Pesadilla en la Cocina: Ojos rojos brillando
            glColor3f(0.9, 0.1, 0.1)
            self.draw_quad(-0.25, 0.1, 0.05)
            self.draw_quad(0.25, 0.1, 0.05)
            # Cejas gruesas fruncidas hacia abajo / \
            glColor3f(0.1, 0.1, 0.1)
            glLineWidth(4.0)
            glBegin(GL_LINES)
            glVertex3f(-0.4, 0.35, 0.0); glVertex3f(-0.1, 0.2, 0.0)
            glVertex3f(0.1, 0.2, 0.0);  glVertex3f(0.4, 0.35, 0.0)
            glEnd()
            # Boca abierta gritando (estilo anime cuadrado)
            self.draw_rect(0.0, -0.35, 0.25, 0.2)
            glLineWidth(1.0)

        elif exp == "ADMIRACION":
            # Ojos grandes de estrella deslumbrante (Rombos grandes amarillos)
            glColor3f(1.0, 0.9, 0.0)
            glPushMatrix()
            glTranslatef(-0.25, 0.1, 0.0)
            glRotatef(45, 0.0, 0.0, 1.0)
            self.draw_quad(0.0, 0.0, 0.12)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(0.25, 0.1, 0.0)
            glRotatef(45, 0.0, 0.0, 1.0)
            self.draw_quad(0.0, 0.0, 0.12)
            glPopMatrix()
            # Boca de "Ohh" (Mini Circulo asombrado)
            glColor3f(0.1, 0.1, 0.1)
            glPushMatrix()
            glTranslatef(0.0, -0.35, 0.0)
            gluSphere(self.quadric, 0.08, 16, 16)
            glPopMatrix()

        glPopMatrix()

    def next_expression(self):
        """Cambia a la siguiente expresión."""
        self.current_exp_idx = (self.current_exp_idx + 1) % len(self.expressions)
        print(f"Expresión actual: {self.expressions[self.current_exp_idx]}")

    def draw_quad(self, x, y, size):
        glBegin(GL_QUADS)
        glVertex3f(x - size, y - size, 0.0)
        glVertex3f(x + size, y - size, 0.0)
        glVertex3f(x + size, y + size, 0.0)
        glVertex3f(x - size, y + size, 0.0)
        glEnd()

    def draw_rect(self, x, y, w, h):
        glBegin(GL_QUADS)
        glVertex3f(x - w/2, y - h/2, 0.0)
        glVertex3f(x + w/2, y - h/2, 0.0)
        glVertex3f(x + w/2, y + h/2, 0.0)
        glVertex3f(x - w/2, y + h/2, 0.0)
        glEnd()

    def draw_limb(self, x, y, pitch, is_arm):
        glPushMatrix()
        glTranslatef(x, y, 0.0)
        glRotatef(pitch, 1.0, 0.0, 0.0) # Preparado para Fase 3 (Animación)
        
        # Manga de Chaqueta / Pantalón
        glColor3f(0.1, 0.2, 0.5) if is_arm else glColor3f(0.05, 0.05, 0.05)
        glPushMatrix()
        glRotatef(90, 1.0, 0.0, 0.0)
        gluCylinder(self.quadric, 0.3, 0.25, 1.5, 16, 16)
        glPopMatrix()
        
        # Mano / Pie
        glTranslatef(0.0, -1.6, 0.0)
        if is_arm:
            glColor3f(0.9, 0.7, 0.6)
            gluSphere(self.quadric, 0.25, 16, 16)
        else:
            glColor3f(0.2, 0.2, 0.2)
            glScalef(1.0, 0.5, 1.5)
            glutSolidCube(0.6)
            
        glPopMatrix()

    def update_animation(self):
        """Calcula los ángulos de las articulaciones frame por frame"""
        self.anim_time += 0.02 # Extremadamente Lento para que las piernas no parezcan correr

        if self.current_action == "IDLE":
            # --- CORRECCIÓN DE BUG: Saiba deja de temblar ---
            # Brazos relajados a los costados
            self.arm_r_pitch = 0.0
            self.arm_l_pitch = 0.0
            
            # Piernas y cuerpo estáticos en el suelo
            self.leg_r_pitch = 0.0
            self.leg_l_pitch = 0.0
            self.body_y_offset = 0.0
            self.body_pitch = 0.0

        elif self.current_action == "CAMINAR":
            # Braceo y zancada más lentos
            self.arm_r_pitch = math.sin(self.anim_time * 0.6) * 45
            self.arm_l_pitch = math.sin(self.anim_time * 0.6 + 3.14) * 45
            self.leg_l_pitch = math.sin(self.anim_time * 0.6) * 45
            self.leg_r_pitch = math.sin(self.anim_time * 0.6 + 3.14) * 45
            self.body_y_offset = abs(math.sin(self.anim_time * 1.2)) * 0.2 # Pequeño rebote al caminar
            self.body_pitch = 0.0 # Reset postura

        elif self.current_action == "SALTAR":
            # Usamos seno para una parábola de salto
            salto = math.sin(self.anim_time * 2.0)
            if salto > 0:
                self.body_y_offset = salto * 2.0
                self.arm_r_pitch = -150 # Levanta brazos
                self.arm_l_pitch = -150
                self.leg_r_pitch = 20   # Dobla piernas hacia atrás
                self.leg_l_pitch = 20
            else:
                self.current_action = "IDLE" # Termina el salto

        elif self.current_action == "AGACHARSE":
            self.body_y_offset = -0.8
            self.body_pitch = 30 # Inclina el torso
            self.arm_r_pitch = -40
            self.arm_l_pitch = -40
            self.leg_r_pitch = -60
            self.leg_l_pitch = -60

        elif self.current_action == "PICAR":
            # 1. Pose de stance (Piernas firmes y separadas)
            self.leg_r_pitch = -10.0; self.leg_l_pitch = 10.0
            
            # 2. Inclinación del cuerpo hacia la mesa (muy importante)
            self.body_pitch = 45.0
            self.body_y_offset = -0.6 # Baja el centro de gravedad
            
            # 3. Brazo Izquierdo: Sosteniendo la comida firme sobre la mesa
            self.arm_l_pitch = -60.0 # Cerca del pecho, codo doblado
            
            # 4. Brazo Derecho (Cuchillo): MOVIMIENTO SÚPER RÁPIDO (SINUSOIDAL)
            # Frecuencia rápida (*8.0) y amplitud alta (*35)
            self.arm_r_pitch = -70.0 + math.sin(self.anim_time * 8.0) * 35.0

        elif self.current_action == "SALTEAR":
            # 1. Pose de balanceo
            self.leg_r_pitch = 5.0; self.leg_l_pitch = -5.0
            self.body_pitch = 20.0 # Menor inclinación
            
            # 2. Balanceo del torso suave (adelante/atrás)
            self.body_y_offset = -0.3 + math.sin(self.anim_time * 4.0) * 0.2
            
            # 3. Brazos Sincronizados (Thrusting): Ambos brazos sostienen el sartén
            thrust = math.sin(self.anim_time * 4.0) * 15.0
            self.arm_r_pitch = -80.0 + thrust
            self.arm_l_pitch = -80.0 + thrust # Brazo izquierdo ayuda a sostener/saltear

        elif self.current_action == "BANDANA":
            # La pose épica: Levanta la mano a la frente
            self.arm_r_pitch = -160 # Brazo arriba tocando la cabeza
            self.arm_l_pitch = 0
            self.body_pitch = 0.0
            self.body_y_offset = 0.0
            self.leg_r_pitch = 0.0
            self.leg_l_pitch = 0.0
            
        elif self.current_action == "SALUDAR":
            # Brazo derecho arriba moviéndose
            self.arm_r_pitch = -150 + math.sin(self.anim_time * 2.0) * 20
            self.arm_l_pitch = 0
            self.body_pitch = 0.0
            self.body_y_offset = 0.0
            self.leg_r_pitch = 0.0
            self.leg_l_pitch = 0.0

    # --- NUEVOS MÉTODOS DE CONTROLES DEL JUGADOR ---
    def check_collision(self, next_x, next_z, colliders):
        """Revisa si la siguiente posición invade algún hitbox del mapa"""
        radio_chef = 1.5 # El grosor de Saiba
        
        for obs in colliders:
            dx = next_x - obs['x']
            dz = next_z - obs['z']
            distancia = math.sqrt(dx**2 + dz**2)
            
            # Si la distancia entre centros es menor a la suma de los radios = CHOQUE
            if distancia < (radio_chef + obs['radius']):
                return True
        return False

    def interactuar(self, colliders):
        """Revisa si hay una estación interactiva cerca y activa la animación"""
        radio_interaccion = 2.5 # Un poco más grande que el radio físico para no tener que estar embarrado
        
        for obs in colliders:
            dx = self.pos_x - obs['x']
            dz = self.pos_z - obs['z']
            distancia = math.sqrt(dx**2 + dz**2)
            
            # Si estamos lo suficientemente cerca y NO es un muro
            if distancia < (radio_interaccion + obs['radius']) and obs.get('type', 'MURO') != 'MURO':
                print(f"¡Cocinando en estación: {obs['type']}!")
                self.current_action = obs['type'] # 'PICAR', 'SALTEAR' o 'BANDANA'
                self.anim_time = 0.0 # Reiniciamos la animación
                return True
                
        print("Saiba: No hay nada con qué interactuar aquí...")
        return False

    def mover_adelante(self, speed=0.5, colliders=None):
        if colliders is None: colliders = []
        self.visual_rot_y = 0.0 # El cuerpo mira al frente
        rad = math.radians(self.rot_y)
        next_x = self.pos_x + math.sin(rad) * speed
        next_z = self.pos_z + math.cos(rad) * speed
        if not self.check_collision(next_x, next_z, colliders):
            self.pos_x = next_x
            self.pos_z = next_z
        self.current_action = "CAMINAR"

    def mover_atras(self, speed=0.5, colliders=None):
        if colliders is None: colliders = []
        self.visual_rot_y = 180.0 # El cuerpo voltea hacia atrás
        rad = math.radians(self.rot_y)
        next_x = self.pos_x - math.sin(rad) * speed
        next_z = self.pos_z - math.cos(rad) * speed
        if not self.check_collision(next_x, next_z, colliders):
            self.pos_x = next_x
            self.pos_z = next_z
        self.current_action = "CAMINAR"

    def rotar_izquierda(self, angle=5.0):
        self.rot_y -= angle

    def rotar_derecha(self, angle=5.0):
        self.rot_y += angle

    # --- MÉTODOS STRAFING PURO (Independientes a la Cámara) ---
    def mover_izquierda(self, speed=0.5, colliders=None):
        if colliders is None: colliders = []
        self.visual_rot_y = 90.0 # El cuerpo voltea a la izquierda sin girar la cámara
        rad = math.radians(self.rot_y)
        next_x = self.pos_x + math.cos(rad) * speed
        next_z = self.pos_z - math.sin(rad) * speed
        if not self.check_collision(next_x, next_z, colliders):
            self.pos_x = next_x
            self.pos_z = next_z
        self.current_action = "CAMINAR"

    def mover_derecha(self, speed=0.5, colliders=None):
        if colliders is None: colliders = []
        self.visual_rot_y = -90.0 # El cuerpo voltea a la derecha sin girar la cámara
        rad = math.radians(self.rot_y)
        next_x = self.pos_x - math.cos(rad) * speed
        next_z = self.pos_z + math.sin(rad) * speed
        if not self.check_collision(next_x, next_z, colliders):
            self.pos_x = next_x
            self.pos_z = next_z
        self.current_action = "CAMINAR"

    def draw_props(self):
        """Dibuja los props (Cuchillo, Sartén) según la acción actual"""
        
        # --- PROPS PARA PICAR (Mano Derecha) ---
        if self.current_action == "PICAR":
            glPushMatrix()
            # Navegar a la ubicación de la mano derecha (ensamblada en draw_limb)
            glTranslatef(1.2, 1.3 + self.body_y_offset, 0.0) # Hombro
            glRotatef(self.arm_r_pitch, 1.0, 0.0, 0.0) # Articulación
            glTranslatef(0.0, -1.6, 0.0) # Mano
            
            # Dibujar Cuchillo Geométrico
            glColor3f(0.8, 0.8, 0.8) # Acero
            glPushMatrix()
            # Hoja (Rectángulo escalado)
            glScalef(0.1, 1.0, 0.6) 
            glutSolidCube(1.0)
            glPopMatrix()
            # Mango (Cubo negro)
            glColor3f(0.1, 0.1, 0.1)
            glPushMatrix()
            glTranslatef(0.0, 0.6, 0.0)
            glScalef(1.2, 0.4, 0.8)
            glutSolidCube(1.0)
            glPopMatrix()
            glPopMatrix()

        # --- PROPS PARA SALTEAR (Mano Derecha - Sartén) ---
        elif self.current_action == "SALTEAR":
            glPushMatrix()
            # Navegar a la mano derecha
            glTranslatef(1.2, 1.3 + self.body_y_offset, 0.0)
            glRotatef(self.arm_r_pitch, 1.0, 0.0, 0.0)
            glTranslatef(0.0, -1.6, 0.0)
            
            # Rotar prop para que se sostenga natural
            glRotatef(90, 1.0, 0.0, 0.0)
            
            # Dibujar Sartén (Cilindro plano y Mango)
            glColor3f(0.05, 0.05, 0.05) # Negro industrial
            # Cuerpo sartén
            glutSolidTorus(0.1, 1.0, 16, 32) # Borde
            glPushMatrix()
            glTranslatef(0.0, 0.0, -0.2)
            gluCylinder(self.quadric, 1.0, 1.0, 0.4, 32, 1) # Fondo simulado
            glPopMatrix()
            
            # Mango (Cilindro extended)
            glTranslatef(1.0, 0.0, 0.0)
            glRotatef(90, 0.0, 1.0, 0.0)
            gluCylinder(self.quadric, 0.1, 0.1, 2.0, 8, 1)
            glPopMatrix()


# === WRAPPER PARA EL MENÚ DE SELECCIÓN ===
_chef_instance = None

def draw_neutral():
    global _chef_instance
    if _chef_instance is None:
        _chef_instance = ChefSaiba()
        # Ajustes iniciales para la vitrina
        _chef_instance.pos_z = 0.0   # Quitar el offset de 8.0 del juego original
        _chef_instance.rot_y = 180.0 # Que mire a la cámara
        _chef_instance.current_action = "IDLE"
        
    _chef_instance.draw()
