"""Frame base de CRUD: listagem com ações + modais de cadastro/edição."""

import tkinter as tk
from tkinter import ttk

from interface.client.api_client import ApiClient, ApiError
from interface.widgets import (
    AreaRolavel,
    ModalFormulario,
    Secao,
    ajustar_altura_lista,
    configurar_acoes_lista,
    confirmar_acao,
    criar_lista_moderna,
    inserir_linha_lista,
    mostrar_alerta,
    mostrar_erro,
    mostrar_sucesso,
)


class BaseCrudFrame(ttk.Frame):
    """Tela genérica: lista + (＋ / caneta / lixeira) abrem modais."""

    def __init__(
        self,
        master,
        api_client: ApiClient,
        recurso: str,
        colunas: list[str],
        titulos: list[str],
        nome_entidade: str,
        titulo_lista: str,
        genero: str = "a",
    ):
        super().__init__(master)

        self.api = api_client
        self.recurso = recurso
        self.colunas = colunas
        self.titulos = titulos
        self.nome_entidade = nome_entidade
        self.titulo_lista = titulo_lista
        self.genero = genero

        self.id_atual: int | None = None
        self.campos: dict[str, tk.Widget] = {}
        self.frame_form = None
        self._modal: ModalFormulario | None = None

        self.area = AreaRolavel(self)
        self.area.pack(fill=tk.BOTH, expand=True)
        self._raiz = self.area.corpo

        self._montar_listagem()
        self.area.ativar_rodinha_em_arvore(self._raiz)

    def _titulo_formulario(self) -> str:
        if self.id_atual is None:
            artigo = "nova" if self.genero == "a" else "novo"
            return f"Cadastrar {artigo} {self.nome_entidade}"
        return f"Editar {self.nome_entidade}"

    def _janela(self):
        return self.winfo_toplevel()

    def _montar_listagem(self) -> None:
        secao = Secao(
            self._raiz,
            self.titulo_lista,
            ao_adicionar=self.abrir_cadastro,
            texto_adicionar="Cadastrar",
            ao_atualizar=self.atualizar_lista,
        )
        secao.pack(fill=tk.X, padx=20, pady=(12, 24))

        flexivel = "email" if "email" in self.colunas else (
            "nome" if "nome" in self.colunas else self.colunas[-1]
        )
        self.tree = criar_lista_moderna(
            secao.corpo,
            colunas=self.colunas,
            titulos=self.titulos,
            altura=1,
            com_acoes=True,
            coluna_flexivel=flexivel,
        )
        configurar_acoes_lista(
            self.tree,
            ao_editar=self.abrir_edicao,
            ao_excluir=self.confirmar_exclusao,
        )

    def definir_campos(self) -> None:
        raise NotImplementedError

    def validar(self) -> str | None:
        raise NotImplementedError

    def montar_payload(self) -> dict:
        raise NotImplementedError

    def preencher_formulario(self, registro: dict) -> None:
        raise NotImplementedError

    def limpar_formulario(self) -> None:
        raise NotImplementedError

    def descricao_registro(self) -> str:
        return ""

    def valores_da_linha(self, registro: dict) -> tuple:
        return tuple(registro.get(coluna, "") for coluna in self.colunas)

    def preparar_formulario(self) -> bool:
        return True

    def ao_exibir(self) -> None:
        self.atualizar_lista()

    def atualizar_lista(self) -> None:
        try:
            registros = self.api.listar(self.recurso)
        except ApiError as erro:
            mostrar_erro(self._janela(), erro.mensagem)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for indice, registro in enumerate(registros):
            inserir_linha_lista(
                self.tree,
                self.valores_da_linha(registro),
                iid=str(registro["id"]),
                indice=indice,
            )

        ajustar_altura_lista(self.tree, len(registros))

    def abrir_cadastro(self) -> None:
        self.id_atual = None
        self._abrir_modal()

    def abrir_edicao(self, id_registro: int) -> None:
        self.id_atual = id_registro
        try:
            registro = self.api.buscar(self.recurso, id_registro)
        except ApiError as erro:
            mostrar_erro(self._janela(), erro.mensagem)
            self.atualizar_lista()
            return
        self._abrir_modal(registro)

    def _abrir_modal(self, registro: dict | None = None) -> None:
        if self._modal is not None and self._modal.winfo_exists():
            self._modal.lift()
            return

        if not self.preparar_formulario():
            return

        modal = ModalFormulario(
            self._janela(),
            titulo=self._titulo_formulario(),
            ao_salvar=self._salvar_modal,
        )
        self._modal = modal
        self.frame_form = modal.corpo
        self.definir_campos()

        if registro is None:
            self.limpar_formulario()
        else:
            self.preencher_formulario(registro)

        modal.focus_set()

    def _salvar_modal(self, modal: ModalFormulario) -> None:
        mensagem_erro = self.validar()
        if mensagem_erro:
            mostrar_alerta(modal, mensagem_erro, titulo="Dados inválidos")
            return

        try:
            dados = self.montar_payload()
            if self.id_atual is None:
                self.api.criar(self.recurso, dados)
                mostrar_sucesso(modal, "Registro criado.")
            else:
                self.api.atualizar(self.recurso, self.id_atual, dados)
                mostrar_sucesso(modal, "Registro atualizado.")
        except ApiError as erro:
            mostrar_erro(modal, erro.mensagem)
            if "não encontrad" in erro.mensagem.lower():
                modal.destroy()
                self._modal = None
                self.id_atual = None
                self.atualizar_lista()
            return

        modal.destroy()
        self._modal = None
        self.id_atual = None
        self.atualizar_lista()

    def confirmar_exclusao(self, id_registro: int) -> None:
        ok = confirmar_acao(
            self._janela(),
            f"Deseja realmente excluir este {self.nome_entidade}?",
            titulo="Confirmar exclusão",
        )
        if not ok:
            return

        try:
            self.api.excluir(self.recurso, id_registro)
            mostrar_sucesso(self._janela(), "Registro excluído.")
        except ApiError as erro:
            mostrar_erro(self._janela(), erro.mensagem)
            if "não encontrad" in erro.mensagem.lower():
                self.atualizar_lista()
            return

        self.atualizar_lista()
