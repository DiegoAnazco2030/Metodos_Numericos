import tkinter as tk
from tkinter import ttk, messagebox
from utils.sympy_utils import parse_function


class FunctionManager:
    def __init__(self, parent):
        self.functions = []

        self.entry = ttk.Entry(parent)
        self.entry.pack(fill=tk.X, padx=10, pady=(0, 5))

        ttk.Button(
            parent,
            text="Agregar función",
            command=self.add_function
        ).pack(fill=tk.X, padx=10, pady=(0, 8))

        self.listbox = tk.Listbox(parent)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def add_function(self):
        expr = self.entry.get()
        if not expr:
            return

        try:
            parse_function(expr)
        except Exception as e:
            messagebox.showerror("Error", f"Función inválida:\n{e}")
            return

        self.functions.append(expr)
        self.listbox.insert(tk.END, expr)
        self.entry.delete(0, tk.END)

    def get_selected_function(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return self.functions[selection[0]]
