from tkinter import ttk

class BaseView(ttk.Frame):
    def __init__(self, parent, layout=None): # Cambiado: ahora acepta layout
        super().__init__(parent)
        self.layout = layout # Guardamos la referencia para usar el FunctionManager
        self.build()

    def build(self):
        raise NotImplementedError("Las vistas deben implementar build()")