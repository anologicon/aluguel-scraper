import pandas as pd;
import numpy as np;

dataFrame = pd.read_csv('alugueis.csv')

dataFrame = dataFrame[dataFrame['Endereco'].notna()]

cidades = dataFrame.Cidade.unique()

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

dataFrame['Endereco'] =  dataFrame.apply(lambda x: cleanEndereco(x.Cidade, x.Endereco), axis=1)

dataFrame = dataFrame[dataFrame['Endereco'].notna()]

dataFrame.to_csv('./alugueisFormatados.csv', index=False)