# main.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import os
import math
import random
import pygame

from estados.game_state import GameState

def ruta_absoluta(ruta_relativa):
    """Obtiene la ruta absoluta correcta para el .exe"""
    try:
        # PyInstaller crea una carpeta temporal _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no estamos en el .exe, usa la ruta de este archivo
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, ruta_relativa)

try:
    import personajes.ajolote as ajolote
    import personajes.chef as chef
    import personajes.knuckles as knuckles
    import personajes.mapache as mapache
    import personajes.pinguino as pinguino
    import personajes.robot as robot
    from personajes.manager import manager
    from sonidos.sound_manager import sound_manager
except ImportError as e:
    print(f"Advertencia al importar: {e}")


estado = GameState()

# === DATOS DE ESTRELLAS PARA PANTALLA DE TÍTULO ===
random.seed(42)  # Semilla fija para que siempre se vean igual
title_stars = []
for _ in range(150):
    title_stars.append({
        "x": random.uniform(0, 1),    # Posición normalizada (0-1)
        "y": random.uniform(0, 1),
        "speed": random.uniform(0.02, 0.12),  # Velocidad de movimiento
        "size": random.uniform(1.0, 3.5),      # Tamaño del punto
        "brightness": random.uniform(0.3, 1.0) # Brillo
    })

# =====================================================================
# 🛠️ PANEL MAESTRO DE AJUSTES 🛠️
# =====================================================================
ESCALAS = {
    0: (1.5, 1.5, 1.5),     # Ajolote
    1: (0.6, 0.45, 0.6),    # Chef 
    2: (0.9, 0.75, 0.9),    # Knuckles
    3: (1.5, 1.5, 1.5),     # Mapache
    4: (1.5, 1.5, 1.5),     # Pinguino
    5: (1.5, 1.5, 1.5)      # Robot
}

ALTURAS = {
    0: -0.5,  # Lumi el Ajolote (Restaurado para el inicio)
    1: -1.7,  # Chef 
    2: -0.3,  # Knuckles
    3: -0.9,  # Mapache
    4: -0.9,  # Pinguino
    5: -1.2   # Robot
}

ROTACIONES_Y = {
    0: 0.0,   
    1: 180.0, 
    2: 0.0,   
    3: 0.0,   
    4: 0.0,   
    5: 0.0    
}

INFO_PERSONAJES = {
    0: ["Lumi el Ajolote", "Acuatico / Curacion", "Mascota Tierna", "W,A,S,D: Movimiento", "1-5: Expresiones Faciales"],
    1: ["Chef Soma", "Fuego / Cocina", "Humano Agil", "W,A,S,D: Mover en cocina", "E: Cocinar / X: Expresion"],
    2: ["Knuckles", "Fuerza / Tierra", "Guerrero Echidna", "Z,X: Caminar y Saltar", "B: Golpear / C: Brazos arriba"],
    3: ["Miko el Mapache", "Agilidad / Bosque", "Bailarin Experto", "Flechas: Caminar", "Z,X,C: Acciones / 1-7: Caras"],
    4: ["Pinguino Bebe", "Hielo / Nieve", "Resistencia Fria", "W: Caminar / J: Saltar", "S: Temblar / Y,T,U: Caras"],
    5: ["Robot Espacial", "Metal / Energia", "Explorador", "W: Caminar / J: Saltar", "E,X: Mover brazos / Saludar"]
}
# =====================================================================

# Offset específico para que los personajes no se hundan en el podio
PODIO_OFFSETS = {
    0: 0.7,   # Lumi el Ajolote
    1: 0.0,   # Chef
    2: 0.8,   # Knuckles
    3: 0.4,   # Mapache
    4: 0.4,   # Pinguino
    5: 0.0    # Robot
}

def init():
    glClearColor(0.02, 0.02, 0.05, 1.0) # Fondo ligeramente más azulado/oscuro
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 5.0, 10.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

def dibujar_modelo(indice):
    """Dibuja el modelo del personaje usando los wrappers neutrales de cada módulo."""
    try:
        if indice == 0: ajolote.draw_axolotl_full(ajolote.state)
        elif indice == 1: chef.get_chef().draw()
        elif indice == 2: 
            # Dibujar a Knuckles con animación de golpes y caminata
            p = manager.knuckles_anim["punch"]
            wc = manager.knuckles_anim["walk_cycle"]
            rot_b = math.sin(p) * 60 if p > 0 else 0
            rot_p = math.sin(wc) * 30
            knuckles.draw_knuckles_full(
                rot_brazo_i=rot_b, rot_brazo_d=-rot_b, 
                rot_pierna_i=rot_p, rot_pierna_d=-rot_p,
                expresion=manager.knuckles_anim["expresion"]
            )
        elif indice == 3: mapache.draw_miko(mapache.state)
        elif indice == 4: pinguino.draw_penguin_full()
        elif indice == 5: robot.draw_robot_full()
    except Exception as e:
        print(f"Error dibujando personaje {indice}: {e}")
        glutSolidTeapot(1.0)

def dibujar_personaje_vs(indice, x, rotacion_y, animacion_ataque):
    """Dibuja al personaje en la pantalla VS con postura de combate"""
    glPushMatrix()
    glTranslatef(x, ALTURAS[indice], 0.0)
    # Gira para verse frente a frente, más su rotación base
    glRotatef(rotacion_y + ROTACIONES_Y[indice], 0, 1, 0)
    
    # Pequeño balanceo suave (sin el empuje loco de antes)
    glTranslatef(0, 0, animacion_ataque) 
    
    sx, sy, sz = ESCALAS[indice]
    # Los hacemos un 50% más grandes para la pantalla VS
    glScalef(sx * 1.5, sy * 1.5, sz * 1.5) 
    
    glEnable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)
    dibujar_modelo(indice)
    glPopMatrix()

def dibujar_personaje(indice, tipo_vista, x, z):
    glPushMatrix()
    glTranslatef(x, 0.0, z)

    if tipo_vista == "centro":
        # 1. PLATAFORMA NEON
        glPushMatrix()
        glColor3f(0.0, 0.8, 1.0) 
        glTranslatef(0, -2.0, 0) 
        glScalef(3.5, 0.2, 3.5)
        glutSolidCube(1.0)
        glPopMatrix()

        # 2. ANIMACIÓN DE ENTRADA
        if estado.tiempo_seleccion <= 1.0:
            progreso = estado.tiempo_seleccion
            salto = math.sin(progreso * math.pi) * 2.5
            giro_animacion = progreso * 360
        else:
            salto = 0.0 
            giro_animacion = 0.0

        glTranslatef(0, salto, 0)
        glRotatef(giro_animacion, 0, 1, 0)

        # 3. ILUMINACIÓN Y COLOR FULL
        glEnable(GL_LIGHTING)
        glTranslatef(0, ALTURAS[indice], 0)
        glRotatef(ROTACIONES_Y[indice], 0, 1, 0)
        
        sx, sy, sz = ESCALAS[indice]
        glScalef(sx, sy, sz)

        glColor3f(1.0, 1.0, 1.0)
        # El ajolote necesita lighting OFF para su look Minecraft plano
        if indice == 0:
            glDisable(GL_LIGHTING)
        dibujar_modelo(indice)
        if indice == 0:
            glEnable(GL_LIGHTING)

    else:
        # 4. MODO SILUETA: Lighting ON pero luz a CERO + COLOR_MATERIAL OFF
        #    Así los glColor3f internos de cada módulo NO afectan el resultado.
        glDisable(GL_COLOR_MATERIAL)  # glColor ya no cambia materiales
        
        # Guardar luz original y poner todo a negro
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
        
        # Material: todo negro con emisión mínima para ver la forma
        negro = [0.0, 0.0, 0.0, 1.0]
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, negro)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, negro)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, negro)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.04, 0.04, 0.08, 1.0])
        
        glPushMatrix()
        glTranslatef(0, -1.5 + ALTURAS[indice], 0) 
        glRotatef(ROTACIONES_Y[indice], 0, 1, 0)
        
        sx, sy, sz = ESCALAS[indice]
        glScalef(sx * 0.7, sy * 0.7, sz * 0.7)
        
        glColor3f(0.03, 0.03, 0.06)
        dibujar_modelo(indice)
        glPopMatrix()
        
        # Restaurar luz y estado OpenGL
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_LIGHTING)

    glPopMatrix()

def draw_arrow_keys(cx, cy):
    """Dibuja 4 teclas de flechas como iconos en 2D"""
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w_win, 0, h_win)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    s = 20  # Tamaño de cada tecla
    gap = 4  # Espacio entre teclas
    
    # Posiciones: arriba-centro, izq-abajo, centro-abajo, der-abajo
    keys = [
        (cx + s + gap, cy + s + gap, "up"),
        (cx,           cy,           "left"),
        (cx + s + gap, cy,           "down"),
        (cx + (s + gap) * 2, cy,     "right"),
    ]
    
    for kx, ky, direction in keys:
        # Fondo de la tecla
        glColor3f(0.15, 0.15, 0.25)
        glBegin(GL_QUADS)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Borde de la tecla
        glColor3f(0.4, 0.7, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Flecha (triángulo grande y visible)
        mx = kx + s / 2
        my = ky + s / 2
        a = 6
        
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        if direction == "up":
            glVertex2f(mx, my + a)
            glVertex2f(mx - a, my - a)
            glVertex2f(mx + a, my - a)
        elif direction == "down":
            glVertex2f(mx, my - a)
            glVertex2f(mx - a, my + a)
            glVertex2f(mx + a, my + a)
        elif direction == "left":
            glVertex2f(mx - a, my)
            glVertex2f(mx + a, my + a)
            glVertex2f(mx + a, my - a)
        elif direction == "right":
            glVertex2f(mx + a, my)
            glVertex2f(mx - a, my + a)
            glVertex2f(mx - a, my - a)
        glEnd()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_wasd_keys(cx, cy):
    """Dibuja 4 teclas WASD como iconos en 2D"""
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w_win, 0, h_win)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    s = 20  # Tamaño de cada tecla
    gap = 4  # Espacio entre teclas
    
    # Posiciones: W arriba-centro, A izq-abajo, S centro-abajo, D der-abajo
    keys = [
        (cx + s + gap, cy + s + gap, "W"),
        (cx,           cy,           "A"),
        (cx + s + gap, cy,           "S"),
        (cx + (s + gap) * 2, cy,     "D"),
    ]
    
    for kx, ky, letra in keys:
        # Fondo de la tecla
        glColor3f(0.15, 0.15, 0.25)
        glBegin(GL_QUADS)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Borde de la tecla
        glColor3f(0.2, 1.0, 0.4)
        glBegin(GL_LINE_LOOP)
        glVertex2f(kx, ky)
        glVertex2f(kx + s, ky)
        glVertex2f(kx + s, ky + s)
        glVertex2f(kx, ky + s)
        glEnd()
        
        # Letra centrada dentro de la tecla
        glColor3f(1.0, 1.0, 1.0)
        letra_w = glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(letra))
        lx = kx + (s - letra_w) / 2
        ly = ky + (s - 14) / 2  # 14 aprox alto de Helvetica 18
        glRasterPos2f(lx, ly)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(letra))
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    glEnable(GL_LIGHTING)

def draw_text_centered(y, text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    """Dibuja texto centrado horizontalmente de forma automática"""
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w_win, 0, h_win)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Ancho real del texto sumando cada carácter
    ancho_real = sum(glutBitmapWidth(font, ord(c)) for c in text)
    x = (w_win - ancho_real) / 2
    
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
        
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_LIGHTING)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w_win = glutGet(GLUT_WINDOW_WIDTH)
    h_win = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w_win, 0, h_win)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_LIGHTING)

