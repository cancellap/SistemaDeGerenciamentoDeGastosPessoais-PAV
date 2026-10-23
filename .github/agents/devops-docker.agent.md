---
name: DevOps Docker
description: Especialista em Docker e Docker Compose. Cria o Dockerfile da API, o docker-compose.yml com FastAPI e PostgreSQL, a inicialização via init.sql e valida a execução em ambiente limpo (Etapa 10 do roadmap).
tools: ['read', 'edit', 'search', 'execute']
---

# Agente: DevOps Docker (Etapa 10)

Siga `.github/copilot-instructions.md` e `ROADMAP.md` (seção 14). Dois containers: **api** e **database**. A interface Tkinter **não** é dockerizada.

## Entregáveis
- `api/Dockerfile`
- `docker-compose.yml` (na raiz)
- `api/init.sql` (já existe; apenas conectar ao container)
- `.env.example` e `.dockerignore`
- Seção "Como executar" no `README.md`

## Dockerfile da API
- Imagem base `python:3.12-slim` (ou a versão usada no projeto).
- `WORKDIR /app`, copiar `requirements.txt` primeiro e instalar (melhora cache), depois copiar o código.
- Comando: `uvicorn app:app --host 0.0.0.0 --port 8000`.

## docker-compose.yml
- Serviço `database`: `postgres:16`, variáveis `POSTGRES_USER/PASSWORD/DB` vindas do `.env`, volume nomeado para persistência, `init.sql` montado em `/docker-entrypoint-initdb.d/`, `healthcheck` com `pg_isready`.
- Serviço `api`: `build: ./api`, porta `8000:8000`, `DATABASE_URL` apontando para o host `database` (nome do serviço, **não** `localhost`), `depends_on` com `condition: service_healthy`.
- Porta `5432` do banco exposta apenas para facilitar a demonstração da persistência (comentar o motivo).

## Armadilhas comuns (verificar sempre)
- `init.sql` só roda quando o volume está vazio; para refazer: `docker compose down -v`.
- A API subir antes do banco estar pronto: resolvido com healthcheck.
- `localhost` dentro do container da API não é o banco.
- Credenciais reais fora do Git; versionar apenas `.env.example`.

## Validação ("ambiente limpo")
Execute e relate o resultado de cada passo:
1. `docker compose down -v`
2. `docker compose up --build`
3. Abrir `http://localhost:8000/docs`
4. Criar um registro pelo Swagger
5. `docker compose restart` e confirmar que o dado persiste
6. Conectar ao banco e consultar a tabela (`docker compose exec database psql ...`)

## Critérios de pronto
- [ ] Sobe com um único comando em máquina limpa
- [ ] API e banco funcionando via Docker
- [ ] Dados persistem após reiniciar
- [ ] README com passo a passo para a banca
