"""
Copyright (c) 2021 JailsonPanizzon, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Jailson Panizzon
"""

import random
import string

# Algoritmo de Hill Climb, a função objetivo está implementada para encontrar uma String
# Altere a string objetivo para uma outra string


def gerar_solucao(length = 10):
    return [random.choice(string.printable)  for _ in range(length)]

def expandir_vizinhanca(solucao):
    index = random.randint(0,len(solucao)-1)
    solucao[index] = random.choice(string.printable)
    return solucao

def funcao_ojetivo(solucao):
    
    objetivo= list("HelloWorld")
    valor_fit = 0
    for i, s in enumerate(objetivo):
        valor_fit += abs(ord(s) - ord(solucao[i]))
    return valor_fit

best = gerar_solucao()
best_score = funcao_ojetivo(best)
iteracao = 0

while True:
    iteracao += 1
    if best_score == 0:
        break
    nova_solucao = list(best)
    expandir_vizinhanca(nova_solucao)
    score = funcao_ojetivo(nova_solucao)
    if funcao_ojetivo(nova_solucao)< best_score:
        best = nova_solucao
        best_score = score
        print("".join(best))
        print(iteracao)