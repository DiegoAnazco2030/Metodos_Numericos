import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from metodos.metodosEncontrarRaices.metodosAbiertos import Secante


class SecanteView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        self.columnconfigure(0, weight=1)

        # --- PANEL DE ENTRADA ---
        input_frame = ttk.LabelFrame(self, text="Método de la Secante")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # f(x)
        row_f = ttk.Frame(input_frame)
        row_f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row_f, text="Función f(x):").pack(side=tk.LEFT)
        self.entry_f = ttk.Entry(row_f)
        self.entry_f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(row_f, text="Usar Seleccionada", command=self._get_from_manager).pack(side=tk.LEFT)

        # Puntos Iniciales y Tolerancia
        row_p = ttk.Frame(input_frame)
        row_p.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(row_p, text="x0:").pack(side=tk.LEFT)
        self.entry_x0 = ttk.Entry(row_p, width=10)
        self.entry_x0.pack(side=tk.LEFT, padx=5)

        ttk.Label(row_p, text="x1:").pack(side=tk.LEFT, padx=5)
        self.entry_x1 = ttk.Entry(row_p, width=10)
        self.entry_x1.pack(side=tk.LEFT, padx=5)

        ttk.Label(row_p, text="Tol:").pack(side=tk.LEFT, padx=5)
        self.entry_tol = ttk.Entry(row_p, width=10)
        self.entry_tol.insert(0, "1e-7")
        self.entry_tol.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Calcular Secante", command=self._calculate).pack(pady=10)

        # --- TABLA CON 5 COLUMNAS ---
        self.tree = ttk.Treeview(self, columns=("it", "x0", "x1", "fx", "error"), show="headings")

        self.tree.heading("it", text="It")
        self.tree.heading("x0", text="xi-1")
        self.tree.heading("x1", text="xi")
        self.tree.heading("fx", text="f(xi)")
        self.tree.heading("error", text="Error")

        self.tree.column("it", width=40, anchor=tk.CENTER)
        self.tree.column("x0", width=140, anchor=tk.CENTER)
        self.tree.column("x1", width=140, anchor=tk.CENTER)
        self.tree.column("fx", width=140, anchor=tk.CENTER)
        self.tree.column("error", width=140, anchor=tk.CENTER)

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
            tol = float(self.entry_tol.get())

            for i in self.tree.get_children(): self.tree.delete(i)

            raiz, historial = Secante(f_str, x0, x1, tol)

            for fila in historial:
                self.tree.insert("", tk.END, values=fila)

            messagebox.showinfo("Resultado", f"Raíz encontrada: {raiz:.10f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))