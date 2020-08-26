import pandas as pd;
from random import randint
import urllib3;
from bs4 import BeautifulSoup
import json
import time
from slugify import slugify

# Google storage
from google.cloud import storage

# Scrapper 
http  = urllib3.PoolManager()
Valor = []
TipoAluguel = []
Iptu = []
Area = []
Quartos = []
Banheiros = []
Vagas = []
Uri = []
Cidade = []
Endereco = []
TipoNegociacao = []

def findTextNull(elementFind):
    elementText = elementFind.text

    if "--" in elementText:
        return 0
    
    return elementText

f = open('configs.json',)

configs = json.load(f)

max = len(configs['cidades']) * len(configs['tipoNegociacao']) * configs['qtdPaginas']

loading = 0

print('Iniciando scraping')

for cidade in configs['cidades']:
    print('Cidade - ', cidade)     
    for tipoNegociacao in configs['tipoNegociacao']:
        print('Tipo Negociacao ', tipoNegociacao)
        for page in range(1,configs['qtdPaginas']):
            sleepTime = randint(60,120)
            print('Tempo de espera para a requisicao: '+str(sleepTime))
            time.sleep(sleepTime)
            url = 'https://www.zapimoveis.com.br/aluguel/'+slugify(tipoNegociacao)+'/sc+'+slugify(cidade)+'/?__zt=srl%3Aa&transacao=Aluguel&tipoUnidade=Residencial&tipo=Im%C3%B3vel%20usado&pagina='+str(page)
            print('GET '+url)
            page = http.urlopen('GET',url)
            print('GET  fim')
            soup = BeautifulSoup(page.data.decode('utf-8'),"html.parser")

            alugueis = soup.find_all('div', {'class': 'card-container'})
            
            loading += 1               

            print(str(loading)+' -- requisicoes de -- '+str(max))
            
            for row in alugueis:

                TipoNegociacao.append(tipoNegociacao)

                Cidade.append(cidade)

                enderecoFind = row.find('p', 'color-dark text-regular simple-card__address')

                Endereco.append(enderecoFind.text)

                valor = row.find("p", "simple-card__price js-price heading-regular heading-regular__bolder align-left")

                TipoAluguel.append(valor.find('small').text.replace('/',''))

                valor.find('small').decompose()

                Valor.append(valor.find("strong").text
                    .replace('.','')
                    .replace(' ','')
                    .replace('R$','')
                    )

                iptuFind = row.find('span', 'card-price__value')

                if(iptuFind):
                    Iptu.append(iptuFind.text
                        .replace('R$','')
                        .replace('.','')
                        )
                else :
                    Iptu.append(0)

                areaFindLi = row.find_all('li', {'class': 'feature__item text-small js-areas'})
                
                areaText = 0

                for li in areaFindLi:
                    areaSpanFind = li.find_all('span')[1]
                    areaText = areaSpanFind.text
                    areaText = areaText.replace('m²','').replace(' ', '')

                Area.append(areaText)

                quartosFindLi = row.find_all('li', 'feature__item text-small js-bedrooms')
                
                quartosText = 0

                for li in quartosFindLi:
                    quartosSpanFind = li.find_all('span')[1]
                    quartosText = quartosSpanFind.text
                    quartosText = quartosText.replace(' ', '')

                Quartos.append(quartosText)

                vagasFindLi = row.find_all('li', 'feature__item text-small js-parking-spaces')
                
                vagasText = 0

                for li in vagasFindLi:
                    vagasSpanFind = li.find_all('span')[1]
                    vagasText = vagasSpanFind.text
                    vagasText = vagasText.replace(' ', '')

                Vagas.append(vagasText)

                banheirosFindLi = row.find_all('li', 'feature__item text-small js-bathrooms')
                
                banheirosText = 0

                for li in banheirosFindLi:
                    banheirosSpanFind = li.find_all('span')[1]
                    banheirosText = banheirosSpanFind.text
                    banheirosText = banheirosText.replace(' ', '')

                Banheiros.append(banheirosText)
                
df=pd.DataFrame(Valor,columns=['Valor'])

df['TipoAluguel'] = TipoAluguel
df['Iptu'] = Iptu
df['Area'] = Area
df['Quartos'] = Quartos
df['Banheiros'] = Banheiros
df['Vagas'] = Vagas
df['TipoNegociacao'] = TipoNegociacao
df['Cidade'] = Cidade
df['Endereco'] = Endereco

# End scrapper
df.to_csv('./alugueis.csv', index=False)

# client = storage.Client()
# bucket = client.bucket('aluguel-data-scraper')
# blob = bucket.blob('alugueis.csv')
# blob.upload_from_filename('alugueis.csv')
