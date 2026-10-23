# Cards — Analise de Gastos Pessoais

> Status inicial de todos os cards: `Backlog`
>
> Formato: cada card possui identificador, prioridade, dependencias e criterio de aceite.

## EP01 — Planejamento e estrutura

### T-001 — Criar estrutura principal
- **Prioridade:** Must
- **Dependencias:** Nenhuma
- **Aceite:** A estrutura separa `api`, `interface` e infraestrutura.

### T-002 — Definir padrao de organizacao
- **Prioridade:** Must
- **Dependencias:** T-001
- **Aceite:** Nomes de arquivos, modulos e identificadores seguem um padrao documentado.

### T-003 — Registrar escopo
- **Prioridade:** Must
- **Dependencias:** Nenhuma
- **Aceite:** Funcionalidades dentro e fora do escopo estao documentadas.

### T-004 — Criar documentacao inicial
- **Prioridade:** Should
- **Dependencias:** T-001
- **Aceite:** A documentacao apresenta objetivo, tecnologias, arquitetura e execucao.

## EP02 — Banco de dados

### T-005 — Criar tabela usuarios
- **Prioridade:** Must
- **Dependencias:** T-001
- **Aceite:** A tabela possui `id`, `nome` e `email`.

### T-006 — Criar tabela categorias
- **Prioridade:** Must
- **Dependencias:** T-001
- **Aceite:** A tabela possui `id` e `nome`.

### T-007 — Criar tabela gastos
- **Prioridade:** Must
- **Dependencias:** T-005, T-006
- **Aceite:** A tabela possui descricao, valor, data, `usuario_id` e `categoria_id`.

### T-008 — Configurar relacao usuario-gasto
- **Prioridade:** Must
- **Dependencias:** T-005, T-007
- **Aceite:** Um usuario pode possuir varios gastos e cada gasto pertence a um usuario.

### T-009 — Configurar relacao categoria-gasto
- **Prioridade:** Must
- **Dependencias:** T-006, T-007
- **Aceite:** Uma categoria pode possuir varios gastos e cada gasto pertence a uma categoria.

### T-010 — Configurar integridade referencial
- **Prioridade:** Must
- **Dependencias:** T-007
- **Aceite:** Chaves primarias e estrangeiras impedem referencias invalidas.

### T-011 — Configurar PostgreSQL
- **Prioridade:** Must
- **Dependencias:** T-001
- **Aceite:** O banco pode ser iniciado para desenvolvimento e Docker.

### T-012 — Criar init.sql
- **Prioridade:** Should
- **Dependencias:** T-005, T-006, T-007
- **Aceite:** O script inicializa o banco limpo quando executado.

### T-013 — Definir tipo monetario
- **Prioridade:** Must
- **Dependencias:** T-007
- **Aceite:** Valores sao persistidos sem perda de precisao.

## EP03 — Modelos e persistencia

### T-014 — Criar modelo Usuario
- **Prioridade:** Must
- **Dependencias:** T-005
- **Aceite:** Existe classe SQLAlchemy correspondente a `usuarios`.

### T-015 — Criar modelo Categoria
- **Prioridade:** Must
- **Dependencias:** T-006
- **Aceite:** Existe classe SQLAlchemy correspondente a `categorias`.

### T-016 — Criar modelo Gasto
- **Prioridade:** Must
- **Dependencias:** T-007
- **Aceite:** Existe classe SQLAlchemy correspondente a `gastos`.

### T-017 — Implementar Usuario.gastos
- **Prioridade:** Must
- **Dependencias:** T-014, T-016
- **Aceite:** O relacionamento retorna os gastos do usuario.

### T-018 — Implementar Categoria.gastos
- **Prioridade:** Must
- **Dependencias:** T-015, T-016
- **Aceite:** O relacionamento retorna os gastos da categoria.

### T-019 — Implementar Gasto.usuario e Gasto.categoria
- **Prioridade:** Must
- **Dependencias:** T-016
- **Aceite:** O gasto permite acessar seu usuario e sua categoria.