def dibujar_forma_objeto(forma, r, g, b, t=0):
    """Centraliza el dibujo de formas para el nivel 1 e intro con mejores diseños"""
    glColor3f(r, g, b)
    if forma == "esfera":
        # Fruta (Manzana/Naranja) con ramita y hoja
        glutSolidSphere(0.5, 16, 16)
        glColor3f(0.4, 0.2, 0.1) # Rama
        glPushMatrix(); glTranslatef(0, 0.5, 0); glScalef(0.05, 0.2, 0.05); glutSolidCube(1.0); glPopMatrix()
        glColor3f(0.2, 0.8, 0.2) # Hoja
        glPushMatrix(); glTranslatef(0.1, 0.55, 0); glRotatef(45, 0, 0, 1); glScalef(0.2, 0.05, 0.1); glutSolidCube(1.0); glPopMatrix()
    elif forma == "cubo":
        # Cubo con bordes (tipo dado o bloque)
        glRotatef(45, 1, 1, 0)
        glutSolidCube(0.8)
        glColor3f(r*0.8, g*0.8, b*0.8)
        glutWireCube(0.81)
    elif forma == "dona":
        # Dona con "chispas" (pequeñas esferas)
        glRotatef(90, 1, 0, 0)
        glutSolidTorus(0.15, 0.35, 12, 16)
        glColor3f(1, 1, 1)
        for i in range(5):
            glPushMatrix()
            glRotatef(i * 72, 0, 0, 1)
            glTranslatef(0.35, 0, 0.1)
            glutSolidSphere(0.05, 6, 6)
            glPopMatrix()
    elif forma == "diamante":
        # Diamante tallado (Octaedro con brillo)
        glPushMatrix()
        glRotatef(t * 100, 0, 1, 0)
        glScalef(0.6, 0.9, 0.6)
        glutSolidSphere(0.6, 4, 2)
        # Brillo
        if (t * 2) % 1 > 0.8:
            glColor3f(1, 1, 1)
            glPushMatrix(); glTranslatef(0.2, 0.2, 0.2); glutSolidSphere(0.1, 8, 8); glPopMatrix()
        glPopMatrix()
    elif forma == "platano":
        # Platano: Cuerpo curvo con grosor variable
        glPushMatrix()
        glRotatef(-45, 0, 0, 1) # Inclinación natural
        # Dibujamos el platano con varios segmentos para la curva
        for i in range(6):
            glPushMatrix()
            # Posición curva
            angle = i * 0.4
            tx = math.sin(angle) * 0.6
            ty = i * 0.25 - 0.7
            glTranslatef(tx, ty, 0)
            # Rotación para seguir la curva
            glRotatef(i * 15, 0, 0, 1)
            # El primero y el último son las puntas (negras/cafés)
            if i == 0 or i == 5:
                glColor3f(0.2, 0.1, 0.0)
                glScalef(0.2, 0.2, 0.2)
            else:
                glColor3f(r, g, b)
                # El centro es más grueso
                grosor = 0.35 if (1 < i < 4) else 0.25
                glScalef(grosor, 0.3, grosor)
            glutSolidCube(1.0)
            glPopMatrix()
        glPopMatrix()
    elif forma == "estrella":
        # Estrella de 5 puntas mejorada (Cono central + 5 picos)
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        for i in range(5):
            glPushMatrix()
            glRotatef(i * 72, 0, 1, 0)
            glTranslatef(0, 0, 0.3)
            # Pirámide para el pico
            glRotatef(-90, 1, 0, 0)
            glutSolidCone(0.2, 0.5, 4, 1)
            glPopMatrix()
        # Centro
        glutSolidSphere(0.25, 10, 10)
        glPopMatrix()
    elif forma == "corazon":
        # Corazón "Puffy" (Gordito y tierno para niños)
        glPushMatrix()
        glScalef(0.8, 0.8, 0.8)
        # Color base rosado/rojo vibrante
        glColor3f(r, g, b)
        # Lóbulo izquierdo
        glPushMatrix()
        glTranslatef(-0.28, 0.2, 0)
        glScalef(1.0, 1.1, 0.9)
        glutSolidSphere(0.48, 24, 24)
        glPopMatrix()
        # Lóbulo derecho
        glPushMatrix()
        glTranslatef(0.28, 0.2, 0)
        glScalef(1.0, 1.1, 0.9)
        glutSolidSphere(0.48, 24, 24)
        glPopMatrix()
        # Relleno central (para evitar el hueco)
        glPushMatrix()
        glTranslatef(0, 0.1, 0)
        glutSolidSphere(0.45, 24, 24)
        glPopMatrix()
        # Punta inferior redondeada (una esfera estirada hacia abajo)
        glPushMatrix()
        glTranslatef(0, -0.25, 0)
        glScalef(0.8, 1.2, 0.8)
        glRotatef(45, 0, 0, 1)
        glutSolidCube(0.65)
        glPopMatrix()
        # Brillo tipo emoji (gota blanca)
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glTranslatef(0.25, 0.4, 0.3)
        glutSolidSphere(0.12, 10, 10)
        glPopMatrix()
        glEnable(GL_LIGHTING)
        glPopMatrix()
    elif forma == "zapato":
        # Zapato: Suela + cuerpo + agujeros/cordones
        glPushMatrix()
        glScalef(1.1, 1.1, 1.1)
        # Suela (negra/café oscura)
        glColor3f(0.2, 0.1, 0.0)
        glPushMatrix(); glTranslatef(0, -0.2, 0); glScalef(0.9, 0.15, 0.45); glutSolidCube(1.0); glPopMatrix()
        # Cuerpo del zapato (color del objeto)
        glColor3f(r, g, b)
        # Parte trasera (talón)
        glPushMatrix(); glTranslatef(-0.25, 0.05, 0); glScalef(0.4, 0.4, 0.4); glutSolidCube(1.0); glPopMatrix()
        # Parte delantera (punta)
        glPushMatrix(); glTranslatef(0.15, -0.05, 0); glScalef(0.6, 0.3, 0.4); glutSolidCube(1.0); glPopMatrix()
        # Lengüeta / Cordones (blancos)
        glColor3f(1, 1, 1)
        glPushMatrix(); glTranslatef(0.0, 0.1, 0); glScalef(0.2, 0.05, 0.3); glutSolidCube(1.0); glPopMatrix()
        glPopMatrix()
    elif forma == "moneda":
        # Moneda: Disco sólido con símbolo
        glPushMatrix()
        glRotatef(t * 60, 0, 1, 0)
        # Cuerpo principal (Cilindro simulado con esfera súper aplastada)
        glColor3f(r, g, b)
        glPushMatrix()
        glScalef(0.9, 0.9, 0.1)
        glutSolidSphere(0.5, 24, 24)
        glPopMatrix()
        # Símbolo '$' en blanco
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix(); glTranslatef(0, 0, 0.06); glScalef(0.1, 0.4, 0.05); glutSolidCube(1.0); glPopMatrix()
        glPushMatrix(); glTranslatef(0, 0.1, 0.06); glScalef(0.3, 0.08, 0.05); glutSolidCube(1.0); glPopMatrix()
        glPushMatrix(); glTranslatef(0, -0.1, 0.06); glScalef(0.3, 0.08, 0.05); glutSolidCube(1.0); glPopMatrix()
        glEnable(GL_LIGHTING)
        glPopMatrix()

def draw_ingredient_model(tipo, estado_ing):
    """Dibuja el modelo 3D del ingrediente según su tipo y si está picado o no"""
    t = estado.tiempo_global
    if tipo == "Jitomate": 
        # Jitomate: Esfera roja con rabo verde
        glColor3f(1.0, 0.0, 0.0)
        if estado_ing == "crudo":
            glPushMatrix()
            glRotatef(t * 50, 0, 1, 0)
            glutSolidSphere(0.6, 16, 16)
            # Rabito verde
            glColor3f(0.0, 0.6, 0.0)
            glTranslatef(0, 0.5, 0)
            glPushMatrix(); glScalef(0.1, 0.3, 0.1); glutSolidCube(1.0); glPopMatrix()
            # Hojitas
            for i in range(4):
                glPushMatrix()
                glRotatef(i * 90, 0, 1, 0)
                glTranslatef(0.15, 0, 0)
                glScalef(0.3, 0.05, 0.1)
                glutSolidCube(1.0)
                glPopMatrix()
            glPopMatrix()
        else:
            # Picado: Cubitos rojos
            glColor3f(0.8, 0.0, 0.0)
            for offset in [(-0.2, 0, -0.2), (0.2, 0.1, 0.2), (0.1, -0.1, 0)]:
                glPushMatrix(); glTranslatef(*offset); glutSolidCube(0.4); glPopMatrix()

    elif tipo == "Lechuga": 
        # Lechuga: Racimo de esferas verdes
        if estado_ing == "crudo":
            glPushMatrix()
            glRotatef(t * 40, 0, 1, 0)
            for i in range(5):
                glColor3f(0.2, 0.8 + (i*0.05), 0.1)
                glPushMatrix()
                glRotatef(i * 72, 0, 1, 0)
                glTranslatef(0.2, 0, 0)
                glutSolidSphere(0.45, 12, 12)
                glPopMatrix()
            # Centro
            glColor3f(0.4, 0.9, 0.2)
            glutSolidSphere(0.5, 12, 12)
            glPopMatrix()
        else:
            # Picado: Hojitas verdes (planos)
            glColor3f(0.3, 0.8, 0.2)
            for i in range(4):
                glPushMatrix()
                glTranslatef(random.uniform(-0.3, 0.3), 0, random.uniform(-0.3, 0.3))
                glScalef(0.4, 0.05, 0.4)
                glutSolidCube(1.0)
                glPopMatrix()

    elif tipo == "Queso": 
        # Queso: Triángulo amarillo con agujeros
        glColor3f(1.0, 0.9, 0.0)
        if estado_ing == "crudo":
            glPushMatrix()
            glRotatef(t * 60, 0, 1, 0)
            # Cuerpo principal (prisma triangular simulado con pirámide truncada)
            glPushMatrix()
            glScalef(1.0, 0.6, 1.0)
            glutSolidSphere(0.6, 4, 2) # Diamante de 4 lados plano
            glPopMatrix()
            # Agujeros negros
            glColor3f(0.2, 0.1, 0.0)
            for pos in [(0.3, 0.1, 0.2), (-0.2, -0.1, 0.3), (0.1, 0.2, -0.3)]:
                glPushMatrix(); glTranslatef(*pos); glutSolidSphere(0.1, 8, 8); glPopMatrix()
            glPopMatrix()
        else:
            # Picado: Cubos amarillos
            for offset in [(-0.2, 0, -0.2), (0.2, 0, 0.2)]:
                glPushMatrix(); glTranslatef(*offset); glutSolidCube(0.4); glPopMatrix()

    elif tipo == "Pollo": 
        # Pollo
        if estado_ing == "crudo":
            glColor3f(1.0, 0.8, 0.0)
            glPushMatrix()
            glRotatef(t * 50, 0, 1, 0)
            glPushMatrix(); glScalef(0.7, 0.6, 0.8); glutSolidCube(1.0); glPopMatrix()
            glPushMatrix(); glTranslatef(0, 0.4, 0.4); glScalef(0.4, 0.4, 0.4); glutSolidCube(1.0)
            glColor3f(1, 0, 0); glPushMatrix(); glTranslatef(0, 0.6, 0); glScalef(0.2, 0.5, 0.5); glutSolidCube(1.0); glPopMatrix()
            glColor3f(1, 0.5, 0); glPushMatrix(); glTranslatef(0, -0.2, 0.6); glScalef(0.4, 0.2, 0.4); glutSolidCube(1.0); glPopMatrix()
            glPopMatrix()
            glColor3f(1.0, 0.8, 0.0)
            glPushMatrix(); glTranslatef(0.4, 0, 0); glScalef(0.1, 0.3, 0.5); glutSolidCube(1.0); glPopMatrix()
            glPushMatrix(); glTranslatef(-0.4, 0, 0); glScalef(0.1, 0.3, 0.5); glutSolidCube(1.0); glPopMatrix()
            glColor3f(1, 0.5, 0)
            glPushMatrix(); glTranslatef(0.2, -0.4, 0); glScalef(0.1, 0.4, 0.1); glutSolidCube(1.0); glPopMatrix()
            glPushMatrix(); glTranslatef(-0.2, -0.4, 0); glScalef(0.1, 0.4, 0.1); glutSolidCube(1.0); glPopMatrix()
            glPopMatrix()
        else:
            glColor3f(0.6, 0.4, 0.2)
            for offset in [(-0.2, 0, 0), (0.2, 0, 0)]:
                glPushMatrix(); glTranslatef(*offset); glutSolidCube(0.4); glPopMatrix()

    elif tipo == "Vaca":
        if estado_ing == "crudo":
            glPushMatrix()
            glRotatef(t * 40, 0, 1, 0)
            # Cuerpo
            glPushMatrix()
            glScalef(0.8, 0.7, 1.2); glColor3f(1, 1, 1); glutSolidCube(1.0); glPopMatrix()
            # Manchas
            glColor3f(0.1, 0.1, 0.1)
            for spot in [(0.4, 0.4, 0.4), (-0.4, 0.2, -0.5), (0.3, -0.3, 0.1)]:
                glPushMatrix(); glTranslatef(*spot); glutSolidSphere(0.2, 8, 8); glPopMatrix()
            # Cabeza
            glColor3f(1, 1, 1)
            glPushMatrix()
            glTranslatef(0, 0.3, 0.6)
            glPushMatrix(); glScalef(0.5, 0.5, 0.5); glutSolidCube(1.0); glPopMatrix()
            # Hocico rosado
            glColor3f(1, 0.7, 0.7)
            glPushMatrix(); glTranslatef(0, -0.15, 0.3); glScalef(0.4, 0.3, 0.25); glutSolidCube(1.0); glPopMatrix()
            glPopMatrix()
            glPopMatrix()
        else:
            glColor3f(0.6, 0.3, 0.1)
            for offset in [(-0.2, 0, 0), (0.2, 0, 0)]:
                glPushMatrix(); glTranslatef(*offset); glutSolidCube(0.4); glPopMatrix()

    elif tipo == "Leche":
        # Botella
        glPushMatrix()
        if estado_ing == "crudo": glRotatef(t * 60, 0, 1, 0)
        glColor3f(0.9, 0.9, 1.0)
        glPushMatrix(); glScalef(0.4, 0.7, 0.4); glutSolidCube(1.0); glPopMatrix()
        glPushMatrix(); glTranslatef(0, 0.45, 0); glScalef(0.2, 0.2, 0.2); glutSolidCube(1.0); glPopMatrix()
        glColor3f(0.2, 0.4, 0.8); glPushMatrix(); glTranslatef(0, 0.55, 0); glScalef(0.22, 0.1, 0.22); glutSolidCube(1.0); glPopMatrix()
        glPopMatrix()

def draw_fence():
    """Dibuja una cerca de madera para delimitar la granja con un hueco para pasar"""
    glColor3f(0.4, 0.2, 0.1) # Café madera
    # Postes horizontales (Hueco de -3 a 3)
    for y in [0.5, 1.2]:
        # Parte izquierda
        glPushMatrix()
        glTranslatef(-11.5, y, 5.0)
        glScalef(17.0, 0.2, 0.2)
        glutSolidCube(1.0)
        glPopMatrix()
        # Parte derecha
        glPushMatrix()
        glTranslatef(11.5, y, 5.0)
        glScalef(17.0, 0.2, 0.2)
        glutSolidCube(1.0)
        glPopMatrix()
    # Postes verticales (Hueco de -3 a 3)
    for x in range(-20, 21, 4):
        if -3 < x < 3: continue
        glPushMatrix()
        glTranslatef(x, 0.8, 5.0)
        glScalef(0.4, 1.6, 0.4)
        glutSolidCube(1.0)
        glPopMatrix()

