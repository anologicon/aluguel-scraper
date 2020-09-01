import pandas as pd;
import numpy as np;

dataFrame = pd.read_csv('alugueis.csv')
dfBairros = pd.read_json('Bairro.json')

dataFrame = dataFrame[dataFrame['Endereco'].notna()]

cidades = dataFrame.Cidade.unique()

bairros = list(dfBairros['Bairro'])
cidades =  list(cidades)

cidades.append('Balneário')

def cleanEndereco(cidade, endereco):
    enderecoWithouSc = endereco.replace('SC','')
    
    for cidadeList in cidades:
        if cidadeList in endereco:
            if cidadeList != cidade:
                endereco = np.nan
                return endereco
            endereco = endereco.replace(cidadeList, '')
    
    if cidade in endereco:
        return endereco
    
    endereco = endereco+' '+cidade

    return endereco

def setBairro(endereco):
    for bairro in bairros:
        if endereco is not np.nan:
            if bairro in endereco:
                bairro = bairro.replace(' ', '')
                return bairro
            
    return np.nan

dataFrame['Endereco'] =  dataFrame.apply(lambda x: cleanEndereco(x.Cidade, x.Endereco), axis=1)
dataFrame['Bairro'] =  dataFrame.apply(lambda x: setBairro(x.Endereco), axis=1)

dataFrame = dataFrame[(dataFrame['Bairro'].notna()) & (dataFrame['Endereco'].notna())]

dataFrame['EnderecoFormatado'] = dataFrame.apply(lambda x: x.Bairro+', '+x.Cidade, axis=1)

dataFrame.to_csv('./alugueisFormatados.csv', index=False)