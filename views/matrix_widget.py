import tkinter as tk
from tkinter import ttk, messagebox

class MatrixWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.entries_A = [] # Guardará los inputs de la Matriz A
        self.entries_b = [] # Guardará los inputs del Vector b
        self.n = 0
        
        self._setup_ui()

    def _setup_ui(self):
        # --- Panel de control (n) ---
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Dimensión (n):").pack(side=tk.LEFT)
        self.entry_n = ttk.Entry(control_frame, width=5)
        self.entry_n.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Generar Matriz", command=self._generate_grid).pack(side=tk.LEFT, padx=5)

        # --- Contenedor de la cuadrícula ---
        # Usamos un canvas por si la matriz es muy grande y necesitamos scroll (opcional simplificado aquí)
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def _generate_grid(self):
        # 1. Limpiar grid anterior
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.entries_A.clear()
        self.entries_b.clear()

        try:
            self.n = int(self.entry_n.get())
            if self.n < 2: raise ValueError
        except:
            messagebox.showerror("Error", "Ingrese una dimensión válida (entero > 1).")
            return

        # 2. Encabezados
        ttk.Label(self.grid_frame, text="Matriz A", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=self.n, pady=5)
        ttk.Label(self.grid_frame, text="Vector b", font=("Arial", 10, "bold")).grid(row=0, column=self.n+1, pady=5)

        # 3. Generar Celdas
        for i in range(self.n):
            row_entries = []
            # Matriz A
            for j in range(self.n):
                entry = ttk.Entry(self.grid_frame, width=8, justify='center')
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.entries_A.append(row_entries)

            # Separador visual
            ttk.Separator(self.grid_frame, orient='vertical').grid(row=i+1, column=self.n, sticky='ns', padx=10)

            # Vector b
            entry_b = ttk.Entry(self.grid_frame, width=8, justify='center')
            entry_b.grid(row=i+1, column=self.n+1, padx=2, pady=2)
            self.entries_b.append(entry_b)

    def get_matrix_system(self):
        """Retorna (A, b) como listas de floats"""
        try:
            A = []
            b = []
            
            # Extraer A
            for i in range(self.n):
                row = []
                for j in range(self.n):
                    val = float(self.entries_A[i][j].get())
                    row.append(val)
                A.append(row)
            
            # Extraer b
            for i in range(self.n):
                val = float(self.entries_b[i].get())
                b.append(val)
                
            return A, b
        except ValueError:
            raise ValueError("Asegúrese de que todas las celdas contengan números válidos.")