import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from metodos.ecuacionesDiferenciales import edps


class EdpsView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)
        self.cbar = None  # Referencia para la barra de colores

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
        # Configuración de pesos: Columna 0 fija, Columna 1 expandible
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # --- PANEL IZQUIERDO: CONFIGURACION ---
        left_panel = ttk.Frame(self, width=320)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_panel.pack_propagate(False)

        ttk.Label(left_panel, text="Tipo de Ecuación (EDP):", font=("Segoe UI", 10, "bold")).pack(pady=(0, 5),
                                                                                                  anchor="w")
        self.combo_metodo = ttk.Combobox(left_panel, state="readonly", values=[
            "Ecuación Laplace (Elíptica)",
            "Ecuación Calor (Parabólica)",
            "Ecuación Onda (Hiperbólica)"
        ])
        self.combo_metodo.current(0)
        self.combo_metodo.pack(fill=tk.X, pady=5)
        self.combo_metodo.bind("<<ComboboxSelected>>", self._update_inputs)

        self.input_container = ttk.LabelFrame(left_panel, text="Parámetros del Sistema")
        self.input_container.pack(fill=tk.BOTH, expand=True, pady=10)

        self.entries = {}
        self._update_inputs(None)

        ttk.Button(left_panel, text="Resolver y Graficar", command=self._calculate).pack(pady=5, fill=tk.X)

        res_frame = ttk.LabelFrame(left_panel, text="Información")
        res_frame.pack(fill=tk.X, pady=5)
        self.lbl_info = ttk.Label(res_frame, text="Esperando ejecución...", wraplength=280, justify="left")
        self.lbl_info.pack(padx=10, pady=10)

        # --- PANEL DERECHO: GRAFICO ---
        right_panel = ttk.Frame(self)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_panel = right_panel

        # Creamos la figura y los ejes con posiciones fijas para que la malla no se mueva
        self.fig = plt.Figure(figsize=(6, 5), dpi=100)

        # add_axes([izquierda, abajo, ancho, alto]) en escala 0 a 1
        self.ax = self.fig.add_axes([0.1, 0.12, 0.70, 0.78])
        self.cax = self.fig.add_axes([0.83, 0.12, 0.03, 0.78])

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _clear_inputs(self):
        for widget in self.input_container.winfo_children():
            widget.destroy()
        self.entries = {}

    def _add_input(self, label_text, key, default_val="", width=15):
        frame = ttk.Frame(self.input_container)
        frame.pack(fill=tk.X, pady=3, padx=5)
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT)
        entry = ttk.Entry(frame, width=width)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))
        if default_val:
            entry.insert(0, str(default_val))
        self.entries[key] = entry

    def _update_inputs(self, event):
        self._clear_inputs()
        metodo = self.combo_metodo.get()

        if "Laplace" in metodo:
            self._add_input("Puntos X (nx):", "nx", "15")
            self._add_input("Puntos Y (ny):", "ny", "15")
            self._add_input("Borde Izq (T):", "te", "75")
            self._add_input("Borde Der (T):", "td", "50")
            self._add_input("Borde Arriba (T):", "ta", "100")
            self._add_input("Borde Abajo (T):", "tb", "0")
            self._add_input("Iteraciones:", "iter", "200")

        elif "Calor" in metodo or "Onda" in metodo:
            self._add_input("Cond. Inicial f(x):", "func", "np.sin(np.pi*x)")
            self._add_input("Longitud (L):", "len", "1.0")
            self._add_input("Tiempo (t):", "time", "0.5")
            self._add_input("Puntos Espacio:", "nx", "20")
            self._add_input("Puntos Tiempo:", "nt", "100")

            if "Calor" in metodo:
                self._add_input("Difusividad (α):", "alpha", "1.0")
            else:
                self._add_input("Velocidad (c):", "vel", "1.0")

    def _calculate(self):
        try:
            metodo = self.combo_metodo.get()

            # Limpiamos ambos ejes para el nuevo dibujo
            self.ax.clear()
            self.cax.clear()

            msg_aux = ""

            if "Laplace" in metodo:
                nx, ny = int(self.entries["nx"].get()), int(self.entries["ny"].get())
                te, td = float(self.entries["te"].get()), float(self.entries["td"].get())
                ta, tb = float(self.entries["ta"].get()), float(self.entries["tb"].get())
                iters = int(self.entries["iter"].get())

                T, historial = edps.resolverLaplace(nx, ny, iters, 1e-4, te, td, ta, tb)
                im = self.ax.imshow(T, cmap='magma', interpolation='bilinear', origin='upper')

                self.fig.colorbar(im, cax=self.cax)  # Usamos el eje reservado
                self.ax.set_title("Laplace: Distribución Térmica")
                msg_aux = f"Estado estable alcanzado.\nError: {historial[-1]:.2e}"

            elif "Calor" in metodo:
                func, L = self.entries["func"].get(), float(self.entries["len"].get())
                t_total, nx, nt = float(self.entries["time"].get()), int(self.entries["nx"].get()), int(
                    self.entries["nt"].get())
                alpha = float(self.entries["alpha"].get())

                u, x, msg = edps.resolverCalorExplicito(func, L, t_total, nx, nt, alpha)
                im = self.ax.imshow(u, extent=[0, L, t_total, 0], aspect='auto', cmap='hot')

                self.fig.colorbar(im, cax=self.cax)
                self.ax.set_title("Calor: Difusión en el Tiempo")
                self.ax.set_xlabel("Posición (x)")
                self.ax.set_ylabel("Tiempo (t)")
                msg_aux = msg if msg else "Simulación completa."

            elif "Onda" in metodo:
                func, L = self.entries["func"].get(), float(self.entries["len"].get())
                t_total, nx, nt = float(self.entries["time"].get()), int(self.entries["nx"].get()), int(
                    self.entries["nt"].get())
                c = float(self.entries["vel"].get())

                u, x, msg = edps.resolverOnda(func, L, t_total, nx, nt, c)
                im = self.ax.imshow(u, extent=[0, L, t_total, 0], aspect='auto', cmap='RdBu_r')

                self.fig.colorbar(im, cax=self.cax)
                self.ax.set_title("Onda: Propagación de Perturbación")
                self.ax.set_xlabel("Posición (x)")
                self.ax.set_ylabel("Tiempo (t)")
                msg_aux = msg if msg else "Oscilación calculada."

            self.lbl_info.config(text=msg_aux)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")