def revisar_musica():
    """Gestiona el cambio de música de fondo según la fase del juego"""
    nueva_musica = ""
    
    if estado.fase_actual == "TITULO":
        nueva_musica = "sonidos/menu.mp3"
    elif estado.fase_actual == "MAPA":
        nueva_musica = "sonidos/game.mp3"
    elif estado.fase_actual == "NIVEL_2":
        nueva_musica = "sonidos/race.mp3"
    elif estado.fase_actual == "NIVEL_3":
        nueva_musica = "sonidos/cooked.mp3"
    elif estado.fase_actual == "GANADOR":
        nueva_musica = "sonidos/winner.mp3"
    elif estado.fase_actual == "PODIO":
        nueva_musica = "sonidos/podium.mp3"
    elif estado.fase_actual == "RONDA_INTRO":
        nueva_musica = "sonidos/wait.mp3"
    elif estado.fase_actual == "VERSUS":
        nueva_musica = ""
        pygame.mixer.music.stop()
    else:
        # SELECCION, CONFIRMAR, LISTOS
        nueva_musica = "sonidos/selection.mp3"
    
    if nueva_musica != "" and estado.musica_actual != nueva_musica:
        estado.musica_actual = nueva_musica
        try:
            # === ¡AQUÍ ESTÁ EL CAMBIO! ===
            ruta_real = ruta_absoluta(nueva_musica)
            pygame.mixer.music.load(ruta_real)
            pygame.mixer.music.play(-1) 
        except Exception as e:
            print(f"Error al cargar música {nueva_musica}: {e}")

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # --- GESTIÓN DE MÚSICA POR FASE ---
    revisar_musica()

    # --- CONFIGURACIÓN DE CÁMARA SEGÚN FASE ---
    if estado.fase_actual == "VERSUS":
        # Cámara cinematográfica de frente
        gluLookAt(0.0, 3.0, 12.0,   
                  0.0, 1.0, 0.0,    
                  0.0, 1.0, 0.0)
    elif estado.fase_actual == "TITULO":
        draw_start_screen()
    elif estado.fase_actual == "RONDA_INTRO":
        draw_ronda_intro()
    elif estado.fase_actual == "MAPA":
        # La cámara se configura más abajo en el bloque de dibujo
        pass
    elif estado.fase_actual in ["SELECCION_P1", "CONFIRMAR_P1", "SELECCION_P2", "CONFIRMAR_P2", "LISTOS"]:
        gluLookAt(0.0, 1.5, 9.0,   
                  0.0, 0.0, 0.0,    
                  0.0, 1.0, 0.0)    
              
    idx_p1 = estado.cursor_index
    idx_p2 = estado.cursor_index_p2
    
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    if estado.fase_actual in ["SELECCION_P1", "SELECCION_P2"]:
        # === MODO CARRUSEL ===
        if estado.fase_actual == "SELECCION_P1":
            idx_actual = idx_p1
            datos = INFO_PERSONAJES[idx_p1]
        else:
            idx_actual = idx_p2
            datos = INFO_PERSONAJES[idx_p2]
        
        idx_izq = (idx_actual - 1) % 6
        idx_der = (idx_actual + 1) % 6
        
        # Si es P2, saltar el personaje del P1 en las siluetas
        if estado.fase_actual == "SELECCION_P2":
            if idx_izq == estado.jugador1_seleccion:
                idx_izq = (idx_izq - 1) % 6
            if idx_der == estado.jugador1_seleccion:
                idx_der = (idx_der + 1) % 6
        
        dibujar_personaje(idx_izq, "silueta", -6.0, -3.0)
        dibujar_personaje(idx_der, "silueta", 6.0, -3.0)
        dibujar_personaje(idx_actual, "centro", 0.0, 0.0)
        
        # Indicador de turno (¡Súper importante para los niños!)
        if estado.fase_actual == "SELECCION_P1":
            glColor3f(0.0, 1.0, 0.0) # Verde para P1
            draw_text_centered(h - 40, "TURNO DEL JUGADOR 1", GLUT_BITMAP_TIMES_ROMAN_24)
        else:
            glColor3f(1.0, 0.0, 0.0) # Rojo para P2
            draw_text_centered(h - 40, "TURNO DEL JUGADOR 2", GLUT_BITMAP_TIMES_ROMAN_24)

        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 80, f"> {datos[0].upper()} <", GLUT_BITMAP_TIMES_ROMAN_24)
        
        glColor3f(0.7, 0.7, 0.7)
        draw_text_centered(30, "Usa Flechas <- -> para navegar  |  [ENTER] Seleccionar", GLUT_BITMAP_HELVETICA_18)
        
    elif estado.fase_actual in ["CONFIRMAR_P1", "CONFIRMAR_P2"]:
        # === MODO VENTANA DE CONFIRMACIÓN ===
        if estado.fase_actual == "CONFIRMAR_P1":
            idx_actual = idx_p1
            datos = INFO_PERSONAJES[idx_p1]
        else:
            idx_actual = idx_p2
            datos = INFO_PERSONAJES[idx_p2]
        
        dibujar_personaje(idx_actual, "centro", 0.0, 0.0)
        
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h - 60, f"¿ELEGIR A {datos[0].upper()}?", GLUT_BITMAP_TIMES_ROMAN_24)

        glColor3f(0.0, 0.9, 1.0)
        draw_text_centered(h - 130, f"CLASE: {datos[1]}  |  ESTILO: {datos[2]}", GLUT_BITMAP_HELVETICA_18)
        
        glColor3f(1.0, 1.0, 1.0)
        if estado.fase_actual == "CONFIRMAR_P1":
            draw_text_centered(h - 190, "CONTROLES:", GLUT_BITMAP_HELVETICA_18)
            draw_wasd_keys(w // 2 + 50, h - 210)
        else:
            draw_text_centered(h - 190, "CONTROLES:", GLUT_BITMAP_HELVETICA_18)
            draw_arrow_keys(w // 2 + 50, h - 210)

        # Botones dinámicos según de quién sea el turno
        jugador_txt = "JUGADOR 1" if estado.fase_actual == "CONFIRMAR_P1" else "JUGADOR 2"
        glColor3f(0.2, 1.0, 0.2)
        draw_text_centered(100, f"[ ENTER ] CONFIRMAR {jugador_txt}", GLUT_BITMAP_TIMES_ROMAN_24)
        glColor3f(1.0, 0.2, 0.2)
        draw_text_centered(50, "[ ESC ] VOLVER AL MENU", GLUT_BITMAP_HELVETICA_18)

    elif estado.fase_actual == "LISTOS":
        # Mostrar ambos personajes seleccionados
        p1_idx = estado.jugador1_seleccion
        p2_idx = estado.jugador2_seleccion
        
        dibujar_personaje(p1_idx, "centro", -3.0, 0.0)
        dibujar_personaje(p2_idx, "centro", 3.0, 0.0)
        
        glColor3f(0.2, 1.0, 0.2)
        draw_text_centered(h - 100, "¡AMBOS JUGADORES LISTOS!", GLUT_BITMAP_TIMES_ROMAN_24)
        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 150, "Presiona [ ENTER ] para jugar en el mapa", GLUT_BITMAP_HELVETICA_18)
        draw_text_centered(50, "Presiona [ ESC ] para reiniciar", GLUT_BITMAP_HELVETICA_18)

    elif estado.fase_actual == "MAPA":
        # Cámara más alta para ver toda la arena de competencia
        mid_x = (estado.p1_pos[0] + estado.p2_pos[0]) / 2
        mid_z = (estado.p1_pos[2] + estado.p2_pos[2]) / 2
        gluLookAt(mid_x, 15.0, mid_z + 18.0,   
                  mid_x, 0.0, mid_z,    
                  0.0, 1.0, 0.0)
                  
        draw_nivel_1()
        
        # Dibujar Jugador 1
        glPushMatrix()
        glTranslatef(estado.p1_pos[0], estado.p1_pos[1], estado.p1_pos[2])
        glRotatef(estado.p1_rot, 0, 1, 0)
        dibujar_modelo_en_mapa(estado.jugador1_seleccion)
        glPopMatrix()
        
        # Dibujar Jugador 2
        glPushMatrix()
        glTranslatef(estado.p2_pos[0], estado.p2_pos[1], estado.p2_pos[2])
        glRotatef(estado.p2_rot, 0, 1, 0)
        dibujar_modelo_en_mapa(estado.jugador2_seleccion)
        glPopMatrix()

        # ==================== UI DE PUNTAJES ====================
        nombre_obj = estado.n1_tipo_objeto["nombre"] if estado.n1_tipo_objeto else "OBJETOS"
        r_obj, g_obj, b_obj = estado.n1_tipo_objeto["color"] if estado.n1_tipo_objeto else (1,1,1)
        
        # Pregunta con color del objeto
        # Si el objeto es oscuro, lo aclaramos un poco
        brightness = r_obj * 0.3 + g_obj * 0.59 + b_obj * 0.11
        if brightness < 0.4:
            color_pregunta = (1.0, 1.0, 1.0) # Blanco
        else:
            color_pregunta = (r_obj, g_obj, b_obj)
            
        # Texto principal
        glColor3f(*color_pregunta)
        draw_text_centered(h - 35, f"¿CUÁNTOS/AS {nombre_obj} HAY?", GLUT_BITMAP_TIMES_ROMAN_24)
        
        glColor3f(0.0, 1.0, 0.0)
        draw_text_centered(h - 70, f"JUGADOR 1: {estado.p1_score} / {estado.meta_puntos} PTS", GLUT_BITMAP_HELVETICA_18)
        
        glColor3f(1.0, 0.3, 0.3)
        draw_text_centered(h - 95, f"JUGADOR 2: {estado.p2_score} / {estado.meta_puntos} PTS", GLUT_BITMAP_HELVETICA_18)

    elif estado.fase_actual == "NIVEL_2":
        # ==================== SPLIT SCREEN SETUP ====================
        
        # JUGADOR 1 (IZQUIERDA)
        glViewport(0, 0, w // 2, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / 2) / max(h, 1), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        gluLookAt(estado.p1_pos[0], 12.0, estado.p1_pos[2] + 10.0,
                  estado.p1_pos[0], 0.0, estado.p1_pos[2] - 5.0,
                  0.0, 1.0, 0.0)
                  
        draw_nivel_2(estado.n2_pista_p1, estado.n2_pasos_p1)
        
        glPushMatrix()
        glTranslatef(estado.p1_pos[0], estado.p1_pos[1], estado.p1_pos[2])
        glRotatef(estado.p1_rot, 0, 1, 0)
        if estado.p1_stun > 0 and math.sin(estado.tiempo_global * 15) > 0:
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        dibujar_modelo_en_mapa(estado.jugador1_seleccion)
        glPopMatrix()
        
        # JUGADOR 2 (DERECHA)
        glViewport(w // 2, 0, w // 2, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / 2) / max(h, 1), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        gluLookAt(estado.p2_pos[0], 12.0, estado.p2_pos[2] + 10.0,
                  estado.p2_pos[0], 0.0, estado.p2_pos[2] - 5.0,
                  0.0, 1.0, 0.0)
                  
        draw_nivel_2(estado.n2_pista_p2, estado.n2_pasos_p2)
        
        glPushMatrix()
        glTranslatef(estado.p2_pos[0], estado.p2_pos[1], estado.p2_pos[2])
        glRotatef(estado.p2_rot, 0, 1, 0)
        if estado.p2_stun > 0 and math.sin(estado.tiempo_global * 15) > 0:
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        dibujar_modelo_en_mapa(estado.jugador2_seleccion)
        glPopMatrix()

        # ==================== RESTAURAR VIEWPORT Y PROYECCIÓN PARA LA UI ====================
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / max(h, 1), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # LÍNEA SEPARADORA
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, w, 0, h)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        glVertex2f(w // 2, 0)
        glVertex2f(w // 2, h)
        glEnd()
        glLineWidth(1.0)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        # ==================== UI DE LA CARRERA (NIVEL 2) ====================
        # Fondo oscuro semitransparente para la UI
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, w, 0, h)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 1.0) # Barra negra sólida
        glBegin(GL_QUADS)
        glVertex2f(0, h - 120)
        glVertex2f(w, h - 120)
        glVertex2f(w, h)
        glVertex2f(0, h)
        glEnd()
        glDisable(GL_BLEND)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)

        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 40, "¡CARRERA ESCALONADA! CORRE A LA RESPUESTA CORRECTA", GLUT_BITMAP_TIMES_ROMAN_24)
        
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, w, 0, h)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # UI Jugador 1 (Izquierda)
        color_p1 = [1.0, 0.0, 0.0] if estado.p1_stun > 0 else [1.0, 1.0, 1.0] # Blanco si no esta aturdido
        if estado.n2_pasos_p1 < estado.n2_meta_pasos:
            p_p1 = estado.n2_pista_p1[estado.n2_pasos_p1]
            txt_p1 = "¡CONGELADO!" if estado.p1_stun > 0 else f"¿{p_p1['n1']} + {p_p1['n2']}? (Paso {estado.n2_pasos_p1+1}/{estado.n2_meta_pasos})"
        else: txt_p1 = "¡EN LA META!"
        
        ancho_p1 = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in f"J1: {txt_p1}")
        x_p1 = (w // 4) - (ancho_p1 // 2)
        y_p1 = h - 80
        glColor3f(*color_p1)
        glRasterPos2f(x_p1, y_p1)
        for char in f"J1: {txt_p1}": glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
            
        # UI Jugador 2 (Derecha)
        color_p2 = [1.0, 0.0, 0.0] if estado.p2_stun > 0 else [1.0, 1.0, 1.0] # Blanco si no esta aturdido
        if estado.n2_pasos_p2 < estado.n2_meta_pasos:
            p_p2 = estado.n2_pista_p2[estado.n2_pasos_p2]
            txt_p2 = "¡CONGELADO!" if estado.p2_stun > 0 else f"¿{p_p2['n1']} + {p_p2['n2']}? (Paso {estado.n2_pasos_p2+1}/{estado.n2_meta_pasos})"
        else: txt_p2 = "¡EN LA META!"
        
        ancho_p2 = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in f"J2: {txt_p2}")
        x_p2 = (3 * w // 4) - (ancho_p2 // 2)
        y_p2 = h - 80
        glColor3f(*color_p2)
        glRasterPos2f(x_p2, y_p2)
        for char in f"J2: {txt_p2}": glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
            
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_LIGHTING)

    elif estado.fase_actual == "PODIO":
        # Cámara del podio un poco más alejada para compensar las nuevas escalas gigantes
        dist_cam = 21.0
        
        gluLookAt(2.0, 5.5, dist_cam,   
                  2.0, 1.5, 0.0,    
                  0.0, 1.0, 0.0)
        
        draw_podio()
        
        # UI del PODIO
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, w, 0, h)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Fondo oscuro en la UI del podio
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.6)
        glBegin(GL_QUADS)
        glVertex2f(0, h - 120)
        glVertex2f(w, h - 120)
        glVertex2f(w, h)
        glVertex2f(0, h)
        glEnd()
        glDisable(GL_BLEND)
        
        idx_ganador = estado.jugador1_seleccion if estado.ganador_nivel_actual == "J1" else estado.jugador2_seleccion
        nombre_ganador = INFO_PERSONAJES[idx_ganador][0]
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h - 60, f"¡{nombre_ganador.upper()} HA GANADO EL NIVEL!", GLUT_BITMAP_TIMES_ROMAN_24)
        
        if math.sin(estado.tiempo_global * 5.0) > 0:
            glColor3f(1.0, 1.0, 1.0)
            draw_text_centered(100, "PRESIONA [ ENTER ] PARA CONTINUAR", GLUT_BITMAP_HELVETICA_18)
            
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
    
    elif estado.fase_actual == "VERSUS":
        # Matemática para un balanceo muy sutil (no loco)
        balanceo = math.sin(estado.tiempo_versus * 2) * 0.1
        
        # J1 (Izquierda mirando a la derecha: 90 grados)
        dibujar_personaje_vs(estado.jugador1_seleccion, -4.0, 90.0, balanceo)
        # J2 (Derecha mirando a la izquierda: -90 grados)
        dibujar_personaje_vs(estado.jugador2_seleccion, 4.0, -90.0, balanceo)
        
        # UI Épica
        glColor3f(1.0, 0.0, 0.0) # Rojo sangre
        draw_text_centered(h/2, "V S", GLUT_BITMAP_TIMES_ROMAN_24)
        glColor3f(1.0, 1.0, 0.0)
        if math.sin(estado.tiempo_versus * 10) > 0: # Parpadeo rápido
            draw_text_centered(h/2 - 50, "¡PREPARENSE PARA LA BATALLA!", GLUT_BITMAP_HELVETICA_18)

    elif estado.fase_actual == "NIVEL_3":
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)
        mitad_w = int(w / 2)

        def render_escena_3d():
            draw_nivel_3()
            # Dibujar P1
            glPushMatrix()
            glTranslatef(estado.p1_pos[0], estado.p1_pos[1], estado.p1_pos[2])
            glRotatef(estado.p1_rot, 0, 1, 0)
            if estado.p1_stun > 0 and math.sin(estado.tiempo_global * 15) > 0: glColor3f(1.0, 0.0, 0.0)
            else: glColor3f(1.0, 1.0, 1.0)
            
            # --- CORRECCIÓN DE ALTURA PARA NIVEL 3 ---
            # Elevamos un poco para compensar el ALTURAS negativo y que queden sobre el pasto (Y=0)
            glPushMatrix()
            glTranslatef(0, 1.2, 0) 
            dibujar_modelo_en_mapa(estado.jugador1_seleccion)
            glPopMatrix()
            
            # --- INGREDIENTE EN MANO J1 ---
            if estado.n3_p1_hand:
                glPushMatrix()
                glTranslatef(0.0, 1.8, 1.2) # Chest height and slightly forward
                glScalef(0.7, 0.7, 0.7)
                draw_ingredient_model(estado.n3_p1_hand, estado.n3_p1_hand_state)
                glPopMatrix()
            glPopMatrix()

            # Dibujar P2
            glPushMatrix()
            glTranslatef(estado.p2_pos[0], estado.p2_pos[1], estado.p2_pos[2])
            glRotatef(estado.p2_rot, 0, 1, 0)
            if estado.p2_stun > 0 and math.sin(estado.tiempo_global * 15) > 0: glColor3f(1.0, 0.0, 0.0)
            else: glColor3f(1.0, 1.0, 1.0)
            
            # --- CORRECCIÓN DE ALTURA PARA NIVEL 3 ---
            glPushMatrix()
            glTranslatef(0, 1.2, 0)
            dibujar_modelo_en_mapa(estado.jugador2_seleccion)
            glPopMatrix()
            
            # --- INGREDIENTE EN MANO J2 ---
            if estado.n3_p2_hand:
                glPushMatrix()
                glTranslatef(0.0, 1.8, 1.2)
                glScalef(0.7, 0.7, 0.7)
                draw_ingredient_model(estado.n3_p2_hand, estado.n3_p2_hand_state)
                glPopMatrix()
            glPopMatrix()

        # ================= PANTALLA JUGADOR 1 (Izquierda) =================
        glViewport(0, 0, mitad_w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, mitad_w/h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # La cámara sigue por la espalda al P1
        gluLookAt(estado.p1_pos[0], 12.0, estado.p1_pos[2] + 15.0,   
                  estado.p1_pos[0], 0.0, estado.p1_pos[2], 0.0, 1.0, 0.0)
        render_escena_3d()

        # ================= PANTALLA JUGADOR 2 (Derecha) =================
        glViewport(mitad_w, 0, mitad_w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, mitad_w/h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # La cámara sigue por la espalda al P2
        gluLookAt(estado.p2_pos[0], 12.0, estado.p2_pos[2] + 15.0,   
                  estado.p2_pos[0], 0.0, estado.p2_pos[2], 0.0, 1.0, 0.0)
        render_escena_3d()

        # ================= UI GENERAL Y LINEA DIVISORIA =================
        glViewport(0, 0, w, h) # Restauramos la pantalla completa para los textos
        
        # Receta Global Arriba con RESTAS
        glColor3f(1.0, 1.0, 0.0)
        txt_receta = "RECETA: "
        for tipo, (v1, v2) in estado.n3_receta_problemas.items():
            txt_receta += f"{tipo.upper()}: {v1} - {v2} | "
        draw_text_centered(h - 40, txt_receta[:-3], GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text_centered(h - 70, "¡Resuelve las restas y trae los ingredientes!", GLUT_BITMAP_HELVETICA_18)

        # Inventario P1 (Centro izquierda)
        glColor3f(0.0, 1.0, 0.0)
        o1 = estado.n3_olla_p1
        prog_p1 = "MI OLLA: "
        for tipo in estado.n3_receta.keys():
            prog_p1 += f"{tipo[0]}:{o1[tipo]}/{estado.n3_receta[tipo]} "
        
        ancho_txt1 = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in prog_p1)
        draw_text(mitad_w // 2 - ancho_txt1 // 2, h - 100, prog_p1, GLUT_BITMAP_HELVETICA_18)
        
        # MENSAJE DE ERROR J1
        if estado.n3_msg_timer_j1 > 0:
            glColor3f(1, 0, 0)
            ancho_err1 = sum(glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ord(c)) for c in estado.n3_msg_j1)
            draw_text(mitad_w // 2 - ancho_err1 // 2, h - 135, estado.n3_msg_j1, GLUT_BITMAP_TIMES_ROMAN_24)
            
        # Instrucción J1
        if estado.n3_p1_hand is None: txt1 = "¡ATRAPA UN INGREDIENTE!"
        else:
            if estado.n3_p1_hand_state == "crudo": txt1 = f"VE A LA TABLA: {estado.n3_p1_hand.upper()}"
            else: txt1 = f"LLEVALO A LA CAZUELA: {estado.n3_p1_hand.upper()}"
            
        ancho_instr1 = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in txt1)
        draw_text(mitad_w // 2 - ancho_instr1 // 2, h - 165, txt1, GLUT_BITMAP_HELVETICA_18)
        
        if estado.p1_stun > 0: 
            draw_text(mitad_w // 2 - 100, h - 200, "¡CUIDADO!", GLUT_BITMAP_TIMES_ROMAN_24)

        # Inventario P2 (Centro derecha)
        glColor3f(1.0, 0.3, 0.3)
        o2 = estado.n3_olla_p2
        prog_p2 = "MI OLLA: "
        for tipo in estado.n3_receta.keys():
            prog_p2 += f"{tipo[0]}:{o2[tipo]}/{estado.n3_receta[tipo]} "
        
        ancho_txt2 = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in prog_p2)
        draw_text(mitad_w + mitad_w // 2 - ancho_txt2 // 2, h - 100, prog_p2, GLUT_BITMAP_HELVETICA_18)
        
        # MENSAJE DE ERROR J2
        if estado.n3_msg_timer_j2 > 0:
            glColor3f(1, 0, 0)
            ancho_err2 = sum(glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ord(c)) for c in estado.n3_msg_j2)
            draw_text(mitad_w + mitad_w // 2 - ancho_err2 // 2, h - 135, estado.n3_msg_j2, GLUT_BITMAP_TIMES_ROMAN_24)
            
        # Instrucción J2
        if estado.n3_p2_hand is None: txt2 = "¡ATRAPA UN INGREDIENTE!"
        else:
            if estado.n3_p2_hand_state == "crudo": txt2 = f"VE A LA TABLA: {estado.n3_p2_hand.upper()}"
            else: txt2 = f"LLEVALO A LA CAZUELA: {estado.n3_p2_hand.upper()}"
            
        ancho_instr2 = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in txt2)
        draw_text(mitad_w + mitad_w // 2 - ancho_instr2 // 2, h - 165, txt2, GLUT_BITMAP_HELVETICA_18)
        
        if estado.p2_stun > 0: 
            draw_text(mitad_w + mitad_w // 2 - 100, h - 200, "¡CUIDADO!", GLUT_BITMAP_TIMES_ROMAN_24)

    elif estado.fase_actual == "GANADOR":
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)
        
        # Fondo oscuro de gala
        glClearColor(0.02, 0.02, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Cámara para el ganador - Más alejada
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 5, 15,  0, 2.0, 0,  0, 1, 0)
        
        # === ILUMINACIÓN DE ESCENARIO ===
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        # Luz Cenital (Spotlight)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 10.0, 2.0, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0]) # Luz cálida
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        
        # Piso del escenario (Círculo de luz)
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glTranslatef(0, -0.1, 0)
        glColor3f(0.1, 0.1, 0.2)
        glScalef(4.0, 0.05, 4.0)
        glutSolidSphere(1.0, 32, 32)
        glPopMatrix()
        glEnable(GL_LIGHTING)
        
        # Dibujar al Gran Ganador - Basado en Victorias Totales
        ganador_final = "J1" if estado.wins_j1 >= estado.wins_j2 else "J2"
        ganador_idx = estado.jugador1_seleccion if ganador_final == "J1" else estado.jugador2_seleccion
        
        glPushMatrix()
        # Elevamos para que no se hunda en el escenario
        y_off = 1.5
        if ganador_idx == 1: y_off = -1.5 # El Chef ya tiene +3.0 interno, 3 - 1.5 = 1.5 final
        glTranslatef(0, y_off, 0)
        glRotatef(estado.tiempo_global * 40, 0, 1, 0) # Rotación lenta triunfal
        dibujar_modelo(ganador_idx)
        glPopMatrix()
        
        # Mostrar puntuación final
        glColor3f(1, 1, 1)
        draw_text_centered(100, f"PUNTUACIÓN FINAL: J1({estado.wins_j1}) - J2({estado.wins_j2})", GLUT_BITMAP_HELVETICA_18)
        
        # === UI DE VICTORIA FINAL ===
        glDisable(GL_LIGHTING)
        nombre_ganador = estado.personajes_disponibles[ganador_idx]
        
        # Texto con sombra/glow
        glColor3f(1.0, 1.0, 1.0)
        draw_text_centered(h - 80, "¡EL GRAN GANADOR ES!", GLUT_BITMAP_TIMES_ROMAN_24)
        
        # Nombre en grande y amarillo
        glColor3f(1.0, 0.9, 0.0)
        draw_text_centered(h - 130, nombre_ganador.upper(), GLUT_BITMAP_TIMES_ROMAN_24)
        
        # Brillo parpadeante
        if math.sin(estado.tiempo_global * 10) > 0:
            glColor3f(1.0, 1.0, 1.0)
            draw_text_centered(100, "PRESIONA [ ENTER ] PARA REINICIAR LA AVENTURA", GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()

def draw_start_screen():
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    t = estado.tiempo_global
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    # =========================================================
    # PARTE 1: FONDO 3D - Rejilla Neon estilo Tron/Retrowave
    # =========================================================
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(60, w / max(h, 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 3, 8,  0, 0, -5,  0, 1, 0)
    
    # Fondo gradiente (dibujar un quad gigante lejos)
    glBegin(GL_QUADS)
    glColor3f(0.02, 0.0, 0.08)  # Púrpura oscuro abajo
    glVertex3f(-50, -5, -50)
    glVertex3f(50, -5, -50)
    glColor3f(0.0, 0.02, 0.12)   # Azul oscuro arriba
    glVertex3f(50, 15, -50)
    glVertex3f(-50, 15, -50)
    glEnd()
    
    # Rejilla neon en el suelo (se mueve hacia la cámara)
    grid_offset = (t * 2.0) % 2.0  # Movimiento continuo
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Blend aditivo para neon
    
    # Líneas horizontales (Z)
    for i in range(-20, 5):
        z = float(i) + grid_offset
        alpha = max(0.0, 1.0 - abs(z + 5) / 20.0) * 0.6
        glColor4f(0.0, 0.8, 1.0, alpha)
        glBegin(GL_LINES)
        glVertex3f(-25, -0.5, z)
        glVertex3f(25, -0.5, z)
        glEnd()
    
    # Líneas verticales (X)
    for i in range(-12, 13):
        x = float(i) * 2
        glColor4f(0.0, 0.5, 1.0, 0.3)
        glBegin(GL_LINES)
        glVertex3f(x, -0.5, -20)
        glVertex3f(x, -0.5, 5)
        glEnd()
    
    # Línea de horizonte brillante
    glLineWidth(2.0)
    glow = 0.7 + 0.3 * math.sin(t * 3.0)
    glColor4f(0.0, glow, 1.0, 0.9)
    glBegin(GL_LINES)
    glVertex3f(-30, -0.5, -20)
    glVertex3f(30, -0.5, -20)
    glEnd()
    glLineWidth(1.0)
    
    # Partículas flotantes (cubitos neon volando)
    for i in range(20):
        px = math.sin(t * 0.3 + i * 1.7) * 12
        py = (math.sin(t * 0.5 + i * 2.3) + 1.0) * 3.0 + 1.0
        pz = ((t * 0.8 + i * 3.0) % 25.0) - 20.0
        size = 0.08 + 0.05 * math.sin(t * 2 + i)
        
        # Color alternando entre cian, magenta, y amarillo
        if i % 3 == 0:
            glColor4f(0.0, 1.0, 1.0, 0.7)
        elif i % 3 == 1:
            glColor4f(1.0, 0.0, 1.0, 0.5)
        else:
            glColor4f(1.0, 1.0, 0.0, 0.5)
        
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(t * 100 + i * 45, 1, 1, 0)
        glutSolidCube(size)
        glPopMatrix()
    
    glDisable(GL_BLEND)
    
    # Restaurar la proyección 3D
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # =========================================================
    # PARTE 2: OVERLAY 2D - Estrellas, Título, Textos
    # =========================================================
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # --- ESTRELLAS ANIMADAS (Titilando) ---
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_POINT_SMOOTH)
    
    for star in title_stars:
        # Mover estrella hacia abajo (efecto de caída)
        sy = (star["y"] - t * star["speed"]) % 1.0
        sx = star["x"]
        
        # Titileo suave
        twinkle = 0.5 + 0.5 * math.sin(t * 4.0 + sx * 20.0 + sy * 15.0)
        alpha = star["brightness"] * twinkle
        
        glPointSize(star["size"])
        glBegin(GL_POINTS)
        glColor4f(0.7, 0.85, 1.0, alpha)
        glVertex2f(sx * w, sy * h)
        glEnd()
    
    glDisable(GL_POINT_SMOOTH)
    
    # --- BORDES DECORATIVOS NEON ---
    glLineWidth(2.0)
    border_alpha = 0.4 + 0.2 * math.sin(t * 2.0)
    glColor4f(0.0, 0.8, 1.0, border_alpha)
    margin = 15
    glBegin(GL_LINE_LOOP)
    glVertex2f(margin, margin)
    glVertex2f(w - margin, margin)
    glVertex2f(w - margin, h - margin)
    glVertex2f(margin, h - margin)
    glEnd()
    
    # Segundo borde interior
    glColor4f(1.0, 0.0, 0.8, border_alpha * 0.5)
    m2 = 25
    glBegin(GL_LINE_LOOP)
    glVertex2f(m2, m2)
    glVertex2f(w - m2, m2)
    glVertex2f(w - m2, h - m2)
    glVertex2f(m2, h - m2)
    glEnd()
    glLineWidth(1.0)
    
    glDisable(GL_BLEND)
    
    # --- TÍTULO PRINCIPAL: "NUMY PLAY" con efecto glow ---
    # Efecto de color cycling suave en el título
    r_title = 0.5 + 0.5 * math.sin(t * 1.2)
    g_title = 0.8 + 0.2 * math.sin(t * 1.5 + 1.0)
    b_title = 0.5 + 0.5 * math.sin(t * 1.8 + 2.0)
    
    # Capa de "glow" (texto repetido con offsets y menor opacidad)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    
    title_y = h // 2 + 80
    for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2), (0, 3), (0, -3)]:
        glColor4f(r_title * 0.4, g_title * 0.4, b_title * 0.4, 0.3)
        # Dibujamos el glow manualmente usando rasterPos
        title_width = sum(glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ord(c)) for c in "NUMY PLAY")
        glRasterPos2f((w - title_width) / 2 + offset[0], title_y + offset[1])
        for char in "NUMY PLAY":
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    
    glDisable(GL_BLEND)
    
    # Texto principal sólido
    glColor3f(r_title, g_title, b_title)
    draw_text_centered(title_y, "NUMY PLAY", GLUT_BITMAP_TIMES_ROMAN_24)
    
    # --- SUBTÍTULO ---
    glColor3f(0.0, 0.85, 1.0)
    draw_text_centered(h // 2 + 40, "- ARCADE MATEMATICO 3D -", GLUT_BITMAP_HELVETICA_18)
    
    # --- LÍNEA SEPARADORA ANIMADA ---
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    sep_y = h // 2 + 15
    line_w = 200 + 50 * math.sin(t * 2.0)
    cx = w / 2
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor4f(1.0, 0.0, 1.0, 0.8)
    glVertex2f(cx - line_w, sep_y)
    glColor4f(0.0, 1.0, 1.0, 0.0)
    glVertex2f(cx, sep_y)
    glEnd()
    glBegin(GL_LINES)
    glColor4f(0.0, 1.0, 1.0, 0.0)
    glVertex2f(cx, sep_y)
    glColor4f(1.0, 0.0, 1.0, 0.8)
    glVertex2f(cx + line_w, sep_y)
    glEnd()
    glLineWidth(1.0)
    glDisable(GL_BLEND)
    
    # --- TEXTO PARPADEANTE ARCADE ---
    if math.sin(t * 5.0) > 0:
        # Efecto glow amarillo en el texto de enter
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glColor4f(1.0, 0.8, 0.0, 0.3)
        draw_text_centered(h // 2 - 50 + 1, "PRESIONA [ ENTER ] PARA JUGAR", GLUT_BITMAP_HELVETICA_18)
        draw_text_centered(h // 2 - 50 - 1, "PRESIONA [ ENTER ] PARA JUGAR", GLUT_BITMAP_HELVETICA_18)
        glDisable(GL_BLEND)
        
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h // 2 - 50, "PRESIONA [ ENTER ] PARA JUGAR", GLUT_BITMAP_HELVETICA_18)
    
    # --- CRÉDITOS / VERSIÓN ---
    draw_text_centered(45, "v1.0  |  2 JUGADORES  |  6 PERSONAJES", GLUT_BITMAP_HELVETICA_12)
    glColor3f(0.5, 0.1, 0.1)
    draw_text_centered(20, "PRESIONA [ ESC ] PARA SALIR DEL JUEGO", GLUT_BITMAP_HELVETICA_12)
    
    # Restaurar estados
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_ronda_intro():
    """Pantalla negra antes de iniciar la ronda, muestra el objetivo"""
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    t = estado.tiempo_global
    
    # 1. DIBUJAR FONDO NEGRO 2D
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(w, 0)
    glVertex2f(w, h)
    glVertex2f(0, h)
    glEnd()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # 2. DIBUJAR OBJETO 3D
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, w/max(h, 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    gluLookAt(0, 0, 8,  0, 0, 0,  0, 1, 0)
    
    if estado.n1_tipo_objeto:
        r_obj, g_obj, b_obj = estado.n1_tipo_objeto["color"]
        forma = estado.n1_tipo_objeto["forma"]
        glPushMatrix()
        glTranslatef(0, -1.0, 0)
        glRotatef(t * 50, 0, 1, 0)  # Rotar
        glScalef(2.0, 2.0, 2.0)     # Hacerlo mas grande
        
        dibujar_forma_objeto(forma, r_obj, g_obj, b_obj, t)
        glPopMatrix()
        
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # 3. DIBUJAR TEXTOS 2D POR ENCIMA (Sin Depth Test)
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    nombre_obj = estado.n1_tipo_objeto["nombre"] if estado.n1_tipo_objeto else "OBJETOS"
    r_obj, g_obj, b_obj = estado.n1_tipo_objeto["color"] if estado.n1_tipo_objeto else (1,1,1)
    
    glColor3f(1.0, 1.0, 1.0)
    draw_text_centered(h // 2 + 100, "NUEVA RONDA", GLUT_BITMAP_TIMES_ROMAN_24)
    
    glColor3f(r_obj, g_obj, b_obj)
    draw_text_centered(h // 2 + 30, f"OBJETIVO: CONTAR {nombre_obj}", GLUT_BITMAP_TIMES_ROMAN_24)
    
    if math.sin(t * 5.0) > 0:
        glColor3f(1.0, 1.0, 0.0)
        draw_text_centered(h // 2 - 80, "PRESIONA [ ENTER ] PARA COMENZAR", GLUT_BITMAP_HELVETICA_18)
        
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def dibujar_modelo_en_mapa(indice):
    glPushMatrix()
    glTranslatef(0, ALTURAS[indice], 0)
    glRotatef(ROTACIONES_Y[indice], 0, 1, 0)
    sx, sy, sz = ESCALAS[indice]
    glScalef(sx, sy, sz)
    if indice == 0: glDisable(GL_LIGHTING)
    dibujar_modelo(indice)
    if indice == 0: glEnable(GL_LIGHTING)
    glPopMatrix()

def draw_nivel_1():
    limit = estado.map_limit
    t = estado.tiempo_global
    
    # ========== 1. CIELO DEGRADADO ==========
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.7, 1.0)  # Azul cielo arriba
    glVertex2f(0, 1)
    glVertex2f(1, 1)
    glColor3f(0.7, 0.85, 1.0)  # Celeste claro abajo
    glVertex2f(1, 0.3)
    glVertex2f(0, 0.3)
    glEnd()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    
    # ========== 2. SUELO DE PRADERA ==========
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.55, 0.1)  # Verde pasto claro centro
    glVertex3f(-limit, -2, -limit)
    glVertex3f(limit, -2, -limit)
    glColor3f(0.15, 0.45, 0.08)  # Verde pasto oscuro borde
    glVertex3f(limit, -2, limit)
    glVertex3f(-limit, -2, limit)
    glEnd()
    
    # Camino de tierra hacia las cajas
    glBegin(GL_QUADS)
    glColor3f(0.55, 0.4, 0.2)
    glVertex3f(-2, -1.98, -16)
    glVertex3f(2, -1.98, -16)
    glColor3f(0.6, 0.45, 0.25)
    glVertex3f(2, -1.98, 10)
    glVertex3f(-2, -1.98, 10)
    glEnd()
    glEnable(GL_LIGHTING)
    
    # ========== 3. ARBOLES DECORATIVOS ==========
    arboles_pos = [(-16, -8), (-14, 2), (-17, 8), (15, -5), (16, 4), (17, 9),
                   (-12, -15), (12, -15), (-18, -2), (18, -10)]
    for ax, az in arboles_pos:
        glPushMatrix()
        glTranslatef(ax, -2, az)
        # Tronco
        glColor3f(0.45, 0.25, 0.1)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        q = gluNewQuadric()
        gluCylinder(q, 0.3, 0.25, 3.0, 8, 1)
        glPopMatrix()
        # Copa del arbol
        glColor3f(0.1, 0.55, 0.15)
        glTranslatef(0, 3.0, 0)
        glutSolidSphere(1.8, 12, 12)
        # Copa superior mas chica
        glColor3f(0.15, 0.65, 0.2)
        glTranslatef(0, 1.2, 0)
        glutSolidSphere(1.2, 10, 10)
        glPopMatrix()
    
    # ========== 4. ARBUSTOS Y FLORES ==========
    random.seed(123)  # Semilla fija para decoracion
    for i in range(25):
        fx = random.uniform(-18, 18)
        fz = random.uniform(-10, 9)
        glPushMatrix()
        glTranslatef(fx, -1.8, fz)
        # Arbusto verde
        glColor3f(0.15 + i * 0.01, 0.5 + (i % 5) * 0.05, 0.1)
        glutSolidSphere(0.35, 8, 8)
        glPopMatrix()
    
    # Flores de colores
    colores_flores = [(1.0, 0.3, 0.3), (1.0, 1.0, 0.3), (0.8, 0.3, 1.0), (1.0, 0.6, 0.8)]
    for i in range(15):
        fx = random.uniform(-17, 17)
        fz = random.uniform(-8, 8)
        glPushMatrix()
        glTranslatef(fx, -1.7, fz)
        glColor3f(*colores_flores[i % len(colores_flores)])
        glutSolidSphere(0.15, 6, 6)
        glPopMatrix()
    random.seed()  # Restaurar semilla aleatoria
    
    # ========== 5. NUBES ==========
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)
    nubes = [(-10, 12, -18), (5, 14, -20), (15, 11, -15), (-5, 13, -22), (0, 15, -25)]
    for nx, ny, nz in nubes:
        drift = math.sin(t * 0.15 + nx) * 2  # Movimiento lento
        glPushMatrix()
        glTranslatef(nx + drift, ny, nz)
        glutSolidSphere(2.0, 10, 10)
        glTranslatef(1.8, -0.3, 0)
        glutSolidSphere(1.5, 10, 10)
        glTranslatef(-3.5, 0.2, 0)
        glutSolidSphere(1.7, 10, 10)
        glPopMatrix()
    glEnable(GL_LIGHTING)

    # ========== 6. OBJETOS A CONTAR ==========
    tipo = estado.n1_tipo_objeto
    if tipo:
        r, g, b = tipo["color"]
        forma = tipo["forma"]
        
        for obj in estado.n1_objetos:
            glPushMatrix()
            glTranslatef(obj[0], -1.3, obj[1])
            glColor3f(r, g, b)
            
            # Usamos la función centralizada de formas (mejor diseño)
            glScalef(1.2, 1.2, 1.2) # Aumentar un poco el tamaño
            dibujar_forma_objeto(forma, r, g, b, t)
            
            # Sombra debajo del objeto
            glDisable(GL_LIGHTING)
            glColor4f(0.0, 0.0, 0.0, 0.3)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glPushMatrix()
            glTranslatef(0, -0.25, 0)
            glScalef(1.0, 0.02, 1.0)
            glutSolidSphere(0.5, 8, 8)
            glPopMatrix()
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            
            glPopMatrix()

    # ========== 7. CAJAS DE RESPUESTA ==========
    from OpenGL.GLUT import GLUT_STROKE_ROMAN
    colores_caja = [(0.9, 0.3, 0.2), (0.2, 0.7, 0.3), (0.2, 0.4, 0.9)]
    for i, blk in enumerate(estado.n1_bloques):
        glPushMatrix()
        glTranslatef(blk["x"], -0.5, blk["z"])
        
        # Caja colorida
        glColor3f(*colores_caja[i])
        glutSolidCube(3.0)
        
        # Borde mas oscuro
        glColor3f(colores_caja[i][0] * 0.5, colores_caja[i][1] * 0.5, colores_caja[i][2] * 0.5)
        glutWireCube(3.05)
        
        glPopMatrix()
        
        # NUMERO GIGANTE 3D en la CARA FRONTAL de la caja
        glDisable(GL_LIGHTING)
        num_str = str(blk["val"])
        
        # Centrar horizontalmente usando el ancho estimado
        # Cada caracter de stroke mide aprox 104 unidades de ancho
        escala_texto = 0.012
        text_w = len(num_str) * 104 * escala_texto
        
        # Posición: al frente de la caja (z + 1.51 para que no haya z-fighting)
        # Y un poco más abajo del centro de la caja (y = -1.0)
        pos_x = blk["x"] - (text_w / 2)
        pos_y = -1.2
        pos_z = blk["z"] + 1.52
        
        # Numero blanco grueso y limpio
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(4.0)
        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glScalef(escala_texto, escala_texto, escala_texto)
        for char in num_str:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
        glPopMatrix()
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHTING)

def draw_podio():
    """Dibuja un podio 3D con el ganador en el centro y el perdedor al lado"""
    t = estado.tiempo_global
    
    # Fondo plano oscuro
    glDisable(GL_LIGHTING)
    glColor3f(0.02, 0.02, 0.1)
    glPushMatrix()
    glTranslatef(0, -10, 0)
    glScalef(100, 1, 100)
    glutSolidCube(1.0)
    glPopMatrix()
    glEnable(GL_LIGHTING)
    
    # Podio Ganador (Centro/Oro)
    glPushMatrix()
    glColor3f(0.8, 0.6, 0.0) # Oro más oscuro
    glTranslatef(0.0, -1.5, 0.0)
    glScalef(4.0, 4.0, 4.0)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Podio Perdedor (Derecha/Plata/Más bajo)
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5) # Plata más oscura
    glTranslatef(4.0, -2.5, 0.0)
    glScalef(3.0, 2.0, 3.0)
    glutSolidCube(1.0)
    glPopMatrix()

    # NÚMEROS EN LOS PILARES
    from OpenGL.GLUT import GLUT_STROKE_ROMAN
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(5.0)
    
    # Numero 1
    glPushMatrix()
    glTranslatef(-0.5, -0.8, 2.1)
    glScalef(0.015, 0.015, 0.015)
    for char in "1": glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()
    
    # Numero 2
    glPushMatrix()
    glTranslatef(3.6, -2.2, 1.6)
    glScalef(0.01, 0.01, 0.01)
    for char in "2": glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()
    glLineWidth(1.0)
    glEnable(GL_LIGHTING)
    
    # Posicionar personajes
    if estado.ganador_nivel_actual == "J1":
        ganador_idx = estado.jugador1_seleccion
        perdedor_idx = estado.jugador2_seleccion
    else:
        ganador_idx = estado.jugador2_seleccion
        perdedor_idx = estado.jugador1_seleccion
        
    # Dibujar Ganador (Sobre el bloque de oro)
    glPushMatrix()
    glScalef(1.8, 1.8, 1.8) # Personajes más grandes y heroicos
    off_g = PODIO_OFFSETS.get(ganador_idx, 0.0)
    # Ajustar altura compensando la escala
    glTranslatef(0.0, (1.1 - ALTURAS[ganador_idx] + off_g) / 1.8, 0.0)
    dibujar_modelo_en_mapa(ganador_idx)
    glPopMatrix()
    
    # Dibujar Perdedor (Sobre el bloque de plata)
    glPushMatrix()
    glScalef(1.4, 1.4, 1.4) # Un poco más pequeño que el ganador pero no diminuto
    off_p = PODIO_OFFSETS.get(perdedor_idx, 0.0)
    # Ajustar altura compensando la escala
    glTranslatef(2.85, (-0.8 - ALTURAS[perdedor_idx] + off_p) / 1.4, 0.0) # 2.85 corregido para que encaje con la escala
    dibujar_modelo_en_mapa(perdedor_idx)
    glPopMatrix()

def draw_nivel_2(pista, pasos):
    # 1. Dibujar la línea de salida ancha
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(0, -1.6, 8.0)
    glScalef(20.0, 0.5, 4.0)
    glutSolidCube(1.0)
    glPopMatrix()

    from OpenGL.GLUT import GLUT_STROKE_ROMAN
    # 2. Dibujar la "Caminata" de plataformas
    for i, paso in enumerate(pista):
        z_pos = paso["z"]
        opciones = paso["opciones"]
        
        # 3 Caminos: Izquierda, Centro, Derecha
        posiciones_x = [-5.0, 0.0, 5.0] 
        
        for j in range(3):
            glPushMatrix()
            glTranslatef(posiciones_x[j], -1.6, z_pos)
            
            # Pintamos de color gris las plataformas que ya pasaron
            if pasos > i:
                glColor3f(0.3, 0.3, 0.3) 
            else:
                glColor3f(0.0, 0.5, 0.8) # Azul brillante las activas

            glScalef(4.0, 0.5, 4.0)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Dibujar el número encima de la plataforma
            glDisable(GL_LIGHTING)
            num_str = str(opciones[j])
            escala_texto = 0.012
            text_w = len(num_str) * 104 * escala_texto
            
            pos_x = posiciones_x[j] - (text_w / 2)
            pos_y = -1.3 # Sobre la plataforma
            pos_z = z_pos + 1.0 # Frente
            
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(4.0)
            glPushMatrix()
            glTranslatef(pos_x, pos_y, pos_z)
            glScalef(escala_texto, escala_texto, escala_texto)
            for char in num_str:
                glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
            glPopMatrix()
            glLineWidth(1.0)
            glEnable(GL_LIGHTING)
            
    # 3. Plataforma de Meta
    glPushMatrix()
    glColor3f(0.0, 0.8, 0.0) # Verde de victoria
    meta_z = 2.0 - (estado.n2_meta_pasos * 10.0)
    glTranslatef(0, -1.6, meta_z)
    glScalef(20.0, 0.5, 4.0)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_nivel_3():
    # 1. Piso del Rancho (Pasto verde)
    glPushMatrix()
    glColor3f(0.2, 0.6, 0.2) # Verde pasto
    glTranslatef(0, -1.0, 0)
    glScalef(40.0, 0.5, 40.0)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # 1. Piso de la Granja (Verde oscuro con parches)
    glColor3f(0.2, 0.5, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-20, 0, -20); glVertex3f(20, 0, -20)
    glVertex3f(20, 0, 5); glVertex3f(-20, 0, 5) # Hasta la cerca
    glEnd()
    
    # Piso de la Cocina (Gris/Baldosas)
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_QUADS)
    glVertex3f(-20, 0, 5); glVertex3f(20, 0, 5)
    glVertex3f(20, 0, 20); glVertex3f(-20, 0, 20)
    glEnd()

    # Parches de pasto (cubos planos)
    glColor3f(0.1, 0.4, 0.1)
    for px, pz in [(-10, -5), (5, -12), (12, -2), (-8, -15)]:
        glPushMatrix()
        glTranslatef(px, 0.01, pz)
        glScalef(3, 0.05, 3)
        glutSolidCube(1.0)
        glPopMatrix()

    # 3. Las Tablas de Picar
    def dibujar_tabla(x, z):
        glPushMatrix()
        glTranslatef(x, 0.0, z)
        # Tablero de madera gruesa
        glColor3f(0.5, 0.3, 0.1)
        glPushMatrix()
        glScalef(3.0, 1.2, 3.0)
        glutSolidCube(1.0)
        glPopMatrix()
        # Superficie blanca de picar
        glColor3f(0.9, 0.9, 0.9)
        glPushMatrix()
        glTranslatef(0, 0.65, 0)
        glScalef(2.5, 0.1, 2.5)
        glutSolidCube(1.0)
        glPopMatrix()
        # Cuchillo decorativo
        glColor3f(0.7, 0.7, 0.7)
        glPushMatrix()
        glTranslatef(0.8, 0.75, 0)
        glRotatef(30, 0, 1, 0)
        glScalef(1.2, 0.05, 0.2)
        glutSolidCube(1.0)
        glPopMatrix()
        glPopMatrix()

    dibujar_tabla(estado.n3_tabla_p1["x"], estado.n3_tabla_p1["z"])
    dibujar_tabla(estado.n3_tabla_p2["x"], estado.n3_tabla_p2["z"])

    # 4. Cacerolas (Ollas negras gigantes con forma de CAZUELA)
    def dibujar_cacerola(x, z, color_aro, olla_data):
        glPushMatrix()
        glTranslatef(x, 0.0, z)
        # Cuerpo de la cacerola (Forma de olla real)
        glColor3f(0.1, 0.1, 0.1) 
        glPushMatrix()
        glScalef(2.6, 1.4, 2.6)
        glutSolidSphere(1.0, 24, 24)
        glPopMatrix()
        # Borde superior (Rim)
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(0, 1.0, 0)
        glRotatef(90, 1, 0, 0)
        glutSolidTorus(0.25, 2.6, 20, 20)
        glPopMatrix()
        # Asas de la olla
        glColor3f(0.3, 0.3, 0.3)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 2.8, 0.5, 0)
            glutSolidSphere(0.4, 12, 12)
            glPopMatrix()
        
        # --- DIBUJAR INGREDIENTES DENTRO DE LA OLLA ---
        # Posiciones aleatorias fijas dentro del radio de la olla
        y_pos = 0.2
        for tipo, cant in olla_data.items():
            for i in range(cant):
                glPushMatrix()
                # Un poco de dispersión aleatoria basada en el índice
                dx = math.sin(i * 1.5) * 1.2
                dz = math.cos(i * 1.5) * 1.2
                glTranslatef(dx, y_pos, dz)
                glScalef(0.6, 0.6, 0.6)
                draw_ingredient_model(tipo, "picado") # Siempre se muestran picados en la olla
                glPopMatrix()
        glPopMatrix()

    dibujar_cacerola(estado.n3_cacerola_p1["x"], estado.n3_cacerola_p1["z"], (0.0, 1.0, 0.0), estado.n3_olla_p1)
    dibujar_cacerola(estado.n3_cacerola_p2["x"], estado.n3_cacerola_p2["z"], (1.0, 0.0, 0.0), estado.n3_olla_p2)

    # 5. Ingredientes "Vivos" (Correteando)
    for ing in estado.n3_ingredientes:
        if not ing["activo"]: continue
        glPushMatrix()
        # Saltar un poquito mientras corren + Elevación base para que no se hundan (0.6 de radio)
        salto = abs(math.sin(estado.tiempo_global * 10)) * 0.3
        glTranslatef(ing["x"], 0.6 + salto, ing["z"])
        draw_ingredient_model(ing["tipo"], "crudo")
        glPopMatrix()

    # 6. Dibujar vallas de los ESTABLOS y Marcadores
    establos_info = [
        (-17.0, (1, 0, 0)),    # Tomate
        (-10.5, (0.4, 1, 0.2)),  # Lechuga
        (-4.0, (1, 1, 0)),      # Queso
        (4.0, (1, 0.8, 0)),    # Pollo
        (10.5, (1, 1, 1)),     # Vaca
        (17.0, (0.9, 0.9, 1.0)) # Leche
    ]
    
    for x, color in establos_info:
        glPushMatrix()
        glColor3f(*color)
        glTranslatef(x, 1.5, 4.8) # Encima de la valla frontal
        glScalef(0.6, 0.6, 0.6)
        glutSolidCube(1.0)
        glPopMatrix()

    for x in [-13.5, -7.5, -1.0, 5.0, 13.5, 19.5]:
        glPushMatrix()
        glColor3f(0.3, 0.15, 0.05) # Madera más oscura
        # Vallas largas que van desde el fondo (z=-20) hasta el frente (z=5)
        glTranslatef(x, 0.4, -7.5) 
        glScalef(0.4, 0.8, 25.0)
        glutSolidCube(1.0)
        glPopMatrix()
        
    # 7. DIBUJAR VACAS LECHERAS
    for v in estado.n3_vacas_lecheras:
        glPushMatrix()
        glTranslatef(v["x"], 0.8, v["z"])
        glRotatef(v["rot"], 0, 1, 0)
        # Dibujar una vaca con un collar/campana azul para distinguirla
        glScalef(0.8, 0.8, 0.8)
        draw_ingredient_model("Vaca", "crudo")
        # Campana azul
        glColor3f(0.2, 0.4, 1.0)
        glTranslatef(0, 0.2, 0.8)
        glutSolidSphere(0.3, 8, 8)
        glPopMatrix()

def teclado_normal(key, x, y):
    key = key.lower()
    if key == b'\r': # Enter
        if estado.fase_actual == "TITULO":
            estado.fase_actual = "SELECCION_P1"
            sound_manager.play_sound(0, "happy") # Sonido de inicio
        elif estado.fase_actual == "SELECCION_P1":
            manager.trigger_characteristic_anim(estado.cursor_index)
            estado.fase_actual = "CONFIRMAR_P1"
            sound_manager.play_sound(estado.cursor_index, "happy")
        elif estado.fase_actual == "CONFIRMAR_P1":
            manager.stop_characteristic_anim(estado.cursor_index)
            # ¡Guardamos la selección del J1 y pasamos al J2!
            estado.jugador1_seleccion = estado.cursor_index
            estado.fase_actual = "SELECCION_P2"
            # Movemos el cursor para que no empiece en el mismo personaje
            estado.cursor_index_p2 = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0
            sound_manager.play_sound(estado.jugador1_seleccion, "surprised")
        elif estado.fase_actual == "SELECCION_P2":
            # Validar que el J2 NO elija el mismo del J1
            if estado.cursor_index_p2 == estado.jugador1_seleccion:
                print("¡Personaje ya ocupado por el J1!")
                # Aquí podríamos poner un sonido de error luego
            else:
                manager.trigger_characteristic_anim(estado.cursor_index_p2)
                estado.fase_actual = "CONFIRMAR_P2"
                sound_manager.play_sound(estado.cursor_index_p2, "happy")
        elif estado.fase_actual == "CONFIRMAR_P2":
            manager.stop_characteristic_anim(estado.cursor_index_p2)
            # ¡Ambos listos!
            estado.jugador2_seleccion = estado.cursor_index_p2
            print(f"¡BATALLA LISTA! J1:{estado.jugador1_seleccion} vs J2:{estado.jugador2_seleccion}")
            estado.fase_actual = "VERSUS"  # ¡BOOM! PANTALLA VS
            estado.tiempo_versus = 0.0
            # Disparar animaciones de ambos personajes para el VS
            manager.trigger_characteristic_anim(estado.jugador1_seleccion)
            manager.trigger_characteristic_anim(estado.jugador2_seleccion)
            sound_manager.play_sound(estado.jugador2_seleccion, "happy")
            try:
                # === ¡AQUÍ ESTÁ EL CAMBIO! ===
                ruta_real = ruta_absoluta("sonidos/ready.mp3")
                efecto_inicio = pygame.mixer.Sound(ruta_real) 
                efecto_inicio.play()
            except Exception as e:
                print(f"No se pudo cargar el audio de inicio: {e}")
        elif estado.fase_actual == "LISTOS":
            estado.fase_actual = "RONDA_INTRO"
            # Detener música para la intro dramática
            sound_manager.stop_bgm()
        elif estado.fase_actual == "RONDA_INTRO":
            estado.fase_actual = "MAPA"
        elif estado.fase_actual == "PODIO":
            # Detener animaciones y resetear expresiones
            manager.stop_characteristic_anim(estado.jugador1_seleccion)
            manager.stop_characteristic_anim(estado.jugador2_seleccion)
            manager.set_expression(estado.jugador1_seleccion, 0)
            manager.set_expression(estado.jugador2_seleccion, 0)
            
            estado.fase_actual = estado.siguiente_fase
            estado.tiempo_global = 0.0
            estado.teclas.clear()
        elif estado.fase_actual == "GANADOR":
            # Reset total del juego
            estado.fase_actual = "TITULO"
            estado.jugador1_seleccion = None
            estado.jugador2_seleccion = None
            estado.p1_score = 0
            estado.p2_score = 0
            estado.wins_j1 = 0
            estado.wins_j2 = 0
            estado.generar_nivel_1()
            
    elif key == b'\x1b': # Esc
        if estado.fase_actual == "TITULO":
            print("Saliendo del juego...")
            os._exit(0)
            
        elif estado.fase_actual == "SELECCION_P1":
            estado.fase_actual = "TITULO"
            sound_manager.play_sound(0, "walk")
            
        elif estado.fase_actual == "CONFIRMAR_P1":
            manager.stop_characteristic_anim(estado.cursor_index)
            estado.fase_actual = "SELECCION_P1"
            
        elif estado.fase_actual == "SELECCION_P2":
            estado.fase_actual = "SELECCION_P1"
            estado.tiempo_seleccion = 0.0
            
        elif estado.fase_actual == "CONFIRMAR_P2":
            manager.stop_characteristic_anim(estado.cursor_index_p2)
            estado.fase_actual = "SELECCION_P2"
            
        else:
            # Cualquier otra fase (Juego, Podio, etc) regresa a Titulo con reset
            print("Regresando al menú principal...")
            estado.fase_actual = "TITULO"
            estado.jugador1_seleccion = None
            estado.jugador2_seleccion = None
            estado.p1_score = 0
            estado.p2_score = 0
            estado.wins_j1 = 0
            estado.wins_j2 = 0
            estado.generar_nivel_1()
            sound_manager.stop_bgm()
            estado.teclas.clear()

    # Controles de navegación P1 (WASD)
    if estado.fase_actual == "SELECCION_P1":
        if key == b'a':
            estado.cursor_index = (estado.cursor_index - 1) % 6
            estado.tiempo_seleccion = 0.0
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)
        elif key == b'd':
            estado.cursor_index = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)

    if estado.fase_actual in ["MAPA", "NIVEL_2", "NIVEL_3"]:
        estado.teclas.add(key)
            
    glutPostRedisplay()

