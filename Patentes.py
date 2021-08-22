
# import libraries
import os
import requests
import urllib.request
import pandas as pd


# extrai a lista de anos para os quais ha pantentes, a partir da lista de heads nivel 3
def capturar_anos(heads_param):
    anos = []
    for head in heads_param:
        ano = int(head.get_text())
        anos.append(ano)
    anos.sort()
    return anos


def contar_patentes(anos_param, links_arquivos_param):
    # contar o total de patentes em cada ano
    patentes = pd.DataFrame(columns=['ano', 'quantidade'])
    patentes['ano'] = anos_param
    patentes['quantidade'] = 0
    patentes.set_index('ano', inplace=True)
    for link in links_arquivos_param:
        aux = int(link.split('/')[5])
        patentes.loc[aux, 'quantidade'] = patentes.loc[aux, 'quantidade'] + 1
    return patentes


def baixararquivos(diretorio_param, links_param, totalpatentes_param):
    count = 0
    # loop para todos os links
    for link in links_param:
        name = str(link.split('/')[-1])
        name = f'{diretorio_param}/{name}'
        count = count+1
        if not os.path.exists(name):
            print('nome :', name, ' numero :', count, 'total :', totalpatentes_param, ' novo')
            r = requests.get(link)
            with open(name, 'wb') as handler:
                handler.write(r.content)
        else:
            print('nome :', name, ' numero :', count, 'total :', totalpatentes_param, ' existente')


def capturardetalhes(links_param, arquivo_param):
    # se o arquivo de dados ainda não existe, gera os dados e cria o arquivo
    if not os.path.exists(arquivo_param):
        listaarquivos = pd.DataFrame(columns=['ano', 'link', 'arquivo', 'tamanho'])
        cont = 0
        for link in links_param:
            aux = link.split('/')
            listaarquivos.loc[cont, 'ano'] = int(aux[5])
            listaarquivos.loc[cont, 'link'] = link
            listaarquivos.loc[cont, 'arquivo'] = str(aux[6])
            with urllib.request.urlopen(link) as handler:
                listaarquivos.loc[cont, 'tamanho'] = int(handler.getheader('Content-Length'))
                cont = cont + 1
                print('contagem de links lidos : ', cont)
        listaarquivos.to_csv(arquivo_param, sep=';')
    # se o arquivo ja existe, faz a leitura e retorna o dataframe lido
    else:
        print('Arquivo já existe na pasta / arquivo existente retorna como resultado')
        listaarquivos = pd.read_csv(arquivo_param, sep=';')

    return listaarquivos
