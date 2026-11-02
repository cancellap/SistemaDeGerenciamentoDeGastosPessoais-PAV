"""Aba de análises: total, média, por categoria e anomalias (por usuário)."""

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

import tkinter as tk
from tkinter import ttk

from interface.client.api_client import ApiClient, ApiError
from interface.tema import (
    COR_BLOCO,
    COR_DESTAQUE,
    COR_FUNDO,
    COR_PAINEL,
    COR_TEXTO_SUAVE,
    fonte,
)
from interface.utils.formatacao import valor_para_exibicao
from interface.widgets import (
    AreaRolavel,
    CartaoExpansivel,
    Secao,
    ajustar_altura_lista,
    criar_bloco_secao,
    criar_lista_moderna,
    inserir_linha_lista,
    mostrar_erro,
)


class AnaliseFrame(ttk.Frame):
    """Consulta análises e organiza os resultados por usuário."""

    def __init__(self, master, api_client: ApiClient):
        super().__init__(master)
        self.api = api_client
        self._cards: dict[int, CartaoExpansivel] = {}
        self._usuario_expandido: int | None = None

        # Página rolável: evita scroll cortado nos cards.
        self.area = AreaRolavel(self)
        self.area.pack(fill=tk.BOTH, expand=True)
        self._raiz = self.area.corpo

        self._montar_resumo()
        self._montar_por_usuario()
        self.area.ativar_rodinha_em_arvore(self._raiz)

    def _montar_resumo(self) -> None:
        """Dois cards arredondados: total e média gerais (API)."""
        linha = tk.Frame(self._raiz, bg=COR_FUNDO)
        linha.pack(fill=tk.X, padx=20, pady=(12, 8))
        linha.columnconfigure(0, weight=1)
        linha.columnconfigure(1, weight=1)

        secao_total = Secao(linha, "Total geral", altura_minima=88)
        secao_total.grid(row=0, column=0, sticky=tk.EW, padx=(0, 8))
        self.rotulo_total = ttk.Label(
            secao_total.corpo, text="R$ —", style="MetricaValor.TLabel"
        )
        self.rotulo_total.pack(anchor=tk.W, pady=10)

        secao_media = Secao(linha, "Média geral", altura_minima=88)
        secao_media.grid(row=0, column=1, sticky=tk.EW, padx=(8, 0))
        self.rotulo_media = ttk.Label(
            secao_media.corpo, text="R$ —", style="MetricaValor.TLabel"
        )
        self.rotulo_media.pack(anchor=tk.W, pady=10)

    def _montar_por_usuario(self) -> None:
        """Cards expansíveis: análises de cada usuário."""
        secao = Secao(
            self._raiz,
            "Por usuário",
            ao_atualizar=self.atualizar,
        )
        secao.pack(fill=tk.X, padx=20, pady=(8, 24))
        self._lista_container = secao.corpo
        self._rotulo_vazio = tk.Label(
            self._lista_container,
            text="Nenhum gasto para analisar.",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SUAVE,
            font=fonte(10),
            anchor=tk.W,
        )

    def ao_exibir(self) -> None:
        """Chamado pela janela principal quando a aba fica visível."""
        self.atualizar()

    def atualizar(self) -> None:
        """Atualiza totais gerais (API) e cards por usuário (gastos)."""
        try:
            total = self.api.get_analise("total")
            media = self.api.get_analise("media")
            gastos = self.api.listar("gastos")
            usuarios = self.api.listar("usuarios")
            categorias = self.api.listar("categorias")
        except ApiError as erro:
            mostrar_erro(self.winfo_toplevel(), erro.mensagem)
            return

        self.rotulo_total.config(
            text=f"R$ {valor_para_exibicao(total.get('total', 0))}"
        )
        self.rotulo_media.config(
            text=f"R$ {valor_para_exibicao(media.get('media', 0))}"
        )

        usuarios_por_id = {item["id"]: item["nome"] for item in usuarios}
        categorias_por_id = {item["id"]: item["nome"] for item in categorias}

        self._limpar_cards()

        if not gastos:
            self._rotulo_vazio.pack(fill=tk.X, padx=4, pady=8)
            return
        self._rotulo_vazio.pack_forget()

        por_usuario: dict[int, list] = defaultdict(list)
        for gasto in gastos:
            uid = gasto.get("usuario_id")
            if uid is None:
                uid = -1
            por_usuario[int(uid)].append(gasto)

        ids_ordenados = sorted(
            por_usuario.keys(),
            key=lambda uid: usuarios_por_id.get(uid, f"#{uid}").lower(),
        )

        for usuario_id in ids_ordenados:
            self._criar_card_usuario(
                usuario_id,
                usuarios_por_id.get(usuario_id, f"Usuário #{usuario_id}"),
                por_usuario[usuario_id],
                categorias_por_id,
            )

        self.area.ativar_rodinha_em_arvore(self._lista_container)

    def _limpar_cards(self) -> None:
        for card in self._cards.values():
            card.destroy()
        self._cards.clear()
        self._usuario_expandido = None
        for filho in list(self._lista_container.winfo_children()):
            if filho is self._rotulo_vazio:
                continue
            filho.destroy()

    def _criar_card_usuario(
        self,
        usuario_id: int,
        nome: str,
        gastos: list,
        categorias_por_id: dict[int, str],
    ) -> None:
        total = self._somar(gastos)
        media = self._media(gastos)
        qtd = len(gastos)
        palavra = "gasto" if qtd == 1 else "gastos"
        # Totais ficam nos chips ao expandir — subtítulo só com a quantidade.
        subtitulo = f"{qtd} {palavra}"

        card = CartaoExpansivel(
            self._lista_container,
            titulo=nome,
            subtitulo=subtitulo,
            ao_alternar=lambda c, exp, uid=usuario_id: self._ao_alternar_card(
                uid, exp
            ),
        )
        card.pack(fill=tk.X, pady=(0, 10))

        # Duas métricas em destaque (sem repetir o subtítulo).
        faixa_metricas = tk.Frame(card.corpo, bg=COR_PAINEL)
        faixa_metricas.pack(fill=tk.X, pady=(0, 12))
        self._criar_chip_metrica(
            faixa_metricas,
            "Total",
            f"R$ {valor_para_exibicao(total)}",
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self._criar_chip_metrica(
            faixa_metricas,
            "Média",
            f"R$ {valor_para_exibicao(media)}",
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        # Por categoria (bloco visual separado).
        bloco_cat = criar_bloco_secao(card.corpo, "Gastos por categoria")
        tree_cat = criar_lista_moderna(
            bloco_cat,
            colunas=["categoria", "total"],
            titulos=["Categoria", "Total"],
            altura=1,
            larguras=[360, 120],
            coluna_flexivel="categoria",
        )
        por_cat = self._totais_por_categoria(gastos, categorias_por_id)
        self._preencher_tree(
            tree_cat,
            [
                (nome_cat, valor_para_exibicao(valor))
                for nome_cat, valor in por_cat
            ],
        )

        # Anomalias (bloco visual separado).
        bloco_anom = criar_bloco_secao(
            card.corpo, "Anomalias (valor > 2 × média)"
        )
        anomalias = self._anomalias(gastos, media)
        if not anomalias:
            tk.Label(
                bloco_anom,
                text="Nenhuma anomalia encontrada para este usuário.",
                bg=COR_BLOCO,
                fg=COR_TEXTO_SUAVE,
                font=fonte(9),
                anchor=tk.W,
            ).pack(fill=tk.X)
        else:
            tree_anom = criar_lista_moderna(
                bloco_anom,
                colunas=["descricao", "valor", "media"],
                titulos=["Descrição", "Valor", "Média"],
                altura=1,
                larguras=[320, 110, 110],
                coluna_flexivel="descricao",
            )
            self._preencher_tree(
                tree_anom,
                [
                    (
                        item["descricao"],
                        valor_para_exibicao(item["valor"]),
                        valor_para_exibicao(item["media"]),
                    )
                    for item in anomalias
                ],
            )

        self._cards[usuario_id] = card

    def _criar_chip_metrica(self, master, rotulo: str, valor: str) -> tk.Frame:
        """Mini-card com rótulo + valor (Total / Média)."""
        chip = tk.Frame(master, bg="#F0FDFA")
        interno = tk.Frame(chip, bg="#F0FDFA")
        interno.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        tk.Label(
            interno,
            text=rotulo,
            bg="#F0FDFA",
            fg=COR_TEXTO_SUAVE,
            font=fonte(9),
            anchor=tk.W,
        ).pack(fill=tk.X)
        tk.Label(
            interno,
            text=valor,
            bg="#F0FDFA",
            fg=COR_DESTAQUE,
            font=fonte(14, True),
            anchor=tk.W,
        ).pack(fill=tk.X, pady=(2, 0))
        return chip

    def _ao_alternar_card(self, usuario_id: int, expandido: bool) -> None:
        """Accordion: só um card aberto por vez."""
        if expandido:
            for uid, card in self._cards.items():
                if uid != usuario_id and card.expandido:
                    card.definir_expandido(False)
            self._usuario_expandido = usuario_id
        elif self._usuario_expandido == usuario_id:
            self._usuario_expandido = None

    def _preencher_tree(self, tree: ttk.Treeview, linhas: list) -> None:
        """Limpa a Treeview, insere linhas e ajusta a altura do card."""
        for item in tree.get_children():
            tree.delete(item)
        for indice, linha in enumerate(linhas):
            inserir_linha_lista(tree, linha, indice=indice)
        ajustar_altura_lista(tree, len(linhas))

    @staticmethod
    def _somar(gastos: list) -> float:
        total = Decimal("0")
        for gasto in gastos:
            total += Decimal(str(gasto.get("valor", 0) or 0))
        return float(
            total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )

    @staticmethod
    def _media(gastos: list) -> float:
        if not gastos:
            return 0.0
        total = Decimal("0")
        for gasto in gastos:
            total += Decimal(str(gasto.get("valor", 0) or 0))
        media = total / Decimal(len(gastos))
        return float(
            media.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )

    @staticmethod
    def _totais_por_categoria(
        gastos: list, categorias_por_id: dict[int, str]
    ) -> list[tuple[str, float]]:
        totais: dict[str, Decimal] = {}
        for gasto in gastos:
            cid = gasto.get("categoria_id")
            nome = categorias_por_id.get(cid, str(cid))
            totais[nome] = totais.get(nome, Decimal("0")) + Decimal(
                str(gasto.get("valor", 0) or 0)
            )
        ordenado = sorted(
            totais.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        return [
            (
                nome,
                float(valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            )
            for nome, valor in ordenado
        ]

    @staticmethod
    def _anomalias(gastos: list, media: float) -> list[dict]:
        limite = Decimal(str(media)) * Decimal("2")
        resultado = []
        for gasto in gastos:
            valor = Decimal(str(gasto.get("valor", 0) or 0))
            if valor > limite:
                resultado.append(
                    {
                        "descricao": gasto.get("descricao", ""),
                        "valor": float(
                            valor.quantize(
                                Decimal("0.01"), rounding=ROUND_HALF_UP
                            )
                        ),
                        "media": media,
                    }
                )
        return resultado
