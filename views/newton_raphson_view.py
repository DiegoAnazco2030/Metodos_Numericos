import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
# Importamos la nueva versión con Mayúscula
from metodos.metodosEncontrarRaices.metodosAbiertos import NewtonRaphson


class NewtonRaphsonView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        self.columnconfigure(0, weight=1)

        # --- PANEL DE ENTRADA ---
        input_frame = ttk.LabelFrame(self, text="Newton-Raphson (Entrada)")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Fila Función
        row_f = ttk.Frame(input_frame)
        row_f.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row_f, text="Función f(x):").pack(side=tk.LEFT)
        self.entry_f = ttk.Entry(row_f)
        self.entry_f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(row_f, text="Usar Seleccionada", command=self._get_from_manager).pack(side=tk.LEFT)

        # Fila Parámetros
        row_p = ttk.Frame(input_frame)
        row_p.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row_p, text="x0:").pack(side=tk.LEFT)
        self.entry_x0 = ttk.Entry(row_p, width=12)
        self.entry_x0.pack(side=tk.LEFT, padx=5)

        ttk.Label(row_p, text="Tolerancia:").pack(side=tk.LEFT, padx=5)
        self.entry_tol = ttk.Entry(row_p, width=12)
        self.entry_tol.insert(0, "1e-7")
        self.entry_tol.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Calcular", command=self._calculate).pack(pady=10)

        # --- TABLA DE RESULTADOS ---
        table_frame = ttk.LabelFrame(self, text="Iteraciones")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 4 Columnas: it, x, f(x), error
        self.tree = ttk.Treeview(table_frame, columns=("it", "x", "fx", "error"), show="headings")

        self.tree.heading("it", text="It")
        self.tree.heading("x", text="xi")
        self.tree.heading("fx", text="f(xi)")
        self.tree.heading("error", text="Error Absoluto")

        # Configuración de columnas
        self.tree.column("it", width=50, anchor=tk.CENTER)
        self.tree.column("x", width=160, anchor=tk.CENTER)
        self.tree.column("fx", width=160, anchor=tk.CENTER)
        self.tree.column("error", width=160, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def _get_from_manager(self):
        """Autocompleta desde el panel de la izquierda"""
        if self.layout and self.layout.function_manager:
            func = self.layout.function_manager.get_selected_function()
            if func:
                self.entry_f.delete(0, tk.END)
                self.entry_f.insert(0, str(func))

    def _calculate(self):
        try:
            f_str = self.entry_f.get()
            x0 = float(self.entry_x0.get())
            tol = float(self.entry_tol.get())

            # Limpiar tabla
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Llamada a la nueva función NewtonRaphson
            raiz, historial = NewtonRaphson(f_str, x0, 50, tol)

            # Llenar la tabla de la GUI
            for fila in historial:
                self.tree.insert("", tk.END, values=fila)

            messagebox.showinfo("Éxito", f"Raíz encontrada: {raiz:.10f}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")