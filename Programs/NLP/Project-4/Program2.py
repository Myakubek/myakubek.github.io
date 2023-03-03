import pickle
import os
import math
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

'''
Compute probability given text, unigram, bigram, and size of training data
Text - Text to classify, Unigram/Bigram Dict - Dictionaries of trained bigrams, V - Vocab size of training data
(I found That using logs gave a better overall accuracy than Laplace smoothing ~97%->99%)
'''
def compute_prob(text, unigram_dict, bigram_dict, V):
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2)) 
    p_log = 0      
    #p_laplace = 1

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_log = p_log + math.log((n + 1) / (d + V))
        #p_laplace = p_laplace * ((n + 1) / (d + V))
    return (p_log)


# A - Read in pickled dictionaries
englishBigramDict = pickle.load(open('englishBigramDict.p', 'rb')) 
englishUnigramDict = pickle.load(open('frenchUnigramDict.p', 'rb')) 
frenchBigramDict = pickle.load(open('frenchBigramDict.p', 'rb')) 
frenchUnigramDict = pickle.load(open('frenchUnigramDict.p', 'rb')) 
italianBigramDict = pickle.load(open('italianBigramDict.p', 'rb')) 
italianUnigramDict = pickle.load(open('italianUnigramDict.p', 'rb')) 

# B - For each line in test file, calculate a probability for each language and write the language with the highest probability to file.
with open(os.path.join(os.getcwd(), 'data/LangId.test'), 'r', encoding="utf8") as f:
    text_in = f.read().split('\n')

probabilityList = []
count = 0
for line in text_in:
    prob_english = compute_prob(line, englishUnigramDict, englishBigramDict, len(englishUnigramDict))
    prob_french = compute_prob(line, frenchUnigramDict, frenchBigramDict, len(frenchUnigramDict))
    prob_italian = compute_prob(line, italianUnigramDict, italianBigramDict, len(italianUnigramDict))
    
    count += 1
    if (prob_english > prob_french and prob_english > prob_italian):
        probabilityList.append(str(count) + ' English')
        #print(count, ' English')
    elif(prob_french > prob_english and prob_french > prob_italian):
        probabilityList.append(str(count) + ' French')
        #print(count, ' French')
    else:
        probabilityList.append(str(count) + ' Italian')
        #print(count, ' Italian')
        
    


# C - Compute and output your accuracy as a percentage of the correctly classified instances in the test set. (LangId.sol holds correct classifications)
with open(os.path.join(os.getcwd(), 'data/LangId.sol'), 'r', encoding="utf8") as f:
    text_sol = f.read().split('\n')

accurateScores = 0
N = len(probabilityList)
incorrectIndexes = []

for index, solution in enumerate(text_sol):
    #print(solution, ' --- ', probabilityList[index])
    if(solution == probabilityList[index]):
        accurateScores += 1
    else:
        incorrectIndexes.append(index)
        
# D - Output accuracy and nline numbers of the incorrectly classified items
print('Accuracy:', accurateScores / N * 100, '%')
print("Indexes of incorrectly classified items:", incorrectIndexes)