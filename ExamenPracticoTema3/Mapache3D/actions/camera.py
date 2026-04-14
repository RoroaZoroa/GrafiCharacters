from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self):
        self.reset_view()

    def reset_view(self):
        self.eyeX, self.eyeY, self.eyeZ = 0.0, 1.5, 5.0
        self.centerX, self.centerY, self.centerZ = 0.0, 0.5, 0.0
        self.upX, self.upY, self.upZ = 0.0, 1.0, 0.0
        self.zoom_level = 45.0

    def update(self):
        gluLookAt(self.eyeX, self.eyeY, self.eyeZ,
                  self.centerX, self.centerY, self.centerZ,
                  self.upX, self.upY, self.upZ)

    def zoom_in(self):
        self.eyeZ -= 0.2
        if self.eyeZ < 1.5: self.eyeZ = 1.5

    def zoom_out(self):
        self.eyeZ += 0.2
        if self.eyeZ > 12.0: self.eyeZ = 12.0

    def pan_left(self): self.eyeX -= 0.2
    def pan_right(self): self.eyeX += 0.2
    def move_up(self): self.eyeY += 0.2
    def move_down(self): self.eyeY -= 0.2
    