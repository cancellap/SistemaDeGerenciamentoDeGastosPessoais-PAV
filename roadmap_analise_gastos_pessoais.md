# Roadmap — Análise de Gastos Pessoais

## 1. Objetivo do projeto

Desenvolver um sistema simples de **Análise de Gastos Pessoais**, permitindo cadastrar usuários, categorias e gastos, além de realizar análises básicas sobre os dados registrados.

O projeto deve evitar funcionalidades desnecessariamente complexas. O foco é cumprir os requisitos acadêmicos com uma implementação simples e fácil de explicar durante a apresentação.

A aplicação terá:

- API REST desenvolvida com FastAPI;
- PostgreSQL como banco de dados;
- SQLAlchemy como ORM;
- Interface gráfica desenvolvida com Tkinter;
- Docker para a API e o banco;
- Funcionalidades de análise de dados.

---

# 2. Escopo do sistema

O sistema permitirá:

- cadastrar usuários;
- cadastrar categorias de gastos;
- cadastrar gastos;
- consultar registros;
- editar registros;
- excluir registros;
- calcular o total de gastos;
- calcular a média dos gastos;
- analisar gastos por categoria;
- identificar gastos acima do padrão.

A parte de Ciência de Dados será baseada em **processamento, agregação e análise dos dados de gastos**.

Não será necessário utilizar Machine Learning.

---

# 3. Modelo do banco de dados

Para manter o projeto simples, serão utilizadas **3 tabelas**:

```text
USUARIO
   |
   | 1:N
   |
GASTO
   |
   | N:1
   |
CATEGORIA
```

## 3.1 Tabela `usuarios`

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| nome | VARCHAR | Nome do usuário |
| email | VARCHAR | E-mail do usuário |

---

## 3.2 Tabela `categorias`

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| nome | VARCHAR | Nome da categoria |

Exemplos:

- Alimentação
- Transporte
- Lazer
- Moradia
- Saúde

---

## 3.3 Tabela `gastos`

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| descricao | VARCHAR | Descrição do gasto |
| valor | DECIMAL | Valor do gasto |
| data | DATE | Data do gasto |
| usuario_id | INTEGER | FK para usuário |
| categoria_id | INTEGER | FK para categoria |

Exemplo:

```text
id: 1
descricao: Almoço
valor: 35.90
data: 20/09/2026
usuario_id: 1
categoria_id: 1
```

## 3.4 Relacionamentos

```text
Usuario 1 ---- N Gasto

Categoria 1 ---- N Gasto
```

Um usuário pode possuir vários gastos.

Cada gasto pertence a um único usuário.

Uma categoria pode possuir vários gastos.

Cada gasto possui uma única categoria.

---

# 4. Regras de negócio

O sistema terá **10 regras de negócio**, cobrindo validação de campos, integridade referencial e análise de dados.

## Regra 1 — Valor do gasto deve ser positivo

O sistema não deve permitir gastos com valor menor ou igual a zero.

```text
valor > 0
```

Exemplos:

```text
R$ 50,00  → permitido
R$ 0,00   → rejeitado
R$ -20,00 → rejeitado
```

---

## Regra 2 — E-mail do usuário deve ser único

Não será permitido cadastrar dois usuários com o mesmo e-mail.

Exemplo:

```text
João → joao@email.com → permitido

Maria → joao@email.com → rejeitado
```

---

## Regra 3 — Categoria deve existir

Ao cadastrar um gasto, a categoria informada deve existir no banco.

Exemplo:

```text
categoria_id = 1 → categoria existente → permitido

categoria_id = 999 → categoria inexistente → rejeitado
```

---

## Regra 4 — Nome do usuário é obrigatório

O sistema não deve permitir o cadastro de um usuário sem nome preenchido.

Exemplo:

```text
Nome: "Maria"  → permitido
Nome: ""       → rejeitado
Nome: null     → rejeitado
```

---

## Regra 5 — E-mail deve ter formato válido

O e-mail informado deve seguir um formato válido, contendo "@" e um domínio.

Exemplo:

```text
maria@email.com → permitido
mariaemail.com  → rejeitado
maria@          → rejeitado
```

---

## Regra 6 — Nome da categoria deve ser único

Não será permitido cadastrar duas categorias com o mesmo nome.

Exemplo:

```text
Alimentação → permitido (primeiro cadastro)

Alimentação → rejeitado (já existe)
```

---

## Regra 7 — Descrição do gasto é obrigatória

O sistema não deve permitir o cadastro de um gasto sem descrição.

Exemplo:

```text
Descrição: "Almoço" → permitido
Descrição: ""       → rejeitado
```

---

## Regra 8 — Usuário deve existir ao cadastrar gasto

Ao cadastrar um gasto, o usuário informado deve existir no banco (mesma lógica da Regra 3, aplicada ao `usuario_id`).

Exemplo:

```text
usuario_id = 1   → usuário existente    → permitido

usuario_id = 999 → usuário inexistente  → rejeitado
```

---

## Regra 9 — Não é possível excluir categoria vinculada a gastos

O sistema não deve permitir a exclusão de uma categoria que possua gastos associados a ela, evitando inconsistência nos dados.

Exemplo:

```text
Categoria "Alimentação" possui gastos cadastrados → exclusão rejeitada

Categoria "Lazer" sem nenhum gasto cadastrado     → exclusão permitida
```

---

## Regra 10 — Identificação de gastos acima do padrão

O sistema deverá calcular a média dos gastos e identificar valores significativamente acima desse padrão.

Uma regra simples pode ser:

```text
gasto > média × 2
```

Exemplo:

```text
Gastos:

R$ 30
R$ 40
R$ 50
R$ 35
R$ 500
```

O sistema calcula a média e pode identificar o gasto de R$ 500 como um gasto acima do padrão.

Essa funcionalidade será utilizada como a principal demonstração de **análise de dados**.

---

# 5. CRUD da API

Todas as entidades deverão possuir operações de:

- POST;
- GET;
- PUT;
- DELETE.

## 5.1 Usuários

```http
POST   /usuarios
GET    /usuarios
GET    /usuarios/{id}
PUT    /usuarios/{id}
DELETE /usuarios/{id}
```

---

## 5.2 Categorias

```http
POST   /categorias
GET    /categorias
GET    /categorias/{id}
PUT    /categorias/{id}
DELETE /categorias/{id}
```

---

## 5.3 Gastos

```http
POST   /gastos
GET    /gastos
GET    /gastos/{id}
PUT    /gastos/{id}
DELETE /gastos/{id}
```

---

# 6. Endpoints de análise

Além dos CRUDs, a API terá endpoints específicos para processamento e análise dos dados.

## 6.1 Total de gastos

```http
GET /analises/gastos/total
```

Exemplo de resposta:

```json
{
    "total": 2450.50
}
```

---

## 6.2 Gastos por categoria

```http
GET /analises/gastos/por-categoria
```

Exemplo:

```json
[
    {
        "categoria": "Alimentação",
        "total": 850.00
    },
    {
        "categoria": "Transporte",
        "total": 400.00
    },
    {
        "categoria": "Lazer",
        "total": 300.00
    }
]
```

Essa funcionalidade realiza agregação e análise dos dados.

---

## 6.3 Média dos gastos

```http
GET /analises/gastos/media
```

Exemplo:

```json
{
    "media": 82.50
}
```

---

## 6.4 Gastos acima do padrão

```http
GET /analises/gastos/anomalias
```

Exemplo:

```json
[
    {
        "descricao": "Compra de TV",
        "valor": 2500.00,
        "media": 350.00
    }
]
```

Essa funcionalidade será apresentada como uma forma simples de identificação de valores fora do comportamento habitual.

---

# 7. Arquitetura da API

A API deverá seguir uma arquitetura organizada em camadas, conforme solicitado no trabalho.

```text
projeto_api/
│
├── entities/
│   ├── usuario.py
│   ├── categoria.py
│   └── gasto.py
│
├── controllers/
│   ├── usuario_controller.py
│   ├── categoria_controller.py
│   └── gasto_controller.py
│
├── services/
│   ├── usuario_service.py
│   ├── categoria_service.py
│   ├── gasto_service.py
│   └── analise_service.py
│
├── repositories/
│   ├── usuario_repository.py
│   ├── categoria_repository.py
│   └── gasto_repository.py
│
├── routes/
│   ├── usuario_routes.py
│   ├── categoria_routes.py
│   ├── gasto_routes.py
│   └── analise_routes.py
│
├── config/
│   └── database.py
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── init.sql
```

