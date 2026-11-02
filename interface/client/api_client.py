"""Cliente HTTP genérico para consumir a API FastAPI."""

import requests

from interface.config import API_URL, TIMEOUT


class ApiError(Exception):
    """Erro amigável para a interface exibir ao usuário."""

    def __init__(self, mensagem: str):
        # Guarda a mensagem em português, pronta para o messagebox.
        self.mensagem = mensagem
        super().__init__(mensagem)


class ApiClient:
    """Encapsula as chamadas HTTP (CRUD + análises) com tratamento de erro."""

    def __init__(self, base_url: str = API_URL, timeout: int = TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def listar(self, recurso: str) -> list:
        """GET /{recurso} -> lista de registros."""
        resposta = self._requisitar("GET", f"/{recurso}")
        return resposta.json()

    def buscar(self, recurso: str, id_registro: int) -> dict:
        """GET /{recurso}/{id} -> um registro."""
        resposta = self._requisitar("GET", f"/{recurso}/{id_registro}")
        return resposta.json()

    def criar(self, recurso: str, dados: dict) -> dict:
        """POST /{recurso} -> registro criado."""
        resposta = self._requisitar("POST", f"/{recurso}", json=dados)
        return resposta.json()

    def atualizar(self, recurso: str, id_registro: int, dados: dict) -> dict:
        """PUT /{recurso}/{id} -> registro atualizado."""
        resposta = self._requisitar(
            "PUT", f"/{recurso}/{id_registro}", json=dados
        )
        return resposta.json()

    def excluir(self, recurso: str, id_registro: int) -> None:
        """DELETE /{recurso}/{id} -> 204 sem corpo."""
        self._requisitar("DELETE", f"/{recurso}/{id_registro}")

    def get_analise(self, caminho: str):
        """GET /analises/gastos/{caminho} -> total, media, etc."""
        resposta = self._requisitar("GET", f"/analises/gastos/{caminho}")
        return resposta.json()

    def _requisitar(self, metodo: str, caminho: str, json: dict | None = None):
        """Executa a requisição e traduz erros HTTP/rede em ApiError."""
        url = f"{self.base_url}{caminho}"
        try:
            resposta = requests.request(
                metodo,
                url,
                json=json,
                timeout=self.timeout,
            )
        except requests.RequestException as erro:
            # Conexão, timeout ou outra falha de rede: janela não trava.
            raise ApiError("Não foi possível conectar à API.") from erro

        if resposta.ok:
            return resposta

        # Traduz o status HTTP para uma mensagem compreensível.
        raise ApiError(self._extrair_mensagem(resposta))

    def _extrair_mensagem(self, resposta: requests.Response) -> str:
        """Lê o JSON de erro da API e devolve texto legível."""
        status = resposta.status_code

        if status == 404:
            return self._mensagem_404(resposta)

        if status in (400, 409, 422):
            return self._mensagem_detail(resposta)

        # Qualquer outro código (500, etc.): mensagem genérica.
        return f"Erro inesperado da API (código {status})."

    def _mensagem_404(self, resposta: requests.Response) -> str:
        """404: usa a mensagem da API ou um texto padrão."""
        detalhe = self._ler_detail(resposta)
        if detalhe:
            return detalhe
        return "Registro não encontrado."

    def _mensagem_detail(self, resposta: requests.Response) -> str:
        """400/409/422: extrai detail (string ou lista de validação)."""
        detalhe = self._ler_detail(resposta)
        if detalhe:
            return detalhe
        return "Não foi possível concluir a operação."

    def _ler_detail(self, resposta: requests.Response) -> str:
        """
        O FastAPI devolve {"detail": "..." } ou
        {"detail": [{"msg": "...", "loc": [...], ...}, ...]}.
        """
        try:
            corpo = resposta.json()
        except ValueError:
            return ""

        detalhe = corpo.get("detail", "")

        # Erro de negócio: detail é uma string simples.
        if isinstance(detalhe, str):
            return detalhe

        # Erro de validação Pydantic: detail é uma lista de objetos.
        if isinstance(detalhe, list):
            mensagens = []
            for item in detalhe:
                if isinstance(item, dict):
                    # Preferimos "msg"; se não houver, usamos o item inteiro.
                    mensagem = str(item.get("msg", item))
                else:
                    mensagem = str(item)
                # Pydantic v2 prefixa com "Value error, "; removemos para ficar legível.
                if mensagem.startswith("Value error, "):
                    mensagem = mensagem[len("Value error, ") :]
                mensagens.append(mensagem)
            return " ".join(mensagens)

        return str(detalhe) if detalhe else ""
