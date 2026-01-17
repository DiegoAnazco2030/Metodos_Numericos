import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView

# Importamos la lógica incluyendo el nuevo helper
from metodos.metodosMatrices.logica_matrices import (
    MetodoJacobi, MetodoGaussSeidel, EliminacionGaussiana, MetodoCholesky, comprobar_solucion
)

class SistemasEcuacionesView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)
        self.current_matrix = None  # Almacena (A, b)

    def build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # --- PANEL IZQUIERDO ---
        left_panel = ttk.Frame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        lbl_mat = ttk.LabelFrame(left_panel, text="Sistema de Ecuaciones (Ax = b)")
        lbl_mat.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botón para cargar matriz seleccionada
        ttk.Button(
            lbl_mat,
            text="Cargar Matriz Seleccionada",
            command=self._load_selected_matrix
        ).pack(fill=tk.X, padx=10, pady=10)
        
        # Área de visualización de la matriz cargada
        ttk.Label(lbl_mat, text="Matriz Actual:").pack(anchor="w", padx=10)
        self.txt_matrix = tk.Text(lbl_mat, height=12, bg="#f9f9f9", font=("Consolas", 9), state='disabled')
        self.txt_matrix.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        lbl_cfg = ttk.LabelFrame(left_panel, text="Configuración")
        lbl_cfg.pack(fill=tk.X, pady=5)

        row1 = ttk.Frame(lbl_cfg)
        row1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row1, text="Método:").pack(side=tk.LEFT)
        self.combo_metodo = ttk.Combobox(row1, state="readonly", values=[
            "Jacobi", "Gauss-Seidel", "Eliminación Gaussiana", "Cholesky"
        ])
        self.combo_metodo.current(0)
        self.combo_metodo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.combo_metodo.bind("<<ComboboxSelected>>", self._toggle_iter_inputs)

        self.frame_params = ttk.Frame(lbl_cfg)
        self.frame_params.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.frame_params, text="Tol:").pack(side=tk.LEFT)
        self.entry_tol = ttk.Entry(self.frame_params, width=8)
        self.entry_tol.insert(0, "1e-6")
        self.entry_tol.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.frame_params, text="Iter:").pack(side=tk.LEFT)
        self.entry_iter = ttk.Entry(self.frame_params, width=6)
        self.entry_iter.insert(0, "100")
        self.entry_iter.pack(side=tk.LEFT, padx=5)

        ttk.Button(lbl_cfg, text="Calcular Solución", command=self._calculate).pack(fill=tk.X, padx=10, pady=10)

        # --- PANEL DERECHO ---
        right_panel = ttk.LabelFrame(self, text="Resultados")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 1. Solución Final Texto
        self.txt_result = tk.Text(right_panel, height=6, bg="#f0f0f0", font=("Consolas", 10))
        self.txt_result.pack(fill=tk.X, padx=5, pady=5)

        # 2. Tabla Iteraciones
        self.lbl_iter = ttk.Label(right_panel, text="Historial de Iteraciones:")
        self.lbl_iter.pack(anchor="w", padx=5)

        cols = ("iter", "x", "error")
        self.tree = ttk.Treeview(right_panel, columns=cols, show="headings", height=8)
        self.tree.heading("iter", text="It")
        self.tree.heading("x", text="Vector x aproximado")
        self.tree.heading("error", text="Error")
        self.tree.column("iter", width=40, anchor="center")
        self.tree.column("x", width=220)
        self.tree.column("error", width=80, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 3. Comprobación (Nueva Sección)
        self.lbl_comp = ttk.Label(right_panel, text="Comprobación (Ax vs b):", font=("Segoe UI", 9, "bold"))
        self.lbl_comp.pack(anchor="w", padx=5, pady=(10,0))

        cols_comp = ("ec", "val_ax", "val_b", "diff")
        self.tree_comp = ttk.Treeview(right_panel, columns=cols_comp, show="headings", height=5)
        self.tree_comp.heading("ec", text="Ec.")
        self.tree_comp.heading("val_ax", text="(Ax) calculado")
        self.tree_comp.heading("val_b", text="Valor b esperado")
        self.tree_comp.heading("diff", text="Diferencia")
        
        self.tree_comp.column("ec", width=40, anchor="center")
        self.tree_comp.pack(fill=tk.X, expand=False, padx=5, pady=5)

    def _load_selected_matrix(self):
        """Carga la matriz seleccionada del MatrixManager"""
        if not self.layout or not hasattr(self.layout, 'matrix_manager'):
            messagebox.showerror("Error", "No se encontró el gestor de matrices.")
            return
        
        matrix_data = self.layout.matrix_manager.get_selected_matrix()
        if matrix_data is None:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una matriz del historial.")
            return
        
        self.current_matrix = matrix_data
        A, b = matrix_data
        
        # Mostrar la matriz cargada
        self.txt_matrix.config(state='normal')
        self.txt_matrix.delete("1.0", tk.END)
        
        # AQUÍ ES DONDE SE FORMATEA LA VISUALIZACIÓN
        self.txt_matrix.insert(tk.END, "Matriz A:\n")
        for row in A:
            self.txt_matrix.insert(tk.END, "  " + "  ".join(f"{val:8.3f}" for val in row) + "\n")
        
        self.txt_matrix.insert(tk.END, "\nVector b:\n")
        for val in b:
            self.txt_matrix.insert(tk.END, f"  {val:8.3f}\n")

        # Mostrar como matriz aumentada [A|b]
        self.txt_matrix.insert(tk.END, "\nMatriz Aumentada [A|b]:\n")
        for i, row in enumerate(A):
            row_str = "  " + "  ".join(f"{val:8.3f}" for val in row)
            row_str += f"  |  {b[i]:8.3f}\n"
            self.txt_matrix.insert(tk.END, row_str)
        
        self.txt_matrix.config(state='disabled')
        
        messagebox.showinfo("Éxito", f"Matriz cargada correctamente ({len(A)}x{len(A)})")

    def _toggle_iter_inputs(self, event=None):
        metodo = self.combo_metodo.get()
        state = 'disabled' if metodo in ["Eliminación Gaussiana", "Cholesky"] else 'normal'
        for widget in self.frame_params.winfo_children():
            widget.configure(state=state)

    def _calculate(self):
        try:
            # Verificar que hay una matriz cargada
            if self.current_matrix is None:
                messagebox.showwarning("Advertencia", "Primero debe cargar una matriz.")
                return
            
            A, b = self.current_matrix
            metodo = self.combo_metodo.get()
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_iter.get())

            res, extras, warning_msg = None, None, None

            if metodo == "Jacobi":
                res, extras, warning_msg = MetodoJacobi(A, b, tol, max_iter)
            elif metodo == "Gauss-Seidel":
                res, extras, warning_msg = MetodoGaussSeidel(A, b, tol, max_iter)
            elif metodo == "Eliminación Gaussiana":
                res, extras = EliminacionGaussiana(A, b)
            elif metodo == "Cholesky":
                res, extras = MetodoCholesky(A, b)

            # Si hay advertencia (divergencia o condiciones), mostrarla pero SEGUIR
            if warning_msg:
                messagebox.showwarning("Advertencia de Método", warning_msg)

            self._display_results(res, extras, metodo, A, b)

        except ValueError as ve:
            messagebox.showerror("Error Matemático", str(ve))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")

    def _display_results(self, x, extras, metodo, A, b):
        self.txt_result.delete("1.0", tk.END)
        for item in self.tree.get_children(): self.tree.delete(item)
        for item in self.tree_comp.get_children(): self.tree_comp.delete(item)

        # 1. Mostrar Resultado X
        res_str = f"Solución ({metodo}):\n"
        res_str += "[" + ", ".join([f"{val:.6f}" for val in x]) + "]"
        self.txt_result.insert(tk.END, res_str)

        # 2. Llenar Tabla Iteraciones
        if metodo in ["Jacobi", "Gauss-Seidel"] and isinstance(extras, list):
            self.lbl_iter.config(text=f"Historial ({len(extras)} iters):")
            for paso in extras:
                vec_str = "[" + ", ".join([f"{v:.3f}" for v in paso['x']]) + "]"
                self.tree.insert("", tk.END, values=(paso['iter'], vec_str, f"{paso['error']:.2e}"))
        elif metodo == "Cholesky":
             # Mostrar L
             for i, row in enumerate(extras):
                self.tree.insert("", tk.END, values=(f"L{i+1}", str([round(v,3) for v in row]), "-"))

        # 3. Llenar Comprobación Ax vs b
        Ax = comprobar_solucion(A, x)
        for i in range(len(b)):
            diff = abs(Ax[i] - b[i])
            self.tree_comp.insert("", tk.END, values=(
                i+1, 
                f"{Ax[i]:.6f}", 
                f"{b[i]:.6f}", 
                f"{diff:.2e}"
            ))