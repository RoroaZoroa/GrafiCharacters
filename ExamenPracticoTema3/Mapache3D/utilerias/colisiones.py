import math
from OpenGL.GL import *

class ColisionManager:
    def __init__(self):
        # Objetos un poco más grandes y con posiciones claras
        self.objetos = [
            {"pos": [2.5, -0.5, -3.0], "color": [1.0, 0.2, 0.2], "activo": True}, # Rojo brillante
            {"pos": [-2.5, -0.5, -4.0], "color": [0.2, 1.0, 0.2], "activo": True}, # Verde neón
            {"pos": [0.0, -0.5, -6.0], "color": [0.2, 0.2, 1.0], "activo": True}   # Azul eléctrico
        ]
        self.radio_miko = 0.8   # Aumentamos un poco el rango de Miko
        self.radio_objeto = 0.6  # Objetos más grandes

    def dibujar_objetos(self):
        for obj in self.objetos:
            if obj["activo"]:
                glPushMatrix()
                glTranslatef(*obj["pos"])
                glColor3f(*obj["color"])
                # Dibujamos el cubo más grande (0.8 en lugar de 0.4)
                self.draw_cube(0.8) 
                glPopMatrix()

    def draw_cube(self, size):
        s = size / 2
        glBegin(GL_QUADS)
        # Cara frontal
        glVertex3f(-s, s, s); glVertex3f(s, s, s); glVertex3f(s, -s, s); glVertex3f(-s, -s, s)
        # Cara superior (para que se vea desde arriba)
        glVertex3f(-s, s, -s); glVertex3f(s, s, -s); glVertex3f(s, s, s); glVertex3f(-s, s, s)
        glEnd()

    def verificar_colisiones(self, pos_miko_x, pos_miko_z, state, sonido):
        for obj in self.objetos:
            if obj["activo"]:
                dist = math.sqrt((obj["pos"][0] - pos_miko_x)**2 + (obj["pos"][2] - pos_miko_z)**2)
                
                if dist < (self.radio_miko + self.radio_objeto):
                    obj["activo"] = False
                    # --- CAMBIO DE COLOR ---
                    # Guardamos el color del objeto en el estado de Miko
                    state.color_miko = obj["color"] 
                    state.expresion = "sorprendido"
                    sonido.reproducir_efecto("sorprendido")
                    return True
        return False

    def reset_objetos(self):
        """Activa de nuevo todos los objetos para que Miko pueda chocar con ellos."""
        for obj in self.objetos:
            obj["activo"] = True