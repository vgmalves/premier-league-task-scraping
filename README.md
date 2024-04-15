## Resultado Final do Projeto

#### Resumo do Time
![Página 1](https://github.com/vgmalves/premier-league-task-scraping/blob/main/Power%20Bi/Telas%20do%20Dashboard/tela-resumo-time.png?raw=true)

#### Comparativo de Resultados
![Página 2](https://github.com/vgmalves/premier-league-task-scraping/blob/main/Power%20Bi/Telas%20do%20Dashboard/tela-medidor-forca-time.png?raw=true)

#### Tabelas (Geral, Home & Away)
![Página 3](https://github.com/vgmalves/premier-league-task-scraping/blob/main/Power%20Bi/Telas%20do%20Dashboard/tabela-geral-tabelas.png?raw=true)

### Acesse o Dashboard Aqui
[Premier League - Power Bi](https://app.powerbi.com/view?r=eyJrIjoiMTNiNWViYjItMjZhNC00NTI4LWJhODEtODRiYzhlMzllMGJhIiwidCI6ImQ1Njc0NmZiLTZjYzItNGFmNi04M2ViLTk1ZWE3YWVkOTQ2ZiJ9)

## Sobre o Projeto

A iniciativa deste projeto surgiu de maneira recreativa. O Futebol é um esporte apreciado por muitos, e eu faço parte desses muitos.

A Premier League é uma das ligas que mais acompanho depois do Campeonato Brasileiro, e a intenção desse projeto foi apenas poder verificar as estatísticas básicas do considerado o campeonato mais competitivo do mundo, pra poder criar insights na roda de amigos para ponteciais palpites esportivos.
Ressalto que a usabilidade é totalmente recreativa e monitorada num grupo seleto de pessoas. Não apresenta quaisquer resultados concretos, se tratando apenas de probabilidades que estão incluídas num infinito quadro de possibilidades e realidades. 

O cálculo que aparece no Dashboard é baseado na modelagem de força do time. Não sendo uma probabilidade, mas apenas um recurso utilizado para medir a "força" de um determinado time dentro do campeonato.
Caso haja necessidade de realizar as simulações, deixei um arquivo .pynb aqui neste repositório com o que seriam a variadas simulações para chegar no resultado. Ressalto que busquei as referêcnias do código no ChatGPT, e pode precisar de aprimoramentos pra aplicações reais.

## Scripts Python:
Observações: podem haver melhorias a implementar.

#### premier_league_home_away.py e premier_league.py
"premier_league_home_away.py" é o arquivo principal. Nele eu criei algumas funções para ajudar a tratar as informações retiradas da página da Web (Referência 1 - Referências)
criei ambos os scripts em momentos diferentes, mas percebi que pode ser interessante mantê-los separados. Por isso, ao executar o premier_league_home_away.py, importo os premier_league.py para utilizar sua função e obter a tabela geral da Liga.

  ### Libs:
  
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import re
    from sqlalchemy import create_engine

  ### Funções:
  
    def buscar_tabelas():
    def jogos_casa():
    def jogos_fora():
    def atualizar_banco_de_dados(): 

#### buscar_tabelas
Busca na url fornecida as tabelas dos jogos home & away dos times da Liga, retornado um dataframe que será tratado e upado numa tabela dentro de um banco de dados nos PostgreSQL, utilizando a função: atualizar_banco_de_dados.

#### jogos_fora, jogos_casa
O mesmo procedimento adotado na função acima é estabelicido nessas duas outras funções, que comportam as últimas 5 rodadas home&away dos times, porém, nesta função há uma maior concentração no tratamento dos dados, pois precisam ser normalizados com a intenção de podermos fazer um relacionamento entre as tabelas futuramente. 

#### atualizar_banco_de_dados:

    def atualizar_banco_de_dados(tabela, nome_da_tabela):
      engine = create_engine('postgresql+psycopg2://usuario:senha@host/banco')
      tabela.to_sql(nome_da_tabela, con=engine, if_exists='replace', index=False)

      return print(f'{nome_da_tabela} atualizado')

Utilizando "from sqlalchemy import create_engine", eu consigo criar uma engine que já determina a estrutura da tabela no banco de dados (por esse motivo eu tipei as informações extratídas da Web no código já (premier_league.py e premier_league_home_away.py)
Aqui, basicamente utilizo uma variável com o dataframe retornado da pesquisa, e dou um nome à tabela. 

## Referências

- [Hipótese Futebol e Probabilidade](https://ufmg.medium.com/s%C3%A3o-s%C3%B3-dois-os-lados-da-mesma-partida-8de8a22d09d7)
