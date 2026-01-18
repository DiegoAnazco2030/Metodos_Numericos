import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from metodos.calculoDiferencialIntegral.Dirivadas import (
    diferencia_adelante,
    diferencia_atras,
    diferencia_centrada
)
from utils.sympy_utils import parse_function
import sympy as sp


class DerivadasView(BaseView):
    def __init__(self, parent, layout=None):
        super().__init__(parent, layout)

    def build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ==========================================
        # PANEL IZQUIERDO: Entrada de Datos
        # ==========================================
        left_panel = ttk.Frame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        input_frame = ttk.LabelFrame(left_panel, text="Cálculo de Derivadas Numéricas")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Fila Función
        row_f = ttk.Frame(input_frame)
        row_f.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(row_f, text="f(x):").pack(side=tk.LEFT)
        self.entry_f = ttk.Entry(row_f)
        self.entry_f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(row_f, text="Usar Seleccionada", command=self._get_from_manager).pack(side=tk.LEFT)

        # Fila Método
        row_metodo = ttk.Frame(input_frame)
        row_metodo.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(row_metodo, text="Método:").pack(side=tk.LEFT)
        self.combo_metodo = ttk.Combobox(row_metodo, state="readonly", values=[
            "Diferencia Adelante",
            "Diferencia Atrás",
            "Diferencia Centrada"
        ])
        self.combo_metodo.current(2)  # Por defecto: Diferencia Centrada (más precisa)
        self.combo_metodo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Fila Parámetros
        row_params = ttk.Frame(input_frame)
        row_params.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(row_params, text="Punto (x):").pack(side=tk.LEFT)
        self.entry_x = ttk.Entry(row_params, width=12)
        self.entry_x.pack(side=tk.LEFT, padx=5)

        ttk.Label(row_params, text="Paso (h):").pack(side=tk.LEFT, padx=(10, 0))
        self.entry_h = ttk.Entry(row_params, width=12)
        self.entry_h.insert(0, "0.001")
        self.entry_h.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Calcular Derivada", command=self._calculate).pack(pady=15)

        # Información del método
        info_frame = ttk.LabelFrame(left_panel, text="Información del Método")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        
        self.txt_info = tk.Text(info_frame, height=8, wrap=tk.WORD, bg="#f9f9f9", 
                                font=("Segoe UI", 9), state='disabled')
        self.txt_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Mostrar info inicial
        self.combo_metodo.bind("<<ComboboxSelected>>", self._update_method_info)
        self._update_method_info()

        # ==========================================
        # PANEL DERECHO: Resultados
        # ==========================================
        right_panel = ttk.LabelFrame(self, text="Resultados")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Área de resultados numéricos
        ttk.Label(right_panel, text="Derivada Numérica:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        
        self.txt_result = tk.Text(right_panel, height=4, bg="#e8f4f8", font=("Consolas", 11, "bold"))
        self.txt_result.pack(fill=tk.X, padx=10, pady=5)
        self.txt_result.tag_config("result", foreground="#1a5490")

        # Derivada analítica (si es posible)
        ttk.Label(right_panel, text="Derivada Analítica (simbólica):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(15, 2))
        
        self.txt_analytic = tk.Text(right_panel, height=4, bg="#f0f8e8", font=("Consolas", 10))
        self.txt_analytic.pack(fill=tk.X, padx=10, pady=5)
        self.txt_analytic.tag_config("formula", foreground="#2d5016")
        self.txt_analytic.tag_config("warning", foreground="#cc6600", font=("Consolas", 10, "italic"))

        # Comparación y Error
        ttk.Label(right_panel, text="Comparación y Error:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(15, 2))
        
        self.txt_comparison = tk.Text(right_panel, height=5, bg="#fff9e6", font=("Consolas", 10))
        self.txt_comparison.pack(fill=tk.X, padx=10, pady=5)
        self.txt_comparison.tag_config("error", foreground="#cc6600")
        self.txt_comparison.tag_config("warning", foreground="#999999", font=("Consolas", 10, "italic"))

        # Tabla de valores
        ttk.Label(right_panel, text="Evaluación de Puntos:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=10, pady=(15, 2))
        
        cols = ("punto", "valor")
        self.tree = ttk.Treeview(right_panel, columns=cols, show="headings", height=4)
        self.tree.heading("punto", text="Punto evaluado")
        self.tree.heading("valor", text="f(punto)")
        self.tree.column("punto", width=150, anchor="center")
        self.tree.column("valor", width=150, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def _get_from_manager(self):
        """Obtiene la función seleccionada del FunctionManager"""
        if self.layout and self.layout.function_manager:
            func = self.layout.function_manager.get_selected_function()
            if func:
                self.entry_f.delete(0, tk.END)
                self.entry_f.insert(0, str(func))

    def _update_method_info(self, event=None):
        """Actualiza la información del método seleccionado"""
        metodo = self.combo_metodo.get()
        
        info_texts = {
            "Diferencia Adelante": 
                "Fórmula: f'(x) ≈ [f(x+h) - f(x)] / h\n\n"
                "Precisión: O(h)\n"
                "Uso: Simple, pero menos preciso.\n"
                "Evalúa: f(x) y f(x+h)",
            
            "Diferencia Atrás":
                "Fórmula: f'(x) ≈ [f(x) - f(x-h)] / h\n\n"
                "Precisión: O(h)\n"
                "Uso: Similar a adelante.\n"
                "Evalúa: f(x) y f(x-h)",
            
            "Diferencia Centrada":
                "Fórmula: f'(x) ≈ [f(x+h) - f(x-h)] / (2h)\n\n"
                "Precisión: O(h²) - Mayor precisión\n"
                "Uso: Recomendado para mejor exactitud.\n"
                "Evalúa: f(x+h) y f(x-h)"
        }
        
        self.txt_info.config(state='normal')
        self.txt_info.delete("1.0", tk.END)
        self.txt_info.insert("1.0", info_texts.get(metodo, ""))
        self.txt_info.config(state='disabled')

    def _calculate(self):
        """Calcula la derivada numérica"""
        try:
            # Obtener datos de entrada
            f_str = self.entry_f.get().strip()
            if not f_str:
                messagebox.showwarning("Advertencia", "Ingrese una función.")
                return
            
            x_val = float(self.entry_x.get())
            h_val = float(self.entry_h.get())
            metodo = self.combo_metodo.get()

            # Convertir función de string a callable
            f_expr = parse_function(f_str)
            x_sym = sp.Symbol('x')
            f_lambda = sp.lambdify(x_sym, f_expr, 'numpy')

            # Seleccionar método
            metodo_func = {
                "Diferencia Adelante": diferencia_adelante,
                "Diferencia Atrás": diferencia_atras,
                "Diferencia Centrada": diferencia_centrada
            }[metodo]

            # Calcular derivada numérica
            derivada_numerica = metodo_func(f_lambda, x_val, h_val)

            # Calcular derivada analítica (simbólica)
            try:
                f_prime = sp.diff(f_expr, x_sym)
                derivada_analitica = float(f_prime.subs(x_sym, x_val))
                tiene_analitica = True
            except:
                derivada_analitica = None
                tiene_analitica = False

            # Mostrar resultados
            self._display_results(derivada_numerica, derivada_analitica, tiene_analitica, 
                                f_lambda, x_val, h_val, metodo, f_prime if tiene_analitica else None)

        except ValueError as ve:
            messagebox.showerror("Error de Datos", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular:\n{str(e)}")

    def _display_results(self, derivada_num, derivada_ana, tiene_ana, f_lambda, x, h, metodo, f_prime):
        """Muestra los resultados en la interfaz"""
        # Limpiar resultados previos
        self.txt_result.delete("1.0", tk.END)
        self.txt_analytic.delete("1.0", tk.END)
        self.txt_comparison.delete("1.0", tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 1. Derivada Numérica
        result_text = f"f'({x}) ≈ {derivada_num:.10f}\n\nMétodo: {metodo}"
        self.txt_result.insert("1.0", result_text, "result")

        # 2. Derivada Analítica
        if tiene_ana:
            analytic_text = f"f'(x) = {f_prime}\n\nf'({x}) = {derivada_ana:.10f}"
            self.txt_analytic.insert("1.0", analytic_text, "formula")
        else:
            warning_text = "No se pudo calcular derivada simbólica\n\n"
            warning_text += "La función no puede derivarse analíticamente\no es demasiado compleja para SymPy."
            self.txt_analytic.insert("1.0", warning_text, "warning")

        # 3. Comparación
        if tiene_ana:
            error_abs = abs(derivada_num - derivada_ana)
            error_rel = (error_abs / abs(derivada_ana) * 100) if derivada_ana != 0 else float('inf')
            
            comp_text = f"Error Absoluto: {error_abs:.2e}\n"
            comp_text += f"Error Relativo: {error_rel:.6f}%\n\n"
            comp_text += f"Diferencia: {derivada_num - derivada_ana:.2e}"
            self.txt_comparison.insert("1.0", comp_text, "error")
        else:
            warning_text = "No se puede calcular error\n\n"
            warning_text += "Sin solución analítica disponible para comparar."
            self.txt_comparison.insert("1.0", warning_text, "warning")

        # 4. Tabla de puntos evaluados
        puntos_eval = []
        if metodo == "Diferencia Adelante":
            puntos_eval = [(x, f_lambda(x)), (x + h, f_lambda(x + h))]
        elif metodo == "Diferencia Atrás":
            puntos_eval = [(x - h, f_lambda(x - h)), (x, f_lambda(x))]
        else:  # Centrada
            puntos_eval = [(x - h, f_lambda(x - h)), (x + h, f_lambda(x + h))]

        for punto, valor in puntos_eval:
            self.tree.insert("", tk.END, values=(f"{punto:.6f}", f"{valor:.10f}"))
