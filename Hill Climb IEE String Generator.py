"""
Copyright (c) 2021 JailsonPanizzon, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Jailson Panizzon
"""

# Algortimo para busca e geração de string de 
# buscas para artigos no IEEXplore usando HillClimb

# A melhor solução será a que retornar a maior quantidade de 
# artigos usando a combinação dos termos e seus plurais

import random
import string
import urllib.request
import ssl
import json
import inflect

context = ssl._create_unverified_context()
p = inflect.engine()


def generate_solution():
    # A solução é representada por uma matriz onde cada linha representa um termo
    # A primeira posição é o termo
    # As outras posições são os sinonimos
    # Se o valor da matriz em determinada posição for 0 o termo não está na string de busca
    # Se o valor for 1 o termo estará na string da maneira como foi digitado
    # Se o valor for 2 o termo estará entre aspas
    # Se o valor for 3 o termo estará no plural

    # Para a primeira string será composta com os termos principais
    solution = []
    for term in terms:
        line = []
        line.append(1)
        for i, synonym in enumerate(term):
            if i > 0:
                line.append(0)
        solution.append(line)
    return solution

def expand_neighborhood(solution):
    strategy = random.randint(0,2)
    i = random.randint(0,len(solution)-1)
    j = random.randint(0,len(solution[i])-1)
    # Adiciona aspas
    if strategy == 0:
        while solution[i][j] <= 0:
            j = random.randint(0,len(solution[i])-1)
        solution[i][j] = 2
        return solution
    # Adiciona o plural de um termo
    if strategy  == 1:
        while solution[i][j] <= 0:
            j = random.randint(0,len(solution[i])-1)
        solution[i][j] = 1 if solution[i][j] == 2 else 3 
        return solution
    # Adiciona ou remove synonimo
    if strategy == 2:
        solution[i][j] = 0 if solution[i][j] > 0 else 1 
        while 1 not in solution[i] and 2 not in solution[i] and 3 not in solution[i]:
            j = random.randint(0,len(solution[i])-1)
            solution[i][j] = 0 if solution[i][j] > 0 else 1 

        return solution
    
    

def objective_function(solution, search_results):
    valor_fit = 0
    if search_results["total_records"] == 0:
        return 0
    for article in search_results["articles"]:
        title = article["title"]
        abstract = article["abstract"]
        for i, linha in enumerate(solution):
                for j, term in enumerate(linha):
                    if term:
                        valor_fit += count_terms(terms[i][j], title)
                        valor_fit += (count_terms(terms[i][j], abstract) * 2)
    
    return valor_fit

def count_terms(term, text):
    ocurrs = text.lower().count(term.lower())
    return ocurrs

def compose_string(solution):
    # Transforma a matriz em uma string real de acordo com as mudanças feitas na solução
    
    search_string = ''

    for i, linha in enumerate(solution):
        string_part =""
        for j, types in enumerate(linha):
            if types > 0:
                if len(string_part) == 0:
                    string_part = "( " + get_term(terms[i][j],types)
                else:
                    string_part += " OR " + get_term(terms[i][j],types)
        string_part += " )"
        if len(search_string) == 0:
            search_string = string_part
        else:
            search_string += " AND "+ string_part

    return search_string

def get_term(term, types):
    # Tipo 1 representa o termo como foi realizado o input
    if types == 1:
        return term
    # Tipo 2 é o termo entra aspas
    if types == 2:
        return "\"" + term + "\""
    # Tipo 3 é o termo no plural
    if types == 3:
        return p.plural(term)


def get_results(search_string):
    IEEExploreKey = "key"
    parms = urllib.parse.urlencode({"querytext":search_string, "apikey": IEEExploreKey})
    url = "https://ieeexploreapi.ieee.org/api/v1/search/articles?"+parms
    with urllib.request.urlopen(url=url,  context=context) as response:
        data = json.loads(response.read())
        
    return data
    
def init_terms():
    while True:
        val = str(input("Insira o "+ str(len(terms)+1)+ "° termo. Digite 0 para terminar."))
        if val != "0":
            terms.append([str(val)])
        else:
            break

    for i, term in enumerate(terms):
        while True:
            val = str(input("Insira o sinonimo para "+ term[0] + ". Digite 0 para terminar."))
            if val != "0":
                terms[i].append(str(val))
            else:
                break

interactions = 30
terms = []

if __name__ == "__main__":
    init_terms()
    best = generate_solution()
    search_results = get_results(compose_string(best))
    best_score = objective_function(best, search_results)
    interactions_count = 0
    while interactions > 0 :
        interactions_count += 1
        print("\n===================================================")
        print("Interação n° ",interactions_count)
        interactions -= 1
        new_solution = best
        new_solution = expand_neighborhood(new_solution)
        search_results = get_results(compose_string(new_solution))
        score = objective_function(new_solution, search_results)
        print("Avaliando: ", compose_string(new_solution))
        print("Score: ", score)
        if score > best_score:
            best = new_solution
            print("New Best found = ", compose_string(new_solution))
            print("New Best Score = ", score)
            best_score = score
        print("===================================================\n")

    print("Best Solution = ", compose_string(best))
    print("Best Score = ", best_score)
    print("Interactions = ", interactions)
