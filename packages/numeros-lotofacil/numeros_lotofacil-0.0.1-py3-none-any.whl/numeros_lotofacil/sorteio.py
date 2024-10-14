from random import sample
from time import sleep

def sorteio_numeros():
    print('--' * 20)
    print(f'{'LOTOFÁCIL':^40}')
    print('--' * 20)
    jogo =[]
    qtde = int(input('Quantos jogos você quer sortear? '))
    aposta = int(input('Quantos números você quer sortear (15, 16 ou 17)? '))
    print(f'{f' Sorteando {qtde} jogos ':=^40}')
    for j in range(0, qtde):
        numeros = sample(range(1, 26), aposta)
        sleep(1)
        jogo.append(numeros)
        jogo[j].sort()
        print(f'Jogo {j + 1}: {jogo[j]}')

