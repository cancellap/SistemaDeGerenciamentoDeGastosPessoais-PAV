# Configurações da interface.
# Separadas do código para facilitar alterar a URL sem mexer no client.

# Endereço base da API (roda no Docker, porta 8000).
API_URL = "http://localhost:8000"

# Tempo máximo de espera por resposta (em segundos).
# Evita a janela ficar travada se a API não responder.
TIMEOUT = 5
