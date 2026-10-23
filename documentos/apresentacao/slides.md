# Slides — Análise de Gastos Pessoais

## Slide 1 — Contexto

- Projeto acadêmico de uma API para análise de gastos pessoais.
- Stack implementada: Python, FastAPI, SQLAlchemy e PostgreSQL.
- A API possui CRUD e endpoints de análise.

## Slide 2 — Problema

- Registros de gastos podem ficar dispersos e difíceis de comparar.
- O sistema centraliza usuários, categorias e gastos.
- As análises mostram total, média, categorias e valores acima do padrão.

## Slide 3 — Requisitos e escopo

- CRUD de usuários, categorias e gastos.
- Regras: valor positivo, e-mail único e categoria existente.
- Anomalia: gasto maior que duas vezes a média.
- Sem Machine Learning e sem novas tabelas.

## Slide 4 — Modelo do banco

- `usuarios (1) ---- (N) gastos (N) ---- (1) categorias`.
- `gastos.usuario_id` referencia `usuarios.id`.
- `gastos.categoria_id` referencia `categorias.id`.
- As tabelas estão em `api/init.sql` e nos modelos SQLAlchemy.

## Slide 5 — Arquitetura

- API: Routes -> Controller -> Service -> Repository -> SQLAlchemy -> PostgreSQL.
- A interface Tkinter e o fluxo Tkinter -> HTTP -> FastAPI são responsabilidade da colega.
- A API está organizada por camadas e routers.

## Slide 6 — Principais classes

- `Usuario`: representa o usuário e seus gastos.
- `Gasto`: representa valor, data, usuário e categoria.
- `GastoService`: valida e executa o CRUD de gastos.
- `AnaliseService`: calcula total, média, categorias e anomalias.
- `GastoRepository`: acessa os registros com SQLAlchemy.

## Slide 7 — Endpoints

- CRUD: `/usuarios`, `/categorias` e `/gastos`.
- Análises: `/analises/gastos/total` e `/media`.
- Análises: `/por-categoria` e `/anomalias`.
- A documentação interativa fica em `/docs`.

## Slide 8 — Interface

- A interface Tkinter não está presente neste repositório no momento.
- Inserir aqui os prints das telas produzidas pela colega.
- A API pode ser demonstrada pelo Swagger enquanto a interface não estiver integrada.

## Slide 9 — Demonstração

- Cadastro, consulta, edição e exclusão pelo Swagger ou pela interface integrada.
- Rejeição de valor inválido, e-mail duplicado e categoria inexistente.
- Análises com dados de exemplo e consulta da persistência.

## Slide 10 — Dificuldades

- A confirmação das dificuldades da equipe está pendente.
- Ponto técnico já identificado: o Docker Desktop precisa estar ativo para validar os containers.
- A configuração usa healthcheck para aguardar o PostgreSQL antes da API.

## Slide 11 — Conclusão e próximos passos

- A API, o CRUD, as análises e a configuração Docker estão implementados.
- Validar a execução completa do Docker Desktop e a persistência real.
- Integrar e testar a interface Tkinter.
- Substituir os nomes provisórios da divisão de falas pelos integrantes reais.

## Divisão provisória de falas

- Integrante A: contexto, problema, requisitos e banco.
- Integrante B: arquitetura, entities, repositories e services.
- Integrante C: endpoints, regras e análises.
- Integrante D: interface, Docker e demonstração.
- Ajustar os papéis conforme o número real de integrantes.
