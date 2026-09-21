# Roadmap — Sistema de Monitoramento de Infraestrutura de Servidores

## 1. Visão geral

O projeto será um **Sistema de Monitoramento de Infraestrutura de Servidores**, com o objetivo de cadastrar servidores, registrar métricas de utilização e analisar o desempenho da infraestrutura.

### Stack definida

| Componente | Tecnologia |
|---|---|
| Linguagem | Python |
| Banco de dados | MySQL |
| ORM | SQLAlchemy |
| API REST | FastAPI |
| Interface gráfica | Tkinter |
| Comunicação | HTTP/JSON |
| Containerização | Docker + Docker Compose |

### Fluxo geral

```text
PARTE 1
Requisitos e regras de negócio
        ↓
PARTE 2
Banco + SQLAlchemy + modelos
        ↓
PARTE 3
API REST + arquitetura em camadas
        ↓
PARTE 4
Interface gráfica + comunicação com API
        ↓
PARTE 5
Docker + Docker Compose
        ↓
PARTE 6
Testes + apresentação
```

---

# 2. PARTE 1 — Requisitos

## 2.1 Entidades

Para manter o projeto dentro do limite de 3 a 5 tabelas, serão utilizadas **4 entidades**:

- `usuarios`
- `servidores`
- `metricas`
- `alertas`

### Relacionamentos

```text
USUARIO

SERVIDOR
   │
   ├──────< METRICA
   │
   └──────< ALERTA
```

- Um servidor possui várias métricas.
- Um servidor possui vários alertas.
- Uma métrica pode estar relacionada a alertas.

---

## 2.2 Requisitos funcionais

### RF01 — Gerenciar usuários

O sistema deverá permitir:

- cadastrar usuários;
- consultar usuários;
- editar usuários;
- excluir usuários.

### RF02 — Gerenciar servidores

O sistema deverá permitir:

- cadastrar servidores;
- consultar servidores;
- editar servidores;
- excluir servidores.

### RF03 — Gerenciar métricas

O sistema deverá permitir:

- cadastrar métricas;
- consultar métricas;
- editar métricas;
- excluir métricas.

### RF04 — Gerenciar alertas

O sistema deverá permitir:

- cadastrar alertas;
- consultar alertas;
- editar alertas;
- excluir alertas.

### RF05 — Classificar métricas

O sistema deverá classificar as métricas como:

- NORMAL
- ATENÇÃO
- CRÍTICO

### RF06 — Gerar indicadores

O sistema deverá apresentar:

- média de CPU;
- média de memória;
- média de disco;
- quantidade de alertas;
- quantidade de ocorrências críticas.

---

# 3. Regras de negócio

## RN01 — Hostname único

O sistema não deverá permitir dois servidores com o mesmo hostname.

## RN02 — IP único

O sistema não deverá permitir dois servidores utilizando o mesmo endereço IP.

## RN03 — Valores não negativos

O sistema não deverá permitir métricas com valores negativos.

## RN04 — Limite das métricas

CPU, memória e disco deverão possuir valores entre **0 e 100%**.

## RN05 — Classificação automática

O sistema deverá classificar automaticamente cada métrica:

```text
0 ≤ valor < 70  → NORMAL
70 ≤ valor < 90 → ATENÇÃO
90 ≤ valor ≤ 100 → CRÍTICO
```

## RN06 — Situação crítica

Uma utilização igual ou superior a 90% deverá ser considerada crítica.

## RN07 — Média por servidor

O sistema deverá permitir calcular médias dos recursos por servidor.

## RN08 — Identificação de valores críticos

O sistema deverá identificar valores críticos registrados.

## RN09 — Geração de alertas

O sistema deverá gerar um alerta quando uma métrica atingir situação crítica.

## RN10 — Indicadores

O sistema deverá apresentar indicadores de desempenho dos servidores.

---

# 4. PARTE 2 — Banco de dados

## 4.1 Banco

SGBD escolhido:

**MySQL**

Banco:

```text
monitoramento_servidores
```

Tabelas:

```text
usuarios
servidores
metricas
alertas
```

---

