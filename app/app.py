import tkinter as tk
from tkinter import ttk
from app.layout import MainLayout


class NumericalMethodsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Métodos Numéricos")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        style = ttk.Style(self.root)
        style.theme_use("clam")

        self.layout = MainLayout(self.root)

    def run(self):
        self.root.mainloop()