### T-020 — Criar UsuarioRepository
- **Prioridade:** Must
- **Dependencias:** T-014
- **Aceite:** Implementa `create`, `get`, `get_all`, `update` e `delete`.

### T-021 — Criar CategoriaRepository
- **Prioridade:** Must
- **Dependencias:** T-015
- **Aceite:** Implementa `create`, `get`, `get_all`, `update` e `delete`.

### T-022 — Criar GastoRepository
- **Prioridade:** Must
- **Dependencias:** T-016
- **Aceite:** Implementa `create`, `get`, `get_all`, `update` e `delete`.

### T-023 — Configurar sessao SQLAlchemy
- **Prioridade:** Must
- **Dependencias:** T-011
- **Aceite:** Conexoes sao abertas, utilizadas e encerradas corretamente.

## EP04 — Regras e services

### T-024 — Criar UsuarioService
- **Prioridade:** Must
- **Dependencias:** T-020
- **Aceite:** O service concentra operacoes e regras de usuario.

### T-025 — Criar CategoriaService
- **Prioridade:** Must
- **Dependencias:** T-021
- **Aceite:** O service concentra operacoes e regras de categoria.

### T-026 — Criar GastoService
- **Prioridade:** Must
- **Dependencias:** T-022
- **Aceite:** O service concentra operacoes e regras de gasto.

### T-027 — Criar AnaliseService
- **Prioridade:** Must
- **Dependencias:** T-022
- **Aceite:** O service concentra os calculos e agregacoes.

### T-028 — Validar valor positivo
- **Prioridade:** Must
- **Dependencias:** T-026
- **Aceite:** Valores menores ou iguais a zero sao rejeitados.

### T-029 — Validar email unico
- **Prioridade:** Must
- **Dependencias:** T-024
- **Aceite:** Um segundo usuario com o mesmo email e rejeitado.

### T-030 — Validar usuario do gasto
- **Prioridade:** Must
- **Dependencias:** T-026
- **Aceite:** Gasto com usuario inexistente e rejeitado.

### T-031 — Validar categoria do gasto
- **Prioridade:** Must
- **Dependencias:** T-026
- **Aceite:** Gasto com categoria inexistente e rejeitado.

### T-032 — Definir exclusao com dependencias
- **Prioridade:** Must
- **Dependencias:** T-024, T-025, T-026
- **Aceite:** O comportamento para usuario ou categoria com gastos vinculados esta documentado e testado.

### T-033 — Validar atualizacoes
- **Prioridade:** Must
- **Dependencias:** T-024, T-025, T-026
- **Aceite:** As mesmas regras do cadastro sao aplicadas no PUT.

### T-034 — Separar camadas
- **Prioridade:** Must
- **Dependencias:** T-024, T-025, T-026, T-027
- **Aceite:** Regras nao ficam misturadas com HTTP ou acesso direto ao banco.

## EP05 — API REST

### T-035 — Criar rotas de usuarios
- **Prioridade:** Must
- **Dependencias:** T-024
- **Aceite:** A API expoe o CRUD completo de usuarios.

### T-036 — Criar rotas de categorias
- **Prioridade:** Must
- **Dependencias:** T-025
- **Aceite:** A API expoe o CRUD completo de categorias.

### T-037 — Criar rotas de gastos
- **Prioridade:** Must
- **Dependencias:** T-026
- **Aceite:** A API expoe o CRUD completo de gastos.

### T-038 — Implementar POST /usuarios
- **Prioridade:** Must
- **Dependencias:** T-035
- **Aceite:** Cadastra usuario valido e retorna o registro criado.

### T-039 — Implementar GET de usuarios
- **Prioridade:** Must
- **Dependencias:** T-035
- **Aceite:** Lista usuarios e consulta usuario por ID.

### T-040 — Implementar PUT e DELETE de usuarios
- **Prioridade:** Must
- **Dependencias:** T-035
- **Aceite:** Permite editar e excluir usuario existente.

### T-041 — Implementar POST /categorias
- **Prioridade:** Must
- **Dependencias:** T-036
- **Aceite:** Cadastra categoria e retorna o registro criado.

