import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from metodos.metodosEncontrarRaices.raicesPolinomicas import Muller


class MullerView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        self.columnconfigure(0, weight=1)

        # --- PANEL DE ENTRADA ---
        input_frame = ttk.LabelFrame(self, text="Método de Müller (Raíces Reales y Complejas)")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Fila Función
        row_f = ttk.Frame(input_frame)
        row_f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row_f, text="f(x):").pack(side=tk.LEFT)
        self.entry_f = ttk.Entry(row_f)
        self.entry_f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(row_f, text="Usar Seleccionada", command=self._get_from_manager).pack(side=tk.LEFT)

        # Fila Puntos Iniciales
        row_p = ttk.Frame(input_frame)
        row_p.pack(fill=tk.X, padx=5, pady=5)

        for label, attr in [("x0:", "entry_x0"), ("x1:", "entry_x1"), ("x2:", "entry_x2")]:
            ttk.Label(row_p, text=label).pack(side=tk.LEFT, padx=(5, 0))
            setattr(self, attr, ttk.Entry(row_p, width=10))
            getattr(self, attr).pack(side=tk.LEFT, padx=5)

        ttk.Label(row_p, text="Tol:").pack(side=tk.LEFT, padx=(5, 0))
        self.entry_tol = ttk.Entry(row_p, width=10)
        self.entry_tol.insert(0, "1e-7")
        self.entry_tol.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Calcular Müller", command=self._calculate).pack(pady=10)

        # --- TABLA ---
        columns = ("it", "x", "fx", "error")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        headings = {"it": "It", "x": "Raíz Aproximada (x)", "fx": "|f(x)|", "error": "Error"}
        for col, text in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        self.tree.column("it", width=50)
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
            x0 = float(self.entry_x0.get())
            x1 = float(self.entry_x1.get())
            x2 = float(self.entry_x2.get())
            tol = float(self.entry_tol.get())

            for i in self.tree.get_children(): self.tree.delete(i)

            raiz, historial = Muller(f_str, x0, x1, x2, tol)

            for fila in historial:
                self.tree.insert("", tk.END, values=fila)

            res_text = f"{raiz.real:.10f}" + (f" + {raiz.imag:.10f}j" if abs(raiz.imag) > 1e-10 else "")
            messagebox.showinfo("Resultado", f"Raíz encontrada:\n{res_text}")

        except Exception as e:
            messagebox.showerror("Error", str(e))