## Fluxo da aplicação

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

Responsabilidades:

### Controllers

Recebem as requisições HTTP e retornam as respostas.

### Services

Contêm as regras de negócio e as análises.

### Repositories

Responsáveis pelo acesso aos dados.

### Entities

Representam as entidades do banco através do SQLAlchemy.

### Routes

Definem os endpoints da API.

### Config

Contém as configurações do banco e da aplicação.

---

# 8. SQLAlchemy

Cada tabela deverá possuir uma classe de modelo utilizando SQLAlchemy.

Classes:

```text
Usuario
Categoria
Gasto
```

Relacionamentos esperados:

```text
Usuario.gastos

Categoria.gastos

Gasto.usuario

Gasto.categoria
```

O objetivo é representar corretamente as entidades e seus relacionamentos.

---

# 9. Orientação a objetos

A API deverá utilizar efetivamente conceitos de Orientação a Objetos.

Os principais conceitos utilizados serão:

- classes;
- construtores;
- encapsulamento;
- herança, quando fizer sentido;
- polimorfismo, quando fizer sentido;
- métodos das classes;
- relacionamento entre objetos.

Exemplos de classes:

```text
Usuario
Categoria
Gasto

UsuarioService
CategoriaService
GastoService
AnaliseService

UsuarioRepository
CategoriaRepository
GastoRepository
```

---

# 10. Programação estruturada

Também deverão ser utilizados conceitos de programação estruturada, como:

- estruturas de condição;
- estruturas de repetição;
- listas;
- dicionários.

Exemplos de aplicação:

```python
if valor <= 0:
    ...
```

```python
for gasto in gastos:
    ...
```

```python
gastos_por_categoria = {}
```

---

# 11. Interface gráfica

A interface gráfica será desenvolvida separadamente da API utilizando **Tkinter**.

A interface ficará fora dos containers Docker.

## 11.1 Tela principal

```text
+--------------------------------------+
|       ANÁLISE DE GASTOS PESSOAIS     |
+--------------------------------------+
|                                      |
| [ Usuários ]                         |
| [ Categorias ]                       |
| [ Gastos ]                            |
| [ Análises ]                         |
|                                      |
+--------------------------------------+
```

---

## 11.2 Tela de usuários

Campos:

```text
Nome:  [________________]
Email: [________________]

[ Cadastrar ]
```

Lista:

```text
ID | Nome | Email
```

Operações:

```text
[Editar] [Excluir]
```

---

## 11.3 Tela de categorias

Campos:

```text
Nome: [________________]

[ Cadastrar ]
```

Lista:

```text
ID | Categoria
```

Operações:

```text
[Editar] [Excluir]
```

---

## 11.4 Tela de gastos

Campos:

```text
Descrição: [_____________]

Valor:     [_____________]

Data:      [_____________]

Usuário:   [ João       ▼ ]

Categoria: [ Alimentação ▼ ]

[ Cadastrar ]
```

Lista:

```text
ID | Descrição | Valor | Data | Categoria
```

Operações:

```text
[Editar] [Excluir]
```

---

## 11.5 Tela de análise

A tela poderá apresentar:

```text
+--------------------------------------+
|           ANÁLISE DE GASTOS          |
+--------------------------------------+

Total gasto:
R$ 2.450,50

Média por gasto:
R$ 82,50

Categoria com maior gasto:
Alimentação

--------------------------------------

Gastos por categoria:

Alimentação     R$ 850,00
Transporte      R$ 400,00
Lazer           R$ 300,00
Moradia         R$ 900,00

--------------------------------------

Gastos acima do padrão:

Compra TV       R$ 2.500,00
```

Gráficos não são obrigatórios para o escopo básico.

---

# 12. Comunicação entre interface e API

A interface Tkinter deverá realizar requisições HTTP para a API FastAPI.

Fluxo:

```text
Tkinter
   │
   │ HTTP
   ▼
FastAPI
   │
   │ SQLAlchemy
   ▼
PostgreSQL
```

Exemplo de cadastro:

```text
Usuário preenche formulário
        ↓
Tkinter envia POST
        ↓
FastAPI recebe requisição
        ↓
Controller
        ↓
Service
        ↓
Repository
        ↓
PostgreSQL
        ↓
Resposta para Tkinter
```

---

# 13. Tratamento de erros

