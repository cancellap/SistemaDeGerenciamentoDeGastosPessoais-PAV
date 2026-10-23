# Contexto do projeto: Análise de Gastos Pessoais

Projeto acadêmico. **Simplicidade é requisito**: toda a equipe precisa conseguir explicar o código na apresentação. Não adicione funcionalidades, bibliotecas ou camadas além do que o roadmap pede. Sem Machine Learning.

O roadmap completo está em `ROADMAP.md`. Em caso de dúvida, ele é a fonte da verdade.

## Stack
Python, FastAPI, SQLAlchemy, PostgreSQL, Tkinter (fora do Docker), Docker e Docker Compose (API + banco).

## Modelo de dados (3 tabelas)
- `usuarios` (id, nome, email)
- `categorias` (id, nome)
- `gastos` (id, descricao, valor DECIMAL, data DATE, usuario_id FK, categoria_id FK)
- Usuario 1:N Gasto; Categoria 1:N Gasto.

## Regras de negócio
1. `valor > 0`.
2. E-mail de usuário único.
3. `categoria_id` precisa existir ao cadastrar/editar gasto.
4. Gasto acima do padrão: `valor > média × 2`.

## Arquitetura da API (camadas)
`Routes → Controller → Service → Repository → SQLAlchemy → PostgreSQL`

- `entities/`: modelos SQLAlchemy
- `repositories/`: acesso a dados (create, get, get_all, update, delete)
- `services/`: regras de negócio e análises
- `controllers/`: recebem a requisição e devolvem a resposta
- `routes/`: definem os endpoints
- `config/`: banco e configurações

Regra de ouro: controller nunca acessa repository; service nunca conhece HTTP; repository não contém regra de negócio.

## Endpoints
CRUD (POST, GET lista, GET por id, PUT, DELETE) para `/usuarios`, `/categorias`, `/gastos`.
Análises: `GET /analises/gastos/total`, `/media`, `/por-categoria`, `/anomalias`.

## Convenções
- Código e nomes de domínio em português (`UsuarioService`, `valor`, `descricao`); termos técnicos consagrados em inglês.
- Use conceitos de POO (classes, construtores, encapsulamento) e estruturados (if, for, listas, dicionários) de forma visível e didática.
- Erros de negócio retornam mensagens em português claras, com status HTTP adequado (404 não encontrado, 409 e-mail duplicado, 422/400 validação).
- Comentários curtos e úteis; nada de código "esperto" difícil de explicar.
- Responda sempre em português do Brasil.