def teclado_arriba(key, x, y):
    key = key.lower()
    if key in estado.teclas:
        estado.teclas.remove(key)
    glutPostRedisplay()

def teclado_especial(key, x, y):
    # Controles de navegación P2 (Arrows)
    if estado.fase_actual == "SELECCION_P2":
        if key == GLUT_KEY_LEFT:
            estado.cursor_index_p2 = (estado.cursor_index_p2 - 1) % 6
            # Saltar personaje de P1
            if estado.cursor_index_p2 == estado.jugador1_seleccion:
                estado.cursor_index_p2 = (estado.cursor_index_p2 - 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index_p2, "walk", volume=0.3)
        elif key == GLUT_KEY_RIGHT:
            estado.cursor_index_p2 = (estado.cursor_index_p2 + 1) % 6
            # Saltar personaje de P1
            if estado.cursor_index_p2 == estado.jugador1_seleccion:
                estado.cursor_index_p2 = (estado.cursor_index_p2 + 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index_p2, "walk", volume=0.3)
    
    # También permitir flechas para P1 si está en su fase
    elif estado.fase_actual == "SELECCION_P1":
        if key == GLUT_KEY_LEFT:
            estado.cursor_index = (estado.cursor_index - 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)
        elif key == GLUT_KEY_RIGHT:
            estado.cursor_index = (estado.cursor_index + 1) % 6
            estado.tiempo_seleccion = 0.0 
            sound_manager.play_sound(estado.cursor_index, "walk", volume=0.3)
    
    if estado.fase_actual in ["MAPA", "NIVEL_2", "NIVEL_3"]:
        estado.teclas.add(key)
            
    glutPostRedisplay()

