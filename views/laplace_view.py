import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import csv
import os

from views.base_view import BaseView
from metodos.laplace.Laplace import resolver_laplace_general


def _parse_value(text: str, length: int, dx: float):
    """Convierte el texto de borde en escalar o vector. Permite expresión en s∈[0,1]."""
    txt = text.strip()
    if not txt:
        raise ValueError("Ingrese un valor o expresión para el borde.")

    # 1) Intentar escalar
    try:
        return float(txt)
    except ValueError:
        pass

    # 2) Intentar lista CSV
    if "," in txt:
        parts = [p.strip() for p in txt.split(",") if p.strip()]
        vals = [float(p) for p in parts]
        if len(vals) != length:
            raise ValueError(f"Se esperaban {length} valores y se recibieron {len(vals)}.")
        return np.array(vals, dtype=float)

    # 3) Expresión Física (Aquí está el cambio)
    # Calculamos la longitud real física de este borde
    longitud_real = (length - 1) * dx
    
    # Generamos los puntos exactos según el dx
    # Ej: si dx=0.5 y length=5 -> [0.0, 0.5, 1.0, 1.5, 2.0]
    s = np.linspace(0, longitud_real, length)
    
    allowed = {k: getattr(np, k) for k in dir(np) if not k.startswith("_")}
    allowed["s"] = s
    allowed["np"] = np
    allowed["pi"] = np.pi
    try:
        vals = eval(txt, {"__builtins__": {}}, allowed)
        vals = np.asarray(vals, dtype=float)
        if vals.size != length:
            raise ValueError(f"La expresión debe generar {length} valores.")
        return vals
    except Exception as e:
        raise ValueError(f"No se pudo interpretar el valor: {e}")


