import os
import pickle
import sys
import nltk
from nltk import word_tokenize

'''
Function takes a text file stored in data/filename and returns a count of unigram and bigram counts based on the text.
'''
# A - Create a function with a filename as argument
def build_ngram(fileName):
    filePath = 'data/' + fileName
    
    # B - Read in the text and remove newlines
    with open(os.path.join(os.getcwd(), filePath), 'r', encoding="utf8") as f:
        text_in = f.read()

    text_in = text_in.replace('\n', '')
    
    # C - Tokenize the text
    tokens = word_tokenize(text_in)
    
    # D - Use nltk to create a bigrams list
    bigrams = [(tokens[k], tokens[k+1]) for k in range(len(tokens)-1)]
    
    # E - Use nltk to create a unigrams list
    unigrams = tokens
    
    # F - Use the bigram list to create a bigram dictionary of bigrams & counts, ['token1 token2'] -> count
    print("Counting Bigram Dictionary for - ", fileName)
    bigramDict = {b:bigrams.count(b) for b in set(bigrams)}
    
    # G - Use the unigram list to create a unigram dictioanry of unigrams and counts, ['token'] -> count
    print("Counting Unigram Dictionary - ", fileName)
    unigramDict = {t:unigrams.count(t) for t in set(unigrams)}
    
    # H - Return the unigram dictionary and bigram dictionary from the function
    return [bigramDict, unigramDict]
    
if __name__ == '__main__':
    # I - Call the function 3 times for each training file, pickle the 6 dictionaries and save to files with appropriate names.
    englishBigram, englishUnigram = build_ngram("LangId.train.English")
    frenchBigram, frenchUnigram = build_ngram("LangId.train.French")
    italianBigram, italianUnigram = build_ngram("LangId.train.Italian")
    
    pickle.dump(englishBigram, open('englishBigramDict.p', 'wb'))
    pickle.dump(englishUnigram, open('englishUnigramDict.p', 'wb'))
    pickle.dump(frenchBigram, open('frenchBigramDict.p', 'wb'))
    pickle.dump(frenchUnigram, open('frenchUnigramDict.p', 'wb'))
    pickle.dump(italianBigram, open('italianBigramDict.p', 'wb'))
    pickle.dump(italianUnigram, open('italianUnigramDict.p', 'wb'))
    
    