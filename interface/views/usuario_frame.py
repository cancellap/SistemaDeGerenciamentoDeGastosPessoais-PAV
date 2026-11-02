"""Aba de CRUD de Usuários (nome + e-mail)."""

import re
import tkinter as tk
from tkinter import ttk

from interface.client.api_client import ApiClient
from interface.views.base_crud_frame import BaseCrudFrame

# Mesma regra da API (api/schemas/usuario_schema.py), para feedback imediato.
PADRAO_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


class UsuarioFrame(BaseCrudFrame):
    """Cadastro, edição, consulta e exclusão de usuários."""

    def __init__(self, master, api_client: ApiClient):
        super().__init__(
            master,
            api_client=api_client,
            recurso="usuarios",
            colunas=["id", "nome", "email"],
            titulos=["ID", "Nome", "E-mail"],
            nome_entidade="usuário",
        )

    def definir_campos(self) -> None:
        """Campos nome e e-mail."""
        ttk.Label(self.frame_form, text="Nome:").grid(
            row=0, column=0, sticky=tk.W, padx=4, pady=4
        )
        self.entrada_nome = ttk.Entry(self.frame_form, width=40)
        self.entrada_nome.grid(row=0, column=1, sticky=tk.W, padx=4, pady=4)

        ttk.Label(self.frame_form, text="E-mail:").grid(
            row=1, column=0, sticky=tk.W, padx=4, pady=4
        )
        self.entrada_email = ttk.Entry(self.frame_form, width=40)
        self.entrada_email.grid(row=1, column=1, sticky=tk.W, padx=4, pady=4)

        self.campos["nome"] = self.entrada_nome
        self.campos["email"] = self.entrada_email

    def validar(self) -> str | None:
        """Valida no cliente; a API ainda pode rejeitar (ex.: e-mail duplicado)."""
        nome = self.entrada_nome.get().strip()
        email = self.entrada_email.get().strip()

        if not nome:
            return "Informe o nome do usuário."
        if not email:
            return "Informe o e-mail do usuário."
        if not PADRAO_EMAIL.fullmatch(email):
            return "O e-mail informado não é válido."
        return None

    def montar_payload(self) -> dict:
        """Corpo do POST/PUT esperado pela API."""
        return {
            "nome": self.entrada_nome.get().strip(),
            "email": self.entrada_email.get().strip(),
        }

    def preencher_formulario(self, registro: dict) -> None:
        """Copia o registro selecionado para os Entries."""
        self.limpar_formulario()
        self.entrada_nome.insert(0, registro.get("nome", ""))
        self.entrada_email.insert(0, registro.get("email", ""))

    def limpar_formulario(self) -> None:
        """Esvazia os campos para um novo cadastro."""
        self.entrada_nome.delete(0, tk.END)
        self.entrada_email.delete(0, tk.END)

    def descricao_registro(self) -> str:
        """Mostra o nome no rótulo de modo (mais amigável que o ID)."""
        return self.entrada_nome.get().strip()
