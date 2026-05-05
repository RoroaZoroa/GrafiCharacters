import math
import personajes.ajolote as ajolote
import personajes.chef as chef
import personajes.knuckles as knuckles
import personajes.mapache as mapache
import personajes.pinguino as pinguino
import personajes.robot as robot

class CharacterManager:
    def __init__(self):
        self.timers = [0.0] * 6
        # Estado para Knuckles
        self.knuckles_anim = {
            "punch": 0.0,
            "expresion": 0
        }
        # Temporizador para la animación especial (para que no sea infinita)
        self.special_timer = 0.0
        self.current_special_idx = -1
        
    def update(self, dt):
        for i in range(6):
            self.timers[i] += dt
        
        # Control del temporizador de animación especial
        if self.special_timer > 0:
            self.special_timer -= dt
            if self.special_timer <= 0:
                self.stop_characteristic_anim(self.current_special_idx)
        
        # --- AJOLOTE ---
        if hasattr(ajolote, 'state'):
            if ajolote.state.movimiento == "giro":
                # Más lento: multiplicador de 15 en lugar de 100
                ajolote.state.frame_animacion = (self.timers[0] * 15) 
            else:
                # Respiración suave
                ajolote.state.frame_animacion = math.sin(self.timers[0] * 3) * 0.2
        
        # --- KNUCKLES ---
        if self.knuckles_anim["punch"] > 0:
            # Velocidad de golpes más moderada
            self.knuckles_anim["punch"] += dt * 4
            
        # --- PINGUINO / ROBOT ---
        for mod in [pinguino, robot]:
            if hasattr(mod, 'state'):
                mod.state.blink_timer = self.timers[4 if mod == pinguino else 5]
                if mod.state.reaction_type:
                    # Velocidad de giro/animación moderada
                    mod.state.reaction_timer += dt * 0.8
                    if mod.state.reaction_timer > mod.state.reaction_duration:
                        mod.state.reaction_type = None
                        mod.state.reaction_timer = 0

    def trigger_characteristic_anim(self, index):
        """Activa la animación especial con un tiempo de vida de 3 segundos"""
        self.current_special_idx = index
        self.special_timer = 3.0 # Duración de la animación en segundos
        
        if index == 0: # Ajolote
            ajolote.state.movimiento = "giro"
        elif index == 1: # Chef
            chef.get_chef().current_action = "BANDANA"
            chef.get_chef().anim_time = 0
        elif index == 2: # Knuckles
            self.knuckles_anim["punch"] = 0.01 
            self.knuckles_anim["expresion"] = 2 
        elif index == 3: # Mapache
            mapache.state.movimiento = "bailar"
        elif index == 4: # Pinguino
            pinguino.state.reaction_type = "spin"
            pinguino.state.reaction_timer = 0
        elif index == 5: # Robot
            robot.state.reaction_type = "spin"
            robot.state.reaction_timer = 0

    def stop_characteristic_anim(self, index):
        """Detiene la animación especial"""
        self.special_timer = 0
        if index == 0: # Ajolote
            ajolote.state.movimiento = "quieto"
        elif index == 1: # Chef
            chef.get_chef().current_action = "IDLE"
        elif index == 2: # Knuckles
            self.knuckles_anim["punch"] = 0.0
            self.knuckles_anim["expresion"] = 0
        elif index == 3: # Mapache
            mapache.state.movimiento = "quieto"
        elif index == 4: # Pinguino
            pinguino.state.reaction_type = None
        elif index == 5: # Robot
            robot.state.reaction_type = None

    def set_expression(self, index, expr_idx):
        if index == 0:
            exprs = ["normal", "enojado", "triste", "sorprendido", "guiño"]
            ajolote.state.expresion = exprs[expr_idx % len(exprs)]
        elif index == 1:
            chef.get_chef().current_exp_idx = expr_idx % len(chef.get_chef().expressions)
        elif index == 2:
            self.knuckles_anim["expresion"] = expr_idx % 6
        elif index == 3:
            exprs = ["normal", "dormido", "guino", "llorando", "enojado", "triste", "sorprendido"]
            mapache.state.expresion = exprs[expr_idx % len(exprs)]
        elif index == 4:
            exprs = ["neutral", "sad", "angry", "surprised", "scared", "happy"]
            pinguino.state.expression = exprs[expr_idx % len(exprs)]
        elif index == 5:
            exprs = ["neutral", "happy", "sad", "surprised", "angry", "scared", "doubt"]
            robot.state.expression = exprs[expr_idx % len(exprs)]

manager = CharacterManager()
