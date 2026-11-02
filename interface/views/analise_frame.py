"""Aba de análises: total, média, por categoria e anomalias."""

import tkinter as tk
from tkinter import messagebox, ttk

from interface.client.api_client import ApiClient, ApiError
from interface.utils.formatacao import valor_para_exibicao


class AnaliseFrame(ttk.Frame):
    """Consulta os 4 endpoints /analises/gastos/* e exibe os resultados."""

    def __init__(self, master, api_client: ApiClient):
        super().__init__(master)
        self.api = api_client

        self._montar_resumo()
        self._montar_por_categoria()
        self._montar_anomalias()
        self._montar_botao()

        # Dados carregados em ao_exibir() quando a aba é selecionada.

    def _montar_resumo(self) -> None:
        """Labels de total e média."""
        frame = ttk.LabelFrame(self, text="Resumo")
        frame.pack(fill=tk.X, padx=8, pady=8)

        self.rotulo_total = ttk.Label(frame, text="Total: —")
        self.rotulo_total.pack(anchor=tk.W, padx=8, pady=4)

        self.rotulo_media = ttk.Label(frame, text="Média: —")
        self.rotulo_media.pack(anchor=tk.W, padx=8, pady=4)

    def _montar_por_categoria(self) -> None:
        """Treeview com o total gasto em cada categoria."""
        frame = ttk.LabelFrame(self, text="Gastos por categoria")
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        colunas = ("categoria", "total")
        self.tree_categorias = ttk.Treeview(
            frame, columns=colunas, show="headings", height=6
        )
        self.tree_categorias.heading("categoria", text="Categoria")
        self.tree_categorias.heading("total", text="Total")
        self.tree_categorias.column("categoria", width=200)
        self.tree_categorias.column("total", width=120)
        self.tree_categorias.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    def _montar_anomalias(self) -> None:
        """Treeview com gastos acima de 2x a média."""
        frame = ttk.LabelFrame(
            self, text="Anomalias (valor > 2 × média)"
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        colunas = ("descricao", "valor", "media")
        self.tree_anomalias = ttk.Treeview(
            frame, columns=colunas, show="headings", height=6
        )
        self.tree_anomalias.heading("descricao", text="Descrição")
        self.tree_anomalias.heading("valor", text="Valor")
        self.tree_anomalias.heading("media", text="Média")
        self.tree_anomalias.column("descricao", width=220)
        self.tree_anomalias.column("valor", width=100)
        self.tree_anomalias.column("media", width=100)
        self.tree_anomalias.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    def _montar_botao(self) -> None:
        """Botão para refazer as consultas na API."""
        ttk.Button(self, text="Atualizar análises", command=self.atualizar).pack(
            padx=8, pady=8
        )

    def ao_exibir(self) -> None:
        """Chamado pela janela principal quando a aba fica visível."""
        self.atualizar()

    def atualizar(self) -> None:
        """Chama os 4 endpoints e preenche a tela."""
        try:
            total = self.api.get_analise("total")
            media = self.api.get_analise("media")
            por_categoria = self.api.get_analise("por-categoria")
            anomalias = self.api.get_analise("anomalias")
        except ApiError as erro:
            messagebox.showerror("Erro", erro.mensagem)
            return

        self.rotulo_total.config(
            text=f"Total: R$ {valor_para_exibicao(total.get('total', 0))}"
        )
        self.rotulo_media.config(
            text=f"Média: R$ {valor_para_exibicao(media.get('media', 0))}"
        )

        self._preencher_tree(
            self.tree_categorias,
            [
                (item.get("categoria", ""), valor_para_exibicao(item.get("total", 0)))
                for item in por_categoria
            ],
        )
        self._preencher_tree(
            self.tree_anomalias,
            [
                (
                    item.get("descricao", ""),
                    valor_para_exibicao(item.get("valor", 0)),
                    valor_para_exibicao(item.get("media", 0)),
                )
                for item in anomalias
            ],
        )

    def _preencher_tree(self, tree: ttk.Treeview, linhas: list) -> None:
        """Limpa a Treeview e insere as linhas novas."""
        for item in tree.get_children():
            tree.delete(item)
        for linha in linhas:
            tree.insert("", tk.END, values=linha)