### T-042 — Implementar GET de categorias
- **Prioridade:** Must
- **Dependencias:** T-036
- **Aceite:** Lista categorias e consulta categoria por ID.

### T-043 — Implementar PUT e DELETE de categorias
- **Prioridade:** Must
- **Dependencias:** T-036
- **Aceite:** Permite editar e excluir categoria existente conforme regra definida.

### T-044 — Implementar POST /gastos
- **Prioridade:** Must
- **Dependencias:** T-037
- **Aceite:** Cadastra gasto somente com dados validos.

### T-045 — Implementar GET de gastos
- **Prioridade:** Must
- **Dependencias:** T-037
- **Aceite:** Lista gastos e consulta gasto por ID.

### T-046 — Implementar PUT e DELETE de gastos
- **Prioridade:** Must
- **Dependencias:** T-037
- **Aceite:** Permite editar e excluir gasto existente.

### T-047 — Criar schemas da API
- **Prioridade:** Must
- **Dependencias:** T-035, T-036, T-037
- **Aceite:** Entradas e saidas possuem formatos definidos.

### T-048 — Padronizar respostas HTTP
- **Prioridade:** Must
- **Dependencias:** T-035 a T-046
- **Aceite:** Sucesso, validacao e registro inexistente retornam respostas consistentes.

### T-049 — Configurar documentacao FastAPI
- **Prioridade:** Should
- **Dependencias:** T-035
- **Aceite:** Os endpoints podem ser consultados e testados na documentacao automatica.

### T-050 — Criar app.py
- **Prioridade:** Must
- **Dependencias:** T-035, T-036, T-037
- **Aceite:** A aplicacao inicia e registra todas as rotas.

## EP06 — Analises

### T-051 — Calcular total de gastos
- **Prioridade:** Must
- **Dependencias:** T-027
- **Aceite:** O total corresponde a soma dos gastos cadastrados.

### T-052 — Calcular media de gastos
- **Prioridade:** Must
- **Dependencias:** T-027
- **Aceite:** A media corresponde ao total dividido pela quantidade de gastos.

### T-053 — Agregar gastos por categoria
- **Prioridade:** Must
- **Dependencias:** T-027
- **Aceite:** Cada categoria retorna seu total acumulado.

### T-054 — Identificar maior categoria
- **Prioridade:** Should
- **Dependencias:** T-053
- **Aceite:** A categoria com maior total e identificada corretamente.

### T-055 — Identificar gastos acima do padrao
- **Prioridade:** Must
- **Dependencias:** T-027
- **Aceite:** Retorna gastos que atendem ao limite aprovado, inicialmente `gasto > media x 2`.

### T-056 — Criar GET /analises/gastos/total
- **Prioridade:** Must
- **Dependencias:** T-051
- **Aceite:** Retorna objeto com o total.

### T-057 — Criar GET /analises/gastos/media
- **Prioridade:** Must
- **Dependencias:** T-052
- **Aceite:** Retorna objeto com a media.

### T-058 — Criar GET /analises/gastos/por-categoria
- **Prioridade:** Must
- **Dependencias:** T-053
- **Aceite:** Retorna categoria e total agrupado.

### T-059 — Criar GET /analises/gastos/anomalias
- **Prioridade:** Must
- **Dependencias:** T-055
- **Aceite:** Retorna descricao, valor e media dos gastos identificados.

### T-060 — Tratar analise sem gastos
- **Prioridade:** Must
- **Dependencias:** T-051, T-052
- **Aceite:** A API retorna resposta definida sem divisao por zero ou erro nao tratado.

### T-061 — Validar arredondamento monetario
- **Prioridade:** Must
- **Dependencias:** T-051 a T-059
- **Aceite:** Calculos e respostas possuem arredondamento consistente.

## EP07 — Interface Tkinter

### T-062 — Criar janela principal
- **Prioridade:** Must
- **Dependencias:** Nenhuma
- **Aceite:** A aplicacao Tkinter inicia com titulo e area principal.

