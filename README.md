# SistemaDeGerenciamentoDeGastosPessoais-PAV

## API

A API utiliza FastAPI, SQLAlchemy e PostgreSQL, organizada nas camadas:

```text
routes -> controllers -> services -> repositories -> entities
```

Os schemas Pydantic ficam em `api/schemas/`.

### Endpoints CRUD

```text
POST   /usuarios
GET    /usuarios
GET    /usuarios/{id}
PUT    /usuarios/{id}
DELETE /usuarios/{id}

POST   /categorias
GET    /categorias
GET    /categorias/{id}
PUT    /categorias/{id}
DELETE /categorias/{id}

POST   /gastos
GET    /gastos
GET    /gastos/{id}
PUT    /gastos/{id}
DELETE /gastos/{id}
```

Para executar localmente:

```bash
uvicorn api.app:app --reload
```

A documentação interativa fica disponível em `/docs`.

### Endpoints de análise

```text
GET /analises/gastos/total
GET /analises/gastos/media
GET /analises/gastos/por-categoria
GET /analises/gastos/anomalias
```

As anomalias são gastos cujo valor é maior que duas vezes a média dos gastos.

## Como executar

Copie `.env.example` para `.env` e ajuste as credenciais se necessário. Os
valores padrao do Compose permitem executar o projeto mesmo sem alterar esse
arquivo.

```bash
docker compose down -v
docker compose up --build
```

A API ficará disponível em `http://localhost:8000` e a documentação Swagger
em `http://localhost:8000/docs`. A interface Tkinter é executada fora do
Docker.

Para consultar os dados diretamente no PostgreSQL:

```bash
docker compose exec database psql -U postgres -d analise_gastos -c "SELECT * FROM categorias;"
```

O volume `postgres_data` mantém os registros após `docker compose restart`.
O arquivo `api/init.sql` só é executado quando o volume está vazio; para
recriar as tabelas, use `docker compose down -v` antes de subir novamente.

## Interface Tkinter

A interface roda fora do Docker e usa a API em `http://localhost:8000`.

Crie o ambiente virtual uma vez:

```powershell
python -m venv interface/.venv
interface/.venv/Scripts/python.exe -m pip install -r interface/requirements.txt
```

Para ativar o ambiente no PowerShell:

```powershell
interface/.venv/Scripts/Activate.ps1
```

Ou instale a dependência diretamente pelo interpretador do ambiente:

```bash
interface/.venv/Scripts/python.exe -m pip install -r interface/requirements.txt
```

Com a API em execução no Docker, inicie a janela principal:

```bash
interface/.venv/Scripts/python.exe -m interface.main
```

Teste manualmente:

1. Cadastre, edite, consulte e exclua uma categoria.
2. Repita o CRUD para usuário e gasto.
3. No gasto, use data `DD/MM/AAAA`, valor com vírgula e os selects de usuário e categoria.
4. Abra análises e confira total, média, maior categoria e anomalias.
5. Derrube a API e confirme que a interface exibe `Não foi possível conectar à API.` sem fechar.
6. Teste valor zero, e-mail inválido/duplicado, categoria duplicada, usuário inexistente, categoria inexistente e campos em branco.

As regras de negócio da API incluem valor positivo, e-mail válido e único,
nome de categoria único, campos obrigatórios, existência de usuário e
categoria nos gastos e bloqueio da exclusão de registros vinculados.

### Testes do backend

Na raiz do projeto, execute:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q api tests
```

Para validar a execução integrada, com o Docker Desktop iniciado:

```powershell
docker compose down -v
docker compose up --build
```
