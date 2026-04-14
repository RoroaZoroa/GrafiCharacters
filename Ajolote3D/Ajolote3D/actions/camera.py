from OpenGL.GLU import gluLookAt

class Camera:
    def __init__(self):
        # Valores iniciales (Vista Normal)
        self.reset_view()

    def reset_view(self):
        """1. Volver a vista normal"""
        self.eyeX, self.eyeY, self.eyeZ = 0.0, 1.5, 10.0
        self.centerX, self.centerY, self.centerZ = 0.0, 0.0, 0.0
        self.upX, self.upY, self.upZ = 0.0, 1.0, 0.0

    def move_up(self):
        """2. Mover la cámara arriba"""
        self.eyeY += 0.5

    def move_down(self):
        """3. Mover la cámara abajo"""
        self.eyeY -= 0.5

    def pan_left(self):
        """4. Paneo a la izquierda"""
        self.eyeX -= 0.5

    def pan_right(self):
        """5. Paneo a la derecha"""
        self.eyeX += 0.5

    def zoom_in(self):
        """6. Zoom hacia dentro"""
        if self.eyeZ > 2.0: # Límite para no atravesar a Lumi
            self.eyeZ -= 0.5

    def zoom_out(self):
        """7. Zoom hacia fuera"""
        self.eyeZ += 0.5

    def update(self):
        """Aplica los valores actuales a OpenGL"""
        gluLookAt(
            self.eyeX, self.eyeY, self.eyeZ,
            self.centerX, self.centerY, self.centerZ,
            self.upX, self.upY, self.upZ
        )