import pandas as pd;
import urllib3;
from bs4 import BeautifulSoup

# Google storage
from google.cloud import storage

# Scrapper 
http  = urllib3.PoolManager()
Valor = []
TipoAluguel = []
Condominio = []
Area = []
Quartos = []
Banheiros = []
Vagas = []
Uri = []
Cidade = []
Endereco = []

def findTextNull(elementFind):
    elementText = elementFind.text

    if "--" in elementText:
        return 0
    
    return elementText

for cidade in ('florianopolis', 'brusque', 'blumenau'):

    for page in range(1,30):

        url = 'https://www.vivareal.com.br/aluguel/santa-catarina/'+cidade+'/?__vt=gv:b&pagina='+str(page)+'tipos=apartamento_residencial,casa_residencial,condominio_residencial,,sobrado_residencial,kitnet_residencial'

        page = http.urlopen('GET',url)

        soup = BeautifulSoup(page.data.decode('utf-8'),"html.parser")

        alugueis = soup.find_all('article', {'class': 'property-card__container js-property-card'})

        for row in alugueis:

            Cidade.append(cidade)

            enderecoFind = row.find('span', 'property-card__address')

            Endereco.append(enderecoFind.text)

            valor = row.find("div", "property-card__price js-property-card-prices js-property-card__price-small")

            TipoAluguel.append(valor.find('span').text.replace('/',''))

            valor.find('span').decompose()

            Valor.append(valor.text
                .replace('.','')
                .replace(' ','')
                .replace('R$','')
                )

            condominioFind = row.find('strong', 'js-condo-price')

            if(condominioFind):
                Condominio.append(condominioFind.text
                    .replace('R$','')
                    .replace('.','')
                    )
            else :
                Condominio.append(0)

            areaFind = row.find('span', 'property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area')

            Area.append(areaFind.text)

            quartosFindLi = row.find_all('li', 'property-card__detail-item property-card__detail-room js-property-detail-rooms')
            
            quartosText = ''

            for quartosFind in quartosFindLi:
                quartosSpan = quartosFind.find('span', 'property-card__detail-value js-property-card-value')
                quartosText = findTextNull(quartosSpan)

            Quartos.append(quartosText)

            banheirosFindLi = row.find_all('li', 'property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom')
            
            banheirosText = ''

            for banheirosFind in banheirosFindLi:
                banheirosSapan = banheirosFind.find('span', 'property-card__detail-value js-property-card-value')
                banheirosText = findTextNull(banheirosSapan)

            Banheiros.append(banheirosText)

            vagasFindLi = row.find_all('li', 'property-card__detail-item property-card__detail-garage js-property-detail-garages')
            
            vagasText = ''

            for vagasFind in vagasFindLi:
                vagasSpan = vagasFind.find('span', 'property-card__detail-value js-property-card-value')
                vagasText = findTextNull(vagasSpan)
            
            Vagas.append(vagasText)

            uriFind = row.find('a', 'property-card__title js-cardLink js-card-title',  href=True)

            Uri.append("https://www.vivareal.com.br/"+uriFind['href'])

df=pd.DataFrame(Valor,columns=['Valor'])

df['TipoAluguel'] = TipoAluguel
df['Condominio'] = Condominio
df['Area'] = Area
df['Quartos'] = Quartos
df['Banheiros'] = Banheiros
df['Vagas'] = Vagas
df['Uri'] = Uri
df['Cidade'] = Cidade
df['Endereco'] = Endereco

# End scrapper
df.to_csv('./aluguel.csv', index=False)

# client = storage.Client()
# bucket = client.bucket('viva-real-alguel')
# blob = bucket.blob('aluguel.csv')
# blob.upload_from_filename('aluguel.csv')
