import math

class State:
    def __init__(self):
        self.pos_y_knuckles  = 0.0
        self.brazo_izq       = 0.0
        self.brazo_der       = 0.0
        self.pierna_izq      = 0.0
        self.pierna_der      = 0.0
        self.tilt_brazo_actual = 45       # 45 = brazos colgando, -90 = brazos arriba
        self.rot_cabeza      = 0.0

        self.expresion_actual  = 0        # 0-5
        self.animacion_actual  = "ninguna"
        self.escenario_actual  = 0        # 0-5
        self.tiempo            = 0.0      # Reloj continuo
        self.tiempo_anim       = 0.0      # Reloj que se reinicia para animaciones de un ciclo

        # Cámara orbital
        self.radio    = 8.0
        self.theta    = 0.0
        self.phi      = math.pi / 2.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.target_z = 0.0
        self.mouse_down = False
        self.last_x = 0
        self.last_y = 0
