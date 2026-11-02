"""Frame base de CRUD: listagem + formulário + botões.

As subclasses (Categoria, Usuario, Gasto) só sobrescrevem os métodos
marcados abaixo; o fluxo de salvar/excluir/atualizar fica aqui.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from interface.client.api_client import ApiClient, ApiError


class BaseCrudFrame(ttk.Frame):
    """Tela genérica de cadastro/consulta/edição/exclusão."""

    def __init__(
        self,
        master,
        api_client: ApiClient,
        recurso: str,
        colunas: list[str],
        titulos: list[str],
        nome_entidade: str,
    ):
        super().__init__(master)

        # Client HTTP compartilhado pela janela principal.
        self.api = api_client
        # Nome do recurso na API, ex.: "categorias".
        self.recurso = recurso
        # Nomes dos campos do JSON (ex.: ["id", "nome"]).
        self.colunas = colunas
        # Rótulos exibidos no cabeçalho da Treeview.
        self.titulos = titulos
        # Nome amigável no singular, ex.: "categoria", "usuário".
        self.nome_entidade = nome_entidade

        # Id do registro selecionado (None = modo cadastro).
        self.id_atual: int | None = None

        # Widgets do formulário: a filha preenche em definir_campos().
        self.campos: dict[str, tk.Widget] = {}

        self._montar_listagem()
        self._montar_formulario()
        self._montar_modo()
        self._montar_botoes()

        # Carrega os dados assim que a aba aparece.
        self.atualizar_lista()
        # Começa pronto para cadastrar (sem seleção).
        self._atualizar_rotulo_modo()

    # ------------------------------------------------------------------
    # Montagem visual (comum a todas as entidades)
    # ------------------------------------------------------------------

    def _montar_listagem(self) -> None:
        """Cria a Treeview com as colunas da entidade."""
        frame_lista = ttk.Frame(self)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.tree = ttk.Treeview(
            frame_lista,
            columns=self.colunas,
            show="headings",
            height=10,
        )
        for coluna, titulo in zip(self.colunas, self.titulos):
            self.tree.heading(coluna, text=titulo)
            self.tree.column(coluna, width=120, anchor=tk.W)

        # Barra de rolagem vertical.
        scroll = ttk.Scrollbar(
            frame_lista, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Clique na linha -> preenche o formulário.
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _montar_formulario(self) -> None:
        """Área do formulário; a filha cria os Entry/Combobox."""
        self.frame_form = ttk.LabelFrame(self, text="Formulário")
        self.frame_form.pack(fill=tk.X, padx=8, pady=4)
        # Hook: cada entidade define seus próprios campos.
        self.definir_campos()

    def _montar_modo(self) -> None:
        """Rótulo que deixa claro se estamos cadastrando ou editando."""
        self.rotulo_modo = ttk.Label(self, text="")
        self.rotulo_modo.pack(fill=tk.X, padx=8, pady=(4, 0))

    def _montar_botoes(self) -> None:
        """Botões de ação do CRUD (nomes alinhados ao que cada um faz)."""
        frame_botoes = ttk.Frame(self)
        frame_botoes.pack(fill=tk.X, padx=8, pady=8)

        # Limpar: só esvazia o formulário (não grava nada na API).
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar).pack(
            side=tk.LEFT, padx=4
        )
        # Salvar: POST (novo) ou PUT (edição), conforme o modo.
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(frame_botoes, text="Excluir", command=self.excluir).pack(
            side=tk.LEFT, padx=4
        )
        # Atualizar lista: refaz o GET; não altera o registro do formulário.
        ttk.Button(
            frame_botoes, text="Atualizar lista", command=self.atualizar_lista
        ).pack(side=tk.LEFT, padx=4)

    # ------------------------------------------------------------------
    # Métodos que as subclasses DEVEM sobrescrever
    # ------------------------------------------------------------------

    def definir_campos(self) -> None:
        """Cria os widgets do formulário dentro de self.frame_form."""
        raise NotImplementedError

    def validar(self) -> str | None:
        """Validação no cliente. Retorna mensagem de erro ou None."""
        raise NotImplementedError

    def montar_payload(self) -> dict:
        """Monta o dicionário JSON enviado no POST/PUT."""
        raise NotImplementedError

    def preencher_formulario(self, registro: dict) -> None:
        """Copia os dados do registro selecionado para o formulário."""
        raise NotImplementedError

    def limpar_formulario(self) -> None:
        """Esvazia os campos (modo cadastro)."""
        raise NotImplementedError

    def descricao_registro(self) -> str:
        """Texto amigável do registro em edição (ex.: nome)."""
        raise NotImplementedError

    def _atualizar_rotulo_modo(self) -> None:
        """Mostra se o Salvar vai criar ou alterar."""
        if self.id_atual is None:
            texto = f"Modo: novo cadastro de {self.nome_entidade}"
        else:
            # Aspas deixam o nome do registro mais fácil de ler.
            texto = (
                f'Modo: editando {self.nome_entidade} '
                f'"{self.descricao_registro()}"'
            )
        self.rotulo_modo.config(text=texto)

    def valores_da_linha(self, registro: dict) -> tuple:
        """Converte um registro JSON na tupla exibida na Treeview."""
        return tuple(registro.get(coluna, "") for coluna in self.colunas)

    # ------------------------------------------------------------------
    # Ações do CRUD
    # ------------------------------------------------------------------

    def atualizar_lista(self) -> None:
        """Busca todos os registros na API e redesenha a Treeview."""
        try:
            registros = self.api.listar(self.recurso)
        except ApiError as erro:
            messagebox.showerror("Erro", erro.mensagem)
            return

        # Limpa linhas antigas.
        for item in self.tree.get_children():
            self.tree.delete(item)

        for registro in registros:
            self.tree.insert(
                "",
                tk.END,
                iid=str(registro["id"]),
                values=self.valores_da_linha(registro),
            )

    def limpar(self) -> None:
        """Esvazia o formulário e volta ao modo de novo cadastro."""
        self.id_atual = None
        self.tree.selection_remove(self.tree.selection())
        self.limpar_formulario()
        self._atualizar_rotulo_modo()

    def salvar(self) -> None:
        """Cria (POST) ou atualiza (PUT) conforme self.id_atual."""
        # Validação local antes de chamar a API.
        mensagem_erro = self.validar()
        if mensagem_erro:
            messagebox.showwarning("Dados inválidos", mensagem_erro)
            return

        try:
            dados = self.montar_payload()
            if self.id_atual is None:
                self.api.criar(self.recurso, dados)
                messagebox.showinfo("Sucesso", "Registro criado.")
            else:
                self.api.atualizar(self.recurso, self.id_atual, dados)
                messagebox.showinfo("Sucesso", "Registro atualizado.")
        except ApiError as erro:
            # Sempre mostra também o erro que a API devolveu.
            messagebox.showerror("Erro", erro.mensagem)
            return

        self.atualizar_lista()
        self.limpar()

    def excluir(self) -> None:
        """Exclui o registro selecionado, com confirmação."""
        if self.id_atual is None:
            messagebox.showwarning(
                "Atenção", "Selecione um registro para excluir."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este registro?",
        )
        if not confirmar:
            return

        try:
            self.api.excluir(self.recurso, self.id_atual)
            messagebox.showinfo("Sucesso", "Registro excluído.")
        except ApiError as erro:
            messagebox.showerror("Erro", erro.mensagem)
            return

        self.atualizar_lista()
        self.limpar()

    def _ao_selecionar(self, _evento=None) -> None:
        """Quando o usuário clica numa linha, preenche o formulário."""
        selecionados = self.tree.selection()
        if not selecionados:
            return

        id_texto = selecionados[0]
        self.id_atual = int(id_texto)

        try:
            registro = self.api.buscar(self.recurso, self.id_atual)
        except ApiError as erro:
            # Ex.: registro excluído por outro lado.
            messagebox.showerror("Erro", erro.mensagem)
            self.atualizar_lista()
            self.limpar()
            return

        self.preencher_formulario(registro)
        self._atualizar_rotulo_modo()