## 4.2 Tabela `usuarios`

| Campo | Tipo | Descrição |
|---|---|---|
| `id_usuario` | INT PK | Identificador do usuário |
| `nome` | VARCHAR | Nome |
| `email` | VARCHAR | E-mail |
| `senha` | VARCHAR | Senha |
| `perfil` | VARCHAR | Administrador ou operador |

---

## 4.3 Tabela `servidores`

| Campo | Tipo | Descrição |
|---|---|---|
| `id_servidor` | INT PK | Identificador |
| `hostname` | VARCHAR | Nome do servidor |
| `ip` | VARCHAR | Endereço IP |
| `sistema_operacional` | VARCHAR | Sistema operacional |
| `ambiente` | VARCHAR | Produção, homologação ou desenvolvimento |
| `status` | VARCHAR | Ativo ou inativo |
| `data_cadastro` | DATE | Data de cadastro |

---

## 4.4 Tabela `metricas`

| Campo | Tipo | Descrição |
|---|---|---|
| `id_metrica` | INT PK | Identificador |
| `id_servidor` | INT FK | Servidor monitorado |
| `data_hora` | DATETIME | Data e hora da medição |
| `cpu_percentual` | DECIMAL | Utilização da CPU |
| `memoria_percentual` | DECIMAL | Utilização da memória |
| `disco_percentual` | DECIMAL | Utilização do disco |
| `rede_mbps` | DECIMAL | Tráfego de rede |
| `classificacao` | VARCHAR | Normal, Atenção ou Crítico |

---

## 4.5 Tabela `alertas`

| Campo | Tipo | Descrição |
|---|---|---|
| `id_alerta` | INT PK | Identificador |
| `id_servidor` | INT FK | Servidor relacionado |
| `id_metrica` | INT FK | Métrica relacionada |
| `tipo_alerta` | VARCHAR | CPU, memória, disco etc. |
| `descricao` | VARCHAR | Descrição do problema |
| `nivel` | VARCHAR | Atenção ou Crítico |
| `data_hora` | DATETIME | Data e hora |
| `resolvido` | BOOLEAN | Indica se foi resolvido |

---

# 5. Relacionamentos

### Servidores → Métricas

```text
1 SERVIDOR ───────── N MÉTRICAS
```

### Servidores → Alertas

```text
1 SERVIDOR ───────── N ALERTAS
```

### Métricas → Alertas

```text
1 MÉTRICA ───────── N ALERTAS
```

---

# 6. Modelo simplificado

```text
┌─────────────────────┐
│     USUARIOS        │
├─────────────────────┤
│ PK id_usuario       │
│    nome             │
│    email            │
│    senha            │
│    perfil           │
└─────────────────────┘


┌─────────────────────┐
│     SERVIDORES      │
├─────────────────────┤
│ PK id_servidor      │
│    hostname         │
│    ip               │
│    sistema_operacional│
│    ambiente         │
│    status            │
│    data_cadastro    │
└──────────┬──────────┘
           │
           │ 1:N
           ▼
┌─────────────────────┐
│      METRICAS       │
├─────────────────────┤
│ PK id_metrica       │
│ FK id_servidor      │
│    data_hora        │
│    cpu_percentual   │
│    memoria_percentual│
│    disco_percentual │
│    rede_mbps        │
│    classificacao    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       ALERTAS       │
├─────────────────────┤
│ PK id_alerta        │
│ FK id_servidor      │
│ FK id_metrica       │
│    tipo_alerta      │
│    descricao        │
│    nivel            │
│    data_hora        │
│    resolvido        │
└─────────────────────┘
```

---

# 7. SQLAlchemy

Cada tabela deverá possuir uma classe de modelo.

Estrutura:

```text
entities/
├── usuario.py
├── servidor.py
├── metrica.py
└── alerta.py
```

As classes deverão representar:

- atributos;
- chaves primárias;
- chaves estrangeiras;
- relacionamentos;
- restrições relevantes.

Exemplo:

```python
class Servidor(Base):
    __tablename__ = "servidores"

    id_servidor = Column(Integer, primary_key=True)
    hostname = Column(String(100), nullable=False)
    ip = Column(String(45), nullable=False)
```