### T-063 — Criar navegacao principal
- **Prioridade:** Must
- **Dependencias:** T-062
- **Aceite:** O usuario acessa Usuarios, Categorias, Gastos e Analises.

### T-064 — Criar tela de usuarios
- **Prioridade:** Must
- **Dependencias:** T-038, T-039, T-040
- **Aceite:** Permite cadastrar, consultar, editar e excluir usuarios.

### T-065 — Criar tela de categorias
- **Prioridade:** Must
- **Dependencias:** T-041, T-042, T-043
- **Aceite:** Permite cadastrar, consultar, editar e excluir categorias.

### T-066 — Criar tela de gastos
- **Prioridade:** Must
- **Dependencias:** T-044, T-045, T-046
- **Aceite:** Permite cadastrar, consultar, editar e excluir gastos.

### T-067 — Selecionar usuario e categoria
- **Prioridade:** Must
- **Dependencias:** T-064, T-065, T-066
- **Aceite:** O formulario de gasto oferece selecoes carregadas da API.

### T-068 — Exibir total e media
- **Prioridade:** Must
- **Dependencias:** T-056, T-057
- **Aceite:** A tela de analise mostra total e media formatados.

### T-069 — Exibir gastos por categoria
- **Prioridade:** Must
- **Dependencias:** T-058
- **Aceite:** A tela lista cada categoria e seu total.

### T-070 — Exibir gastos acima do padrao
- **Prioridade:** Must
- **Dependencias:** T-059
- **Aceite:** A tela lista os gastos retornados pela analise.

### T-071 — Atualizar listas apos operacoes
- **Prioridade:** Must
- **Dependencias:** T-064, T-065, T-066
- **Aceite:** Listas refletem cadastro, edicao e exclusao sem reiniciar a aplicacao.

### T-072 — Validar campos obrigatorios
- **Prioridade:** Must
- **Dependencias:** T-064, T-065, T-066
- **Aceite:** Campos vazios geram mensagem compreensivel.

### T-073 — Exibir erros de validacao
- **Prioridade:** Must
- **Dependencias:** T-028, T-048
- **Aceite:** Valor invalido, registro inexistente e categoria invalida sao informados ao usuario.

### T-074 — Exibir erro de comunicacao
- **Prioridade:** Must
- **Dependencias:** T-064, T-070
- **Aceite:** API indisponivel gera mensagem sem encerrar a interface.

### T-075 — Executar interface fora do Docker
- **Prioridade:** Must
- **Dependencias:** T-062
- **Aceite:** A interface inicia localmente e acessa a API por HTTP.

## EP08 — Integracao HTTP

### T-076 — Criar cliente HTTP
- **Prioridade:** Must
- **Dependencias:** T-035
- **Aceite:** Existe modulo responsavel pelas requisicoes da interface.

### T-077 — Integrar usuarios
- **Prioridade:** Must
- **Dependencias:** T-076
- **Aceite:** A interface consome todos os endpoints de usuarios.

### T-078 — Integrar categorias
- **Prioridade:** Must
- **Dependencias:** T-076
- **Aceite:** A interface consome todos os endpoints de categorias.

### T-079 — Integrar gastos
- **Prioridade:** Must
- **Dependencias:** T-076
- **Aceite:** A interface consome todos os endpoints de gastos.

### T-080 — Integrar analises
- **Prioridade:** Must
- **Dependencias:** T-076
- **Aceite:** A interface consome todos os endpoints de analise.

### T-081 — Converter respostas HTTP
- **Prioridade:** Must
- **Dependencias:** T-077, T-078, T-079, T-080
- **Aceite:** Respostas sao convertidas em dados exibiveis nas telas.

### T-082 — Converter erros HTTP
- **Prioridade:** Must
- **Dependencias:** T-076
- **Aceite:** Erros HTTP e de conexao chegam como mensagens compreensiveis.

### T-083 — Validar fluxo completo
- **Prioridade:** Must
- **Dependencias:** T-064 a T-082
- **Aceite:** Um cadastro feito no Tkinter chega ao PostgreSQL pela API e pode ser consultado novamente.

## EP09 — Docker

