import pandas as pd;
import urllib3;
from bs4 import BeautifulSoup

http  = urllib3.PoolManager()

Valor = []
TipoAluguel = []
Condominio = []

for page in range(1,5):

    url = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/?__vt=gv:b&pagina='+str(page)+'#onde=BR-Santa_Catarina-NULL-Florianopolis'

    page = http.urlopen('GET',url)

    soup = BeautifulSoup(page.data.decode('utf-8'),"html.parser")

    alugueis = soup.find_all('article', {'class': 'property-card__container js-property-card'})

    for row in alugueis:

        valor = row.find("div", "property-card__price js-property-card-prices js-property-card__price-small")

        TipoAluguel.append(valor.find('span').text.replace('/',''))

        valor.find('span').decompose()

        Valor.append(valor.text.replace(' ','').replace('R$',''))

        condominioFind = row.find('strong', 'js-condo-price')

        if(condominioFind):
            Condominio.append(condominioFind.text.replace('R$',''))
        else :
            Condominio.append(0)

df=pd.DataFrame(Valor,columns=['Valor'])


df['TipoAluguel'] = TipoAluguel
df['Condominio'] = Condominio

df.to_csv('./result.csv', index=False)