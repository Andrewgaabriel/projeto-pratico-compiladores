import sys 
import pandas as pd

codigoFonte = list(open(sys.argv[1]))
afd = pd.read_csv(sys.argv[2], sep=",", index_col=0)

tabelaSimbolos, estadosFinais, fitaSaida, alcancaveis = [], [], [], []

separadores = [' ', '\n', '\t', '+', '-', '{', '}', '=', '.']
espacos = [' ', '\n', '\t']
operadores = ['+', '-', '=', '.']







def determina_estados_finais():
    """ Adiciona os estados finais no vetor estadosFinais """
    for index, row in afd.iterrows():
        if '*' in index:
            index = index.replace('*', '')
            estadosFinais.append(index)
            
        



def remove_nomenclatura_estados_finais():
    for idx in afd.index:
        if '*' in idx or idx == '->S':
            afd.rename(index = { idx: idx.replace('*', '').replace('->', '') }, inplace = True)




def determina_estados_alcancaveis(estado):
    if estado not in alcancaveis:
        alcancaveis.append(estado)
        for col in afd.loc[estado]:
            if col not in alcancaveis:
                determina_estados_alcancaveis(col)
                




def remove_estados_inalcancaveis():
    for idx in afd.index:
        if idx not in alcancaveis:
            afd.drop(idx, inplace = True)
            if idx in estadosFinais:
                estadosFinais.remove(idx)








def corrige_estados():
    """ Corrige os estados que na verdade  são estados finais """
    
    to_rename = []
    for estadoAtual, row in afd.iterrows():
        for col in row:
            if col in estadosFinais: # quer dizer que o estado atual é final
                if estadoAtual not in to_rename and estadoAtual.replace('*', '') not in estadosFinais and estadoAtual != 'S':
                    to_rename.append(estadoAtual)
                    estadosFinais.append(estadoAtual)
    print("To RENAME:  \n", to_rename)

        







def analisador_lexico():
    for index, linha in enumerate(codigoFonte):
        for i, char in enumerate(linha):
            if char in separadores:
                if char in espacos:
                    pass
                elif char in operadores:
                    tabelaSimbolos.append([char, 'operador', index, i])
                else:
                    tabelaSimbolos.append([char, 'separador', index, i])
            else:
                pass
    





# print(codigoFonte)
# print(afd)

# Teste acessando o dicionario
# print(afd['a']['->S'])
# Modelo: afd[<token>][<estadoAtual>] = <estadoSeguinte>

# Teste acessando o dataframe
# print(afd.loc['->S', 'a'])
# Modelo: afd.loc[<estadoAtual>, <token>] = <estadoSeguinte>





def main():
    """  """
    
    # print(afd)
    # afd = afd.rename(index = { '->S': 'S' })
    # print(afd)
    
    print("Estados Finais: ", estadosFinais)
    determina_estados_finais()
    print("Estados Finais: ", estadosFinais)
    
    remove_nomenclatura_estados_finais()
    
    print("Alcancaveis: ", alcancaveis)
    determina_estados_alcancaveis('S')
    print("Alcancaveis: ", alcancaveis)
    
    print(afd)
    remove_estados_inalcancaveis()
    print("Removidos: \n\n\n", afd)
    
    # print(afd)
    # corrige_estados()
    # print(afd)
    print("Estados Finais: ", estadosFinais)

    
    
    
    
if __name__ == "__main__":
    main()