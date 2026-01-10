import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from views.matrix_widget import MatrixWidget

# Importamos el método de Leverrier
from metodos.metodosMatrices.Leverrier_Faddeev import (
    favveed_Leberrier, 
    multiplicacion_matriz_vector
)

# Importamos la función de comprobación (ajusta el nombre del archivo si lo guardaste diferente)
from metodos.metodosMatrices.logica_matrices import comprobar_solucion

class LeverrierFaddeevView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        # Layout: Izquierda (Matriz) | Derecha (Resultados detallados)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ==========================================
        # PANEL IZQUIERDO: Entrada
        # ==========================================
        left_panel = ttk.Frame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        lbl_input = ttk.LabelFrame(left_panel, text="Entrada de Datos")
        lbl_input.pack(fill=tk.BOTH, expand=True)

        self.matrix_widget = MatrixWidget(lbl_input)
        self.matrix_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Button(left_panel, text="Calcular Método Leverrier-Faddeev", 
                   command=self._calculate).pack(fill=tk.X, pady=10)

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

    def _calculate(self):
        try:
            # 1. Obtener datos del widget
            A, b = self.matrix_widget.get_matrix_system()
            n = len(A)

            # 2. Llamar a TU método (favveed_Leberrier)
            c, det, inversa = favveed_Leberrier(A)

            # 3. Calcular vector x = Inversa * b
            x = multiplicacion_matriz_vector(inversa, b)

            # 4. Calcular comprobación Ax
            Ax = comprobar_solucion(A, x)

            # 5. Mostrar Resultados
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

        # Solución X (Solo texto simple, el detalle va en la tabla)
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