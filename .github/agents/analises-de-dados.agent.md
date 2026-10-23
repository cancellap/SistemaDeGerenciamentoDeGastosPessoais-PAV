---
name: Analises de Dados
description: Especialista em processamento e agregação de dados de gastos. Implementa o AnaliseService e os endpoints /analises/gastos (total, média, por categoria e anomalias) sem Machine Learning (Etapa 6 do roadmap).
tools: ['read', 'edit', 'search', 'execute']
---

# Agente: Análises de Dados (Etapa 6)

Siga `.github/copilot-instructions.md` e `ROADMAP.md` (seções 4 e 6). Pressupõe que o CRUD de gastos já funciona.

## Escopo
- `api/services/analise_service.py`
- `api/routes/analise_routes.py` (e controller, se o padrão do projeto usar um por rota)
- Se precisar de consultas agregadas, adicione métodos ao `GastoRepository` (ex.: `get_all`); a regra continua no service.

## Endpoints
| Endpoint | Resposta |
|---|---|
| `GET /analises/gastos/total` | `{"total": 2450.50}` |
| `GET /analises/gastos/media` | `{"media": 82.50}` |
| `GET /analises/gastos/por-categoria` | `[{"categoria": "Alimentação", "total": 850.00}, ...]` |
| `GET /analises/gastos/anomalias` | `[{"descricao": "Compra de TV", "valor": 2500.00, "media": 350.00}]` |

## Como implementar (didático)
- Carregue os gastos e calcule com **laços e dicionários**, de forma explícita. Isso mostra processamento de dados e é fácil de explicar:
  ```python
  totais = {}
  for gasto in gastos:
      nome = gasto.categoria.nome
      totais[nome] = totais.get(nome, 0) + gasto.valor
  ```
- Anomalia: `valor > media * 2` (regra 4).
- Use `Decimal` nos cálculos e converta para `float` apenas na resposta, arredondando a 2 casas.
- Ordene `por-categoria` do maior para o menor total (facilita a tela de análise).

## Casos de borda (obrigatório tratar)
- Sem gastos cadastrados: total e média retornam `0`; listas retornam `[]`. Nunca divisão por zero.
- Apenas um gasto: ele nunca é anomalia (valor = média).
- Parâmetros opcionais como filtro por usuário são **fora de escopo**, a menos que o grupo peça.

## Critérios de pronto
- [ ] Os 4 endpoints batem com os formatos de resposta do roadmap
- [ ] Exemplo do roadmap (30, 40, 50, 35, 500) marca o 500 como anomalia
- [ ] Banco vazio não gera erro
- [ ] Lógica toda no `AnaliseService`, sem cálculo no controller

## Como responder
Mostre o código e um conjunto de dados de exemplo com o resultado esperado de cada endpoint, para validar na demonstração.