A interface deve apresentar mensagens compreensíveis para situações de erro.

Casos mínimos:

## Valor inválido

```text
Valor: -50

Mensagem:
"O valor do gasto deve ser maior que zero."
```

## Registro inexistente

```text
Usuário: 999

Mensagem:
"Usuário não encontrado."
```

## Categoria inexistente

```text
Categoria: 999

Mensagem:
"A categoria informada não existe."
```

## Erro de comunicação

Caso a API esteja indisponível:

```text
"Não foi possível conectar à API."
```

## Campos obrigatórios

```text
Nome: [             ]

Mensagem:
"O campo nome é obrigatório."
```

## E-mail inválido

```text
Email: mariaemail.com

Mensagem:
"O e-mail informado não é válido."
```

## Exclusão bloqueada

```text
Categoria: Alimentação (possui gastos vinculados)

Mensagem:
"Não é possível excluir uma categoria que possui gastos cadastrados."
```

---

# 14. Docker

O projeto deverá possuir dois containers principais:

```text
docker-compose
│
├── api
│   └── FastAPI
│
└── database
    └── PostgreSQL
```

A interface Tkinter será executada fora do Docker.

## 14.1 API

O `Dockerfile` deverá:

- utilizar uma imagem base adequada;
- instalar as dependências;
- copiar o código;
- configurar o ambiente;
- iniciar a API.

---

## 14.2 Banco

O PostgreSQL deverá possuir seu próprio container.

O projeto deverá fornecer o script:

```text
init.sql
```

Esse script será utilizado para inicialização do banco, quando necessário.

---

## 14.3 Docker Compose

O arquivo:

```text
docker-compose.yml
```

será responsável por configurar e executar:

```text
API
PostgreSQL
```

---

# 15. Ordem de desenvolvimento

## Etapa 1 — Criar o banco

Criar as tabelas:

```text
usuarios
categorias
gastos
```

Definir as chaves primárias e estrangeiras.

---

## Etapa 2 — Criar os modelos SQLAlchemy

Criar:

```text
Usuario
Categoria
Gasto
```

Implementar os relacionamentos.

---

## Etapa 3 — Criar os repositories

Implementar operações básicas:

```text
create
get
get_all
update
delete
```

---

## Etapa 4 — Criar os services

Implementar:

- CRUD;
- validação de campos obrigatórios (nome, descrição);
- validação de valor;
- validação de e-mail (unicidade e formato);
- validação de categoria e usuário (existência);
- validação de nome de categoria único;
- validação de exclusão de categoria vinculada a gastos;
- demais regras de negócio (10 regras, ver Seção 4).

---

## Etapa 5 — Criar a API

Implementar todos os endpoints:

```text
POST
GET
PUT
DELETE
```

para:

```text
usuarios
categorias
gastos
```

---

## Etapa 6 — Implementar as análises

Criar:

```text
GET /analises/gastos/total

GET /analises/gastos/media

GET /analises/gastos/por-categoria

GET /analises/gastos/anomalias
```

---

## Etapa 7 — Criar a interface Tkinter

Criar as telas:

```text
Usuários
Categorias
Gastos
Análises
```

---

## Etapa 8 — Integrar Tkinter com FastAPI

A interface deverá consumir os endpoints HTTP.

---

## Etapa 9 — Implementar tratamento de erros

Testar:

- valores inválidos;
- registros inexistentes (usuário/categoria);
- categorias inexistentes;
- e-mails com formato inválido;
- e-mails duplicados;
- nomes de categoria duplicados;
- campos obrigatórios (nome, descrição);
- exclusão de categoria vinculada a gastos;
- API indisponível.

---

## Etapa 10 — Dockerizar

Criar:

```text
Dockerfile
docker-compose.yml
init.sql
```

Testar a execução em ambiente limpo.

---

## Etapa 11 — Preparar a apresentação

Preparar slides e demonstração prática.

---

# 16. Roteiro da demonstração

Durante a apresentação, demonstrar:

### 1. Cadastro

Cadastrar:

- um usuário;
- uma categoria;
- alguns gastos.

### 2. Consulta

Mostrar os registros cadastrados.

### 3. Edição

Alterar um gasto.

### 4. Exclusão

Excluir um registro.

### 5. Regras de negócio (validações de campo)

Demonstrar, por exemplo:

