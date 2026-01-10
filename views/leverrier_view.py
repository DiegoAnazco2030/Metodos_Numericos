import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from views.matrix_widget import MatrixWidget

# Importamos TU archivo tal cual (asegúrate de moverlo a la carpeta correcta)
from metodos.metodosMatrices.Leverrier_Faddeev import (
    favveed_Leberrier, 
    multiplicacion_matriz_vector
)

class LeverrierFaddeevView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        # Layout: Izquierda (Matriz) | Derecha (Resultados detallados)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # --- PANEL IZQUIERDO: Entrada ---
        left_panel = ttk.Frame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        lbl_input = ttk.LabelFrame(left_panel, text="Entrada de Datos")
        lbl_input.pack(fill=tk.BOTH, expand=True)

        self.matrix_widget = MatrixWidget(lbl_input)
        self.matrix_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Button(left_panel, text="Calcular Método Leverrier-Faddeev", 
                   command=self._calculate).pack(fill=tk.X, pady=10)

        # --- PANEL DERECHO: Resultados ---
        right_panel = ttk.LabelFrame(self, text="Resultados del Análisis")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Usamos un Text con scroll porque la matriz inversa ocupa espacio
        self.txt_result = tk.Text(right_panel, font=("Consolas", 10), padx=10, pady=10)
        self.txt_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(right_panel, orient="vertical", command=self.txt_result.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_result.config(yscrollcommand=scroll.set)

        # Tags para negritas y colores
        self.txt_result.tag_config("title", font=("Consolas", 11, "bold"), foreground="#2c3e50")
        self.txt_result.tag_config("important", foreground="#e74c3c") # Rojo para notas

    def _calculate(self):
        try:
            # 1. Obtener datos del widget
            A, b = self.matrix_widget.get_matrix_system()
            n = len(A)

            # 2. Llamar a TU método (favveed_Leberrier)
            # Retorna: coeficientes, determinante, inversa
            c, det, inversa = favveed_Leberrier(A)

            # 3. Calcular vector x = Inversa * b
            # Usamos la función auxiliar que ya viene en tu archivo
            x = multiplicacion_matriz_vector(inversa, b)

            # 4. Mostrar Resultados
            self._display_results(n, c, det, inversa, x)

        except ZeroDivisionError:
            messagebox.showerror("Error", "El determinante es 0. La matriz no tiene inversa.")
        except ValueError as ve:
            messagebox.showerror("Error de Datos", str(ve))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")

    def _display_results(self, n, c, det, inversa, x):
        self.txt_result.delete("1.0", tk.END)

        # --- Polinomio Característico ---
        self.txt_result.insert(tk.END, "1. Polinomio Característico:\n", "title")
        poly_str = "P(λ) = "
        for i in range(len(c)):
            coef = c[i]
            exponente = n - i
            
            # Formateo bonito del signo
            signo = "+ " if coef >= 0 and i > 0 else "- " if coef < 0 else ""
            val = abs(coef)
            
            if i == 0: # El primer término suele ser 1*lambda^n
                term = f"λ^{exponente} "
            elif exponente == 0:
                term = f"{val:.4f}"
            else:
                term = f"{val:.4f}λ^{exponente} "
            
            poly_str += f"{signo}{term}"
        
        self.txt_result.insert(tk.END, poly_str + "\n\n")

        # --- Determinante ---
        self.txt_result.insert(tk.END, "2. Determinante:\n", "title")
        self.txt_result.insert(tk.END, f"Det(A) = {det:.6f}\n\n")

        # --- Matriz Inversa ---
        self.txt_result.insert(tk.END, "3. Matriz Inversa (A⁻¹):\n", "title")
        for fila in inversa:
            row_str = "  | " + "  ".join([f"{val:9.4f}" for val in fila]) + " |\n"
            self.txt_result.insert(tk.END, row_str)
        self.txt_result.insert(tk.END, "\n")

        # --- Solución del Sistema ---
        self.txt_result.insert(tk.END, "4. Solución del Sistema (x):\n", "title")
        self.txt_result.insert(tk.END, "Nota: Calculado mediante x = A⁻¹ · b\n", "important")
        
        for i, val in enumerate(x):
            self.txt_result.insert(tk.END, f"  x{i+1} = {val:.8f}\n")