"""Janela principal com abas (Notebook) para cada módulo."""

import tkinter as tk
from tkinter import ttk

from interface.client.api_client import ApiClient
from interface.views.categoria_frame import CategoriaFrame
from interface.views.gasto_frame import GastoFrame
from interface.views.usuario_frame import UsuarioFrame


class MainWindow(tk.Tk):
    """Janela raiz da aplicação Tkinter."""

    def __init__(self):
        super().__init__()

        self.title("Análise de Gastos Pessoais")
        self.geometry("800x560")

        # Um único client HTTP compartilhado por todas as abas.
        self.api = ApiClient()

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        notebook.add(CategoriaFrame(notebook, self.api), text="Categorias")
        notebook.add(UsuarioFrame(notebook, self.api), text="Usuários")
        notebook.add(GastoFrame(notebook, self.api), text="Gastos")
        notebook.add(self._aba_placeholder("Análises"), text="Análises")

    def _aba_placeholder(self, nome: str) -> ttk.Frame:
        """Frame temporário até a entidade ser implementada."""
        frame = ttk.Frame(self)
        label = ttk.Label(
            frame,
            text=f"Aba {nome}: será implementada nas próximas fases.",
        )
        label.pack(padx=16, pady=16)
        return frame
