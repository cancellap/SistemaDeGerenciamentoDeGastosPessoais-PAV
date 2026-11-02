"""Aba de CRUD de Gastos (com Combobox de usuário e categoria)."""

import tkinter as tk
from collections import defaultdict
from tkinter import ttk

from interface.client.api_client import ApiClient, ApiError
from interface.tema import COR_TEXTO_SUAVE, fonte
from interface.utils.formatacao import (
    data_para_api,
    data_para_exibicao,
    valor_para_api,
    valor_para_exibicao,
)
from interface.views.base_crud_frame import BaseCrudFrame
from interface.widgets import (
    CartaoExpansivel,
    Secao,
    ajustar_altura_lista,
    configurar_acoes_lista,
    criar_bloco_secao,
    criar_lista_moderna,
    inserir_linha_lista,
    mostrar_erro,
)


class GastoFrame(BaseCrudFrame):
    """Cadastro, edição, consulta e exclusão de gastos."""

    # Colunas da tabela interna (sem "usuário": já está no card).
    COLUNAS_LISTA = ["id", "descricao", "valor", "data", "categoria"]
    TITULOS_LISTA = ["ID", "Descrição", "Valor", "Data", "Categoria"]
    LARGURAS_LISTA = [48, 180, 88, 102, 150]

    def __init__(self, master, api_client: ApiClient):
        # Mapas id -> nome, usados na lista e nos Combobox.
        self.usuarios_por_id: dict[int, str] = {}
        self.categorias_por_id: dict[int, str] = {}
        # Cards expansíveis por usuário e a tree de cada um.
        self._cards: dict[int, CartaoExpansivel] = {}
        self._arvores: dict[int, ttk.Treeview] = {}
        self._usuario_expandido: int | None = None

        super().__init__(
            master,
            api_client=api_client,
            recurso="gastos",
            colunas=[
                "id",
                "descricao",
                "valor",
                "data",
                "usuario",
                "categoria",
            ],
            titulos=[
                "ID",
                "Descrição",
                "Valor",
                "Data",
                "Usuário",
                "Categoria",
            ],
            nome_entidade="gasto",
            titulo_lista="Gastos",
            genero="o",
        )

    def _montar_listagem(self) -> None:
        """Lista agrupada por usuário: card expansível → tabela de gastos."""
        secao = Secao(
            self._raiz,
            self.titulo_lista,
            ao_adicionar=self.abrir_cadastro,
            texto_adicionar="Cadastrar",
            ao_atualizar=self.atualizar_lista,
        )
        secao.pack(fill=tk.X, padx=20, pady=(12, 24))
        self._lista_container = secao.corpo
        self.tree = None  # várias trees (uma por usuário)
        self._rotulo_vazio = tk.Label(
            self._lista_container,
            text="Nenhum gasto cadastrado ainda.",
            bg=self._lista_container.cget("background"),
            fg=COR_TEXTO_SUAVE,
            font=fonte(10),
            anchor=tk.W,
        )

    def preparar_formulario(self) -> bool:
        """Garante Combobox de usuário/categoria antes de abrir o modal."""
        return self._carregar_combos()

    def definir_campos(self) -> None:
        """Campos do gasto + selects de usuário e categoria."""
        ttk.Label(
            self.frame_form, text="Descrição:", style="Card.TLabel"
        ).grid(row=0, column=0, sticky=tk.W, padx=(4, 12), pady=6)
        self.entrada_descricao = ttk.Entry(self.frame_form, width=42)
        self.entrada_descricao.grid(
            row=0, column=1, sticky=tk.EW, padx=(0, 4), pady=6
        )

        ttk.Label(
            self.frame_form, text="Valor (ex: 10,50):", style="Card.TLabel"
        ).grid(row=1, column=0, sticky=tk.W, padx=(4, 12), pady=6)
        self.entrada_valor = ttk.Entry(self.frame_form, width=20)
        self.entrada_valor.grid(
            row=1, column=1, sticky=tk.W, padx=(0, 4), pady=6
        )

        ttk.Label(
            self.frame_form, text="Data (DD/MM/AAAA):", style="Card.TLabel"
        ).grid(row=2, column=0, sticky=tk.W, padx=(4, 12), pady=6)
        self.entrada_data = ttk.Entry(self.frame_form, width=20)
        self.entrada_data.grid(
            row=2, column=1, sticky=tk.W, padx=(0, 4), pady=6
        )

        ttk.Label(
            self.frame_form, text="Usuário:", style="Card.TLabel"
        ).grid(row=3, column=0, sticky=tk.W, padx=(4, 12), pady=6)
        # readonly: só permite escolher itens da lista.
        self.combo_usuario = ttk.Combobox(
            self.frame_form, width=40, state="readonly"
        )
        self.combo_usuario.grid(
            row=3, column=1, sticky=tk.EW, padx=(0, 4), pady=6
        )

        ttk.Label(
            self.frame_form, text="Categoria:", style="Card.TLabel"
        ).grid(row=4, column=0, sticky=tk.W, padx=(4, 12), pady=6)
        self.combo_categoria = ttk.Combobox(
            self.frame_form, width=40, state="readonly"
        )
        self.combo_categoria.grid(
            row=4, column=1, sticky=tk.EW, padx=(0, 4), pady=6
        )

    def validar(self) -> str | None:
        """Valida no cliente antes do POST/PUT."""
        descricao = self.entrada_descricao.get().strip()
        if not descricao:
            return "Informe a descrição do gasto."

        texto_valor = self.entrada_valor.get().strip()
        if not texto_valor:
            return "Informe o valor do gasto."
        try:
            valor = valor_para_api(texto_valor)
        except ValueError:
            return "Valor inválido. Use números, ex.: 10,50."
        if valor <= 0:
            return "O valor do gasto deve ser maior que zero."

        texto_data = self.entrada_data.get().strip()
        if not texto_data:
            return "Informe a data do gasto (DD/MM/AAAA)."
        try:
            data_para_api(texto_data)
        except ValueError:
            return "Data inválida. Use o formato DD/MM/AAAA."

        # Sem cadastros prévios, o Combobox fica vazio — mensagem mais clara.
        if not self.combo_usuario["values"]:
            return "Cadastre um usuário antes de criar um gasto."
        if not self.combo_categoria["values"]:
            return "Cadastre uma categoria antes de criar um gasto."
        if not self.combo_usuario.get():
            return "Selecione um usuário."
        if not self.combo_categoria.get():
            return "Selecione uma categoria."

        return None

    def montar_payload(self) -> dict:
        """Converte a tela para o JSON que a API espera."""
        return {
            "descricao": self.entrada_descricao.get().strip(),
            "valor": valor_para_api(self.entrada_valor.get()),
            "data": data_para_api(self.entrada_data.get()),
            "usuario_id": self._id_do_combo(self.combo_usuario),
            "categoria_id": self._id_do_combo(self.combo_categoria),
        }

    def preencher_formulario(self, registro: dict) -> None:
        """Copia o gasto da API para o formulário (formatos BR)."""
        self.limpar_formulario()

        self.entrada_descricao.insert(0, registro.get("descricao", ""))
        self.entrada_valor.insert(
            0, valor_para_exibicao(registro.get("valor", 0))
        )
        self.entrada_data.insert(
            0, data_para_exibicao(registro.get("data", ""))
        )

        usuario_id = registro.get("usuario_id")
        categoria_id = registro.get("categoria_id")
        self.combo_usuario.set(self._texto_combo(usuario_id, self.usuarios_por_id))
        self.combo_categoria.set(
            self._texto_combo(categoria_id, self.categorias_por_id)
        )

    def limpar_formulario(self) -> None:
        """Esvazia campos e Combobox."""
        self.entrada_descricao.delete(0, tk.END)
        self.entrada_valor.delete(0, tk.END)
        self.entrada_data.delete(0, tk.END)
        self.combo_usuario.set("")
        self.combo_categoria.set("")

    def descricao_registro(self) -> str:
        """Usa a descrição do gasto no rótulo de modo."""
        return self.entrada_descricao.get().strip()

    def valores_da_linha(self, registro: dict) -> tuple:
        """Linha sem coluna de usuário (já aparece no card)."""
        categoria_id = registro.get("categoria_id")
        return (
            registro.get("id", ""),
            registro.get("descricao", ""),
            valor_para_exibicao(registro.get("valor", 0)),
            data_para_exibicao(registro.get("data", "")),
            self.categorias_por_id.get(categoria_id, str(categoria_id)),
        )

    def atualizar_lista(self) -> None:
        """Recarrega mapas e redesenha os cards por usuário."""
        if not self._carregar_mapas():
            return

        try:
            registros = self.api.listar(self.recurso)
        except ApiError as erro:
            mostrar_erro(self.winfo_toplevel(), erro.mensagem)
            return

        self._limpar_cards()

        if not registros:
            self._rotulo_vazio.pack(fill=tk.X, padx=4, pady=8)
            return
        self._rotulo_vazio.pack_forget()

        por_usuario: dict[int, list] = defaultdict(list)
        for registro in registros:
            uid = registro.get("usuario_id")
            if uid is None:
                uid = -1
            por_usuario[int(uid)].append(registro)

        ids_ordenados = sorted(
            por_usuario.keys(),
            key=lambda uid: self.usuarios_por_id.get(uid, f"#{uid}").lower(),
        )

        for usuario_id in ids_ordenados:
            self._criar_card_usuario(usuario_id, por_usuario[usuario_id])

        self.area.ativar_rodinha_em_arvore(self._lista_container)

    def _limpar_cards(self) -> None:
        for card in self._cards.values():
            card.destroy()
        self._cards.clear()
        self._arvores.clear()
        self._usuario_expandido = None
        for filho in list(self._lista_container.winfo_children()):
            if filho is self._rotulo_vazio:
                continue
            filho.destroy()

    def _criar_card_usuario(self, usuario_id: int, gastos: list) -> None:
        nome = self.usuarios_por_id.get(usuario_id, f"Usuário #{usuario_id}")
        total = sum(float(g.get("valor", 0) or 0) for g in gastos)
        qtd = len(gastos)
        palavra = "gasto" if qtd == 1 else "gastos"
        subtitulo = f"{qtd} {palavra} · R$ {valor_para_exibicao(total)}"

        card = CartaoExpansivel(
            self._lista_container,
            titulo=nome,
            subtitulo=subtitulo,
            ao_alternar=lambda c, exp, uid=usuario_id: self._ao_alternar_card(
                uid, exp
            ),
        )
        card.pack(fill=tk.X, pady=(0, 10))

        bloco = criar_bloco_secao(card.corpo, "Gastos deste usuário")
        tree = criar_lista_moderna(
            bloco,
            colunas=self.COLUNAS_LISTA,
            titulos=self.TITULOS_LISTA,
            altura=1,
            larguras=self.LARGURAS_LISTA,
            com_acoes=True,
            coluna_flexivel="descricao",
        )
        configurar_acoes_lista(
            tree,
            ao_editar=self.abrir_edicao,
            ao_excluir=self.confirmar_exclusao,
        )

        for indice, registro in enumerate(gastos):
            inserir_linha_lista(
                tree,
                self.valores_da_linha(registro),
                iid=str(registro["id"]),
                indice=indice,
            )
        ajustar_altura_lista(tree, len(gastos))

        self._cards[usuario_id] = card
        self._arvores[usuario_id] = tree

    def _ao_alternar_card(self, usuario_id: int, expandido: bool) -> None:
        """Accordion: só um card aberto por vez."""
        if expandido:
            for uid, card in self._cards.items():
                if uid != usuario_id and card.expandido:
                    card.definir_expandido(False)
            self._usuario_expandido = usuario_id
        elif self._usuario_expandido == usuario_id:
            self._usuario_expandido = None

    def _carregar_mapas(self) -> bool:
        """Atualiza mapas id→nome (sem depender dos Combobox do modal)."""
        try:
            usuarios = self.api.listar("usuarios")
            categorias = self.api.listar("categorias")
        except ApiError as erro:
            mostrar_erro(self.winfo_toplevel(), erro.mensagem)
            return False

        self.usuarios_por_id = {
            item["id"]: item["nome"] for item in usuarios
        }
        self.categorias_por_id = {
            item["id"]: item["nome"] for item in categorias
        }
        return True

    def _carregar_combos(self) -> bool:
        """Busca usuários/categorias e preenche os Combobox do modal."""
        if not self._carregar_mapas():
            return False

        if not hasattr(self, "combo_usuario"):
            return True

        self.combo_usuario["values"] = [
            self._texto_combo(item_id, self.usuarios_por_id)
            for item_id in self.usuarios_por_id
        ]
        self.combo_categoria["values"] = [
            self._texto_combo(item_id, self.categorias_por_id)
            for item_id in self.categorias_por_id
        ]
        return True

    def _texto_combo(self, item_id: int | None, mapa: dict[int, str]) -> str:
        """Formato exibido no Combobox: 'id - nome'."""
        if item_id is None:
            return ""
        nome = mapa.get(item_id, "?")
        return f"{item_id} - {nome}"

    def _id_do_combo(self, combo: ttk.Combobox) -> int:
        """Extrai o id do texto 'id - nome'."""
        texto = combo.get()
        # Parte antes do ' - ' é o id.
        return int(texto.split(" - ", 1)[0])