class LaplaceView(BaseView):
    def __init__(self, parent, layout=None):
        # build() se llama en BaseView; no sobrescribir después
        super().__init__(parent, layout)
        self.cbar = None
        self.T_result = None  # Guardar matriz resuelta para descargar

    def destroy(self):
        """Limpiar recursos de matplotlib antes de destruir la vista."""
        try:
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.get_tk_widget().destroy()
            if hasattr(self, 'fig') and self.fig:
                plt.close(self.fig)
        except:
            pass
        super().destroy()

    def build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # Panel izquierdo
        left = ttk.Frame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        cfg = ttk.LabelFrame(left, text="Parámetros de la malla")
        cfg.pack(fill=tk.X, pady=5)

        # Dimensiones y parámetros
        row0 = ttk.Frame(cfg)
        row0.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(row0, text="Filas:").pack(side=tk.LEFT)
        self.entry_rows = ttk.Entry(row0, width=8)
        self.entry_rows.insert(0, "20")
        self.entry_rows.pack(side=tk.LEFT, padx=3)
        ttk.Label(row0, text="Cols:").pack(side=tk.LEFT)
        self.entry_cols = ttk.Entry(row0, width=8)
        self.entry_cols.insert(0, "20")
        self.entry_cols.pack(side=tk.LEFT, padx=3)

        row1 = ttk.Frame(cfg)
        row1.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(row1, text="dx:").pack(side=tk.LEFT)
        self.entry_dx = ttk.Entry(row1, width=8)
        self.entry_dx.insert(0, "1.0")
        self.entry_dx.pack(side=tk.LEFT, padx=3)
        ttk.Label(row1, text="w (0<w<2):").pack(side=tk.LEFT)
        self.entry_w = ttk.Entry(row1, width=8)
        self.entry_w.insert(0, "1.5")
        self.entry_w.pack(side=tk.LEFT, padx=3)

        row2 = ttk.Frame(cfg)
        row2.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(row2, text="tol:").pack(side=tk.LEFT)
        self.entry_tol = ttk.Entry(row2, width=10)
        self.entry_tol.insert(0, "1e-4")
        self.entry_tol.pack(side=tk.LEFT, padx=3)
        ttk.Label(row2, text="max_iter:").pack(side=tk.LEFT)
        self.entry_max_iter = ttk.Entry(row2, width=10)
        self.entry_max_iter.insert(0, "500")
        self.entry_max_iter.pack(side=tk.LEFT, padx=3)

        # Label de dominio (se actualiza dinámicamente)
        domain_frame = ttk.Frame(cfg)
        domain_frame.pack(fill=tk.X, padx=5, pady=6)
        self.lbl_domain = ttk.Label(
            domain_frame, 
            text="Dominio: Configurar filas/cols/dx primero",
            foreground="#0066cc",
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_domain.pack(anchor="w")
        
        # Bindings para actualizar dominio automáticamente
        self.entry_rows.bind("<KeyRelease>", lambda e: self._update_domain_label())
        self.entry_cols.bind("<KeyRelease>", lambda e: self._update_domain_label())
        self.entry_dx.bind("<KeyRelease>", lambda e: self._update_domain_label())
        self._update_domain_label()  # Inicializar

        # Condiciones de borde
        self.borders = {}
        border_frame = ttk.LabelFrame(left, text="Condiciones de borde")
        border_frame.pack(fill=tk.BOTH, expand=True, pady=8)

        for name in ("arriba", "abajo", "izquierda", "derecha"):
            group = ttk.LabelFrame(border_frame, text=name.capitalize())
            group.pack(fill=tk.X, padx=5, pady=4)

            top = ttk.Frame(group)
            top.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(top, text="Tipo:").pack(side=tk.LEFT)
            cb = ttk.Combobox(top, state="readonly", values=["dirichlet", "neumann"], width=12)
            cb.current(0)
            cb.pack(side=tk.LEFT, padx=4)

            ttk.Label(top, text="Valor (escalar, CSV o expr en s):").pack(side=tk.LEFT, padx=4)
            entry = ttk.Entry(group)
            entry.pack(fill=tk.X, padx=5, pady=(0, 4))
            entry.insert(0, "0")

            # Ayuda contextual con info de rango de s
            if name in ("arriba", "abajo"):
                help_text = "Ejemplos: 50   |   0,20,40,20,0   |   100*sin(pi*s)  (s recorre el ancho X)"
            else:  # izquierda, derecha
                help_text = "Ejemplos: 50   |   0,20,40,20,0   |   100*sin(pi*s)  (s recorre el alto Y)"
            
            help_lbl = ttk.Label(
                group,
                text=help_text,
                foreground="#555",
                font=("Segoe UI", 8)
            )
            help_lbl.pack(anchor="w", padx=6, pady=(0, 4))

            self.borders[name] = {"type": cb, "value": entry}

        btns = ttk.Frame(left)
        btns.pack(fill=tk.X, pady=6)
        ttk.Button(btns, text="Generar malla y resolver", command=self._solve).pack(fill=tk.X, padx=5)

        # Panel derecho
        right = ttk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=7)  # Heatmap: 70%
        right.rowconfigure(1, weight=3)  # Tabla: 30%

        info = ttk.Frame(right)
        info.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5))
        info.columnconfigure(1, weight=1)
        info.columnconfigure(3, weight=1)
        ttk.Label(info, text="Iteraciones:").grid(row=0, column=0, sticky="w", padx=4)
        self.lbl_iters = ttk.Label(info, text="-")
        self.lbl_iters.grid(row=0, column=1, sticky="w")
        ttk.Label(info, text="Error final:").grid(row=0, column=2, sticky="w", padx=4)
        self.lbl_error = ttk.Label(info, text="-")
        self.lbl_error.grid(row=0, column=3, sticky="w")

        # Heatmap
        heatmap_frame = ttk.LabelFrame(right, text="Campo de Temperatura")
        heatmap_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        heatmap_frame.columnconfigure(0, weight=1)
        heatmap_frame.rowconfigure(0, weight=1)
        self.heatmap_frame = heatmap_frame  # Guardar referencia para recrear canvas

        self.fig, self.ax = plt.subplots(figsize=(5.5, 4), dpi=100)
        self.fig.tight_layout(pad=2.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=heatmap_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Tabla con scrollbars
        txt_frame = ttk.LabelFrame(right, text="Matriz T")
        txt_frame.grid(row=1, column=0, sticky="nsew")
        txt_frame.columnconfigure(0, weight=1)
        txt_frame.rowconfigure(0, weight=1)

        # Frame interno para scrollbars
        scroll_frame = ttk.Frame(txt_frame)
        scroll_frame.grid(row=0, column=0, sticky="nsew")
        scroll_frame.columnconfigure(0, weight=1)
        scroll_frame.rowconfigure(0, weight=1)

        self.txt_matrix = tk.Text(scroll_frame, height=8, font=("Courier", 8), wrap=tk.NONE, state='disabled')
        scrollbar_v = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.txt_matrix.yview)
        scrollbar_h = ttk.Scrollbar(scroll_frame, orient="horizontal", command=self.txt_matrix.xview)
        
        self.txt_matrix.config(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        self.txt_matrix.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        # Botón descargar CSV
        btn_frame = ttk.Frame(txt_frame)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(btn_frame, text="Descargar como CSV", command=self._download_csv).pack(side=tk.LEFT, padx=2)

    def _update_domain_label(self):
        """Actualiza el label de dominio con los valores actuales de filas/cols/dx."""
        try:
            filas = int(self.entry_rows.get())
            cols = int(self.entry_cols.get())
            dx = float(self.entry_dx.get())
            
            x_max = dx * (cols - 1)
            y_max = dx * (filas - 1)
            
            self.lbl_domain.config(
                text=f"Dominio físico: X ∈ [0, {x_max:.2f}],  Y ∈ [0, {y_max:.2f}]"
            )
        except ValueError:
            self.lbl_domain.config(text="Dominio: Ingrese valores válidos de filas/cols/dx")

    def _solve(self):
        try:
            filas = int(self.entry_rows.get())
            cols = int(self.entry_cols.get())
            if filas < 3 or cols < 3:
                raise ValueError("La matriz debe ser al menos 3x3.")

            dx = float(self.entry_dx.get())
            w = float(self.entry_w.get())
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_max_iter.get())

            # Preparar condiciones
            condiciones = {}
            for name in ("arriba", "abajo", "izquierda", "derecha"):
                cb = self.borders[name]["type"]
                val_entry = self.borders[name]["value"]
                tipo = cb.get()
                val_text = val_entry.get()

                length = cols if name in ("arriba", "abajo") else filas
                valor = _parse_value(val_text, length, dx)
                condiciones[name] = {"tipo": tipo, "valor": valor}

            # Malla inicial
            T0 = np.zeros((filas, cols), dtype=float)

            T, error, iters = resolver_laplace_general(T0, dx, condiciones, max_iter=max_iter, tol=tol, w=w)
            self.T_result = T  # Guardar para descargar

            # Mostrar resultados
            self.lbl_iters.config(text=str(iters))
            self.lbl_error.config(text=f"{error:.3e}")

            # Limpiar canvas anterior completamente
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.get_tk_widget().grid_forget()
                self.canvas.get_tk_widget().destroy()
            
            # Limpiar gráfico previo y su colorbar
            self.ax.clear()
            if self.cbar:
                try:
                    self.cbar.remove()
                except Exception:
                    pass
                self.cbar = None

            im = self.ax.imshow(T, origin="upper", cmap="plasma")
            self.ax.set_title("Distribución de temperatura")
            self.cbar = self.fig.colorbar(im, ax=self.ax, shrink=0.8)
            
            # Recrear canvas completamente
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.heatmap_frame)
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
            self.canvas.draw()

            self.txt_matrix.delete("1.0", tk.END)
            np.set_printoptions(precision=4, suppress=True)
            self.txt_matrix.config(state='normal')
            self.txt_matrix.insert("1.0", str(T))
            self.txt_matrix.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _download_csv(self):
        """Descarga la matriz T como CSV."""
        if self.T_result is None:
            messagebox.showwarning("Advertencia", "Primero resuelve el problema de Laplace.")
            return

        try:
            # Ruta por defecto: Descargas del usuario
            home = os.path.expanduser("~")
            downloads = os.path.join(home, "Downloads")
            if not os.path.exists(downloads):
                downloads = home

            # Nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(downloads, f"laplace_{timestamp}.csv")

            # Guardar CSV
            np.savetxt(filename, self.T_result, delimiter=",", fmt="%.6f")
            messagebox.showinfo("Éxito", f"Archivo guardado en:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error al descargar", str(e))
