
# MBA Big Data, Business Analytics e gestão de negocios
# IDP

# Técnicas Avançadas de Captura e Tratamento de Dados
# Prof. Bernardo Alves Furtado¶

# Aluno:  Cristiano Logrado

# Exercicio de Captura Massiva de Dados
# Informação de patentes registradas nos Estados Unidos de 2015 a 1976


# Importacao de Bibliotecas

import os
import requests
import urllib.request
from bs4 import BeautifulSoup as BS
import pandas as pd
import Patentes

if __name__ == '__main__':

    url_base = 'http://storage.googleapis.com/'
    url_in = 'https://www.google.com/googlebooks/uspto-patents-grants-text.html'
    diretorio_arquivos = 'data'

# leitura do htmls da paginas
    response = urllib.request.urlopen(url_in)
    html_in = BS(response)

    anos = Patentes.capturar_anos(html_in.find_all('h3'))

# importando os links
links1 = html_in.find_all('a', href=True)

#filtrando links para os arquivos zip
links2 = [l.get('href') for l in links1 if 'http://storage.googleapis.com/patents/grant_full_text' in l.get('href')]

contagempatentes = Patentes.contar_patentes(anos,links2)

# salvando o total de patentes de cada ano
contagempatentes.to_csv('contagem_patentes.csv',sep=';')

# grafico com total de patentes por ano
#contagempatentes.plot(kind='bar',figsize=(15,6),xlabel='ano',ylabel='quantidade patantes no ano')

#criar pasta para salvar arquivos de dados das patentes
if not os.path.exists(diretorio_arquivos):
    os.mkdir(diretorio_arquivos)

Patentes.baixararquivos(diretorio_arquivos, links2[0:25], contagempatentes['quantidade'].sum())

detalhes_por_ano = Patentes.capturardetalhes(links2,'detalhes_por_ano.csv')