def teclado_especial_arriba(key, x, y):
    if key in estado.teclas:
        estado.teclas.remove(key)
    glutPostRedisplay()

def animacion():
    dt = 0.016
    estado.tiempo_global += dt
    manager.update(dt)
    
    if estado.tiempo_seleccion <= 1.0:
        estado.tiempo_seleccion += 0.007
    else:
        estado.tiempo_seleccion = 1.01 
        
    if estado.p1_stun > 0: estado.p1_stun -= dt
    if estado.p2_stun > 0: estado.p2_stun -= dt
    
    # TEMPORIZADOR PANTALLA VS
    if estado.fase_actual == "VERSUS":
        estado.tiempo_versus += dt
        # Esperamos a que el audio termine para pasar al siguiente nivel
        # Ponemos un mínimo de 1.0s por si el audio es muy corto o falla
        if estado.tiempo_versus > 1.0 and not sound_manager.is_busy(): 
            estado.fase_actual = "RONDA_INTRO" # Empieza la intro de la ronda
            manager.stop_characteristic_anim(estado.jugador1_seleccion)
            manager.stop_characteristic_anim(estado.jugador2_seleccion)
            sound_manager.stop_bgm()
            
    if estado.fase_actual in ["MAPA", "NIVEL_2", "NIVEL_3"]:
        mover_jugadores(dt)
        # Cooldowns para recolección en Nivel 3
        if estado.n3_p1_cooldown > 0: estado.n3_p1_cooldown -= dt
        if estado.n3_p2_cooldown > 0: estado.n3_p2_cooldown -= dt
        
        # ====== MOVIMIENTO DE INGREDIENTES NIVEL 3 (Vivos) ======
        if estado.fase_actual == "NIVEL_3":
            for ing in estado.n3_ingredientes:
                # 1. Movimiento tranquilo (Wandering)
                huyendo = False # Ya no huyen, solo pasean
                
                # 2. Caminar tranquilos si nadie los persigue (DENTRO DE SUS ESTABLOS)
                if not huyendo:
                    dx = ing["target_x"] - ing["x"]
                    dz = ing["target_z"] - ing["z"]
                    mag = math.sqrt(dx**2 + dz**2)
                    
                    # Usar las zonas definidas en el estado
                    limites_x = estado.n3_establous_x
                    x_min, x_max = limites_x[ing["tipo"]]
                    
                    if mag > 0.2:
                        ing["x"] += (dx/mag) * ing["velocidad"]
                        ing["z"] += (dz/mag) * ing["velocidad"]
                    
                    ing["cooldown_giro"] -= dt
                    if ing["cooldown_giro"] <= 0:
                        ing["target_x"] = random.uniform(x_min, x_max)
                        ing["target_z"] = random.uniform(-15, 4)
                        ing["cooldown_giro"] = random.uniform(2.0, 5.0)

                # Mantenerlos dentro de sus establos específicos
                x_min, x_max = estado.n3_establous_x[ing["tipo"]]
                ing["x"] = max(x_min, min(x_max, ing["x"]))
                ing["z"] = max(-15.0, min(4.5, ing["z"]))
                
    if estado.fase_actual == "NIVEL_3":
        # Decrementar timers de mensajes
        dt = 0.016 # Aprox 60fps
        if estado.n3_msg_timer_j1 > 0: estado.n3_msg_timer_j1 -= dt
        if estado.n3_msg_timer_j2 > 0: estado.n3_msg_timer_j2 -= dt
        
    if estado.fase_actual == "PODIO":
        # Forzar animación del ganador constante en el podio
        ganador_idx = estado.jugador1_seleccion if estado.ganador_nivel_actual == "J1" else estado.jugador2_seleccion
        manager.trigger_characteristic_anim(ganador_idx)
        
    glutPostRedisplay()

