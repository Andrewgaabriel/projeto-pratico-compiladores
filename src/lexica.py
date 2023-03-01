import sys
import pandas as pd

entrada = list(open("inputs/entrada.txt"))

simbolos, estados_finais, estados = [], [], []
gramatica, afnd = {}, {}
gramaticapd = pd.DataFrame()
count = 0



def tratar_entrada(entrada):
    estado_inicial = ''
    for linha in entrada:
        if '<S> ::=' in linha:
            estado_inicial = linha
        if '::=' in linha:
            tratar_gramatica(linha, estado_inicial)
        else:
            tratar_token(linha)





def tratar_gramatica(linha, estado_inicial):
    """ Faz o tratamento da gramatica, criando as regras e adicionando na gramatica """
    global count
    linha = linha.replace('\n', '')
    
    for i in linha.split(' ::= ')[1].replace('<', '').replace('>', '').split(' | '):
        if i[0] not in simbolos and not i[0].isupper():
            simbolos.append(i[0])
    regra = linha.split(' ::= ')[0].replace('<', '').replace('>', str(count))
    
    print("regra: ", regra)
    
    if regra[0] == 'S':
        count += 1        
        gramatica['S'] += linha.split(' ::= ')[1].replace('>', str(count) + '>').split(' | ')
    else:
        gramatica[regra] = linha.split(' ::= ')[1].replace('>', str(count) + '>').split(' | ')

    if '<S>' in linha.split(' ::= ')[1]:
        criar_inicial_alternativo(estado_inicial)    
    
    


def criar_inicial_alternativo(estado_inicial):
    """ Faz a criação de um estado inicial alternativo """
    global count
    if 'S' + str(count) in gramatica:
        return
    gramatica['S' + str(count)] = estado_inicial.replace('\n', '').split(' ::= ')[1].replace('>', str(count) + '>').split(' | ')
    
    
    
    
def tratar_token(linha):
    """ Faz o tratamento dos tokens, adicionando na gramatica """
    
    linha = linha.replace('\n', '')
    aux = linha
    linha = list(linha)
    
    for i in range(len(linha)):
        
        """ Se o simbolo não estiver na lista de simbolos e não for maiusculo, adiciona na lista de simbolos """
        if linha[i] not in simbolos and not linha[i].isupper():
            simbolos.append(linha[i])
            
        """ Se o tamanho do token for 1, adiciona na gramatica e adiciona o estado final na lista de estados finais """
        if len(linha) == 1:
            inicio_regra = '<' + aux.upper() + '>'
            gramatica['S'] += str(linha[i] + inicio_regra).split() # Adiciona na gramatica no estado inicial
            gramatica[aux.upper()] = []
            estados_finais.append(aux.upper())
                
        elif i == 0 and i != len(linha) - 1: # Se for a primeira posição e não for a ultima
            inicio_regra = '<' + aux.upper() + '1>'
            gramatica['S'] += str(linha[i] + inicio_regra).split()
            
        elif i == len(linha) - 1: # Se for a ultima posição
            final_regra = '<' + aux.upper() + '>'
            gramatica[aux.upper() + str(i)] = str(linha[i] + final_regra).split()
            gramatica[aux.upper()] = []
            estados_finais.append(aux.upper())
        
        else: # Se for uma posição intermediaria
            proxima_regra = '<' + aux.upper() + str(i + 1) + '>'
            gramatica[aux.upper() + str(i)] = str(linha[i] + proxima_regra).split()
            


def criar_afnd():
    
    """ Cria a estrutura do AFND """
    for estado in gramatica:
        afnd[estado] = {}
        estados.append(estado)
        for simbolo in simbolos:
            afnd[estado][simbolo] = []
        afnd[estado]['*'] = []
        
    """ Adiciona as transições no AFND """
    for estado in gramatica:
        for regra in gramatica[estado]:
            if len(regra) == 1 and regra.islower() and estado not in estados_finais:
                estados_finais.append(estado)
            elif regra == '*' and estado not in estados_finais:
                estados_finais.append(estado)
            elif regra[0] == '<':
                afnd[estado]['*'].append(regra.split('<')[1][:-1])
            elif regra != '*':
                afnd[estado][regra[0]].append(regra.split('<')[1][:-1])



def find_eps(estado_transicoes):
    for x in estado_transicoes:
        for y in afnd[x]['*']:
            if y not in estado_transicoes:
                estado_transicoes.append(y)
    return estado_transicoes


def eliminar_epsilon_transicoes():
    for regra in afnd:
        et_set = find_eps(afnd[regra]['*'])
        for estado in et_set:
            if estado in estados_finais:
                estados_finais.append(regra)
            for simbolo in afnd[estado]:
                for transicao in afnd[estado][simbolo]:
                    if transicao not in afnd[regra][simbolo]:
                        afnd[regra][simbolo].append(transicao)
        afnd[regra]['*'] = []
            
    

def main():
    gramatica['S'] = []
    tratar_entrada(entrada)
    criar_afnd()
    dataframe = pd.DataFrame(afnd)
    dataframe = dataframe.T
    print(dataframe)
    eliminar_epsilon_transicoes()
    print('------------------------')
    dataframe = pd.DataFrame(afnd)
    dataframe = dataframe.T
    print(dataframe)
    

if __name__ == '__main__':
    main()