---

# 8. Configuração do banco

Estrutura:

```text
config/
├── database.py
└── settings.py
```

Fluxo:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
MySQL
```

---

# 9. Script SQL

Criar:

```text
database/
└── init.sql
```

O script deverá conter os comandos necessários para inicialização do banco e suas tabelas.

Esse arquivo será utilizado posteriormente pelo Docker.

---

# 10. PARTE 3 — API REST

Framework escolhido:

**FastAPI**

Estrutura:

```text
projeto_API/
│
├── entities/
├── controllers/
├── services/
├── repositories/
├── routes/
├── config/
├── app.py
└── requirements.txt
```

---

# 11. Responsabilidade das camadas

## `entities/`

Contém os modelos SQLAlchemy:

```text
Usuario
Servidor
Metrica
Alerta
```

## `repositories/`

Responsável pelo acesso ao banco.

Exemplo:

```text
ServidorRepository

    criar()
    buscar_todos()
    buscar_por_id()
    atualizar()
    excluir()
```

## `services/`

Responsável pelas regras de negócio:

- verificar hostname;
- verificar IP;
- validar métricas;
- classificar métricas;
- gerar alertas;
- calcular indicadores.

## `controllers/`

Responsável por receber a requisição e chamar os services.

Fluxo:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
Banco
```

## `routes/`

Responsável por definir as URLs da API.

---

# 12. Endpoints CRUD

Todas as entidades deverão possuir POST, GET, PUT e DELETE.

## Usuários

```text
POST   /usuarios
GET    /usuarios
GET    /usuarios/{id}
PUT    /usuarios/{id}
DELETE /usuarios/{id}
```

## Servidores

```text
POST   /servidores
GET    /servidores
GET    /servidores/{id}
PUT    /servidores/{id}
DELETE /servidores/{id}
```

## Métricas

```text
POST   /metricas
GET    /metricas
GET    /metricas/{id}
PUT    /metricas/{id}
DELETE /metricas/{id}
```

## Alertas

```text
POST   /alertas
GET    /alertas
GET    /alertas/{id}
PUT    /alertas/{id}
DELETE /alertas/{id}
```

Total: **20 operações CRUD básicas**.

---

# 13. Endpoints de análise

Além do CRUD, implementar endpoints para demonstrar o processamento de dados.

### Média de CPU

```text
GET /analises/media-cpu/{id_servidor}
```

### Média de memória

```text
GET /analises/media-memoria/{id_servidor}
```

### Servidores críticos

```text
GET /analises/servidores-criticos
```

### Dashboard

```text
GET /analises/dashboard
```

Exemplo de resposta:

```json
{
    "total_servidores": 10,
    "servidores_criticos": 2,
    "total_alertas": 15,
    "media_cpu": 63.5,
    "media_memoria": 58.2
}
```

---

# 14. Orientação a objetos

A API deverá utilizar efetivamente:

- classes;
- construtores;
- encapsulamento;
- herança;
- polimorfismo.

Sugestão de hierarquia:

```text
BaseRepository
      │
      ├── UsuarioRepository
      ├── ServidorRepository
      ├── MetricaRepository
      └── AlertaRepository
```

Principais classes:

```text
Usuario
Servidor
Metrica
Alerta

UsuarioService
ServidorService
MetricaService
AlertaService

UsuarioRepository
ServidorRepository
MetricaRepository
AlertaRepository
```

---

# 15. Programação estruturada

O projeto também deverá utilizar:

### Estruturas condicionais

```python
if cpu >= 90:
    classificacao = "CRITICO"
elif cpu >= 70:
    classificacao = "ATENCAO"
else:
    classificacao = "NORMAL"
```

### Repetições

```python
for metrica in metricas:
    ...
```

### Listas

```python
servidores = []
```

### Dicionários

```python
indicadores = {
    "total": 10,
    "criticos": 2
}
```

---

# 16. PARTE 4 — Interface gráfica

A interface será um projeto separado da API.

Tecnologia:

**Tkinter**

Estrutura sugerida:

