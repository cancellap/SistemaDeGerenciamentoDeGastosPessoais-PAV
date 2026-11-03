"""Aba de análises: total, média, por categoria e anomalias (via API)."""

import tkinter as tk
from tkinter import ttk

from interface.client.api_client import ApiClient, ApiError
from interface.tema import (
    COR_BLOCO,
    COR_FUNDO,
    COR_TEXTO_SUAVE,
    fonte,
)
from interface.utils.formatacao import valor_para_exibicao
from interface.widgets import (
    AreaRolavel,
    Secao,
    ajustar_altura_lista,
    criar_bloco_secao,
    criar_lista_moderna,
    inserir_linha_lista,
    mostrar_erro,
)


class AnaliseFrame(ttk.Frame):
    """Consulta os quatro endpoints de análise da API."""

    def __init__(self, master, api_client: ApiClient):
        super().__init__(master)
        self.api = api_client

        self.area = AreaRolavel(self)
        self.area.pack(fill=tk.BOTH, expand=True)
        self._raiz = self.area.corpo

        self._montar_resumo()
        self._montar_detalhes()
        self.area.ativar_rodinha_em_arvore(self._raiz)

    def _montar_resumo(self) -> None:
        """Cards: total, média e categoria com maior gasto."""
        linha = tk.Frame(self._raiz, bg=COR_FUNDO)
        linha.pack(fill=tk.X, padx=20, pady=(12, 8))
        for coluna in range(3):
            linha.columnconfigure(coluna, weight=1)

        secao_total = Secao(linha, "Total geral", altura_minima=88)
        secao_total.grid(row=0, column=0, sticky=tk.EW, padx=(0, 8))
        self.rotulo_total = ttk.Label(
            secao_total.corpo, text="R$ —", style="MetricaValor.TLabel"
        )
        self.rotulo_total.pack(anchor=tk.W, pady=10)

        secao_media = Secao(linha, "Média geral", altura_minima=88)
        secao_media.grid(row=0, column=1, sticky=tk.EW, padx=8)
        self.rotulo_media = ttk.Label(
            secao_media.corpo, text="R$ —", style="MetricaValor.TLabel"
        )
        self.rotulo_media.pack(anchor=tk.W, pady=10)

        secao_maior = Secao(linha, "Maior categoria", altura_minima=88)
        secao_maior.grid(row=0, column=2, sticky=tk.EW, padx=(8, 0))
        self.rotulo_maior_cat = ttk.Label(
            secao_maior.corpo,
            text="—",
            style="Card.TLabel",
            font=fonte(11, True),
        )
        self.rotulo_maior_cat.pack(anchor=tk.W, pady=(6, 0))
        self.rotulo_maior_valor = ttk.Label(
            secao_maior.corpo, text="R$ —", style="MetricaValor.TLabel"
        )
        self.rotulo_maior_valor.pack(anchor=tk.W, pady=(2, 8))

    def _montar_detalhes(self) -> None:
        """Listas alimentadas por /por-categoria e /anomalias."""
        secao = Secao(
            self._raiz,
            "Detalhes das análises",
            ao_atualizar=self.atualizar,
        )
        secao.pack(fill=tk.X, padx=20, pady=(8, 24))
        self._lista_container = secao.corpo

        bloco_cat = criar_bloco_secao(
            self._lista_container, "Gastos por categoria"
        )
        self.tree_categoria = criar_lista_moderna(
            bloco_cat,
            colunas=["categoria", "total"],
            titulos=["Categoria", "Total"],
            altura=1,
            larguras=[360, 120],
            coluna_flexivel="categoria",
        )
        self._rotulo_cat_vazio = tk.Label(
            bloco_cat,
            text="Nenhuma categoria com gastos.",
            bg=COR_BLOCO,
            fg=COR_TEXTO_SUAVE,
            font=fonte(9),
            anchor=tk.W,
        )

        bloco_anom = criar_bloco_secao(
            self._lista_container,
            "Anomalias (valor > 2 × média geral)",
        )
        self.tree_anomalia = criar_lista_moderna(
            bloco_anom,
            colunas=["descricao", "valor", "media"],
            titulos=["Descrição", "Valor", "Média geral"],
            altura=1,
            larguras=[320, 110, 120],
            coluna_flexivel="descricao",
        )
        self._rotulo_anom_vazio = tk.Label(
            bloco_anom,
            text="Nenhuma anomalia encontrada.",
            bg=COR_BLOCO,
            fg=COR_TEXTO_SUAVE,
            font=fonte(9),
            anchor=tk.W,
        )

    def ao_exibir(self) -> None:
        """Chamado pela janela principal quando a aba fica visível."""
        self.atualizar()

    def atualizar(self) -> None:
        """Busca total, média, por-categoria e anomalias na API."""
        try:
            total = self.api.get_analise("total")
            media = self.api.get_analise("media")
            por_categoria = self.api.get_analise("por-categoria")
            anomalias = self.api.get_analise("anomalias")
        except ApiError as erro:
            mostrar_erro(self.winfo_toplevel(), erro.mensagem)
            return

        if not isinstance(por_categoria, list):
            por_categoria = []
        if not isinstance(anomalias, list):
            anomalias = []

        self.rotulo_total.config(
            text=f"R$ {valor_para_exibicao(total.get('total', 0))}"
        )
        self.rotulo_media.config(
            text=f"R$ {valor_para_exibicao(media.get('media', 0))}"
        )

        if por_categoria:
            maior = por_categoria[0]
            self.rotulo_maior_cat.config(
                text=str(maior.get("categoria", "—"))
            )
            self.rotulo_maior_valor.config(
                text=f"R$ {valor_para_exibicao(maior.get('total', 0))}"
            )
        else:
            self.rotulo_maior_cat.config(text="—")
            self.rotulo_maior_valor.config(text="R$ —")

        self._preencher_categorias(por_categoria)
        self._preencher_anomalias(anomalias)
        self.area.ativar_rodinha_em_arvore(self._lista_container)

    def _preencher_categorias(self, por_categoria: list) -> None:
        self._preencher_tree(
            self.tree_categoria,
            [
                (
                    item.get("categoria", ""),
                    valor_para_exibicao(item.get("total", 0)),
                )
                for item in por_categoria
            ],
        )
        if por_categoria:
            self._rotulo_cat_vazio.pack_forget()
        else:
            self._rotulo_cat_vazio.pack(fill=tk.X, pady=(4, 0))

    def _preencher_anomalias(self, anomalias: list) -> None:
        self._preencher_tree(
            self.tree_anomalia,
            [
                (
                    item.get("descricao", ""),
                    valor_para_exibicao(item.get("valor", 0)),
                    valor_para_exibicao(item.get("media", 0)),
                )
                for item in anomalias
            ],
        )
        if anomalias:
            self._rotulo_anom_vazio.pack_forget()
        else:
            self._rotulo_anom_vazio.pack(fill=tk.X, pady=(4, 0))

    def _preencher_tree(self, tree: ttk.Treeview, linhas: list) -> None:
        """Limpa a Treeview, insere linhas e ajusta a altura."""
        for item in tree.get_children():
            tree.delete(item)
        for indice, linha in enumerate(linhas):
            inserir_linha_lista(tree, linha, indice=indice)
        ajustar_altura_lista(tree, len(linhas))
