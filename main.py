# MBA Big Data, Business Analytics e gestão de negocios
# IDP

# Técnicas Avançadas de Captura e Tratamento de Dados
# Prof. Bernardo Alves Furtado¶

# Aluno:  Cristiano Logrado

# Exercicio de Captura Massiva de Dados
# Informação de patentes registradas nos Estados Unidos de 2015 a 1976


# Importacao de Bibliotecas
import os
import urllib.request
from bs4 import BeautifulSoup
import Patentes
import matplotlib.pyplot as plt

if __name__ == '__main__':
    url_base = 'http://storage.googleapis.com/'
    url_in = 'https://www.google.com/googlebooks/uspto-patents-grants-text.html'
    diretorio_arquivos = 'data'

    # leitura do htmls da paginas
    response = urllib.request.urlopen(url_in)
    html_in = BeautifulSoup(response)

    anos = Patentes.capturar_anos(html_in.find_all('h3'))

    # importando os links
    links1 = html_in.find_all('a', href=True)
    # filtrando links para os arquivos zip
    links2 = [link.get('href') for link in links1 if
              'http://storage.googleapis.com/patents/grant_full_text' in link.get('href')]
    contagempatentes = Patentes.contar_patentes(anos, links2)
    # salvando o total de patentes de cada ano
    contagempatentes.to_csv('contagem_patentes.csv', sep=';')
    # criar pasta para salvar arquivos de dados das patentes
    if not os.path.exists(diretorio_arquivos):
        os.mkdir(diretorio_arquivos)
    Patentes.baixararquivos(diretorio_arquivos, links2[0:5], contagempatentes['quantidade'].sum())
    detalhes_por_ano = Patentes.capturardetalhes(links2, 'detalhes_por_ano.csv')

#   totalizando o total de dados em cada ano
    total_ano = detalhes_por_ano[['ano', 'tamanho']].groupby('ano').sum()

#   guardando a informacao no arquivo de contagem de patentes
    contagempatentes['bytes'] = total_ano['tamanho']
    contagempatentes.to_csv('contagem_patentes.csv', sep=';')

# grafico com total de patentes por ano
# excluindo o nao de 2015, que não dispoe de dados completos
    contagempatentes[0:-1].plot(kind='bar', figsize=(15, 6), xlabel='ano', ylabel='bytes', y='bytes',
                          title=' Total de Bytes, por ano')
    plt.show()
