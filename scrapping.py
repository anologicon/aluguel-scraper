import pandas as pd;
import urllib3;
from bs4 import BeautifulSoup

http  = urllib3.PoolManager()

Valor = []
TipoAluguel = []
Condominio = []
Area = []
Quartos = []
Banheiros = []
Vagas = []
Uri = []

def findTextNull(elementFind):
    elementText = elementFind.text

    if "--" in elementText:
        return 0
    
    return elementText

for page in range(1,5):

    url = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/?__vt=gv:b&pagina='+str(page)+'#onde=BR-Santa_Catarina-NULL-Florianopolis'

    page = http.urlopen('GET',url)

    soup = BeautifulSoup(page.data.decode('utf-8'),"html.parser")

    alugueis = soup.find_all('article', {'class': 'property-card__container js-property-card'})

    for row in alugueis:

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

        quartosFind = row.find('span', 'property-card__detail-value js-property-card-value')

        quartosText = findTextNull(quartosFind)

        Quartos.append(quartosText)

        banheirosFind = row.find('span', 'property-card__detail-value js-property-card-value')

        Banheiros.append(findTextNull(banheirosFind))

        vagasFind = row.find('span', 'property-card__detail-value js-property-card-value')
        
        Vagas.append(findTextNull(vagasFind))

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

df.to_csv('./result.csv', index=False)