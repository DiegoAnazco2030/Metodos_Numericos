import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from metodos.metodosEncontrarRaices.metodosCerrados import FalsaPosicion


class FalsaPosicionView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        self.columnconfigure(0, weight=1)

        input_frame = ttk.LabelFrame(self, text="Método de Falsa Posición")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Fila Función
        row_f = ttk.Frame(input_frame)
        row_f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row_f, text="f(x):").pack(side=tk.LEFT)
        self.entry_f = ttk.Entry(row_f)
        self.entry_f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(row_f, text="Usar Seleccionada", command=self._get_from_manager).pack(side=tk.LEFT)

        # Fila Parámetros
        row_p = ttk.Frame(input_frame)
        row_p.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row_p, text="a (Inf):").pack(side=tk.LEFT)
        self.entry_a = ttk.Entry(row_p, width=10)
        self.entry_a.pack(side=tk.LEFT, padx=5)

        ttk.Label(row_p, text="b (Sup):").pack(side=tk.LEFT, padx=5)
        self.entry_b = ttk.Entry(row_p, width=10)
        self.entry_b.pack(side=tk.LEFT, padx=5)

        ttk.Label(row_p, text="Tol (%):").pack(side=tk.LEFT, padx=5)
        self.entry_tol = ttk.Entry(row_p, width=10)
        self.entry_tol.insert(0, "0.0001")
        self.entry_tol.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Calcular Falsa Posición", command=self._calculate).pack(pady=10)

        # --- TABLA ---
        columns = ("it", "a", "b", "xr", "fxr", "error")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        headings = {"it": "It", "a": "Lim. Inf (a)", "b": "Lim. Sup (b)",
                    "xr": "Posición (xr)", "fxr": "f(xr)", "error": "Error (%)"}

        for col, text in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=120, anchor=tk.CENTER)

        self.tree.column("it", width=40)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _get_from_manager(self):
        if self.layout and self.layout.function_manager:
            func = self.layout.function_manager.get_selected_function()
            if func:
                self.entry_f.delete(0, tk.END)
                self.entry_f.insert(0, str(func))

    def _calculate(self):
        try:
            f_str = self.entry_f.get()
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            tol = float(self.entry_tol.get())

            for i in self.tree.get_children(): self.tree.delete(i)

            raiz, historial = FalsaPosicion(f_str, a, b, tol)

            for fila in historial:
                self.tree.insert("", tk.END, values=fila)

            messagebox.showinfo("Resultado", f"Raíz encontrada: {raiz:.10f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))