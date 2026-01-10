import tkinter as tk
from tkinter import ttk

# ===== IMPORTA AQUÍ LAS VISTAS DE LOS MÉTODOS =====
from views.empty_view import EmptyView
from views.minimos_cuadrados_view import MinimosCuadradosView
from views.newton_raphson_view import NewtonRaphsonView
# Descomenta estas líneas conforme crees los archivos correspondientes:
from views.punto_fijo_view import PuntoFijoView
from views.secante_view import SecanteView
from views.biseccion_view import BiseccionView
from views.falsa_posicion_view import FalsaPosicionView
from views.muller_view import MullerView
from views.sistemas_ecuaciones_view import SistemasEcuacionesView

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

        # Panel dividido verticalmente (Funciones / Métodos)
        self.paned = ttk.PanedWindow(self.sidebar, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # ----- SECCIÓN FUNCIONES -----
        self.func_section = self._create_scrollable_section("Funciones")

        # Gestor de funciones (Panel Superior Izquierdo)
        from app.function_manager import FunctionManager
        self.function_manager = FunctionManager(self.func_section.content)

        # ----- SECCIÓN MÉTODOS -----
        self.method_section = self._create_scrollable_section("Métodos Numéricos")
        self._create_method_buttons(self.method_section.content)

        # Distribución de paneles
        self.paned.add(self.func_section, weight=1)
        self.paned.add(self.method_section, weight=1)

    # ==================================================
    # ========== SECCIÓN CON SCROLL REUTILIZABLE =========
    # ==================================================
    def _create_scrollable_section(self, title):
        container = ttk.Frame(self.paned)

        ttk.Label(
            container,
            text=title,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 4))

        body = ttk.Frame(container)
        body.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(body, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient=tk.VERTICAL, command=canvas.yview)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        content = ttk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        def _resize_content(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", _resize_content)
        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        container.content = content
        return container

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

        # ---- Mínimos Cuadrados ----
        ttk.Button(
            parent,
            text="Mínimos Cuadrados",
            command=lambda: self.show_view(MinimosCuadradosView)
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