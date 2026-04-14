class State:
    def __init__(self):
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.color_miko = [1.0, 1.0, 1.0] #color inicial de Miko

        self.escenario_actual = 0  
        
        self.expresion = "normal"
        
        self.movimiento = "quieto"
        
        self.mostrar_instrucciones = True
        self.mostrar_acerca_de = False 
        self.mute = False
        
        self.frame_animacion = 0.0

    def reset(self):
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.color_miko = [1.0, 1.0, 1.0]
        self.expresion = "normal"
        self.movimiento = "quieto"
        self.frame_animacion = 0.0
        self.mostrar_acerca_de = False

  