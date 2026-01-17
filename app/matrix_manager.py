import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from views.matrix_widget import MatrixWidget


class MatrixManager:
    def __init__(self, parent):
        self.matrices = []  # Almacena las matrices como (A, b)
        
        ttk.Button(
            parent,
            text="Agregar Matriz",
            command=self.add_matrix
        ).pack(fill=tk.X, padx=10, pady=(0, 8))

        self.listbox = tk.Listbox(parent)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def add_matrix(self):
        """Abre un diálogo con el widget de matriz"""
        dialog = tk.Toplevel()
        dialog.title("Agregar Matriz")
        dialog.geometry("500x400")
        
        # Crear el widget de matriz
        matrix_widget = MatrixWidget(dialog)
        matrix_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para botones
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_matrix():
            try:
                A, b = matrix_widget.get_matrix_system()
                self.matrices.append((A, b))
                self.listbox.insert(tk.END, f"Matriz {len(self.matrices)}")
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            button_frame,
            text="Guardar",
            command=save_matrix
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy
        ).pack(side=tk.RIGHT)

    def get_selected_matrix(self):
        """Retorna la matriz seleccionada como (A, b)"""
        selection = self.listbox.curselection()
        if not selection:
            return None
        return self.matrices[selection[0]]