```text
valor = -50            → rejeitado
nome do usuário = ""   → rejeitado
```

### 6. Regras de negócio (unicidade)

Tentar cadastrar um usuário com e-mail já existente e/ou uma categoria com nome já existente.

### 7. Regras de negócio (integridade referencial)

Tentar cadastrar gasto com categoria/usuário inexistente e tentar excluir uma categoria vinculada a gastos.

### 8. Análise

Mostrar:

- total de gastos;
- média;
- gastos por categoria;
- gastos acima do padrão.

### 9. Comunicação

Demonstrar que a interface Tkinter está consumindo a API.

### 10. Persistência

Mostrar os dados persistidos no PostgreSQL.

---

# 17. Estrutura final do projeto

```text
analise-gastos/
│
├── api/
│   ├── entities/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── routes/
│   ├── config/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── init.sql
│
├── interface/
│   ├── telas/
│   ├── services/
│   ├── api_client.py
│   └── main.py
│
├── docker-compose.yml
│
└── README.md
```

---

# 18. Checklist dos requisitos

## Parte 2 — Dados e modelos

- [ ] 3 tabelas
- [ ] Relacionamentos coerentes
- [ ] PostgreSQL
- [ ] SQLAlchemy
- [ ] Classe para cada tabela
- [ ] Relacionamentos implementados

## Parte 3 — API

- [ ] FastAPI
- [ ] POST para todas as entidades
- [ ] GET para todas as entidades
- [ ] PUT para todas as entidades
- [ ] DELETE para todas as entidades
- [ ] Controllers
- [ ] Services
- [ ] Repositories
- [ ] Routes
- [ ] Entities
- [ ] Config
- [ ] 10 regras de negócio
- [ ] Orientação a objetos
- [ ] Programação estruturada

## Parte 4 — Interface

- [ ] Tkinter
- [ ] Cadastro de usuário
- [ ] Edição de usuário
- [ ] Consulta de usuário
- [ ] Exclusão de usuário
- [ ] Cadastro de categoria
- [ ] Edição de categoria
- [ ] Consulta de categoria
- [ ] Exclusão de categoria
- [ ] Cadastro de gasto
- [ ] Edição de gasto
- [ ] Consulta de gasto
- [ ] Exclusão de gasto
- [ ] Tela de análise
- [ ] Tratamento de erros
- [ ] Comunicação com a API

## Parte 5 — Docker

- [ ] Dockerfile da API
- [ ] Container da API
- [ ] Container PostgreSQL
- [ ] docker-compose.yml
- [ ] init.sql
- [ ] API funcionando via Docker
- [ ] Banco funcionando via Docker

## Parte 6 — Apresentação

- [ ] Contexto
- [ ] Problema
- [ ] Requisitos
- [ ] Modelo do banco
- [ ] Arquitetura
- [ ] Principais classes
- [ ] Endpoints
- [ ] Interface
- [ ] Demonstração
- [ ] Dificuldades

## Demonstração obrigatória

- [ ] Cadastro
- [ ] Consulta
- [ ] Edição
- [ ] Exclusão
- [ ] Amostra das 10 regras de negócio
- [ ] Comunicação interface/API
- [ ] Persistência no banco
- [ ] 2 casos de erro/validação

---

# 19. Escopo final resumido

```text
ANÁLISE DE GASTOS PESSOAIS

Banco:
├── Usuario
├── Categoria
└── Gasto

CRUD:
├── Usuario
├── Categoria
└── Gasto

Regras de negócio (10):
├── Valor do gasto positivo
├── E-mail único
├── Categoria deve existir
├── Nome do usuário obrigatório
├── E-mail com formato válido
├── Nome da categoria único
├── Descrição do gasto obrigatória
├── Usuário deve existir
├── Categoria vinculada não pode ser excluída
└── Identificação de gastos acima do padrão

Análises:
├── Total de gastos
├── Média dos gastos
├── Gastos por categoria
└── Gastos acima do padrão

Tecnologias:
├── Python
├── FastAPI
├── SQLAlchemy
├── PostgreSQL
├── Tkinter
├── Docker
└── Docker Compose
```

O objetivo é manter o projeto pequeno o suficiente para que todos os integrantes consigam compreender e explicar o código durante a apresentação, enquanto as funcionalidades de análise garantem que o sistema não seja apenas um CRUD.
