import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from metodos.calculoDiferencialIntegral.Integrales import (
    regla_trapecio,
    simpson_1_3,
    simpson_3_8
)
from utils.sympy_utils import parse_function
import sympy as sp


class IntegralesView(BaseView):
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

        input_frame = ttk.LabelFrame(left_panel, text="Integración Numérica")
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
            "Regla del Trapecio",
            "Simpson 1/3",
            "Simpson 3/8"
        ])
        self.combo_metodo.current(1)  # Por defecto: Simpson 1/3 (buena precisión)
        self.combo_metodo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.combo_metodo.bind("<<ComboboxSelected>>", self._update_method_info)

        # Fila Límites de integración
        row_limits = ttk.Frame(input_frame)
        row_limits.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(row_limits, text="Límite Inf (a):").pack(side=tk.LEFT)
        self.entry_a = ttk.Entry(row_limits, width=12)
        self.entry_a.pack(side=tk.LEFT, padx=5)

        ttk.Label(row_limits, text="Límite Sup (b):").pack(side=tk.LEFT, padx=(10, 0))
        self.entry_b = ttk.Entry(row_limits, width=12)
        self.entry_b.pack(side=tk.LEFT, padx=5)

        # Fila Segmentos
        row_n = ttk.Frame(input_frame)
        row_n.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(row_n, text="Segmentos (n):").pack(side=tk.LEFT)
        self.entry_n = ttk.Entry(row_n, width=12)
        self.entry_n.insert(0, "10")
        self.entry_n.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row_n, text="(debe ser par para Simpson 1/3, múltiplo de 3 para Simpson 3/8)", 
                  font=("Segoe UI", 8), foreground="#666").pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Calcular Integral", command=self._calculate).pack(pady=15)

        # Información del método
        info_frame = ttk.LabelFrame(left_panel, text="Información del Método")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        
        self.txt_info = tk.Text(info_frame, height=8, wrap=tk.WORD, bg="#f9f9f9", 
                                font=("Segoe UI", 9), state='disabled')
        self.txt_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Mostrar info inicial
        self._update_method_info()

        # ==========================================
        # PANEL DERECHO: Resultados
        # ==========================================
        right_panel = ttk.LabelFrame(self, text="Resultados")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Área de resultados numéricos
        ttk.Label(right_panel, text="Integral Numérica:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        
        self.txt_result = tk.Text(right_panel, height=4, bg="#e8f4f8", font=("Consolas", 11, "bold"))
        self.txt_result.pack(fill=tk.X, padx=10, pady=5)
        self.txt_result.tag_config("result", foreground="#1a5490")

        # Integral analítica (si es posible)
        ttk.Label(right_panel, text="Integral Analítica (simbólica):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(15, 2))
        
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

        # Tabla de información de particiones
        ttk.Label(right_panel, text="Información de Particiones:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=10, pady=(15, 2))
        
        cols = ("parametro", "valor")
        self.tree = ttk.Treeview(right_panel, columns=cols, show="headings", height=5)
        self.tree.heading("parametro", text="Parámetro")
        self.tree.heading("valor", text="Valor")
        self.tree.column("parametro", width=180, anchor="w")
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
            "Regla del Trapecio": 
                "Fórmula: ∫f(x)dx ≈ (h/2)[f(a) + 2∑f(xi) + f(b)]\n\n"
                "Precisión: O(h²)\n"
                "Restricción: n puede ser cualquier entero positivo\n"
                "Uso: Método simple y rápido, aproxima con trapecios.\n"
                "h = (b-a)/n",
            
            "Simpson 1/3":
                "Fórmula: ∫f(x)dx ≈ (h/3)[f(a) + 4∑f(impares) + 2∑f(pares) + f(b)]\n\n"
                "Precisión: O(h⁴) - Mayor precisión\n"
                "Restricción: n debe ser PAR\n"
                "Uso: Recomendado, usa parábolas de 2º grado.\n"
                "h = (b-a)/n",
            
            "Simpson 3/8":
                "Fórmula: ∫f(x)dx ≈ (3h/8)[f(a) + 3∑f(no-múlt-3) + 2∑f(múlt-3) + f(b)]\n\n"
                "Precisión: O(h⁴)\n"
                "Restricción: n debe ser MÚLTIPLO DE 3\n"
                "Uso: Similar a 1/3, usa parábolas de 3er grado.\n"
                "h = (b-a)/n"
        }
        
        self.txt_info.config(state='normal')
        self.txt_info.delete("1.0", tk.END)
        self.txt_info.insert("1.0", info_texts.get(metodo, ""))
        self.txt_info.config(state='disabled')

    def _calculate(self):
        """Calcula la integral numérica"""
        try:
            # Obtener datos de entrada
            f_str = self.entry_f.get().strip()
            if not f_str:
                messagebox.showwarning("Advertencia", "Ingrese una función.")
                return
            
            a_val = float(self.entry_a.get())
            b_val = float(self.entry_b.get())
            n_val = int(self.entry_n.get())
            metodo = self.combo_metodo.get()

            # Convertir función de string a callable
            f_expr = parse_function(f_str)
            x_sym = sp.Symbol('x')
            f_lambda = sp.lambdify(x_sym, f_expr, 'numpy')

            # Seleccionar método
            metodo_func = {
                "Regla del Trapecio": regla_trapecio,
                "Simpson 1/3": simpson_1_3,
                "Simpson 3/8": simpson_3_8
            }[metodo]

            # Calcular integral numérica
            integral_numerica = metodo_func(f_lambda, a_val, b_val, n_val)

            # Calcular integral analítica (simbólica)
            try:
                F = sp.integrate(f_expr, x_sym)
                # Verificar si SymPy retornó una integral no resuelta
                if F.has(sp.Integral):
                    raise ValueError("Integral no evaluable")
                
                integral_analitica = float(F.subs(x_sym, b_val) - F.subs(x_sym, a_val))
                tiene_analitica = True
            except:
                integral_analitica = None
                tiene_analitica = False
                F = None

            # Mostrar resultados
            self._display_results(integral_numerica, integral_analitica, tiene_analitica, 
                                a_val, b_val, n_val, metodo, f_expr, F)

        except ValueError as ve:
            messagebox.showerror("Error de Datos", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular:\n{str(e)}")

    def _display_results(self, integral_num, integral_ana, tiene_ana, a, b, n, metodo, f_expr, F):
        """Muestra los resultados en la interfaz"""
        # Limpiar resultados previos
        self.txt_result.delete("1.0", tk.END)
        self.txt_analytic.delete("1.0", tk.END)
        self.txt_comparison.delete("1.0", tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 1. Integral Numérica
        result_text = f"∫[{a}, {b}] f(x)dx ≈ {integral_num:.10f}\n\nMétodo: {metodo}"
        self.txt_result.insert("1.0", result_text, "result")

        # 2. Integral Analítica
        if tiene_ana:
            analytic_text = f"∫f(x)dx = {F} + C\n\n"
            analytic_text += f"∫[{a}, {b}] f(x)dx = {integral_ana:.10f}"
            self.txt_analytic.insert("1.0", analytic_text, "formula")
        else:
            warning_text = "No se pudo calcular integral simbólica\n\n"
            warning_text += "La función no puede integrarse analíticamente,\nes muy compleja, o no tiene antiderivada elemental."
            self.txt_analytic.insert("1.0", warning_text, "warning")

        # 3. Comparación
        if tiene_ana:
            error_abs = abs(integral_num - integral_ana)
            error_rel = (error_abs / abs(integral_ana) * 100) if integral_ana != 0 else float('inf')
            
            comp_text = f"Error Absoluto: {error_abs:.2e}\n"
            comp_text += f"Error Relativo: {error_rel:.6f}%\n\n"
            comp_text += f"Diferencia: {integral_num - integral_ana:.2e}"
            self.txt_comparison.insert("1.0", comp_text, "error")
        else:
            warning_text = "No se puede calcular error\n\n"
            warning_text += "Sin solución analítica disponible para comparar."
            self.txt_comparison.insert("1.0", warning_text, "warning")

        # 4. Tabla de información
        h = (b - a) / n
        
        self.tree.insert("", tk.END, values=("Límite inferior (a)", f"{a}"))
        self.tree.insert("", tk.END, values=("Límite superior (b)", f"{b}"))
        self.tree.insert("", tk.END, values=("Número de segmentos (n)", f"{n}"))
        self.tree.insert("", tk.END, values=("Tamaño de paso (h)", f"{h:.6f}"))
        self.tree.insert("", tk.END, values=("Intervalo total", f"{b - a:.6f}"))
        
        # Info específica del método
        if metodo == "Simpson 1/3":
            self.tree.insert("", tk.END, values=("Validación", f"n={n} es {'par ✓' if n % 2 == 0 else 'impar ✗'}"))
        elif metodo == "Simpson 3/8":
            self.tree.insert("", tk.END, values=("Validación", f"n={n} es {'múltiplo de 3 ✓' if n % 3 == 0 else 'NO múltiplo de 3 ✗'}"))
