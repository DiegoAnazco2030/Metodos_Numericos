import tkinter as tk
from tkinter import ttk

# ===== IMPORTA AQUÍ LAS VISTAS DE LOS MÉTODOS =====
# Cada método nuevo que implementes debe tener su propia vista
from views.empty_view import EmptyView
from views.minimos_cuadrados_view import MinimosCuadradosView


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

        # Aquí se crea el gestor de funciones
        from app.function_manager import FunctionManager
        self.function_manager = FunctionManager(self.func_section.content)

        # ----- SECCIÓN MÉTODOS -----
        self.method_section = self._create_scrollable_section("Métodos Numéricos")

        # AQUÍ SE AGREGAN LOS BOTONES DE LOS MÉTODOS
        self._create_method_buttons(self.method_section.content)

        # Distribución 50 / 50
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

        # Ajusta el ancho del contenido al canvas
        def _resize_content(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", _resize_content)

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Referencia pública para insertar widgets
        container.content = content
        return container

    # ==================================================
    # ========== BOTONES DE MÉTODOS NUMÉRICOS ===========
    # ==================================================
    def _create_method_buttons(self, parent):
        """
        👉 AQUÍ DEBES AGREGAR LOS BOTONES DE LOS MÉTODOS
        👉 Cada botón debe llamar a self.show_view(TuVista)
        👉 No pongas lógica matemática aquí
        """

        # ---- MÉTODO IMPLEMENTADO ----
        ttk.Button(
            parent,
            text="Mínimos Cuadrados",
            command=lambda: self.show_view(MinimosCuadradosView)
        ).pack(fill=tk.X, padx=10, pady=6)

        # ---- EJEMPLOS PARA FUTUROS MÉTODOS ----
        # (DESCOMENTA CUANDO LOS IMPLEMENTES)

        # from views.biseccion_view import BiseccionView
        # ttk.Button(
        #     parent,
        #     text="Bisección",
        #     command=lambda: self.show_view(BiseccionView)
        # ).pack(fill=tk.X, padx=10, pady=6)

        # from views.newton_view import NewtonView
        # ttk.Button(
        #     parent,
        #     text="Newton-Raphson",
        #     command=lambda: self.show_view(NewtonView)
        # ).pack(fill=tk.X, padx=10, pady=6)

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
        for widget in self.content.winfo_children():
            widget.destroy()

        view = view_class(self.content)
        view.pack(fill=tk.BOTH, expand=True)
