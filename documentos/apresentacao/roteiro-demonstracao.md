# Roteiro da demonstração

## Duração sugerida: 8 minutos

Os nomes dos apresentadores são provisórios. Substituir `Integrante A/B/C/D` pelos nomes do grupo.

## Preparação

1. Com Docker Desktop ativo, executar `docker compose up --build`.
2. Abrir `http://localhost:8000/docs`.
3. Se o Docker não estiver disponível, usar a API local e o Swagger com o banco já populado.
4. Se a interface Tkinter da colega estiver pronta, iniciar a interface fora do Docker.

## Dados prontos

- Usuário: `João`, e-mail `joao@email.com`.
- Categorias: `Alimentação` e `Lazer`.
- Gastos: `30`, `40`, `50`, `35` e `500`.
- Resultado esperado: total `655`, média `131` e anomalia de `500`.

## 1. Cadastro — 1 minuto

**Integrante A** cadastra o usuário e as duas categorias.

**Integrante B** cadastra os cinco gastos usando `POST /gastos` ou a interface Tkinter integrada.

## 2. Consulta — 40 segundos

Mostrar `GET /usuarios`, `GET /categorias` e `GET /gastos`.

Explicar que as respostas vêm das camadas Route, Controller, Service e Repository.

## 3. Edição — 40 segundos

Alterar a descrição do gasto de `35` para `Lanche` usando `PUT /gastos/{id}`.

Consultar novamente o gasto para confirmar a alteração.

## 4. Exclusão — 30 segundos

Excluir o gasto editado com `DELETE /gastos/{id}`.

Consultar a lista para confirmar que o registro não aparece mais.

## 5. Regras rejeitadas — 1 minuto e 30 segundos

1. Enviar gasto com `valor = -50`: esperar `422` e mensagem de valor maior que zero.
2. Cadastrar outro usuário com `joao@email.com`: esperar `409` por e-mail duplicado.
3. Enviar gasto com `categoria_id = 999`: esperar `404` por categoria inexistente.

## 6. Análises — 1 minuto e 30 segundos

- `GET /analises/gastos/total` retorna `655.0`.
- `GET /analises/gastos/media` retorna `131.0`.
- `GET /analises/gastos/por-categoria` agrupa os valores por categoria.
- `GET /analises/gastos/anomalias` identifica o gasto de `500`.

## 7. Interface e persistência — 1 minuto

Se a interface da colega estiver pronta, repetir uma consulta mostrando o Tkinter consumindo a API por HTTP.

Executar `docker compose restart` e consultar novamente para demonstrar a persistência no PostgreSQL.

## Plano B

- Se o Tkinter falhar: demonstrar todos os fluxos pelo Swagger em `/docs`.
- Se a API falhar: usar a API local ou o banco já populado para apresentar as respostas esperadas.
- Se o Docker falhar: explicar a configuração e usar os testes locais; não afirmar que a persistência Docker foi validada.
- Se um dado estiver ausente: usar o conjunto de dados preparado antes da apresentação.

## Divisão de falas

- Integrante A: preparação, cadastro e regras de negócio.
- Integrante B: consulta, edição, exclusão e fluxo das camadas.
- Integrante C: endpoints de análise e interpretação dos resultados.
- Integrante D: interface, Docker, persistência e plano B.
- Cada integrante deve revisar o código da parte que apresentará.
