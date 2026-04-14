import tkinter as tk
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from characters import knuckles
from escenarios import escenarios
from audio import audio
from states.state import State
import actions.actions as actions

# Inicializar estado
estado = State()

class KnucklesGL(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def initgl(self):
        self._ready = True
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 10.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.8, 0.8, 0.8, 1.0])

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / self.height if self.height > 0 else 1
        gluPerspective(45, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def redraw(self):
        if not getattr(self, '_ready', False):
            return
            
        fondos = {
            1: (0.5, 0.8, 1.0,  1.0),
            2: (0.1, 0.1, 0.15, 1.0),
            3: (0.8, 0.3, 0.1,  1.0),
            4: (0.9, 0.9, 0.9,  1.0),
            5: (0.0, 0.0, 0.0,  1.0),
        }
        r, g, b, a = fondos.get(estado.escenario_actual, (0.5, 0.8, 1.0, 1.0))
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        cam_x = estado.target_x + estado.radio * math.sin(estado.phi) * math.cos(estado.theta)
        cam_y = estado.target_y + estado.radio * math.cos(estado.phi)
        cam_z = estado.target_z + estado.radio * math.sin(estado.phi) * math.sin(estado.theta)
        gluLookAt(cam_x, cam_y, cam_z, estado.target_x, estado.target_y, estado.target_z, 0, 1, 0)

        escenarios.dibujar(estado.escenario_actual)

        glPushMatrix()
        glTranslatef(0.0, estado.pos_y_knuckles, 0.0)
        knuckles.draw_knuckles_full(
            rot_brazo_i   = estado.brazo_izq,
            rot_brazo_d   = estado.brazo_der,
            rot_pierna_i  = estado.pierna_izq,
            rot_pierna_d  = estado.pierna_der,
            expresion     = estado.expresion_actual,
            tilt_brazos   = estado.tilt_brazo_actual,
            rot_cabeza    = estado.rot_cabeza,
        )
        glPopMatrix()

def mostrar_instrucciones():
    win = tk.Toplevel(ventana)
    win.title("Instrucciones")
    win.resizable(False, False)
    win.configure(bg="#1e1e2e")
    win.geometry("520x540")
    win.grab_set()

    tk.Label(win, text="🎮  Knuckles — Instrucciones",
             bg="#1e1e2e", fg="#cba6f7",
             font=("Consolas", 14, "bold")).pack(pady=(16, 4))

    separador = tk.Frame(win, bg="#cba6f7", height=2)
    separador.pack(fill="x", padx=20, pady=4)

    texto = """ANIMACIONES
  Z  →  Caminar          X  →  Saltar
  C  →  Brazos Arriba    V  →  Giro de Cabeza
  B  →  Golpear          N  →  Detener animación

EXPRESIONES FACIALES
  0  →  Normal           1  →  Guiño
  2  →  Ira              3  →  Sonrisa
  4  →  Tristeza         5  →  Sorpresa

ESCENARIOS
  T  →  Cambiar escenario (ciclo entre 6 fondos)
  (también disponibles en el menú ESCENARIOS)

CÁMARA
  Clic izq. + arrastrar  →  Rotar cámara orbital
  Rueda del ratón        →  Zoom acercar / alejar
  Flechas ↑ ↓ ← →        →  Panó vertical / horizontal
  R                      →  Resetear cámara
  +  /  -                →  Zoom teclado

SONIDO
  M  →  Activar / Silenciar todo el audio
  (también en el menú SONIDO)

GENERAL
  ESC  →  Salir del programa"""

    txt = tk.Text(win, bg="#181825", fg="#cdd6f4",
                  font=("Consolas", 10), relief="flat",
                  padx=16, pady=10, bd=0, wrap="none")
    txt.insert("1.0", texto)
    txt.configure(state="disabled")
    txt.pack(fill="both", expand=True, padx=20, pady=8)

    tk.Button(win, text="Cerrar", command=win.destroy,
              bg="#cba6f7", fg="#1e1e2e",
              font=("Consolas", 10, "bold"),
              relief="flat", padx=20, pady=6,
              cursor="hand2").pack(pady=(0, 14))

def mostrar_acerca_de():
    win = tk.Toplevel(ventana)
    win.title("Acerca de")
    win.resizable(False, False)
    win.configure(bg="#1e1e2e")
    win.geometry("400x300")
    win.grab_set()

    tk.Label(win, text="👊  Knuckles",
             bg="#1e1e2e", fg="#cba6f7",
             font=("Consolas", 16, "bold")).pack(pady=(24, 4))

    tk.Label(win, text="Creación y animación de personaje",
             bg="#1e1e2e", fg="#a6e3a1",
             font=("Consolas", 9)).pack()

    tk.Frame(win, bg="#cba6f7", height=2).pack(fill="x", padx=30, pady=12)

    tk.Label(win, text="Creador",
             bg="#1e1e2e", fg="#89b4fa",
             font=("Consolas", 9, "bold")).pack()
    tk.Label(win, text="Sebastián Ballesteros Gutiérrez",
             bg="#1e1e2e", fg="#cdd6f4",
             font=("Consolas", 12, "bold")).pack(pady=(2, 12))

    tk.Label(win, text="Institución",
             bg="#1e1e2e", fg="#89b4fa",
             font=("Consolas", 9, "bold")).pack()
    tk.Label(win, text="Instituto Tecnológico de Toluca",
             bg="#1e1e2e", fg="#cdd6f4",
             font=("Consolas", 11)).pack(pady=(2, 20))

    tk.Button(win, text="Cerrar", command=win.destroy,
              bg="#cba6f7", fg="#1e1e2e",
              font=("Consolas", 10, "bold"),
              relief="flat", padx=20, pady=6,
              cursor="hand2").pack(pady=14)

ventana = tk.Tk()
ventana.title("Knuckles 3D - Proyecto Interactivo")
ventana.geometry("800x600")
ventana.resizable(True, True)

audio.init_audio()
audio.cambiar_bgm(0)

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

m_anim = tk.Menu(barra_menu, tearoff=0)
m_anim.add_command(label="Normal (Detener)",  command=lambda: actions.set_animacion(estado, "ninguna"))
m_anim.add_separator()
m_anim.add_command(label="Caminar  [Z]",      command=lambda: actions.set_animacion(estado, "caminar"))
m_anim.add_command(label="Saltar   [X]",      command=lambda: actions.set_animacion(estado, "saltar"))
m_anim.add_command(label="Brazos Arriba  [C]",command=lambda: actions.set_animacion(estado, "brazos"))
m_anim.add_command(label="Giro de Cabeza [V]",command=lambda: actions.set_animacion(estado, "agacharse"))
m_anim.add_command(label="Golpear  [B]",      command=lambda: actions.set_animacion(estado, "golpear"))
barra_menu.add_cascade(label="ANIMACIONES", menu=m_anim)

m_exp = tk.Menu(barra_menu, tearoff=0)
m_exp.add_command(label="Normal    [0]", command=lambda: actions.set_expresion(estado, 0))
m_exp.add_command(label="Guiño     [1]", command=lambda: actions.set_expresion(estado, 1))
m_exp.add_command(label="Ira       [2]", command=lambda: actions.set_expresion(estado, 2))
m_exp.add_command(label="Sonrisa   [3]", command=lambda: actions.set_expresion(estado, 3))
m_exp.add_command(label="Tristeza  [4]", command=lambda: actions.set_expresion(estado, 4))
m_exp.add_command(label="Sorpresa  [5]", command=lambda: actions.set_expresion(estado, 5))
barra_menu.add_cascade(label="EXPRESIONES", menu=m_exp)

m_esc = tk.Menu(barra_menu, tearoff=0)
m_esc.add_command(label="Fondo Vacío          [T]", command=lambda: actions.set_escenario(estado, 0))
m_esc.add_command(label="El Parque            [T]", command=lambda: actions.set_escenario(estado, 1))
m_esc.add_command(label="El Callejón          [T]", command=lambda: actions.set_escenario(estado, 2))
m_esc.add_command(label="Campo de Batalla     [T]", command=lambda: actions.set_escenario(estado, 3))
m_esc.add_command(label="Aula de Clases       [T]", command=lambda: actions.set_escenario(estado, 4))
m_esc.add_command(label="Escenario Teatral    [T]", command=lambda: actions.set_escenario(estado, 5))
barra_menu.add_cascade(label="ESCENARIOS", menu=m_esc)

m_son = tk.Menu(barra_menu, tearoff=0)
m_son.add_command(label="Activar / Silenciar  [M]", command=actions.toggle_sonido)
barra_menu.add_cascade(label="SONIDO", menu=m_son)

barra_menu.add_command(label="INSTRUCCIONES", command=mostrar_instrucciones)
barra_menu.add_command(label="ACERCA DE", command=mostrar_acerca_de)
barra_menu.add_command(label="SALIR", command=ventana.quit)

app = KnucklesGL(ventana, width=800, height=600)
app.pack(fill=tk.BOTH, expand=tk.YES)

ventana.bind("<KeyPress>",    lambda event: actions.teclado(event, estado, app, ventana))
app.bind("<ButtonPress-1>",   lambda event: actions.raton_presionar(event, estado))
app.bind("<ButtonRelease-1>", lambda event: actions.raton_soltar(event, estado))
app.bind("<B1-Motion>",       lambda event: actions.raton_arrastrar(event, estado, app))
app.bind("<MouseWheel>",      lambda event: actions.raton_rueda(event, estado, app))

ventana.after(200, actions.actualizar_animacion, estado, app, ventana)
ventana.mainloop()
