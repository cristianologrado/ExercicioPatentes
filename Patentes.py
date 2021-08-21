
#import libraries

import os
import requests
import urllib.request
# from bs4 import BeautifulSoup as BS
import pandas as pd


#extrai a lista de anos para os quais ha pantentes, a partir da lista de heads nivel 3
def capturar_anos(links_param):
    anos = []
    for l in links_param:
        ano = int(l.get_text())
        anos.append(ano)
    anos.sort()
    return anos

# contar o total de patentes em cada ano
def contar_patentes(anos_param, links_arquivos_param):
    patentes = pd.DataFrame(columns=['ano', 'quantidade'])
    patentes['ano'] = anos_param
    patentes['quantidade'] = 0
    patentes.set_index('ano', inplace=True)

    for link in links_arquivos_param:
        aux = int(link.split('/')[5])
        patentes.loc[aux, 'quantidade'] = patentes.loc[aux, 'quantidade'] + 1

    return patentes


def baixararquivos(diretorio_param,links_param,totalpatentes_param):
    count = 0
    #loop para todos os links
    for l in links_param:
        name = str(l.split('/')[-1])
        name = f'{diretorio_param}/{name}'
        count = count+1
        if not os.path.exists(name):
            print('nome :', name, ' numero :', count, 'total :', totalpatentes_param,' novo')
            r = requests.get(l)
            with open(name, 'wb') as handler:
                handler.write(r.content)
        else:
            print('nome :',name,' numero :', count, 'total :', totalpatentes_param,' existente')


def capturardetalhes(links_param, arquivo_param):

    ListaArquivos = pd.DataFrame(columns=['ano', 'link', 'arquivo', 'tamanho'])
    cont = 0

    for l in links_param:
        aux = l.split('/')
        ListaArquivos.loc[cont, 'ano'] = int(aux[5])
        ListaArquivos.loc[cont, 'link'] = l
        ListaArquivos.loc[cont, 'arquivo'] = str(aux[6])
        with urllib.request.urlopen(l) as handler:
            ListaArquivos.loc[cont, 'tamanho'] = int(handler.getheader('Content-Length'))
        cont = cont + 1
        print('contagem ', cont)

    ListaArquivos.to_csv(arquivo_param,sep=';')
    return ListaArquivos

