# Perguntas prováveis da banca

## Por que usar três tabelas?

Para separar usuários, categorias e gastos e representar os relacionamentos `1:N` sem duplicar dados.

## Por que o valor do gasto usa `Decimal`?

Valores monetários precisam evitar imprecisões comuns de ponto flutuante.

## Onde ficam as regras de negócio?

Nos services. O controller traduz erros para HTTP e o repository acessa o banco.

## Como o sistema impede valor inválido?

O service rejeita valores menores ou iguais a zero, e o banco também possui `CHECK (valor > 0)`.

## Como o e-mail duplicado é tratado?

O service consulta o repository antes do cadastro ou alteração, e a coluna também é `UNIQUE` no banco.

## Como a categoria é validada?

O `GastoService` consulta o `CategoriaRepository` antes de criar ou alterar o gasto.

## Como a anomalia é calculada?

Um gasto é anomalia quando `valor > média * 2`. A média é calculada sobre os gastos cadastrados.

## O sistema usa Machine Learning?

Não. O escopo usa agregação, média, agrupamento por categoria e uma regra simples de detecção.

## O que acontece quando não existem gastos?

Total e média retornam `0.0`; categorias e anomalias retornam listas vazias.

## Por que existe um controller separado?

Para manter a separação de responsabilidades: a rota recebe HTTP, o controller traduz a resposta e o service executa a regra.

## Como a API se conecta ao PostgreSQL no Docker?

A variável `DATABASE_URL` usa `database` como host, que é o nome do serviço no Compose, e não `localhost`.

## O Docker foi validado em execução?

A configuração foi validada com `docker compose config`, mas a execução completa depende do Docker Desktop estar ativo.

## A interface Tkinter já está implementada?

Não neste repositório. Ela está atribuída à colega e deve consumir os endpoints HTTP da API.

## Quais são os próximos passos?

Validar o ambiente Docker completo, integrar a interface Tkinter e substituir os dados provisórios da apresentação pelos registros reais da equipe.
