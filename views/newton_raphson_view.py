import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from metodos.metodosEncontrarRaices.metodosAbiertos import *  # Asegúrate que la ruta sea correcta
from metodos.usoGeneralFunicones import usoVariablesSympy as uv


class NewtonRaphsonView(BaseView):
    def build(self):
        self.columnconfigure(0, weight=1)

        # --- Panel de Entrada ---
        input_frame = ttk.LabelFrame(self, text="Parámetros de Entrada")
        input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ttk.Label(input_frame, text="Función f(x):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_f = ttk.Entry(input_frame, width=30)
        self.entry_f.grid(row=0, column=1, padx=5, pady=5)

        # Botón para jalar función del FunctionManager
        ttk.Button(input_frame, text="Usar Seleccionada", command=self._get_from_manager).grid(row=0, column=2, padx=5)

        ttk.Label(input_frame, text="x0 (Punto Inicial):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_x0 = ttk.Entry(input_frame, width=15)
        self.entry_x0.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(input_frame, text="Calcular", command=self._calculate).grid(row=2, column=1, pady=10)

        # --- Tabla de Resultados ---
        table_frame = ttk.LabelFrame(self, text="Iteraciones")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.rowconfigure(1, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=("i", "xi", "error"), show="headings")
        self.tree.heading("i", text="Iteración")
        self.tree.heading("xi", text="xi")
        self.tree.heading("error", text="Error Relativo")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Resultado Final ---
        self.lbl_res = ttk.Label(self, text="Raíz: -", font=("Arial", 12, "bold"))
        self.lbl_res.grid(row=2, column=0, pady=5)

    def _get_from_manager(self):
        # Accedemos al app -> layout -> function_manager (ajusta según tu estructura real)
        try:
            # Buscamos la instancia de FunctionManager a través del root/layout
            func = self.master.master.layout.function_manager.get_selected_function()
            if func:
                self.entry_f.delete(0, tk.END)
                self.entry_f.insert(0, func)
        except:
            messagebox.showwarning("Aviso", "No se pudo obtener la función seleccionada.")

    def _calculate(self):
        try:
            f_str = self.entry_f.get()
            x0 = float(self.entry_x0.get())

            # Limpiar tabla
            for i in self.tree.get_children(): self.tree.delete(i)

            # Necesitamos que tu método devuelva la lista de iteraciones para llenar la tabla
            # Si tu método actual en metodosAbiertos solo imprime,
            # deberías modificarlo para que retorne (raiz, lista_iteraciones)

            f_eval = uv.deStringAFuncionEvaluable(f_str)
            f_sym = uv.deStringAFuncionSimbolica(f_str)

            # Llamada al método (asumiendo una versión que retorne datos)
            raiz = newtonRaphson(f_eval, f_sym, x0)

            if raiz is not None:
                self.lbl_res.config(text=f"Raíz encontrada: {raiz:.10f}")
                # Aquí llenarías la tabla con los datos que retorne el método
            else:
                self.lbl_res.config(text="El método no convergió.")

        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")