```text
projeto_interface/
│
├── telas/
│   ├── login.py
│   ├── usuarios.py
│   ├── servidores.py
│   ├── metricas.py
│   ├── alertas.py
│   └── dashboard.py
│
├── services/
│   └── api_client.py
│
└── main.py
```

---

# 17. Telas necessárias

## Login

Campos:

- e-mail;
- senha.

Botão:

- Entrar.

## Usuários

Operações:

- cadastrar;
- consultar;
- editar;
- excluir.

## Servidores

Operações:

- cadastrar;
- consultar;
- editar;
- excluir.

## Métricas

Operações:

- cadastrar;
- consultar;
- editar;
- excluir.

## Alertas

Operações:

- cadastrar;
- consultar;
- editar;
- excluir.

## Dashboard

Exibir:

- total de servidores;
- total de alertas;
- servidores críticos;
- médias de utilização;
- gráficos/indicadores.

---

# 18. Comunicação da interface com a API

A interface não deverá acessar o banco diretamente.

Fluxo correto:

```text
Tkinter
   ↓ HTTP/JSON
FastAPI
   ↓
Services
   ↓
Repositories
   ↓
SQLAlchemy
   ↓
MySQL
```

Criar um cliente da API:

```text
services/
└── api_client.py
```

Esse módulo será responsável pelas requisições HTTP.

---

# 19. Tratamento de erros

A interface deverá tratar situações como:

## Erro 1 — IP duplicado

Mensagem:

> Já existe um servidor cadastrado com este endereço IP.

## Erro 2 — CPU inválida

Entrada:

```text
150
```

Mensagem:

> A utilização da CPU deve estar entre 0% e 100%.

## Erro 3 — Registro inexistente

Mensagem:

> Servidor não encontrado.

## Erro 4 — API indisponível

Mensagem:

> Não foi possível conectar ao servidor. Verifique se a API está em execução.

## Erro 5 — Campo obrigatório

Mensagem:

> Preencha todos os campos obrigatórios.

---

# 20. PARTE 5 — Docker

A aplicação deverá possuir:

- container da API;
- container do MySQL;
- interface executando fora dos containers.

Arquitetura:

```text
┌──────────────────┐
│     Tkinter      │
│   FORA DO DOCKER │
└────────┬─────────┘
         │ HTTP
         ▼
┌──────────────────┐
│   API FastAPI    │
│    CONTAINER     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│      MySQL       │
│    CONTAINER     │
└──────────────────┘
```

---

# 21. Estrutura do Docker

```text
projeto/
│
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
│
├── database/
│   └── init.sql
│
├── interface/
│   └── ...
│
└── docker-compose.yml
```

---

# 22. Dockerfile da API

O Dockerfile deverá:

1. utilizar uma imagem base Python adequada;
2. instalar as dependências;
3. copiar o código;
4. configurar o ambiente;
5. definir o comando de inicialização da API.

Fluxo:

```text
Imagem Python
     ↓
Instalar dependências
     ↓
Copiar projeto
     ↓
Configurar ambiente
     ↓
Iniciar Uvicorn/FastAPI
```

---

# 23. Docker Compose

O `docker-compose.yml` deverá configurar:

```text
api
mysql
```

Ao executar:

```bash
docker compose up
```

deverá ocorrer:

```text
MySQL inicia
     ↓
Banco é inicializado
     ↓
API inicia
     ↓
API conecta ao MySQL
```

---

# 24. PARTE 6 — Testes

## 24.1 Testes CRUD

### Usuários

- [ ] Cadastrar
- [ ] Consultar
- [ ] Editar
- [ ] Excluir

### Servidores

- [ ] Cadastrar
- [ ] Consultar
- [ ] Editar
- [ ] Excluir

### Métricas

- [ ] Cadastrar
- [ ] Consultar
- [ ] Editar
- [ ] Excluir

### Alertas

- [ ] Cadastrar
- [ ] Consultar
- [ ] Editar
- [ ] Excluir

---

# 25. Testes das regras de negócio

## Teste 1 — IP duplicado

