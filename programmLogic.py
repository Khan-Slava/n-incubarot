from collections import defaultdict
import random
import numpy as np
import torch


def build_bigram(filename):

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

    while current_letter != '$':
        # possible_bigrams = [bigram for bigram in all_bigrams.keys() if bigram.startswith(current_letter)]
        # next_bigram = np.random.choice(possible_bigrams)
        # bigram_probabilities_list[next_bigram] = all_bigrams[next_bigram]
        # name += str(next_bigram[1])
        # current_letter = str(next_bigram[1])


        # 
        possible_bigrams = [bigram for bigram in all_bigrams.keys() if bigram.startswith(current_letter)]
        probabilities = torch.Tensor([all_bigrams[bigram] for bigram in possible_bigrams])
        probabilities /= probabilities.sum()

        idx = torch.multinomial(probabilities, 1)[0]
        next_bigram = possible_bigrams[idx]
        bigram_probabilities_list[next_bigram] = all_bigrams[next_bigram]
        name += str(next_bigram[1])
        current_letter = str(next_bigram[1])



    bigram_probabilities_list['current_name']= name[:-1]  

    return bigram_probabilities_list




# test = defaultdict(int)
# test["^s"]=1
# test["sl"]=1
# test["la"]=1
# test["^v"]=1
# test["va"]=1
# test["a$"]=1 


# name = ""
# current_letter = "^"

# while current_letter != '$':
#         possible_bigrams = [bigram for bigram in test.keys() if bigram.startswith(current_letter)]
#         bigram_probabilities_list = [test[bigram] for bigram in possible_bigrams]
#         next_bigram = np.random.choice(possible_bigrams)
#         print(next_bigram)
#         name += str(next_bigram[1])
#         current_letter = str(next_bigram[1])

# print(name)


