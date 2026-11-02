"""Aba de CRUD de Gastos (com Combobox de usuário e categoria)."""

import tkinter as tk
from tkinter import messagebox, ttk

from interface.client.api_client import ApiClient, ApiError
from interface.utils.formatacao import (
    data_para_api,
    data_para_exibicao,
    valor_para_api,
    valor_para_exibicao,
)
from interface.views.base_crud_frame import BaseCrudFrame


class GastoFrame(BaseCrudFrame):
    """Cadastro, edição, consulta e exclusão de gastos."""

    def __init__(self, master, api_client: ApiClient):
        # Mapas id -> nome, usados na lista e nos Combobox.
        self.usuarios_por_id: dict[int, str] = {}
        self.categorias_por_id: dict[int, str] = {}

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
        )

    def definir_campos(self) -> None:
        """Campos do gasto + selects de usuário e categoria."""
        ttk.Label(self.frame_form, text="Descrição:").grid(
            row=0, column=0, sticky=tk.W, padx=4, pady=4
        )
        self.entrada_descricao = ttk.Entry(self.frame_form, width=40)
        self.entrada_descricao.grid(
            row=0, column=1, sticky=tk.W, padx=4, pady=4
        )

        ttk.Label(self.frame_form, text="Valor (ex: 10,50):").grid(
            row=1, column=0, sticky=tk.W, padx=4, pady=4
        )
        self.entrada_valor = ttk.Entry(self.frame_form, width=20)
        self.entrada_valor.grid(row=1, column=1, sticky=tk.W, padx=4, pady=4)

        ttk.Label(self.frame_form, text="Data (DD/MM/AAAA):").grid(
            row=2, column=0, sticky=tk.W, padx=4, pady=4
        )
        self.entrada_data = ttk.Entry(self.frame_form, width=20)
        self.entrada_data.grid(row=2, column=1, sticky=tk.W, padx=4, pady=4)

        ttk.Label(self.frame_form, text="Usuário:").grid(
            row=3, column=0, sticky=tk.W, padx=4, pady=4
        )
        # readonly: só permite escolher itens da lista.
        self.combo_usuario = ttk.Combobox(
            self.frame_form, width=37, state="readonly"
        )
        self.combo_usuario.grid(row=3, column=1, sticky=tk.W, padx=4, pady=4)

        ttk.Label(self.frame_form, text="Categoria:").grid(
            row=4, column=0, sticky=tk.W, padx=4, pady=4
        )
        self.combo_categoria = ttk.Combobox(
            self.frame_form, width=37, state="readonly"
        )
        self.combo_categoria.grid(
            row=4, column=1, sticky=tk.W, padx=4, pady=4
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
        # Sem Combobox atualizados, não dá para selecionar usuário/categoria.
        if not self._carregar_combos():
            return
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
        """Mostra valor/data no formato BR e nomes em vez de IDs."""
        usuario_id = registro.get("usuario_id")
        categoria_id = registro.get("categoria_id")
        return (
            registro.get("id", ""),
            registro.get("descricao", ""),
            valor_para_exibicao(registro.get("valor", 0)),
            data_para_exibicao(registro.get("data", "")),
            self.usuarios_por_id.get(usuario_id, str(usuario_id)),
            self.categorias_por_id.get(categoria_id, str(categoria_id)),
        )

    def atualizar_lista(self) -> None:
        """Recarrega Combobox (usuários/categorias) e a lista de gastos."""
        if not self._carregar_combos():
            return
        super().atualizar_lista()

    def _carregar_combos(self) -> bool:
        """Busca usuários e categorias na API para os Combobox."""
        try:
            usuarios = self.api.listar("usuarios")
            categorias = self.api.listar("categorias")
        except ApiError as erro:
            messagebox.showerror("Erro", erro.mensagem)
            return False

        self.usuarios_por_id = {
            item["id"]: item["nome"] for item in usuarios
        }
        self.categorias_por_id = {
            item["id"]: item["nome"] for item in categorias
        }

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