### T-084 — Criar Dockerfile da API
- **Prioridade:** Must
- **Dependencias:** T-050
- **Aceite:** A imagem instala dependencias, copia o projeto e inicia a API.

### T-085 — Criar docker-compose.yml
- **Prioridade:** Must
- **Dependencias:** T-084
- **Aceite:** O Compose define os servicos API e PostgreSQL.

### T-086 — Configurar container PostgreSQL
- **Prioridade:** Must
- **Dependencias:** T-085
- **Aceite:** O banco inicia com volume e configuracao documentados.

### T-087 — Configurar container da API
- **Prioridade:** Must
- **Dependencias:** T-085
- **Aceite:** A API inicia e fica acessivel pelo endereco configurado.

### T-088 — Configurar variaveis de ambiente
- **Prioridade:** Must
- **Dependencias:** T-085
- **Aceite:** Credenciais e URL do banco nao ficam fixas no codigo.

### T-089 — Configurar ordem de inicializacao
- **Prioridade:** Should
- **Dependencias:** T-085
- **Aceite:** A API aguarda o banco estar disponivel ou trata a indisponibilidade corretamente.

### T-090 — Testar ambiente limpo
- **Prioridade:** Must
- **Dependencias:** T-086, T-087
- **Aceite:** Os containers sobem em uma maquina sem estado anterior do projeto.

### T-091 — Documentar comandos Docker
- **Prioridade:** Must
- **Dependencias:** T-090
- **Aceite:** README informa como iniciar, parar e consultar os servicos.

### T-092 — Conectar interface ao Docker
- **Prioridade:** Must
- **Dependencias:** T-083, T-090
- **Aceite:** Tkinter acessa a API em execucao no container.

## EP10 — Testes e qualidade

### T-093 — Testar CRUD de usuarios
- **Prioridade:** Must
- **Dependencias:** T-038, T-039, T-040
- **Aceite:** Criacao, consulta, edicao e exclusao passam com dados validos.

### T-094 — Testar CRUD de categorias
- **Prioridade:** Must
- **Dependencias:** T-041, T-042, T-043
- **Aceite:** Criacao, consulta, edicao e exclusao passam com dados validos.

### T-095 — Testar CRUD de gastos
- **Prioridade:** Must
- **Dependencias:** T-044, T-045, T-046
- **Aceite:** Criacao, consulta, edicao e exclusao passam com dados validos.

### T-096 — Testar valor invalido
- **Prioridade:** Must
- **Dependencias:** T-028
- **Aceite:** Zero e valores negativos sao rejeitados.

### T-097 — Testar email duplicado
- **Prioridade:** Must
- **Dependencias:** T-029
- **Aceite:** O segundo cadastro com o mesmo email e rejeitado.

### T-098 — Testar usuario inexistente
- **Prioridade:** Must
- **Dependencias:** T-030
- **Aceite:** Gasto com usuario inexistente retorna erro controlado.

### T-099 — Testar categoria inexistente
- **Prioridade:** Must
- **Dependencias:** T-031
- **Aceite:** Gasto com categoria inexistente retorna erro controlado.

### T-100 — Testar total e media
- **Prioridade:** Must
- **Dependencias:** T-051, T-052
- **Aceite:** Resultados correspondem a um conjunto conhecido de gastos.

### T-101 — Testar agrupamento por categoria
- **Prioridade:** Must
- **Dependencias:** T-053
- **Aceite:** Totais agrupados correspondem aos dados cadastrados.

### T-102 — Testar anomalias
- **Prioridade:** Must
- **Dependencias:** T-055
- **Aceite:** Um gasto acima do limite e identificado e um gasto normal nao e incluido.

### T-103 — Testar analise vazia
- **Prioridade:** Must
- **Dependencias:** T-060
- **Aceite:** Endpoints de analise respondem sem erro quando nao ha gastos.

### T-104 — Testar API indisponivel
- **Prioridade:** Must
- **Dependencias:** T-074
- **Aceite:** A interface exibe mensagem de conexao e permanece utilizavel.