```text
Cadastrar SRV-01
IP: 192.168.1.10

Cadastrar SRV-02
IP: 192.168.1.10

Resultado esperado:
ERRO — IP já cadastrado.
```

## Teste 2 — CPU inválida

```text
CPU = 150

Resultado esperado:
ERRO — CPU deve estar entre 0 e 100%.
```

## Teste 3 — Classificação crítica

```text
CPU = 95%

Resultado esperado:
Classificação = CRÍTICO
Alerta = GERADO
```

---

# 26. Teste de persistência

Realizar:

```text
Cadastrar servidor
       ↓
Fechar API
       ↓
Iniciar API novamente
       ↓
Consultar servidor
       ↓
Servidor continua existente
```

Também testar o funcionamento através do Docker.

---

# 27. PARTE 6 — Apresentação

A apresentação deverá conter os 10 pontos solicitados.

## Slide 1 — Contexto

Apresentar o problema de monitoramento da infraestrutura de servidores.

## Slide 2 — Problema

Explicar a necessidade de identificar servidores com alta utilização de recursos.

## Slide 3 — Requisitos principais

Apresentar:

- cadastro;
- métricas;
- classificação;
- alertas;
- indicadores.

## Slide 4 — Modelo do banco

Mostrar o DER.

## Slide 5 — Arquitetura

Mostrar:

```text
Tkinter
   ↓
FastAPI
   ↓
Controllers
   ↓
Services
   ↓
Repositories
   ↓
SQLAlchemy
   ↓
MySQL
```

## Slide 6 — Principais classes

Mostrar:

```text
Servidor
Metrica
Alerta
Usuario

Services
Repositories
Controllers
```

## Slide 7 — Endpoints

Exemplos:

```text
POST /servidores
GET /servidores
PUT /servidores/{id}
DELETE /servidores/{id}

POST /metricas
GET /metricas

GET /analises/dashboard
```

## Slide 8 — Interface

Mostrar screenshots de:

- Login;
- Servidores;
- Métricas;
- Alertas;
- Dashboard.

## Slide 9 — Demonstração

Demonstrar:

1. Cadastro;
2. Consulta;
3. Edição;
4. Exclusão;
5. Registro de métrica;
6. Classificação;
7. Geração de alerta;
8. Dashboard.

## Slide 10 — Dificuldades

Possíveis dificuldades:

- integração API ↔ banco;
- relacionamentos SQLAlchemy;
- regras de negócio;
- comunicação Tkinter ↔ API;
- Docker;
- tratamento de erros.

---

# 28. Roteiro da demonstração

A demonstração deve cobrir todos os requisitos obrigatórios.

### 1. Cadastro

Cadastrar um servidor.

### 2. Consulta

Mostrar o servidor cadastrado.

### 3. Edição

Alterar alguma informação do servidor.

### 4. Exclusão

Excluir um registro de teste.

### 5. Regra de negócio

Cadastrar uma métrica com:

```text
CPU = 95%
```

Demonstrar:

```text
CRÍTICO
↓
ALERTA GERADO
```

### 6. Segundo caso de regra

Tentar cadastrar um servidor com IP duplicado.

Mostrar:

```text
Operação proibida.
IP já cadastrado.
```

### 7. Caso de erro

Tentar registrar:

```text
CPU = 150%
```

Mostrar a mensagem de validação.

### 8. Persistência

Consultar os dados após reiniciar a API.

### 9. Comunicação

Mostrar que a operação realizada na interface foi enviada para a API e persistida no MySQL.

---

# 29. Ordem recomendada de desenvolvimento

## Etapa 1 — Planejamento

- [ ] Definir requisitos
- [ ] Definir regras de negócio
- [ ] Definir tabelas
- [ ] Fazer DER

## Etapa 2 — Banco

- [ ] Criar banco MySQL
- [ ] Criar tabelas
- [ ] Criar relacionamentos
- [ ] Criar `init.sql`
- [ ] Testar banco

## Etapa 3 — SQLAlchemy

- [ ] Criar `Usuario`
- [ ] Criar `Servidor`
- [ ] Criar `Metrica`
- [ ] Criar `Alerta`
- [ ] Configurar relacionamentos
- [ ] Testar conexão

