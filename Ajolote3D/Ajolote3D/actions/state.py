# actions/state.py

class State:
    def __init__(self):
        # Información básica (Punto 1.1)
        self.personaje_nombre = "Lumi"
        
        # Control de Expresiones
        # Valores: "normal", "enojado", "triste", "guiño", "sorprendido"
        self.expresion = "normal"  
        
        # Control de Movimientos
        # Valores: "quieto", "caminando", "saltando", "saludo", "giro"
        self.movimiento = "quieto" 
        
        # Control de Escenarios 
        # Índice del 0 al 4
        self.escenario_actual = 0         
        
        # Control de Sonido
        self.sonido_global = True      
        
        # Interfaces 
        self.mostrar_instrucciones = False
        self.mostrar_acerca_de = False

        # Variables para cálculos de animación (frames)
        self.frame_animacion = 0.0
        self.subiendo_salto = True