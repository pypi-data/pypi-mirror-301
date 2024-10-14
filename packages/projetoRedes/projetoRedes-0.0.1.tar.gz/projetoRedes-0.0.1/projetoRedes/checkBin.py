import random

def compDeUm(somaDosBins):
    retorno = []
    for i in range(15, -1, -1):
        if somaDosBins[i] == '0':
            retorno.insert(0, '1')
        else:
            retorno.insert(0, '0')

    return retorno


def somaBinario(binario1, binario2):
    retorno = []
    aux = "0"
    print(binario1, '\n', binario2, '\n')
    for a in range(15, -1, -1):
        if(aux == "0"):
            if(binario1[a] == '1' and  binario2[a] == '1'):
                retorno.insert(0, '0')
                aux = '1'
            elif(binario1[a] == '1' or  binario2[a] == '1'):
                retorno.insert(0, '1')
            else:
                retorno.insert(0, '0')

        else:
            if(binario1[a] == '1' and  binario2[a] == '1'):
                aux = "1"
                retorno.insert(0, '1')
            elif(binario1[a] == '1' or  binario2[a] == '1'):
                aux = "1"
                retorno.insert(0, '0')
            else:
                aux = "0"
                retorno.insert(0, '1')
    
    if aux == "1":
        aux = ["1"]
        verificaBits(aux)
        retorno = somaBinario(retorno, aux)

    return retorno
'''..........................................................................................'''


def verificaBits(binario):
    while(len(binario) != 16):
        binario.insert(0, '0')
    
    return binario
'''..........................................................................................'''


def geraBins(quantNum):
    if quantNum < 2:
        return False
    
    matrizDeBinarios = [quantNum]
    #print('Valores binários:')
    ################################################################################################
    #For para gerar os binários de 16 bits:
    for i in range(0, quantNum, 1):
        #decimal aleatório que convertendo em binário fica no máximo 16 bits (2^16 - 1):
        decimal = random.randint(0, 1000000) % 65536
        
        #Transformando a string em binário para remover o '0b'
        binario = list(bin(decimal))

        del binario[0]
        del binario[0]

        #Acrescenta a quantidade de bits que falta, preservando o valor decimal convertido
        binario = verificaBits(binario)

        #adicionando o binário na matriz
        matrizDeBinarios.append(binario)
        print(binario, decimal)
        ################################################################################################
    
    del matrizDeBinarios[0]
    return matrizDeBinarios
'''..........................................................................................'''

################################################################################################


#print('\n\nPares somados:')
#While para fazer a soma de verificação dos bits gerados
def checksum(matrizDeBinarios):
    while(len(matrizDeBinarios) != 1):
        novoValor = somaBinario(matrizDeBinarios[0], matrizDeBinarios[1])
        del matrizDeBinarios[0]
        del matrizDeBinarios[0]
        matrizDeBinarios.insert(0, novoValor)

    #print('\n\nResultado da Soma: ', matrizDeBinarios)
    finalSoma = compDeUm(matrizDeBinarios[0])

    #print('\n\n')
    #print('CheckSum: ',finalSoma)
    return finalSoma
