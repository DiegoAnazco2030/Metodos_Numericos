from tkinter import ttk


class BaseView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build()

    def build(self):
        raise NotImplementedError("Las vistas deben implementar build()")
