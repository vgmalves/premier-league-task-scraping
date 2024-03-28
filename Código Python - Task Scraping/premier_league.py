import requests
from bs4 import BeautifulSoup
import pandas as pd


def premier_geral():

    url_tabela_geral = 'https://footystats.org/england/premier-league'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url_tabela_geral, headers=headers)


    if response.status_code == 200:
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')

        # Definir o valor máximo da tabela a utilizar no looping

        valor_máximo = soup.find_all('td', class_='position bold zone zone-1')
        for i in valor_máximo:
            maximo = i.text.strip()
        maximo = int(maximo)


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
        # acima_de_1_5_gols = []
        # acima_de_2_5_gols = []
        media_total_de_gols_por_jogo = []
        prob_v = []
        prob_d = []
        prob_e = []
        posicao = []

        # Salvando as informações da tabela GERAL em listas
        for j in range(maximo):

            nome_dos_times = soup.find_all('td', class_='team borderRightContent')
            partidas_dos_times = soup.find_all('td', class_='mp')
            vitorias_dos_times = soup.find_all('td', class_='win')
            empates_dos_times = soup.find_all('td', class_='draw')
            derrotas_dos_times = soup.find_all('td', class_='loss')
            gols_feitos_dos_times = soup.find_all('td', class_='gf')
            gols_sofridos_dos_times = soup.find_all('td', class_='ga')
            saldo_de_gols_dos_times = soup.find_all('td', class_='gd')
            pontos_dos_times = soup.find_all('td', class_='points bold')
            ultimas_cinco_dos_times = soup.find_all('td', class_='form')
            jogos_sem_levar_gols_dos_times = soup.find_all('td', class_='cs')
            jogos_ambas_marcam_dos_times = soup.find_all('td', class_='btts')
            gols_por_jogo_dos_times = soup.find_all('td', class_='avg bold')

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

        return df_nova
    
    else:
        print(f'Erro ao acessar a página. Código de status: {response.status_code}')

#premier_geral()