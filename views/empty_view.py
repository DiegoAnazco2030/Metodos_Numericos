from views.base_view import BaseView
from tkinter import ttk


class EmptyView(BaseView):
    def build(self):
        ttk.Label(
            self,
            text="Seleccione un método numérico desde el panel izquierdo",
            font=("Segoe UI", 14)
        ).pack(expand=True)
