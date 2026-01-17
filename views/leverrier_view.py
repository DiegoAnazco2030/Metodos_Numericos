import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView

# Importamos el método de Leverrier
from metodos.metodosMatrices.Leverrier_Faddeev import (
    favveed_Leberrier, 
    multiplicacion_matriz_vector
)

# Importamos la función de comprobación
from metodos.metodosMatrices.logica_matrices import comprobar_solucion

class LeverrierFaddeevView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)
        self.current_matrix = None  # Almacena (A, b)

    def build(self):
        # Layout: Izquierda (Carga de Matriz) | Derecha (Resultados detallados)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ==========================================
        # PANEL IZQUIERDO: Entrada
        # ==========================================
        left_panel = ttk.Frame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        lbl_input = ttk.LabelFrame(left_panel, text="Matriz para Análisis")
        lbl_input.pack(fill=tk.BOTH, expand=True, pady=5)

        # Botón para cargar matriz seleccionada
        ttk.Button(
            lbl_input,
            text="Cargar Matriz Seleccionada",
            command=self._load_selected_matrix
        ).pack(fill=tk.X, padx=10, pady=10)

        # Área de visualización de la matriz cargada
        ttk.Label(lbl_input, text="Matriz Cargada:").pack(anchor="w", padx=10, pady=(10, 2))
        
        self.txt_matrix = tk.Text(lbl_input, height=10, font=("Consolas", 9), state='disabled')
        self.txt_matrix.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Botón calcular
        ttk.Button(
            left_panel,
            text="Calcular Método Leverrier-Faddeev",
            command=self._calculate
        ).pack(fill=tk.X, pady=10)

        # ==========================================
        # PANEL DERECHO: Resultados
        # ==========================================
        right_panel = ttk.LabelFrame(self, text="Resultados del Análisis")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Usamos PanedWindow para dividir Texto (Arriba) y Tabla (Abajo)
        paned = ttk.PanedWindow(right_panel, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- 1. Área de Texto (Polinomio, Inversa, Det) ---
        self.txt_result = tk.Text(paned, height=12, font=("Consolas", 10), padx=10, pady=10)
        # Scroll para el texto
        scroll_txt = ttk.Scrollbar(self.txt_result, orient="vertical", command=self.txt_result.yview)
        scroll_txt.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_result.config(yscrollcommand=scroll_txt.set)
        
        # Tags de estilo
        self.txt_result.tag_config("title", font=("Consolas", 11, "bold"), foreground="#2c3e50")
        self.txt_result.tag_config("important", foreground="#e74c3c") 

        paned.add(self.txt_result, weight=3)

        # --- 2. Tabla de Comprobación (Ax vs b) ---
        frame_comp = ttk.Frame(paned)
        paned.add(frame_comp, weight=1)

        ttk.Label(frame_comp, text="Comprobación de Solución (Ax vs b):", 
                  font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5,2))

        cols_comp = ("ec", "val_ax", "val_b", "diff")
        self.tree_comp = ttk.Treeview(frame_comp, columns=cols_comp, show="headings", height=5)
        
        self.tree_comp.heading("ec", text="Ec.")
        self.tree_comp.heading("val_ax", text="(Ax) Calculado")
        self.tree_comp.heading("val_b", text="b Esperado")
        self.tree_comp.heading("diff", text="Diferencia")
        
        self.tree_comp.column("ec", width=40, anchor="center")
        self.tree_comp.column("val_ax", width=100, anchor="center")
        self.tree_comp.column("val_b", width=100, anchor="center")
        self.tree_comp.column("diff", width=100, anchor="center")
        
        # Scroll para la tabla
        scroll_tree = ttk.Scrollbar(frame_comp, orient="vertical", command=self.tree_comp.yview)
        scroll_tree.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_comp.configure(yscrollcommand=scroll_tree.set)
        
        self.tree_comp.pack(fill=tk.BOTH, expand=True)

    def _load_selected_matrix(self):
        """Carga la matriz seleccionada del sidebar"""
        if not self.layout or not hasattr(self.layout, 'matrix_manager'):
            messagebox.showerror("Error", "No hay gestor de matrices disponible")
            return
        
        matrix_data = self.layout.matrix_manager.get_selected_matrix()
        if not matrix_data:
            messagebox.showwarning("Advertencia", "Seleccione una matriz del historial")
            return
        
        self.current_matrix = matrix_data
        A, b = matrix_data
        
        # Mostrar la matriz aumentada [A|b]
        self.txt_matrix.config(state='normal')
        self.txt_matrix.delete(1.0, tk.END)

        # AQUÍ ES DONDE SE FORMATEA LA VISUALIZACIÓN
        self.txt_matrix.insert(tk.END, "Matriz A:\n")
        for row in A:
            self.txt_matrix.insert(tk.END, "  " + "  ".join(f"{val:8.3f}" for val in row) + "\n")
        
        self.txt_matrix.insert(tk.END, "\nVector b:\n")
        for val in b:
            self.txt_matrix.insert(tk.END, f"  {val:8.3f}\n")
        
        self.txt_matrix.insert(tk.END, "\nMatriz Aumentada [A|b]:\n")
        for i, row in enumerate(A):
            row_str = "  " + "  ".join(f"{val:8.3f}" for val in row)
            row_str += f"  |  {b[i]:8.3f}\n"
            self.txt_matrix.insert(tk.END, row_str)
        
        self.txt_matrix.config(state='disabled')

    def _calculate(self):
        """Ejecuta el cálculo del método Leverrier-Faddeev"""
        try:
            # Verificar que hay una matriz cargada
            if self.current_matrix is None:
                messagebox.showwarning("Advertencia", "Primero debe cargar una matriz.")
                return
            
            A, b = self.current_matrix
            n = len(A)

            # Llamar al método de Leverrier-Faddeev
            c, det, inversa = favveed_Leberrier(A)

            # Calcular vector x = Inversa * b
            x = multiplicacion_matriz_vector(inversa, b)

            # Calcular comprobación Ax
            Ax = comprobar_solucion(A, x)

            # Mostrar Resultados
            self._display_results(n, c, det, inversa, x, Ax, b)

        except ZeroDivisionError:
            messagebox.showerror("Error", "El determinante es 0. La matriz no tiene inversa.")
        except ValueError as ve:
            messagebox.showerror("Error de Datos", str(ve))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")

    def _display_results(self, n, c, det, inversa, x, Ax, b):
        # --- Limpiar todo ---
        self.txt_result.delete("1.0", tk.END)
        for item in self.tree_comp.get_children():
            self.tree_comp.delete(item)

        # ==========================================
        # PARTE 1: Texto (Polinomio, Det, Inversa)
        # ==========================================
        
        # Polinomio
        self.txt_result.insert(tk.END, "1. Polinomio Característico:\n", "title")
        poly_str = "P(λ) = "
        for i in range(len(c)):
            coef = c[i]
            exponente = n - i
            
            signo = "+ " if coef >= 0 and i > 0 else "- " if coef < 0 else ""
            val = abs(coef)
            
            if i == 0: 
                term = f"λ^{exponente} "
            elif exponente == 0:
                term = f"{val:.4f}"
            else:
                term = f"{val:.4f}λ^{exponente} "
            
            poly_str += f"{signo}{term}"
        
        self.txt_result.insert(tk.END, poly_str + "\n\n")

        # Determinante
        self.txt_result.insert(tk.END, "2. Determinante:\n", "title")
        self.txt_result.insert(tk.END, f"Det(A) = {det:.6f}\n\n")

        # Matriz Inversa
        self.txt_result.insert(tk.END, "3. Matriz Inversa (A⁻¹):\n", "title")
        for fila in inversa:
            row_str = "  | " + "  ".join([f"{val:9.4f}" for val in fila]) + " |\n"
            self.txt_result.insert(tk.END, row_str)
        self.txt_result.insert(tk.END, "\n")

        # Solución X
        self.txt_result.insert(tk.END, "4. Vector Solución (x):\n", "title")
        self.txt_result.insert(tk.END, "Nota: Calculado mediante x = A⁻¹ · b\n", "important")
        vec_x_str = "[" + ", ".join([f"{val:.6f}" for val in x]) + "]"
        self.txt_result.insert(tk.END, f"{vec_x_str}\n")

        # ==========================================
        # PARTE 2: Tabla de Comprobación
        # ==========================================
        for i in range(len(b)):
            diff = abs(Ax[i] - b[i])
            self.tree_comp.insert("", tk.END, values=(
                i+1, 
                f"{Ax[i]:.6f}", 
                f"{b[i]:.6f}", 
                f"{diff:.2e}"
            ))