def mover_jugadores(dt):
    # En el nivel 3 el mapa es más grande, necesitamos más velocidad
    vel_factor = 6.5 if estado.fase_actual == "NIVEL_3" else 4.2
    vel = vel_factor * dt
    
    # Player 1 (WASD)
    moliendo_p1 = False
    if estado.p1_stun <= 0:
        next_p1 = list(estado.p1_pos)
        
        if b'w' in estado.teclas:
            next_p1[2] -= vel
            estado.p1_rot = 180
            moliendo_p1 = True
        if b's' in estado.teclas:
            next_p1[2] += vel
            estado.p1_rot = 0
            moliendo_p1 = True
        if b'a' in estado.teclas:
            next_p1[0] -= vel
            estado.p1_rot = 270
            moliendo_p1 = True
        if b'd' in estado.teclas:
            next_p1[0] += vel
            estado.p1_rot = 90
            moliendo_p1 = True
            
        if not check_limites(next_p1):
            estado.p1_pos = next_p1
            verificar_respuesta(estado.p1_pos, "J1")
        
    manager.set_walking(estado.jugador1_seleccion, moliendo_p1)
    
    # Player 2 (Arrows)
    moliendo_p2 = False
    if estado.p2_stun <= 0:
        next_p2 = list(estado.p2_pos)
        
        if GLUT_KEY_UP in estado.teclas:
            next_p2[2] -= vel
            estado.p2_rot = 180
            moliendo_p2 = True
        if GLUT_KEY_DOWN in estado.teclas:
            next_p2[2] += vel
            estado.p2_rot = 0
            moliendo_p2 = True
        if GLUT_KEY_LEFT in estado.teclas:
            next_p2[0] -= vel
            estado.p2_rot = 270
            moliendo_p2 = True
        if GLUT_KEY_RIGHT in estado.teclas:
            next_p2[0] += vel
            estado.p2_rot = 90
            moliendo_p2 = True

        if not check_limites(next_p2):
            estado.p2_pos = next_p2
            verificar_respuesta(estado.p2_pos, "J2")

    manager.set_walking(estado.jugador2_seleccion, moliendo_p2)

