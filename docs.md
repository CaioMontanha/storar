STORAR
Previsão de ruptura de estoque


COMO USAR COM A IA

Cole este documento inteiro e peça: construa o projeto completo de uma vez, sem me fazer perguntas. Onde faltar detalhe, decida e anote a decisão no README. Siga os contratos de API ao pé da letra, escreva os testes da função de previsão e entregue com docker compose up subindo tudo, inclusive migrate e seed.


A IDEIA EM DUAS LINHAS

Sistema para uma lojinha de produtos de praia descobrir quais itens vão acabar primeiro. A previsão é calculada a partir do histórico real de vendas, e o sistema ainda diz até quando dá para esperar antes de pedir reposição.


O QUE TIRA ISSO DO NÍVEL DE CRUD

A média de vendas nunca é um campo digitado. Ela é calculada sobre uma janela de dias das vendas registradas. Os casos de borda são tratados de propósito: média zero não vira divisão por zero, estoque zero não vira previsão de dias, e dias sem venda entram na média como zero. Quem divide só pelos dias em que vendeu superestima o giro e prevê ruptura cedo demais.


STACK

Backend: Python 3.12, Django 5, Django REST Framework, django-filter, django-cors-headers
Banco: PostgreSQL 16
Frontend: React + TypeScript + Vite + Recharts
Infra: docker compose com db, api e web


ESTRUTURA DE PASTAS

storar/
  docker-compose.yml
  .env.example
  backend/config/settings.py
  backend/inventory/models.py
  backend/inventory/forecast.py             função pura da previsão
  backend/inventory/services.py             registrar venda e reposição com transaction.atomic
  backend/inventory/serializers.py
  backend/inventory/views.py
  backend/inventory/filters.py
  backend/inventory/urls.py
  backend/inventory/tests/test_forecast.py
  backend/inventory/tests/test_api.py
  backend/inventory/management/commands/seed_storar.py
  frontend/src/pages/Dashboard.tsx
  frontend/src/pages/ProductDetail.tsx
  frontend/src/components/StatusBadge.tsx
  frontend/src/components/ConsumptionChart.tsx
  frontend/src/components/ProductForm.tsx
  frontend/src/api.ts
  frontend/src/types.ts


MODELO DE DADOS

Product: sku (único), nome, estoque_atual (inteiro, nunca negativo), prazo_reposicao_dias (padrão 7), ativo
VendaDia: product, data, quantidade. Único em (product, data). Uma linha por produto por dia.
Índice em VendaDia (product, data).


REGRAS

Média diária = soma das quantidades vendidas nos últimos N dias dividida por N. O padrão é N = 14 e pode vir por query string (7, 14 ou 30). Dias sem registro contam como zero.

Dias restantes = estoque_atual dividido pela média diária, arredondado para baixo.

Status, nesta ordem de checagem:
  esgotado: estoque_atual igual a zero
  sem_giro: estoque maior que zero e média igual a zero (dias restantes fica nulo, nada de divisão por zero)
  critico: 7 dias ou menos
  atencao: de 8 a 21 dias
  ok: mais de 21 dias

Pedir até = hoje + dias restantes menos prazo_reposicao_dias. Se essa data já passou, devolve reposicao_atrasada true.

Registrar venda: dentro de transaction.atomic, trava o produto com select_for_update. Se quantidade for maior que o estoque, responde 409 com { erro: "estoque_insuficiente", mensagem, estoque_atual }. Senão desconta do estoque e soma na linha do dia (cria se não existir).

Registrar reposição: soma no estoque, quantidade positiva.

Função pura:
calcular_previsao(estoque, total_vendido_na_janela, janela_dias, prazo_reposicao_dias, hoje) devolve dict com media_diaria, dias_restantes, status, pedir_ate, reposicao_atrasada. Sem ORM.

Na listagem, calcule o total da janela com uma anotação do ORM (Sum com filter) para evitar uma query por produto. Esse é o tipo de detalhe que separa intermediário de iniciante.


CONTRATO DA API

