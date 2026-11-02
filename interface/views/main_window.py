"""Janela principal com abas em formato de pílula."""

import tkinter as tk

from interface.client.api_client import ApiClient
from interface.tema import (
    COR_CABECALHO,
    COR_CABECALHO_SUB,
    COR_CABECALHO_TEXTO,
    COR_DESTAQUE,
    aplicar_tema,
    fonte,
)
from interface.views.analise_frame import AnaliseFrame
from interface.views.categoria_frame import CategoriaFrame
from interface.views.gasto_frame import GastoFrame
from interface.views.usuario_frame import UsuarioFrame
from interface.widgets import NavegacaoAbas


class MainWindow(tk.Tk):
    """Janela raiz da aplicação Tkinter."""

    def __init__(self):
        super().__init__()

        self.title("Análise de Gastos Pessoais")
        self.geometry("960x720")
        self.minsize(820, 580)

        # Tema visual aplicado uma vez na janela raiz.
        aplicar_tema(self)

        # Um único client HTTP compartilhado por todas as abas.
        self.api = ApiClient()

        self._montar_cabecalho()

        # Abas próprias (pílulas) — sem o Notebook do ttk que “encolhe”.
        self.navegacao = NavegacaoAbas(self)
        self.navegacao.pack(fill=tk.BOTH, expand=True, padx=20, pady=(16, 20))

        self.navegacao.adicionar(
            "Categorias", CategoriaFrame(self.navegacao.area, self.api)
        )
        self.navegacao.adicionar(
            "Usuários", UsuarioFrame(self.navegacao.area, self.api)
        )
        self.navegacao.adicionar(
            "Gastos", GastoFrame(self.navegacao.area, self.api)
        )
        self.navegacao.adicionar(
            "Análises", AnaliseFrame(self.navegacao.area, self.api)
        )
        self.navegacao.mostrar_primeira()

    def _montar_cabecalho(self) -> None:
        """Cabeçalho em destaque (fundo teal)."""
        cabecalho = tk.Frame(self, bg=COR_CABECALHO)
        cabecalho.pack(fill=tk.X)

        tk.Label(
            cabecalho,
            text="Análise de Gastos Pessoais",
            bg=COR_CABECALHO,
            fg=COR_CABECALHO_TEXTO,
            font=fonte(20, True),
            anchor=tk.W,
        ).pack(anchor=tk.W, padx=24, pady=(18, 2))

        tk.Label(
            cabecalho,
            text="Cadastre usuários, categorias e gastos - e acompanhe as análises.",
            bg=COR_CABECALHO,
            fg=COR_CABECALHO_SUB,
            font=fonte(10),
            anchor=tk.W,
        ).pack(anchor=tk.W, padx=24, pady=(0, 18))

        # Detalhe mais escuro na base do cabeçalho.
        tk.Frame(self, bg=COR_DESTAQUE, height=2).pack(fill=tk.X)
