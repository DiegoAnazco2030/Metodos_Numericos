import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from views.matrix_widget import MatrixWidget

# Importamos la lógica matemática
from metodos.metodosMatrices.logica_matrices import (
    MetodoJacobi, MetodoGaussSeidel, EliminacionGaussiana, MetodoCholesky
)

class SistemasEcuacionesView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        # Dividir pantalla: Izquierda (Config) | Derecha (Resultados)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ==========================================
        # PANEL IZQUIERDO: MATRIZ Y CONFIGURACIÓN
        # ==========================================
        left_panel = ttk.Frame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 1. Widget de Matriz (Reutilizable)
        lbl_mat = ttk.LabelFrame(left_panel, text="Sistema de Ecuaciones (Ax = b)")
        lbl_mat.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.matrix_widget = MatrixWidget(lbl_mat)
        self.matrix_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 2. Configuración del Método
        lbl_cfg = ttk.LabelFrame(left_panel, text="Configuración")
        lbl_cfg.pack(fill=tk.X, pady=5)

        # Selector de Método
        row1 = ttk.Frame(lbl_cfg)
        row1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row1, text="Método:").pack(side=tk.LEFT)
        self.combo_metodo = ttk.Combobox(row1, state="readonly", values=[
            "Jacobi", 
            "Gauss-Seidel", 
            "Eliminación Gaussiana", 
            "Cholesky"
        ])
        self.combo_metodo.current(0) # Seleccionar Jacobi por defecto
        self.combo_metodo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.combo_metodo.bind("<<ComboboxSelected>>", self._toggle_iter_inputs)

        # Parámetros (Tol, Max Iter)
        self.frame_params = ttk.Frame(lbl_cfg)
        self.frame_params.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.frame_params, text="Tolerancia:").pack(side=tk.LEFT)
        self.entry_tol = ttk.Entry(self.frame_params, width=10)
        self.entry_tol.insert(0, "1e-6")
        self.entry_tol.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.frame_params, text="Max Iter:").pack(side=tk.LEFT)
        self.entry_iter = ttk.Entry(self.frame_params, width=10)
        self.entry_iter.insert(0, "100")
        self.entry_iter.pack(side=tk.LEFT, padx=5)

        # Botón Calcular
        ttk.Button(lbl_cfg, text="Calcular Solución", command=self._calculate).pack(fill=tk.X, padx=10, pady=10)

        # ==========================================
        # PANEL DERECHO: RESULTADOS
        # ==========================================
        right_panel = ttk.LabelFrame(self, text="Resultados")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Área de texto para la solución final
        self.txt_result = tk.Text(right_panel, height=8, bg="#f0f0f0", font=("Consolas", 10))
        self.txt_result.pack(fill=tk.X, padx=5, pady=5)

        # Tabla para iteraciones (Solo visible en Jacobi/Seidel)
        self.lbl_iter = ttk.Label(right_panel, text="Historial de Iteraciones:")
        self.lbl_iter.pack(anchor="w", padx=5)

        columns = ("iter", "x", "error")
        self.tree = ttk.Treeview(right_panel, columns=columns, show="headings")
        self.tree.heading("iter", text="It")
        self.tree.heading("x", text="Vector x aproximado")
        self.tree.heading("error", text="Error Norma")
        
        self.tree.column("iter", width=40, anchor="center")
        self.tree.column("x", width=200, anchor="w")
        self.tree.column("error", width=100, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _toggle_iter_inputs(self, event=None):
        """Oculta los inputs de iteración si el método es directo (Gauss/Cholesky)"""
        metodo = self.combo_metodo.get()
        if metodo in ["Eliminación Gaussiana", "Cholesky"]:
            # Ocultar visualmente pero mantener en memoria
            for widget in self.frame_params.winfo_children():
                widget.configure(state='disabled')
        else:
            for widget in self.frame_params.winfo_children():
                widget.configure(state='normal')

    def _calculate(self):
        try:
            # 1. Obtener Matriz y Vector del Widget
            A, b = self.matrix_widget.get_matrix_system()
            
            # 2. Obtener parámetros
            metodo = self.combo_metodo.get()
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_iter.get())

            resultado = None
            extras = None

            # 3. Selección del algoritmo
            if metodo == "Jacobi":
                resultado, extras = MetodoJacobi(A, b, tol, max_iter)
            elif metodo == "Gauss-Seidel":
                resultado, extras = MetodoGaussSeidel(A, b, tol, max_iter)
            elif metodo == "Eliminación Gaussiana":
                resultado, extras = EliminacionGaussiana(A, b) # extras es []
            elif metodo == "Cholesky":
                resultado, extras = MetodoCholesky(A, b) # extras es L

            # 4. Mostrar Resultados
            self._display_results(resultado, extras, metodo)

        except ValueError as ve:
            messagebox.showerror("Error Matemático", str(ve))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")

    def _display_results(self, x, extras, metodo):
        # Limpiar
        self.txt_result.delete("1.0", tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Mostrar Vector Solución X
        res_str = f"Solución encontrada para {metodo}:\n\n"
        for i, val in enumerate(x):
            res_str += f"x{i+1} = {val:.8f}\n"
        self.txt_result.insert(tk.END, res_str)

        # Mostrar Iteraciones (Si existen en extras y es una lista)
        if metodo in ["Jacobi", "Gauss-Seidel"] and isinstance(extras, list):
            self.lbl_iter.config(text="Historial de Convergencia:")
            for paso in extras:
                # Formatear el vector x para que quepa en la tabla
                vec_str = "[" + ", ".join([f"{v:.4f}" for v in paso['x']]) + "]"
                self.tree.insert("", tk.END, values=(
                    paso['iter'], 
                    vec_str, 
                    f"{paso['error']:.2e}"
                ))
        
        elif metodo == "Cholesky":
            self.lbl_iter.config(text="Matriz L (Triangular Inferior):")
            # Usamos el treeview para mostrar la matriz L de forma improvisada
            self.tree.heading("x", text="Filas de L")
            self.tree.heading("error", text="")
            for i, row in enumerate(extras):
                row_str = "[" + ", ".join([f"{v:.4f}" for v in row]) + "]"
                self.tree.insert("", tk.END, values=(f"Fila {i+1}", row_str, ""))