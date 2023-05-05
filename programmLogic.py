from collections import defaultdict

import torch


def build_bigram(filename):
        # читаем переданный файл с именами и создаем биграммы 
        with open(filename ,"r")as file:
                names =[line.strip() for line in file] 

        all_bigrams = defaultdict(int)
        for name in names:
                name = "^"+name+"$"
                for i in range(len(name)-1):
                    bigram = name[i:i+2]
                    all_bigrams[bigram] +=1
        total_bigrams = sum(all_bigrams.values())
        current_bigram_list = {bigram: count/total_bigrams for bigram, count in all_bigrams.items()}

        return current_bigram_list

def create_new_name(all_bigrams):
    name = ""
    current_letter = "^"
    bigram_probabilities_list = {}
    
    # логика для нового имени
    while current_letter != '$':

        possible_bigrams = [bigram for bigram in all_bigrams.keys() if bigram.startswith(current_letter)]
        probabilities = torch.Tensor([all_bigrams[bigram] for bigram in possible_bigrams])
        probabilities /= probabilities.sum()

        idx = torch.multinomial(probabilities, 1)[0]
        next_bigram = possible_bigrams[idx]
        bigram_probabilities_list[next_bigram] = all_bigrams[next_bigram]
        name += str(next_bigram[1])
        current_letter = str(next_bigram[1])

    # все биграммы записываю в "bigram_probabilities_list", а также записываю полностью имя
    bigram_probabilities_list['current_name']= name[:-1]  

    return bigram_probabilities_list





