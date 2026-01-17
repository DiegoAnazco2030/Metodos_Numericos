import tkinter as tk
from tkinter import ttk

# ===== IMPORTA AQUÍ LAS VISTAS DE LOS MÉTODOS =====
from views.empty_view import EmptyView
from views.minimos_cuadrados_view import MinimosCuadradosView
from views.newton_raphson_view import NewtonRaphsonView
from views.punto_fijo_view import PuntoFijoView
from views.secante_view import SecanteView
from views.biseccion_view import BiseccionView
from views.falsa_posicion_view import FalsaPosicionView
from views.muller_view import MullerView
from views.sistemas_ecuaciones_view import SistemasEcuacionesView
from views.leverrier_view import LeverrierFaddeevView
from views.derivadas_view import DerivadasView
from views.integrales_view import IntegralesView
from views.edos_view import EdosView
from views.edps_view import EdpsView

class MainLayout:
    def __init__(self, root):
        self.root = root

        # Frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar (izquierda) y área de contenido (derecha)
        self._create_sidebar()
        self._create_content_area()

        # Vista inicial
        self.show_view(EmptyView)

    # ==================================================
    # =============== SIDEBAR IZQUIERDO ================
    # ==================================================
    def _create_sidebar(self):
        self.sidebar = ttk.Frame(self.main_frame, width=320)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # ----- SECCIÓN FUNCIONES (Altura fija: 250px) -----
        self.func_section = ttk.Frame(self.sidebar, height=250)
        self.func_section.pack(fill=tk.X, side=tk.TOP)
        self.func_section.pack_propagate(False)

        ttk.Label(
            self.func_section,
            text="Funciones",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 4))

        # Gestor de funciones
        from app.function_manager import FunctionManager
        func_content = ttk.Frame(self.func_section)
        func_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.function_manager = FunctionManager(func_content)

        # ----- SECCIÓN MATRICES (Altura fija: 250px) -----
        self.matrix_section = ttk.Frame(self.sidebar, height=250)
        self.matrix_section.pack(fill=tk.X, side=tk.TOP)
        self.matrix_section.pack_propagate(False)

        ttk.Label(
            self.matrix_section,
            text="Matrices",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 4))

        # Gestor de matrices
        from app.matrix_manager import MatrixManager
        matrix_content = ttk.Frame(self.matrix_section)
        matrix_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.matrix_manager = MatrixManager(matrix_content)

        # ----- SECCIÓN MÉTODOS NUMÉRICOS (Resto del espacio con scroll) -----
        self.method_section = ttk.Frame(self.sidebar)
        self.method_section.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        ttk.Label(
            self.method_section,
            text="Métodos Numéricos",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 4))

        # Canvas con scrollbar para los botones
        canvas_frame = ttk.Frame(self.method_section)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        methods_content = ttk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=methods_content, anchor="nw")

        def _resize_content(event):
            canvas.itemconfig(window_id, width=event.width)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind("<Configure>", _resize_content)
        methods_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Habilitar scroll con rueda del mouse
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Crear los botones de métodos
        self._create_method_buttons(methods_content)

    # ==================================================
    # ========== BOTONES DE MÉTODOS NUMÉRICOS ===========
    # ==================================================
    def _create_method_buttons(self, parent):
        """
        Registro de botones para navegar entre métodos.
        """
        ttk.Button(
            parent,
            text="Bisección",
            command=lambda: self.show_view(BiseccionView)
        ).pack(fill=tk.X, padx=10, pady=6)

        ttk.Button(
            parent,
            text="Falsa Posición",
            command=lambda: self.show_view(FalsaPosicionView)
        ).pack(fill=tk.X, padx=10, pady=6)

        ttk.Button(
            parent,
            text="Punto Fijo",
            command=lambda: self.show_view(PuntoFijoView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # ---- Newton-Raphson ----
        ttk.Button(
            parent,
            text="Newton-Raphson",
            command=lambda: self.show_view(NewtonRaphsonView)
        ).pack(fill=tk.X, padx=10, pady=6)

        ttk.Button(
            parent,
            text="Secante",
            command=lambda: self.show_view(SecanteView)
        ).pack(fill=tk.X, padx=10, pady=6)

        ttk.Button(
            parent,
            text="Método de Müller",
            command=lambda: self.show_view(MullerView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # --- Metodos de matrices ----

        ttk.Button(
            parent,
            text="Sistemas Ax=b (Jacobi, Gauss...)",
            command=lambda: self.show_view(SistemasEcuacionesView)
        ).pack(fill=tk.X, padx=10, pady=6)

        ttk.Button(
            parent,
            text="Leverrier-Faddeev (Inversa/Eigen)",
            command=lambda: self.show_view(LeverrierFaddeevView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # ---- Mínimos Cuadrados ----
        ttk.Button(
            parent,
            text="Mínimos Cuadrados",
            command=lambda: self.show_view(MinimosCuadradosView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # ---- Derivadas Numéricas ----
        ttk.Button(
            parent,
            text="Derivadas Numéricas",
            command=lambda: self.show_view(DerivadasView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # ---- Integrales Numéricas ----
        ttk.Button(
            parent,
            text="Integrales Numéricas",
            command=lambda: self.show_view(IntegralesView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # ---- Ecuaciones diferenciales ----
        ttk.Button(
            parent,
            text="Ecuaciones diferenciales ordinarias",
            command=lambda: self.show_view(EdosView)
        ).pack(fill=tk.X, padx=10, pady=6)

        ttk.Button(
            parent,
            text="Ecuaciones diferenciales parciales",
            command=lambda: self.show_view(EdpsView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # Nota: Aquí puedes agregar más botones siguiendo el mismo formato.

    # ==================================================
    # =============== ÁREA DE CONTENIDO ================
    # ==================================================
    def _create_content_area(self):
        self.content = ttk.Frame(self.main_frame)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ==================================================
    # =============== CAMBIO DE VISTAS =================
    # ==================================================
    def show_view(self, view_class):
        """
        Destruye la vista actual y monta la nueva.
        Pasa 'self' a la vista para permitir comunicación con el FunctionManager.
        """
        for widget in self.content.winfo_children():
            widget.destroy()

        # Importante: Pasamos 'self' como segundo argumento
        view = view_class(self.content, self)
        view.pack(fill=tk.BOTH, expand=True)