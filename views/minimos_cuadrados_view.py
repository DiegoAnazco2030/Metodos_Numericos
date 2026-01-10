import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from metodos.regresion.minimos_cuadrados.minimos_cuadrados import minimos_cuadrados


class MinimosCuadradosView(BaseView):

    def build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._build_table()
        self._build_results()

    # ==================================================
    # =============== TABLA DE DATOS ===================
    # ==================================================
    def _build_table(self):
        frame = ttk.LabelFrame(self, text="Datos (x, y)")
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.tree = ttk.Treeview(
            frame,
            columns=("x", "y"),
            show="headings",
            selectmode="browse"
        )
        self.tree.heading("x", text="x")
        self.tree.heading("y", text="y")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ---- Eventos para edición ----
        self.tree.bind("<Double-1>", self._edit_cell)

        btns = ttk.Frame(frame)
        btns.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btns, text="Agregar fila", command=self._add_row).pack(side=tk.LEFT)
        ttk.Button(btns, text="Eliminar fila", command=self._remove_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Calcular", command=self._calculate).pack(side=tk.RIGHT)

    # ==================================================
    # =============== RESULTADOS =======================
    # ==================================================
    def _build_results(self):
        frame = ttk.LabelFrame(self, text="Resultados")
        frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.text = tk.Text(frame, height=18)
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==================================================
    # =============== EDICIÓN DE CELDAS ================
    # ==================================================
    def _edit_cell(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not row_id or not column:
            return

        x, y, width, height = self.tree.bbox(row_id, column)

        value = self.tree.set(row_id, column)

        entry = ttk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_value(event=None):
            self.tree.set(row_id, column, entry.get())
            entry.destroy()

        entry.bind("<Return>", save_value)
        entry.bind("<FocusOut>", save_value)

    # ==================================================
    # =============== MANEJO DE FILAS ==================
    # ==================================================
    def _add_row(self):
        self.tree.insert("", tk.END, values=("", ""))

    def _remove_row(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    # ==================================================
    # =============== CÁLCULO ==========================
    # ==================================================
    def _calculate(self):
        try:
            x = []
            y = []

            for item in self.tree.get_children():
                xi, yi = self.tree.item(item)["values"]
                x.append(float(xi))
                y.append(float(yi))

            m, b, reporte, y_pred = minimos_cuadrados(x, y)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, reporte)

        self.ax.clear()
        self.ax.scatter(x, y, label="Datos")
        self.ax.plot(x, y_pred, color="red", label=f"y = {m:.4f}x + {b:.4f}")
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()