def check_limites(pos):
    """Evita que los niños se salgan del mapa"""
    if estado.fase_actual == "NIVEL_2":
        # Límites para la carrera escalonada
        if pos[0] < -7.0 or pos[0] > 7.0:
            return True
        if pos[2] > 10.0: # No pueden ir más atrás del inicio
            return True
        return False
    elif estado.fase_actual == "NIVEL_3":
        # Límites del mapa general
        limit = estado.map_limit - 1.0
        if abs(pos[0]) > limit or abs(pos[2]) > limit: return True
        
        # Colisión con las OLLAS (Cacerolas) - Colisión rectangular
        for pot in [estado.n3_cacerola_p1, estado.n3_cacerola_p2]:
            if abs(pos[0] - pot["x"]) < 2.5 and abs(pos[2] - pot["z"]) < 2.0:
                return True
        
        # Colisión con las TABLAS de picar
        for tab in [estado.n3_tabla_p1, estado.n3_tabla_p2]:
            if abs(pos[0] - tab["x"]) < 2.0 and abs(pos[2] - tab["z"]) < 2.0:
                return True

        # Colisión con las vallas LATERALES de los establos
        for x_fence in [-13.5, -7.5, -1.0, 5.0, 13.5, 19.5]:
            if abs(pos[0] - x_fence) < 0.5 and pos[2] < 5.0:
                return True
                
        return False
    else:
        limit = estado.map_limit - 1.0
        if abs(pos[0]) > limit or abs(pos[2]) > limit:
            return True
        return False

