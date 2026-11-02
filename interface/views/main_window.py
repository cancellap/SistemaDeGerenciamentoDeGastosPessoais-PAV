"""Janela principal com abas (Notebook) para cada módulo."""

import tkinter as tk
from tkinter import ttk

from interface.client.api_client import ApiClient
from interface.views.analise_frame import AnaliseFrame
from interface.views.categoria_frame import CategoriaFrame
from interface.views.gasto_frame import GastoFrame
from interface.views.usuario_frame import UsuarioFrame


class MainWindow(tk.Tk):
    """Janela raiz da aplicação Tkinter."""

    def __init__(self):
        super().__init__()

        self.title("Análise de Gastos Pessoais")
        self.geometry("800x620")

        # Um único client HTTP compartilhado por todas as abas.
        self.api = ApiClient()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.notebook.add(CategoriaFrame(self.notebook, self.api), text="Categorias")
        self.notebook.add(UsuarioFrame(self.notebook, self.api), text="Usuários")
        self.notebook.add(GastoFrame(self.notebook, self.api), text="Gastos")
        self.notebook.add(AnaliseFrame(self.notebook, self.api), text="Análises")

        # Ao trocar de aba, recarrega os dados da aba visível.
        self.notebook.bind("<<NotebookTabChanged>>", self._ao_mudar_aba)
        # Garante o primeiro carregamento da aba inicial.
        self._carregar_aba_atual()

    def _ao_mudar_aba(self, _evento=None) -> None:
        """Dispara o carregamento da aba selecionada."""
        self._carregar_aba_atual()

    def _carregar_aba_atual(self) -> None:
        """Chama ao_exibir() da aba ativa (se existir)."""
        aba_id = self.notebook.select()
        if not aba_id:
            return
        aba = self.notebook.nametowidget(aba_id)
        if hasattr(aba, "ao_exibir"):
            aba.ao_exibir()
