import pandas as pd;

dataFrame = pd.read_csv('alugueis.csv')

def cleanEndereco(cidade, endereco):
    enderecoWithouSc = endereco.replace('SC','')

    if cidade in endereco:
        return endereco
    
    endereco = endereco+', '+cidade

    return endereco

dataFrame['Endereco'] =  dataFrame.apply(lambda x: cleanEndereco(x.Cidade, x.Endereco), axis=1)

dataFrame.to_csv('./alugueis.csv', index=False)