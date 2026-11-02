"""Aba de CRUD de Categorias (a entidade mais simples)."""

import tkinter as tk
from tkinter import ttk

from interface.client.api_client import ApiClient
from interface.views.base_crud_frame import BaseCrudFrame


class CategoriaFrame(BaseCrudFrame):
    """Cadastro, edição, consulta e exclusão de categorias."""

    def __init__(self, master, api_client: ApiClient):
        # Colunas do JSON da API e títulos exibidos na Treeview.
        super().__init__(
            master,
            api_client=api_client,
            recurso="categorias",
            colunas=["id", "nome"],
            titulos=["ID", "Nome"],
            nome_entidade="categoria",
            titulo_lista="Categorias",
            genero="a",
        )

    def definir_campos(self) -> None:
        """Um único campo: nome da categoria."""
        ttk.Label(self.frame_form, text="Nome:", style="Card.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=(4, 12), pady=8
        )
        self.entrada_nome = ttk.Entry(self.frame_form, width=42)
        self.entrada_nome.grid(
            row=0, column=1, sticky=tk.EW, padx=(0, 4), pady=8
        )
        self.campos["nome"] = self.entrada_nome

    def validar(self) -> str | None:
        """No cliente: nome não pode ficar em branco."""
        nome = self.entrada_nome.get().strip()
        if not nome:
            return "Informe o nome da categoria."
        return None

    def montar_payload(self) -> dict:
        """Corpo do POST/PUT esperado pela API."""
        return {"nome": self.entrada_nome.get().strip()}

    def preencher_formulario(self, registro: dict) -> None:
        """Copia o registro selecionado para o Entry."""
        self.limpar_formulario()
        self.entrada_nome.insert(0, registro.get("nome", ""))

    def limpar_formulario(self) -> None:
        """Esvazia o campo para um novo cadastro."""
        self.entrada_nome.delete(0, tk.END)

    def descricao_registro(self) -> str:
        """Nome da categoria selecionada, para o rótulo de modo."""
        return self.entrada_nome.get().strip()