### T-105 — Testar integracao com Docker
- **Prioridade:** Must
- **Dependencias:** T-090, T-083
- **Aceite:** Fluxo completo funciona com API e banco em containers.

### T-106 — Revisar checklist academico
- **Prioridade:** Must
- **Dependencias:** T-093 a T-105
- **Aceite:** Todos os itens do roadmap estao implementados ou possuem pendencia registrada.

## EP11 — Apresentacao e entrega

### T-107 — Preparar contexto e problema
- **Prioridade:** Must
- **Dependencias:** T-003
- **Aceite:** A apresentacao explica o problema e o objetivo do sistema.

### T-108 — Documentar requisitos implementados
- **Prioridade:** Must
- **Dependencias:** T-106
- **Aceite:** Requisitos funcionais, regras e restricoes estao listados.

### T-109 — Preparar modelo do banco
- **Prioridade:** Must
- **Dependencias:** T-010
- **Aceite:** O diagrama mostra usuarios, categorias, gastos e relacionamentos.

### T-110 — Preparar arquitetura
- **Prioridade:** Must
- **Dependencias:** T-034
- **Aceite:** A apresentacao mostra Controller, Service, Repository, ORM e banco.

### T-111 — Preparar principais classes
- **Prioridade:** Must
- **Dependencias:** T-014 a T-027
- **Aceite:** As entidades, services e repositories sao explicados.

### T-112 — Preparar endpoints
- **Prioridade:** Must
- **Dependencias:** T-035 a T-059
- **Aceite:** CRUD e analises sao demonstrados com suas rotas.

### T-113 — Demonstrar cadastro e consulta
- **Prioridade:** Must
- **Dependencias:** T-093
- **Aceite:** O roteiro cadastra usuario, categoria e gastos e consulta os registros.

### T-114 — Demonstrar edicao e exclusao
- **Prioridade:** Must
- **Dependencias:** T-093, T-094, T-095
- **Aceite:** O roteiro altera e exclui pelo menos um registro.

### T-115 — Demonstrar regras de negocio
- **Prioridade:** Must
- **Dependencias:** T-096, T-097, T-098, T-099
- **Aceite:** O roteiro demonstra valor invalido, email duplicado e categoria inexistente.

### T-116 — Demonstrar analises
- **Prioridade:** Must
- **Dependencias:** T-100, T-101, T-102
- **Aceite:** O roteiro mostra total, media, agrupamento e anomalias.

### T-117 — Demonstrar comunicacao Tkinter/API
- **Prioridade:** Must
- **Dependencias:** T-083
- **Aceite:** Fica evidenciado que a interface usa HTTP para acessar a API.

### T-118 — Demonstrar persistencia PostgreSQL
- **Prioridade:** Must
- **Dependencias:** T-105
- **Aceite:** Um registro e localizado no banco apos ser criado pela interface.

### T-119 — Registrar dificuldades e decisoes
- **Prioridade:** Should
- **Dependencias:** T-106
- **Aceite:** Dificuldades, decisoes e limitacoes conhecidas estao documentadas.

### T-120 — Ensaiar demonstracao em ambiente limpo
- **Prioridade:** Must
- **Dependencias:** T-107 a T-119
- **Aceite:** O roteiro completo executa sem depender de configuracoes ocultas.

## Fluxo sugerido

1. Executar T-001 a T-013.
2. Executar T-014 a T-034.
3. Executar T-035 a T-061.
4. Executar T-062 a T-083.
5. Executar T-084 a T-092.
6. Executar T-093 a T-106.
7. Executar T-107 a T-120.

## Pendencias para refinamento

- Definir comportamento ao excluir usuario ou categoria com gastos vinculados.
- Confirmar se a anomalia sera global, por usuario ou por categoria.
- Confirmar validacao de formato de email.
- Confirmar se datas futuras serao aceitas.
- Definir volume esperado de dados e usuarios simultaneos.
- Confirmar necessidade de autenticacao.
- Definir versoes das tecnologias.
- Definir se `init.sql` criara categorias iniciais.
- Definir como a interface selecionara registros para editar e excluir.
