import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importamos los metodos del backend
from metodos.ecuacionesDiferenciales import edos


class EdosView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def destroy(self):
        """Limpiar recursos de matplotlib antes de destruir la vista."""
        try:
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.get_tk_widget().destroy()
            if hasattr(self, 'fig') and self.fig:
                plt.close(self.fig)
        except:
            pass
        super().destroy()

    def build(self):
        # Configuración de pesos para que el gráfico (col 1) crezca más que los controles (col 0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # --- PANEL IZQUIERDO: CONFIGURACION Y TABLA ---
        left_panel = ttk.Frame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 1. Selector de Metodo
        config_frame = ttk.LabelFrame(left_panel, text="Configuración EDO")
        config_frame.pack(fill=tk.X, pady=5)

        ttk.Label(config_frame, text="Método:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_metodo = ttk.Combobox(config_frame, state="readonly", values=[
            "Euler", "Heun", "Runge-Kutta 4", "RK Fehlberg (Adaptativo)", "Multipasos (Adams)"
        ])
        self.combo_metodo.current(0)
        self.combo_metodo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.combo_metodo.bind("<<ComboboxSelected>>", self._on_method_change)

        # 2. Entradas
        inputs_frame = ttk.Frame(config_frame)
        inputs_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)
        inputs_frame.columnconfigure(1, weight=1)

        # Funcion f(x,y)
        ttk.Label(inputs_frame, text="f(x,y):").grid(row=0, column=0, sticky="e")
        self.entry_f = ttk.Entry(inputs_frame)
        self.entry_f.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=2)
        ttk.Button(inputs_frame, text="<", width=3, command=self._get_from_manager).grid(row=0, column=3, padx=2)

        # x0, y0
        ttk.Label(inputs_frame, text="x0:").grid(row=1, column=0, sticky="e")
        self.entry_x0 = ttk.Entry(inputs_frame, width=10)
        self.entry_x0.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(inputs_frame, text="y0:").grid(row=1, column=2, sticky="e")
        self.entry_y0 = ttk.Entry(inputs_frame, width=10)
        self.entry_y0.grid(row=1, column=3, sticky="w", padx=5, pady=2)

        # h, n, tol
        ttk.Label(inputs_frame, text="Paso (h):").grid(row=2, column=0, sticky="e")
        self.entry_h = ttk.Entry(inputs_frame, width=10)
        self.entry_h.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        self.lbl_n = ttk.Label(inputs_frame, text="Iteraciones (n):")
        self.lbl_n.grid(row=2, column=2, sticky="e")
        self.entry_n = ttk.Entry(inputs_frame, width=10)
        self.entry_n.grid(row=2, column=3, sticky="w", padx=5, pady=2)

        # Boton Calcular
        ttk.Button(config_frame, text="Resolver EDO", command=self._calculate).grid(row=2, column=0, columnspan=2,
                                                                                    pady=10)

        # 3. Tabla de Resultados (con altura limitada para no desplazar todo)
        table_frame = ttk.LabelFrame(left_panel, text="Tabla de Iteraciones")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Limitamos la altura del Treeview (height=12 filas visibles)
        self.tree = ttk.Treeview(table_frame, show="headings", height=12)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        # --- PANEL DERECHO: GRAFICO ---
        right_panel = ttk.Frame(self)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_panel = right_panel  # Guardar referencia para recrear canvas

        # Ajustamos el tamaño de la figura para que sea legible
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.fig.tight_layout(pad=3.0)  # Evita que las etiquetas se corten
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _get_from_manager(self):
        if self.layout and self.layout.function_manager:
            func = self.layout.function_manager.get_selected_function()
            if func:
                self.entry_f.delete(0, tk.END)
                self.entry_f.insert(0, str(func))

    def _on_method_change(self, event):
        metodo = self.combo_metodo.get()
        if "Fehlberg" in metodo:
            self.lbl_n.config(text="x final:")
        else:
            self.lbl_n.config(text="Iteraciones (n):")

    def _setup_tree_columns(self, metodo):
        # Limpiar columnas previas
        self.tree["columns"] = ()

        cols = []
        headers = []

        if "Euler" in metodo:
            cols = ("it", "x", "y", "f", "ynet")
            headers = ["i", "x", "y", "f(x,y)", "y_next"]
        elif "Heun" in metodo:
            cols = ("it", "x", "y", "yp", "yc", "err")
            headers = ["i", "x", "y", "y_pred", "y_corr", "Error"]
        elif "Runge-Kutta 4" in metodo:
            cols = ("it", "x", "y", "k1", "k2", "k3", "k4", "yn")
            headers = ["i", "x", "y", "k1", "k2", "k3", "k4", "y_next"]
        elif "Fehlberg" in metodo:
            cols = ("it", "x", "y", "h", "err")
            headers = ["i", "x", "y", "h_actual", "Error Est."]
        elif "Multipasos" in metodo:
            cols = ("it", "x", "y", "info")
            headers = ["i", "x", "y", "Detalle"]

        self.tree["columns"] = cols
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=70, anchor=tk.CENTER, stretch=True)

    def _calculate(self):
        try:
            f_str = self.entry_f.get()
            if not f_str: raise ValueError("Debe ingresar f(x,y)")

            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            h = float(self.entry_h.get())
            param_n = float(self.entry_n.get())

            metodo = self.combo_metodo.get()
            self._setup_tree_columns(metodo)

            # Limpiar tabla
            for i in self.tree.get_children():
                self.tree.delete(i)

            y_res = 0
            tabla = []

            if metodo == "Euler":
                y_res, tabla = edos.metodoEuler(f_str, x0, y0, h, int(param_n))
            elif metodo == "Heun":
                y_res, tabla = edos.metodoHeun(f_str, x0, y0, h, int(param_n))
            elif metodo == "Runge-Kutta 4":
                y_res, tabla = edos.metodoRungeKutta4(f_str, x0, y0, h, int(param_n))
            elif "Fehlberg" in metodo:
                y_res, tabla = edos.metodoRKFehlberg(f_str, x0, y0, h, param_n)
            elif "Multipasos" in metodo:
                y_res, tabla = edos.metodoMultipasos(f_str, x0, y0, h, int(param_n))

            # Llenar tabla y recolectar puntos
            puntos_x, puntos_y = [], []
            for row in tabla:
                self.tree.insert("", tk.END, values=row)
                try:
                    puntos_x.append(float(row[1]))
                    puntos_y.append(float(row[2]))
                except:
                    pass

            # Actualizar Gráfico
            # Limpiar canvas anterior
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.get_tk_widget().pack_forget()
            
            self.ax.clear()
            self.ax.plot(puntos_x, puntos_y, 'b-o', markersize=4, linewidth=1, label='Solución Numérica')
            self.ax.set_title(f"Solución EDO: {metodo}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend()
            
            # Recrear canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.canvas.draw()

            messagebox.showinfo("Resultado", f"Cálculo completado.\nValor final aproximado: {y_res:.6f}")

        except ValueError as ve:
            messagebox.showerror("Error de entrada", f"Verifique los datos: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")