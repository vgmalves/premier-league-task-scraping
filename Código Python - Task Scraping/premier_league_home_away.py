import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine

import premier_league

# url_base = 'https://footystats.org/england'
# end_point_premier = '/premier-league'
# end_point_home_away = '/premier-league/home-away-league-table'

url_tabela_home_away = 'https://footystats.org/england/premier-league/home-away-league-table'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url_tabela_home_away, headers=headers)

if response.status_code == 200:
    content = response.text

    soup = BeautifulSoup(content, 'html.parser')

    # Encontrando todas as tabelas na página
    tabelas = soup.find_all('table', class_='full-league-table table-sort col-sm-12 mobify-table')
    primeira_tabela = tabelas[0]
    segunda_tabela = tabelas[1]
    casa = 'casa'
    fora = 'fora'
    
    # Definir o valor máximo da tabela a utilizar no looping
    valor_máximo = soup.find_all('td', class_='position bold zone')

    for i in valor_máximo:
        maximo = int(i.text.strip())

    if maximo > 0:
    
        def buscar_tabelas(tabela, lugar):

            # Definir listas para salvar as informações do campeonato
            times = []
            partidas = []
            vitorias = []
            empates = []
            derrotas = []
            gols_feitos = []
            gols_sofridos = []
            saldo_gols = []
            pontos = []
            ultimas_cinco = []
            jogos_sem_levar_gols = []
            jogos_ambas_marcam = []
            media_total_de_gols_por_jogo = []
            prob_v = []
            prob_d = []
            prob_e = []
            posicao = []

            # Salvando as informações da tabela HOME em listas
            for j in range(maximo):

                nome_dos_times = tabela.find_all('td', class_='team borderRightContent')
                partidas_dos_times = tabela.find_all('td', class_='mp')
                vitorias_dos_times = tabela.find_all('td', class_='win')
                empates_dos_times = tabela.find_all('td', class_='draw')
                derrotas_dos_times = tabela.find_all('td', class_='loss')
                gols_feitos_dos_times = tabela.find_all('td', class_='gf')
                gols_sofridos_dos_times = tabela.find_all('td', class_='ga')
                saldo_de_gols_dos_times = tabela.find_all('td', class_='gd')
                pontos_dos_times = tabela.find_all('td', class_='points bold')
                ultimas_cinco_dos_times = tabela.find_all('td', class_='form')
                jogos_sem_levar_gols_dos_times = tabela.find_all('td', class_='cs')
                jogos_ambas_marcam_dos_times = tabela.find_all('td', class_='btts')
                gols_por_jogo_dos_times = tabela.find_all('td', class_='avg bold')


                position = j + 1
                posicao.append(position)

                # Salvar as informações nas listas
                time = nome_dos_times[j].text.strip()
                times.append(str(time).replace('FC', '').replace(' ', ''))

                partida =  partidas_dos_times[j].text.strip()
                partidas.append(int(partida))

                vitoria  = vitorias_dos_times[j].text.strip()
                vitorias.append(int(vitoria))

                empate = empates_dos_times[j].text.strip()
                empates.append(int(empate))

                derrota = derrotas_dos_times[j].text.strip()
                derrotas.append(int(derrota))

                gol_feito = gols_feitos_dos_times[j].text.strip()
                gols_feitos.append(int(gol_feito))

                gol_sofrido = gols_sofridos_dos_times[j].text.strip()
                gols_sofridos.append(int(gol_sofrido))

                saldo_gol = saldo_de_gols_dos_times[j].text.strip()
                saldo_gols.append(int(saldo_gol))

                ponto = pontos_dos_times[j].text.strip()
                pontos.append(int(ponto))

                ultima_rodada = ultimas_cinco_dos_times[j].text.strip()
                ultimas_cinco.append(ultima_rodada)

                jogo_sem_gol = jogos_sem_levar_gols_dos_times[j].text.strip()
                jogos_sem_levar_gols.append(jogo_sem_gol)

                marcar_ambas = jogos_ambas_marcam_dos_times[j].text.strip()
                jogos_ambas_marcam.append(marcar_ambas)

                gol_por_jogo = gols_por_jogo_dos_times[j].text.strip()
                media_total_de_gols_por_jogo.append(float(gol_por_jogo))

                # Calcular Probabilidades
                p_vitoria = (int(vitoria) / int(partida)) * 100
                prob_v.append(round(float(p_vitoria), 2))

                p_derrota = (int(derrota) / int(partida)) * 100
                prob_d.append(round(float(p_derrota), 2))

                p_empate = (int(empate) / int(partida)) * 100
                prob_e.append(round(float(p_empate), 2))

            # Criar um Dicionário para Tabela

            tabela_geral_dict = {
                
                "time" :  times ,
                "partidas" : partidas,
                "v" : vitorias,
                "e" : empates,
                "d" :  derrotas,
                "gols_feitos" : gols_feitos,
                "gols_sofridos" : gols_sofridos,
                "saldo_de_gols" : saldo_gols,
                "pontos" : pontos,
                "ultimas_5" : ultimas_cinco,
                "clean_sheets" : jogos_sem_levar_gols,
                "ambas_marcam" : jogos_ambas_marcam,
                "media_de_gols_por_jogo" : media_total_de_gols_por_jogo,
                "prob_v" : prob_v,
                "prob_e" : prob_e,
                "prob_d" : prob_d,
                "posicao" : posicao
            }

            df = pd.DataFrame(tabela_geral_dict, index=None)
            df_nova = df.copy()

            #return print(f'A tabela {lugar} foi baixada com sucesso')
            return df_nova

        def jogos_casa(df):
            
            #df =  pd.read_excel(r'tabela_premier_casa.xlsx')
            df_nova = df.copy()

            for i in range(20):
                df_nova['Limpeza'] = df['ultimas_5'].apply(lambda x: x.split('Premier League'))

            # Evidenciar as informações para tratá-las individualmente
            lista_time = []
            lista_resultados = []

            for j in range(20):
                time = df_nova['time'][j]#.replace('FC', '').replace(' ', '')
                for k in range(5):
                    lista_time.append(time)
                    lista_resultados.append(df_nova['Limpeza'][j][k+1].replace(' ', ''))

            resultados_premier = {

                'time':lista_time, 
                'resultado_casa' : lista_resultados
            }

            df_resultados = pd.DataFrame(resultados_premier)

            # Fazer a Limpeza dos Dados e exportar um DataFrame completo
            lista_valores_resultado = ['W', 'D', 'L']
            times_totais_ultimas_5 = []

            for l in range(20):
                time = df_nova['time'][l]#.replace('FC', '').replace(' ', '')
                for m in range(3):
                    resultado_final = lista_valores_resultado[m]
                    time_novo = f'{resultado_final}{time}'
                    times_totais_ultimas_5.append(time_novo)


            df_resultados['resultado_casa'] = df_resultados['resultado_casa'].replace(times_totais_ultimas_5, '', regex=True)

            # * Trecho dedicado a buscar uma solução melhor, mas como estou apenas testando, isso vai funcionar * #

            # Gambiarras
            times_gambiarreiros = ['DAFCBournemouth', 'WAFCBournemouth', 'LAFCBournemouth']
            df_resultados['resultado_casa'] = df_resultados['resultado_casa'].replace(times_gambiarreiros, '', regex=True)
            # Gambiarras FIM


            # Tratar os dados e inserir mais informações no DataFrame
            df_resultados[['placar_final', 'primeiro_tempo']] = df_resultados['resultado_casa'].str.extract(r'(\d+-\d+)FT\(HT:(\d+-\d+)')
            df_resultados['time_adversario'] = df_resultados['resultado_casa'].apply(lambda x: re.search(r'FT\(HT:\d+-\d+(\D+)', x).group(1))
            df_resultados['time_adversario'] = df_resultados['time_adversario'].str.replace(')', '')

            df_resultados.drop(columns=['resultado_casa'], inplace=True)


            resultado_da_partida_casa = []
            #lista_time_visitante = []

            for o in range(len(df_resultados['time'])):

                if int(df_resultados['placar_final'][o][0]) < int(df_resultados['placar_final'][o][2]):
                    resultado_da_partida_casa.append('D')

                elif int(df_resultados['placar_final'][o][0]) > int(df_resultados['placar_final'][o][2]):
                    resultado_da_partida_casa.append('V')
                else:
                    resultado_da_partida_casa.append('E')

            partidas_premier_fora = {'resultado' : resultado_da_partida_casa}
            df_partidas = pd.DataFrame(partidas_premier_fora)
            df_resultados = pd.merge(df_partidas, df_resultados, left_index=True, right_index=True)

            # Reordenar as colunas do DataFrame

            ordem_lista_jogos_casa = ['time', 'primeiro_tempo', 'placar_final', 'time_adversario', 'resultado']
            df_resultados = df_resultados[ordem_lista_jogos_casa]
            #df_resultados.to_excel('Ultimas5_Casa.xlsx', index=None)
            #df_resultados.to_csv(f'ultimas_cinco_casa.csv', encoding='utf-8', sep=',', index=None)
            
            # df_nova['time'] = df_nova['time'].str.replace(' ', '').str.replace('FC', '')
            # df_nova['media_de_gols_por_jogo'] = df_nova['media_de_gols_por_jogo'].apply(lambda x: str(x).replace('.', ','))
            # df_nova.drop(columns=['ultimas_5', 'Limpeza'], inplace=True)
            # df_nova.to_excel(f'tabela_premier_casa.xlsx', index=None)


            return df_resultados

        def jogos_fora(df):
            
            #df =  pd.read_excel(r'tabela_premier_fora.xlsx')
            df_nova = df.copy()

            premier_league = ['Premier League']
            for i in range(20):
                df_nova['Limpeza'] = df['ultimas_5'].replace(premier_league, ' ', regex=True)

            times_fora = []
            jogos_fora = []
            #resultado_partida_fora = []

            for j in range(20):
                time = df_nova['time'][j].replace('FC', '').replace(' ', '')
                times_fora.append(time)
                jogos_fora.append(df_nova['Limpeza'][j][1:].replace(' ', ''))
                #resultado_partida_fora.append(df_nova['Limpeza'][j][:1])

            jogos_fora_de_casa = {'time' : times_fora, 'jogo_fora_de_casa' : jogos_fora}
            df_jogos_fora = pd.DataFrame(jogos_fora_de_casa)

            # Fazer a Limpeza dos Dados e exportar um DataFrame completo

            lista_valores_resultado = ['W', 'D', 'L']
            times_totais_ultimas_5 = []

            for k in range(20):
                time = df_nova['time'][k].replace('FC', '').replace(' ', '')
                for l in range(3):
                    resultado_final = lista_valores_resultado[l]
                    time_novo = f'{time}{resultado_final}'
                    times_totais_ultimas_5.append(time_novo)

            df_jogos_fora['jogo_fora_de_casa'] = df_jogos_fora['jogo_fora_de_casa'].replace(times_totais_ultimas_5, '', regex=True)

            # * Trecho dedicado a buscar uma solução melhor, mas como estou apenas testando, isso vai funcionar * #
            # Gambiarras
            times_gambiarreiros = ['AFCBournemouthD', 'AFCBournemouthW', 'AFCBournemouthL']
            df_jogos_fora['jogo_fora_de_casa'] = df_jogos_fora['jogo_fora_de_casa'].replace(times_gambiarreiros, '', regex=True)
            df_jogos_fora['jogo_fora_de_casa'] = df_jogos_fora['jogo_fora_de_casa'].apply(lambda x : x.split(')'))
            # Gambiarras FIM
        
            # Evidenciar as informações para tratá-las individualmente
            lista_time = []
            lista_resultados = []

            for m in range(20):
                time = df_nova['time'][m].replace('FC', '').replace(' ', '')
                for n in range(5):
                    lista_time.append(time)
                    lista_resultados.append(df_jogos_fora['jogo_fora_de_casa'][m][n])

            resultados_premier_fora = {'time':lista_time, 'resultado_fora' : lista_resultados}
            df_resultados = pd.DataFrame(resultados_premier_fora)

            # Separar os Times Adversários e o Resultado
            df_resultados['time_adversario'] = df_resultados['resultado_fora'].apply(lambda x: re.search('[A-Za-z]+', x).group())
            #df_resultados['resultado_fora'] =df_resultados['resultado_fora'].apply(lambda x: re.search('[0-9]+-[0-9]+', x).group())
            # Tratar os dados e inserir mais informações no DataFrame
            df_resultados[['placar_final', 'primeiro_tempo']] = df_resultados['resultado_fora'].str.extract(r'(\d+-\d+)FT\(HT:(\d+-\d+)')

            df_resultados.drop(columns=['resultado_fora'], inplace=True)

            resultado_da_partida_fora_de_casa = []
            lista_time_visitante = []

            for o in range(len(df_resultados['time'])):

                if int(df_resultados['placar_final'][o][0]) > int(df_resultados['placar_final'][o][2]):
                    resultado_da_partida_fora_de_casa.append('D')

                elif int(df_resultados['placar_final'][o][0]) < int(df_resultados['placar_final'][o][2]):
                    resultado_da_partida_fora_de_casa.append('V')
                else:
                    resultado_da_partida_fora_de_casa.append('E')


            partidas_premier_fora = {'resultado' : resultado_da_partida_fora_de_casa}
            df_partidas = pd.DataFrame(partidas_premier_fora)
            df_resultados = pd.merge(df_partidas, df_resultados, left_index=True, right_index=True)

            # Reordenar as colunas do DataFrame

            ordem_lista_jogos_fora = ['time_adversario', 'primeiro_tempo', 'placar_final', 'time', 'resultado']
            df_resultados = df_resultados[ordem_lista_jogos_fora]
            #df_resultados.to_excel('Ultimas5_Fora.xlsx', index=None)
            #df_resultados.to_csv(f'ultimas_cinco_fora.csv', encoding='utf-8', sep=',', index=None)
            
            # df_nova['time'] = df_nova['time'].str.replace(' ', '').str.replace('FC', '')
            # df_nova['media_de_gols_por_jogo'] = df_nova['media_de_gols_por_jogo'].apply(lambda x: str(x).replace('.', ','))
            # df_nova.drop(columns=['ultimas_5', 'Limpeza'], inplace=True)
            # df_nova.to_excel(f'tabela_premier_fora.xlsx', index=None)
            
            return df_resultados

        def atualizar_banco_de_dados(tabela, nome_da_tabela):

            engine = create_engine('postgresql+psycopg2://postgres:vgmeloalves@localhost/Futebol')
            tabela.to_sql(nome_da_tabela, con=engine, if_exists='replace', index=False)

            return print(f'{nome_da_tabela} atualizado')

        ##################### HOME & AWAY #####################
        # Tabelas Casa
        tabela = buscar_tabelas(primeira_tabela, casa)

        df = tabela.copy()
        df.drop(columns={'ultimas_5'}, inplace=True)
        atualizar_banco_de_dados(df, 'premier_league_casa')

        ultimas_cinco_casa = jogos_casa(tabela)
        atualizar_banco_de_dados(ultimas_cinco_casa, 'ultimas_cinco_casa')

        # Tabelas Fora
        tabela = buscar_tabelas(segunda_tabela, fora)

        df = tabela.copy()
        df.drop(columns={'ultimas_5'}, inplace=True)
        atualizar_banco_de_dados(df, 'premier_league_fora')

        ultimas_cinco_fora = jogos_fora(tabela)
        atualizar_banco_de_dados(ultimas_cinco_fora, 'ultimas_cinco_fora')

        ##################### GERAL #####################

        tabela = premier_league.premier_geral()
        atualizar_banco_de_dados(tabela, 'premier_league')
    else:
        print('Nenhuma tabela foi encontrada... ')

else:
    print(f'Erro ao acessar a página. Código de status: {response.status_code}')