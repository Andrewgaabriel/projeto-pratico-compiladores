import sys
import pandas as pd

entrada = list(open("inputs/entrada.txt"))
codigo = list(open("inputs/codigo.txt"))

simbolos, estados_finais, estados, alcancaveis, estados_vivos = [], [], [], [], []
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
        for derivacao in gramatica[estado]:
            if len(derivacao) == 1 and derivacao.islower() and estado not in estados_finais:
                estados_finais.append(estado)
            elif derivacao == '*' and estado not in estados_finais:
                estados_finais.append(estado)
            elif derivacao[0] == '<':
                afnd[estado]['*'].append(derivacao.split('<')[1][:-1])
            elif derivacao != '*':
                afnd[estado][derivacao[0]].append(derivacao.split('<')[1][:-1])



def find_eps(estado_transicoes):
    for x in estado_transicoes:
        for y in afnd[x]['*']:
            if y not in estado_transicoes:
                estado_transicoes.append(y)
    return estado_transicoes


def eliminar_epsilon_transicoes():
    for regra in afnd:
        et_set = find_eps(afnd[regra]['*'])
        for state in et_set:
            if state in estados_finais:
                estados_finais.append(regra)
            for simbolo in afnd[state]:
                for transicao in afnd[state][simbolo]:
                    if transicao not in afnd[regra][simbolo]:
                        afnd[regra][simbolo].append(transicao)
        afnd[regra]['*'] = []
            
    
def determinizacao():
    newEstado = []
    for regra in afnd:
        for derivacao in afnd[regra]:
            if len(afnd[regra][derivacao]) > 1:
                new = []
                for state in afnd[regra][derivacao]:
                    if ':' in state:
                        for aux in state.split(':'):
                            if aux not in new:
                                new.append(aux)
                    else:
                        if state not in new:
                            new.append(state)
                if new:
                    new = sorted(new)
                    new = ':'.join(new)

                if new and new not in newEstado and new not in list(afnd.keys()):
                    newEstado.append(new)
                afnd[regra][derivacao] = new.split()
    if newEstado:
        novoEstado(newEstado)


def novoEstado(newState):
    for x in newState:
        afnd[x] = {}
        estados.append(x)
        for y in simbolos:
            afnd[x][y] = []
        afnd[x]['*'] = []
    
    for round in newState:
        agroup = sorted(round.split(':'))
        for x in agroup:
            if x in estados_finais and round not in estados_finais:
                estados_finais.append(round)
            for simbolo in simbolos:
                for transicao in afnd[x][simbolo]:
                    if not afnd[round][simbolo].__contains__(transicao):
                        afnd[round][simbolo].append(transicao)
    determinizacao()
    
    
def find_alcancaveis(estado):
    if estado not in alcancaveis:
        alcancaveis.append(estado)
        for s in afnd[estado]:
            if afnd[estado][s] \
                    and afnd[estado][s][0] not in alcancaveis:
                find_alcancaveis(afnd[estado][s][0])  


def eliminar_estados_inalcancaveis():
    find_alcancaveis('S')
    aux = {}
    aux.update(afnd)
    for regra in aux:
        if regra not in alcancaveis:
            del afnd[regra]



def adiciona_estado_erro():
    afnd['ERRO'] = {}
    for s in simbolos:
        afnd['ERRO'][s] = []
    afnd['ERRO']['*'] = []
    for regra in afnd:
        for s in simbolos:
            if not afnd[regra][s]:
                afnd[regra][s] = ['ERRO']
                
                
                
                
                
def buscar_vivos():
    change = False
    
    for regra in afnd:
        for s in afnd[regra]:
            if afnd[regra][s][0] in estados_vivos and regra not in estados_vivos:
                estados_vivos.append(regra)
                change = True
    if change:
        buscar_vivos()
                
                
                
def elimina_mortos():
    estados_vivos.extend(estados_finais)
    buscar_vivos()
    dead = []
    for regra in afnd:
        if regra not in estados_vivos and regra != 'ERRO':
            dead.append(regra)
    
    for regra in dead:
        del afnd[regra]
    
    
def print_af():
    dataframe = pd.DataFrame(afnd)
    dataframe = dataframe.T
    print(dataframe)
                

def main():
    gramatica['S'] = []
    tratar_entrada(entrada)
    
    criar_afnd()
    
    print('----------AFND CRIADO--------------')    
    print_af()
    
    eliminar_epsilon_transicoes()
    
    print('----------EPSILON TRANSICOES ELIMINADAS--------------')
    print_af()
    
    determinizacao()
    
    print('------------DETERMINIZADO------------')
    print_af()
    
    eliminar_estados_inalcancaveis()
    
    print('------------ELIMINOU INALCANCAVEIS------------')
    print_af()
    
    adiciona_estado_erro()
    
    print('------------ADICIONOU ESTADO DE ERRO------------')
    print_af()
    
    elimina_mortos() 
    
    print('------------ELIMINOU MORTOS------------')
    print_af()
    
    afd = pd.DataFrame(afnd)
    afd = afd.T
    afd.to_csv('outputs/afd.csv', index=True, header=True)
    
    
if __name__ == '__main__':
    main()
    # TODO:
    # 1. Finalizar a implementação do analisador léxico
    # 2. Implementar o analisador sintático (em outro arquivo)