def verificar_respuesta(pos, jugador):
    """Verifica si un jugador chocó contra una de las cajas/plataformas"""
    radio_caja = 2.0
    
    if estado.fase_actual == "MAPA": # Nivel 1
        for blk in estado.n1_bloques:
            dx = pos[0] - blk["x"]
            dz = pos[2] - blk["z"]
            dist = math.sqrt(dx*dx + dz*dz)
            
            if dist < radio_caja:
                if blk["val"] == estado.n1_target:
                    sound_manager.play_sound(0, "happy")
                    if jugador == "J1": estado.p1_score += 1
                    else: estado.p2_score += 1
                    
                    if estado.p1_score >= estado.meta_puntos or estado.p2_score >= estado.meta_puntos:
                        print(f"¡GANÓ {jugador} EL NIVEL 1!")
                        estado.ganador_nivel_actual = jugador
                        estado.p1_score = 0
                        estado.p2_score = 0
                        estado.generar_nivel_2()
                        estado.siguiente_fase = "NIVEL_2"
                        estado.fase_actual = "PODIO"
                        estado.teclas.clear()
                        
                        # Activar animaciones de podio
                        ganador_idx = estado.jugador1_seleccion if jugador == "J1" else estado.jugador2_seleccion
                        perdedor_idx = estado.jugador2_seleccion if jugador == "J1" else estado.jugador1_seleccion
                        manager.trigger_characteristic_anim(ganador_idx)
                        manager.set_expression(ganador_idx, 5) # Feliz
                        manager.set_expression(perdedor_idx, 2) # Triste
                    else:
                        estado.generar_nivel_1()
                        estado.fase_actual = "RONDA_INTRO"
                        estado.teclas.clear()
                else:
                    sound_manager.play_sound(0, "angry")
                    pos[2] += 4.0
                break

    elif estado.fase_actual == "NIVEL_2":
        # Revisamos en qué paso de la pista va cada jugador
        paso_p1 = estado.n2_pasos_p1
        paso_p2 = estado.n2_pasos_p2
        
        if jugador == "J1":
            if paso_p1 < estado.n2_meta_pasos:
                datos_paso = estado.n2_pista_p1[paso_p1]
                # Si el J1 cruza la línea Z de las plataformas actuales...
                if pos[2] < datos_paso["z"] + 2.0:
                    # Detectar en qué carril está (Izquierdo, Centro, Derecho)
                    if pos[0] < -2.5: idx = 0
                    elif pos[0] > 2.5: idx = 2
                    else: idx = 1
                    
                    # ¿Pisó el bloque con la suma correcta?
                    if datos_paso["opciones"][idx] == datos_paso["ans"]:
                        estado.n2_pasos_p1 += 1 # ¡Avanza el nivel!
                    else:
                        pos[2] += 3.0 # Rebota hacia atrás
                        estado.p1_stun = 3.0 # Castigo de 3 segundos
            else:
                # Ya completó las sumas, ahora debe llegar al CENTRO del piso verde final
                meta_z = 2.0 - (estado.n2_meta_pasos * 10.0)
                if pos[2] < meta_z: # Centro de la plataforma verde
                    print("¡JUGADOR 1 GANA LA CARRERA!")
                    estado.ganador_nivel_actual = "J1"
                    estado.teclas.clear()
                    manager.trigger_characteristic_anim(estado.jugador1_seleccion)
                    manager.set_expression(estado.jugador1_seleccion, 5)
                    manager.set_expression(estado.jugador2_seleccion, 2)
                    estado.generar_nivel_3()
                    estado.siguiente_fase = "NIVEL_3"
                    estado.fase_actual = "PODIO"
                    
        # LO MISMO PARA EL JUGADOR 2
        elif jugador == "J2":
            if paso_p2 < estado.n2_meta_pasos:
                datos_paso = estado.n2_pista_p2[paso_p2]
                if pos[2] < datos_paso["z"] + 2.0:
                    if pos[0] < -2.5: idx = 0
                    elif pos[0] > 2.5: idx = 2
                    else: idx = 1
                    
                    if datos_paso["opciones"][idx] == datos_paso["ans"]:
                        estado.n2_pasos_p2 += 1
                    else:
                        pos[2] += 3.0
                        estado.p2_stun = 3.0
            else:
                # Camino al CENTRO del piso verde final
                meta_z = 2.0 - (estado.n2_meta_pasos * 10.0)
                if pos[2] < meta_z: # Centro de la plataforma verde
                    print("¡JUGADOR 2 GANA LA CARRERA!")
                    estado.ganador_nivel_actual = "J2"
                    estado.teclas.clear()
                    manager.trigger_characteristic_anim(estado.jugador2_seleccion)
                    manager.set_expression(estado.jugador2_seleccion, 5)
                    manager.set_expression(estado.jugador1_seleccion, 2)
                    estado.generar_nivel_3()
                    estado.siguiente_fase = "NIVEL_3"
                    estado.fase_actual = "PODIO"

    elif estado.fase_actual == "NIVEL_3":
        # Atajos para el jugador actual
        if jugador == "J1":
            hand = estado.n3_p1_hand
            hand_state = estado.n3_p1_hand_state
            olla = estado.n3_olla_p1
            tabla = estado.n3_tabla_p1
            olla_pos = estado.n3_cacerola_p1
        else:
            hand = estado.n3_p2_hand
            hand_state = estado.n3_p2_hand_state
            olla = estado.n3_olla_p2
            tabla = estado.n3_tabla_p2
            olla_pos = estado.n3_cacerola_p2

        # 1. ATRAPAR INGREDIENTES (Solo si la mano está vacía)
        if hand is None:
            for ing in estado.n3_ingredientes:
                if not ing["activo"]: continue
                dist = math.sqrt((pos[0] - ing["x"])**2 + (pos[2] - ing["z"])**2)
                if dist < 2.2: 
                    # VERIFICAR SI EL INGREDIENTE ES NECESARIO
                    if ing["tipo"] in estado.n3_receta and olla[ing["tipo"]] < estado.n3_receta[ing["tipo"]]:
                        if jugador == "J1":
                            estado.n3_p1_hand = ing["tipo"]
                            estado.n3_p1_hand_state = "crudo"
                        else:
                            estado.n3_p2_hand = ing["tipo"]
                            estado.n3_p2_hand_state = "crudo"
                        
                        sound_manager.play_sound(0, "jump") 
                    else:
                        # INGREDIENTE EQUIVOCADO O YA LLENO -> PENALIZACIÓN
                        sound_manager.play_sound(0, "angry")
                        if jugador == "J1": 
                            estado.p1_stun = 2.0
                            estado.n3_msg_j1 = "INGREDIENTE INCORRECTO" if ing["tipo"] not in estado.n3_receta else "INGREDIENTE COMPLETO"
                            estado.n3_msg_timer_j1 = 2.0
                        else: 
                            estado.p2_stun = 2.0
                            estado.n3_msg_j2 = "INGREDIENTE INCORRECTO" if ing["tipo"] not in estado.n3_receta else "INGREDIENTE COMPLETO"
                            estado.n3_msg_timer_j2 = 2.0
                        
                        # TELETRANSPORTE A LA ENTRADA DEL ESTABLO
                        x_min, x_max = estado.n3_establous_x[ing["tipo"]]
                        pos[0] = (x_min + x_max) / 2.0
                        pos[2] = 7.0 # Justo afuera en la cocina
                        print(f"¡{jugador} intentó agarrar {ing['tipo']} por error!")

                    # El ingrediente se reposiciona siempre EN SU ESTABLO
                    x_min, x_max = estado.n3_establous_x[ing["tipo"]]
                    ing["x"] = random.uniform(x_min, x_max)
                    ing["z"] = random.uniform(-15, 0) # En la zona de granja
                    break

        # 1.5 OBTENER LECHE DE LAS VACAS LECHERAS
        if hand is None:
            for v in estado.n3_vacas_lecheras:
                dist_v = math.sqrt((pos[0] - v["x"])**2 + (pos[2] - v["z"])**2)
                if dist_v < 2.0:
                    # ¿Se necesita leche en la receta?
                    if "Leche" in estado.n3_receta and olla["Leche"] < estado.n3_receta["Leche"]:
                        if jugador == "J1":
                            estado.n3_p1_hand = "Leche"
                            estado.n3_p1_hand_state = "picado" # La leche no se corta
                        else:
                            estado.n3_p2_hand = "Leche"
                            estado.n3_p2_hand_state = "picado"
                        sound_manager.play_sound(0, "happy")
                    else:
                        # No se necesita leche
                        sound_manager.play_sound(0, "angry")
                        if jugador == "J1": 
                            estado.p1_stun = 2.0
                            estado.n3_msg_j1 = "INGREDIENTE INCORRECTO" if "Leche" not in estado.n3_receta else "INGREDIENTE COMPLETO"
                            estado.n3_msg_timer_j1 = 2.0
                            x_min, x_max = estado.n3_establous_x["Leche"]
                            pos[0] = (x_min + x_max) / 2.0
                            pos[2] = 7.0
                        else: 
                            estado.p2_stun = 2.0
                            estado.n3_msg_j2 = "INGREDIENTE INCORRECTO" if "Leche" not in estado.n3_receta else "INGREDIENTE COMPLETO"
                            estado.n3_msg_timer_j2 = 2.0
                            x_min, x_max = estado.n3_establous_x["Leche"]
                            pos[0] = (x_min + x_max) / 2.0
                            pos[2] = 7.0
                    break

        # 2. TABLA DE PICAR (Procesar el ingrediente en mano)
        dist_tabla = math.sqrt((pos[0] - tabla["x"])**2 + (pos[2] - tabla["z"])**2)
        if dist_tabla < 3.0 and hand is not None and hand_state == "crudo":
            if jugador == "J1": estado.n3_p1_hand_state = "picado"
            else: estado.n3_p2_hand_state = "picado"
            sound_manager.play_sound(0, "walk")
            print(f"¡{jugador} picó el {hand}!")

        # 3. ENTREGAR EN LA OLLA
        dist_olla_j1 = math.sqrt((pos[0] - estado.n3_cacerola_p1["x"])**2 + (pos[2] - estado.n3_cacerola_p1["z"])**2)
        dist_olla_j2 = math.sqrt((pos[0] - estado.n3_cacerola_p2["x"])**2 + (pos[2] - estado.n3_cacerola_p2["z"])**2)
        
        # Definir la distancia a la olla propia para el chequeo principal
        dist_olla = dist_olla_j1 if jugador == "J1" else dist_olla_j2
        
        # Verificar cercanía a la olla incorrecta
        if (jugador == "J1" and dist_olla_j2 < 3.0) or (jugador == "J2" and dist_olla_j1 < 3.0):
            if estado.tiempo_global % 0.5 < 0.1: # Evitar spam de print
                 print(f"¡{jugador} intentó usar la olla del oponente!")
            if jugador == "J1":
                estado.n3_msg_j1 = "¡ESA NO ES TU CAZUELA!"
                estado.n3_msg_timer_j1 = 1.5
            else:
                estado.n3_msg_j2 = "¡ESA NO ES TU CAZUELA!"
                estado.n3_msg_timer_j2 = 1.5

        if dist_olla < 3.0 and hand is not None:
            if hand_state == "picado":
                # Verificar si aún se necesita este ingrediente según la receta
                if olla[hand] < estado.n3_receta[hand]:
                    olla[hand] += 1
                    sound_manager.play_sound(0, "happy")
                    # Vaciar mano
                    if jugador == "J1": 
                        estado.n3_p1_hand = None
                        estado.n3_msg_j1 = "¡BIEN HECHO!"
                        estado.n3_msg_timer_j1 = 1.0
                    else: 
                        estado.n3_p2_hand = None
                        estado.n3_msg_j2 = "¡BIEN HECHO!"
                        estado.n3_msg_timer_j2 = 1.0
                    
                    # ¿COMPLETÓ LA RECETA?
                    win_j1 = all(estado.n3_olla_p1.get(t, 0) >= q for t, q in estado.n3_receta.items())
                    win_j2 = all(estado.n3_olla_p2.get(t, 0) >= q for t, q in estado.n3_receta.items())
                    
                    if win_j1:
                        print("¡JUGADOR 1 GANA EL BANQUETE!")
                        estado.wins_j1 += 1
                        estado.ganador_nivel_actual = "J1"
                        estado.siguiente_fase = "GANADOR"
                        estado.fase_actual = "PODIO"
                    elif win_j2:
                        print("¡JUGADOR 2 GANA EL BANQUETE!")
                        estado.wins_j2 += 1
                        estado.ganador_nivel_actual = "J2"
                        estado.siguiente_fase = "GANADOR"
                        estado.fase_actual = "PODIO"
                else:
                    # Ya tiene suficientes de ese ingrediente
                    sound_manager.play_sound(0, "angry")
                    if jugador == "J1": 
                        estado.p1_stun = 2.0
                        estado.n3_msg_j1 = "YA TIENES ESE INGREDIENTE"
                        estado.n3_msg_timer_j1 = 2.0
                    else: 
                        estado.p2_stun = 2.0
                        estado.n3_msg_j2 = "YA TIENES ESE INGREDIENTE"
                        estado.n3_msg_timer_j2 = 2.0
                    pos[2] -= 4.0 # Rebote
            else:
                # No se puede entregar crudo
                sound_manager.play_sound(0, "angry")
                if jugador == "J1": 
                    estado.p1_stun = 2.0
                    estado.n3_msg_j1 = "VE A LA TABLA A PICAR"
                    estado.n3_msg_timer_j1 = 2.0
                else: 
                    estado.p2_stun = 2.0
                    estado.n3_msg_j2 = "VE A LA TABLA A PICAR"
                    estado.n3_msg_timer_j2 = 2.0
                pos[2] -= 4.0 # Rebote

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1280, 720) 
    glutCreateWindow(b"Numy Play - Arcade Selection")
    glutFullScreen() # Pantalla completa desde el inicio
    
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado_normal)
    glutKeyboardUpFunc(teclado_arriba)
    glutSpecialFunc(teclado_especial)
    glutSpecialUpFunc(teclado_especial_arriba)
    glutIdleFunc(animacion)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