GET     /api/products?status=critico&janela=14&ordering=dias_restantes&search=
        cada produto com media_diaria, dias_restantes, status, pedir_ate, reposicao_atrasada
POST    /api/products
GET     /api/products/{id}
PATCH   /api/products/{id}
DELETE  /api/products/{id}
        remoção lógica: só marca ativo false
GET     /api/products/{id}/sales?days=30
        série diária completa, com zeros nos dias sem venda, para o gráfico
POST    /api/products/{id}/sales
        corpo: data (padrão hoje) e quantidade. Responde 201.
POST    /api/products/{id}/restock
        corpo: quantidade
GET     /api/dashboard
        contagem por status e os 5 produtos mais críticos

Erros no formato { erro, mensagem }.


TELAS

Dashboard: cards com quantidade de produtos críticos, em atenção, ok e sem giro. Abaixo, tabela ordenada por dias restantes com o produto mais urgente no topo: nome, estoque, média por dia, previsão com badge (vermelho, amarelo, verde ou cinza) e a coluna Pedir até. Filtro por status e busca por nome.
Detalhe do produto: gráfico de consumo dos últimos 30 dias com a linha da média, formulário de Registrar venda, formulário de Registrar reposição, e botão de editar que abre ProductForm em modal.
O badge mostra texto, por exemplo 3 dias, Sem giro, Esgotado. Atualização otimista ou refetch logo depois de registrar venda, sem recarregar a página.


DADOS DE SEED (comando seed_storar)

Doze produtos de uma lojinha de Porto de Galinhas: Camiseta Porto, Bermuda Surf, Boné Nordeste, Chinelo Nordestino, Canga Maracaípe, Protetor Solar FPS 50, Saída de Praia, Garrafa Térmica, Regata Dry Fit, Óculos Esportivo, Bolsa Estanque, Chaveiro Jangada.

60 dias de vendas por produto, com variação aleatória de mais ou menos 30% e fins de semana vendendo cerca de 1,6 vez mais.

Três produtos ajustados para o exemplo do projeto:
  Camiseta Porto: estoque 12, média perto de 4 por dia, previsão crítica
  Bermuda Surf: estoque 37, média perto de 3 por dia, previsão em atenção
  Boné Nordeste: estoque 82, média perto de 2 por dia, previsão ok

Dois casos de borda de propósito:
  Chaveiro Jangada: estoque 40 e nenhuma venda, deve aparecer como sem giro
  Garrafa Térmica: estoque 0, deve aparecer como esgotado


ORDEM DE CONSTRUÇÃO

passo 1: docker compose, settings, models e migrations
passo 2: forecast.py com testes
passo 3: services, serializers, views e urls
passo 4: seed_storar
passo 5: frontend


TESTES OBRIGATÓRIOS

média zero devolve dias_restantes nulo e status sem_giro, sem exceção
estoque zero devolve esgotado
dias sem venda entram como zero na média (10 vendidos em 14 dias é média 0,71, não 10 dividido pelos dias com venda)
limites de status: 7 dias é crítico, 8 é atenção, 21 é atenção, 22 é ok
pedir_ate no passado marca reposicao_atrasada
registrar venda maior que o estoque responde 409 e não altera nada
a listagem faz um número fixo de queries, independente de quantos produtos existem (assertNumQueries)


O QUE PRECISA ESTAR LÁ PARA PARECER INTERMEDIÁRIO

Previsão como função pura testada nos limites. Anotação no ORM contra o problema de N+1. select_for_update na venda. Remoção lógica. Série temporal completa com zeros para o gráfico. Docker compose que sobe com um comando.


FORA DO ESCOPO

Login, várias lojas, cadastro de fornecedor, preço e financeiro, previsão com machine learning.


PRONTO QUANDO

A lista abre com a Camiseta Porto no topo em vermelho, com 3 dias. Registrar uma venda de 10 camisetas atualiza estoque, média e status na hora, sem recarregar. A Garrafa Térmica aparece como Esgotado, o Chaveiro Jangada como Sem giro, e tentar vender mais do que existe mostra erro claro em vez de deixar o estoque negativo.