## Etapa 4 — API

- [ ] Criar projeto FastAPI
- [ ] Configurar SQLAlchemy
- [ ] Criar repositories
- [ ] Criar services
- [ ] Criar controllers
- [ ] Criar routes

## Etapa 5 — CRUD

- [ ] CRUD Usuários
- [ ] CRUD Servidores
- [ ] CRUD Métricas
- [ ] CRUD Alertas

## Etapa 6 — Regras de negócio

- [ ] Validar hostname
- [ ] Validar IP
- [ ] Validar métricas
- [ ] Classificar métricas
- [ ] Gerar alertas
- [ ] Calcular médias
- [ ] Criar indicadores

## Etapa 7 — Interface

- [ ] Login
- [ ] Tela de usuários
- [ ] Tela de servidores
- [ ] Tela de métricas
- [ ] Tela de alertas
- [ ] Dashboard
- [ ] Criar `api_client.py`

## Etapa 8 — Tratamento de erros

- [ ] Dados inválidos
- [ ] Registro inexistente
- [ ] Operação proibida
- [ ] Campos obrigatórios
- [ ] API indisponível

## Etapa 9 — Docker

- [ ] Criar Dockerfile
- [ ] Criar docker-compose.yml
- [ ] Configurar MySQL
- [ ] Configurar API
- [ ] Configurar `init.sql`
- [ ] Testar containers

## Etapa 10 — Testes finais

- [ ] Testar CRUD
- [ ] Testar regras
- [ ] Testar erros
- [ ] Testar persistência
- [ ] Testar interface
- [ ] Testar API
- [ ] Testar Docker

## Etapa 11 — Apresentação

- [ ] Criar slides
- [ ] Inserir DER
- [ ] Inserir arquitetura
- [ ] Inserir classes
- [ ] Inserir endpoints
- [ ] Inserir screenshots
- [ ] Preparar demonstração
- [ ] Dividir apresentação entre integrantes
- [ ] Ensaiar

---

# 30. Checklist final de entrega

## Banco

- [ ] 3–5 tabelas
- [ ] Relacionamentos coerentes
- [ ] MySQL
- [ ] SQLAlchemy
- [ ] Classe para cada tabela

## API

- [ ] FastAPI
- [ ] POST
- [ ] GET
- [ ] PUT
- [ ] DELETE
- [ ] Controllers
- [ ] Services
- [ ] Repositories
- [ ] Routes
- [ ] Orientação a objetos
- [ ] Programação estruturada
- [ ] 10 regras implementadas

## Interface

- [ ] Tkinter
- [ ] Cadastro
- [ ] Consulta
- [ ] Edição
- [ ] Exclusão
- [ ] Comunicação com API
- [ ] Tratamento de erros

## Docker

- [ ] Dockerfile
- [ ] Container da API
- [ ] Container do MySQL
- [ ] `docker-compose.yml`
- [ ] `init.sql`
- [ ] API inicia pelo container

## Apresentação

- [ ] Contexto
- [ ] Problema
- [ ] Requisitos
- [ ] Banco
- [ ] Arquitetura
- [ ] Classes
- [ ] Endpoints
- [ ] Interface
- [ ] Demonstração
- [ ] Dificuldades
- [ ] 3 regras demonstradas
- [ ] 2 casos de erro demonstrados
- [ ] Persistência demonstrada

---

# 31. Prioridade de desenvolvimento

A ordem mais segura é:

```text
BANCO
  ↓
SQLALCHEMY
  ↓
CRUD DA API
  ↓
REGRAS DE NEGÓCIO
  ↓
ANÁLISES
  ↓
INTERFACE
  ↓
TRATAMENTO DE ERROS
  ↓
DOCKER
  ↓
TESTES
  ↓
APRESENTAÇÃO
```

## Regra importante

Não começar pela interface ou pelo Docker.

Primeiro fazer o **banco + API funcionar completamente**. Depois conectar a interface. Por último, dockerizar o projeto.

Isso reduz a chance de haver várias partes parcialmente prontas e nenhuma funcionando de ponta a ponta.
