# ============================================================
# state.py - Estado global compartido entre módulos
# ============================================================
# Almacena todas las variables de estado accedidas por
# múltiples módulos (cámara, personaje, input, update, etc.).
# ============================================================

# ─── Cámara ───
zoom = 10.0
camera_follow = True
mouse_down = False
last_mouse_x = 0
last_mouse_y = 0

# ─── Posición del pingüino ───
penguin_x = 0.0
penguin_z = 0.0
penguin_speed = 0.15

# ─── Rotación del objeto ───
rotate_x = 0.0
rotate_y = 0.0

# ─── Movimiento con flechas (estado de teclas) ───
key_up = False
key_down = False
key_left = False
key_right = False

# ─── Animación del personaje ───
walking = False
animation_angle = 0.0      # Ángulo para animación de caminar
tail_angle = 0.0           # Ángulo para cola
blink_timer = 0.0          # Temporizador para parpadeo
arm_wave_angle = 0.0       # Ángulo para mover brazos

# ─── Expresiones (happy, sad, surprised, angry, scared, neutral) ───
expression = "neutral"

# ─── Reacciones / Movimientos ───
reaction_type = None        # "jump", "spin", "shake", "wave_arms", "walk"
reaction_timer = 0
reaction_duration = 30      # Frames que dura la reacción

# ─── Escenarios (1-5) ───
current_scenario = 1        # 1=Parque, 2=Noche Ártica, 3=Playa, 4=Montaña, 5=Ciudad

# ─── Sonido ───
sound_enabled = True

# ─── HUD / UI ───
show_instructions = False
show_about = False

# ─── Límites de la escena ───
scene_bounds = {
    "x": (-8, 8),
    "z": (-8, 8)
}
