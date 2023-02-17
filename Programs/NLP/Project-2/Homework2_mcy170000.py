'''
HOW TO RUN:
> Python Homework2_mcy170000.py anat19.txt

Replace anat19.txt with your filename
'''
import os
import sys
import nltk
from random import seed
from random import randint
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#To download (if needed)
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')


'''
Tokenize text and calculate the Lexical diversity
Input: string of text
output: prints the Lexical diversity of tokens (unique/total) 
'''
def calcLexDiversity(text_input):
    tokens = word_tokenize(text_input)
    
    # Print(Unique tokens / total tokens)
    print("Lexical diversity: %.2f" % (len(set(tokens)) / len(tokens)), "\n\n")



'''
Preprocess raw text
Input: string of text
Output: Return list of tokens and nouns from the text
'''
def preprocess(text_input):
    
    # A- Tokenize lower-case raw text, reduce to those that are alpha, not in NLTK stop words list, and have length > 5
    tokens = word_tokenize(text_input)
    filterA = [t.lower() for t in tokens if t.isalpha() and len(t) > 5 and t not in stopwords.words('english')]
    
    #B- Lemmatize tokens and use set to make a list of unique lemmas
    wnl = WordNetLemmatizer()
    lemmaFilterA = [wnl.lemmatize(t) for t in filterA]
    filterB = list(set(lemmaFilterA))
    
    #C- do POS tagging on the unique lemmas and print the first 20 tagged
    filterC = nltk.pos_tag(filterB)
    print("First 20 unique lemmas tagged: ", filterC[:20], "\n\n")
    
    #D - Create a list of only those lemmas that are nouns
    filterD = [word for word in filterC if word[1] in ['NN', 'NNS', 'NNP', 'NNPS']] 
    
    #E - Print the number of tokens (from step A), and the number of nouns (step D)
    print("Number of tokens: ", len(filterA), "")
    print("Number of nouns: ", len(filterD), "\n\n")
    
    # F - return tokens (not unique) from step A, and nouns from the function
    return filterA, filterD
    
    
    
'''
Guessing Game
Given a list of 50 tokenized words have the user guess characters to reveal a randomly selected word.
Users have 5 points and gain/lose them on correct/incorrect guesses.
Will continue until the user enters '!'
'''
def guessingGame(top50List):
    userScore = 5
    
    #Choose random word and create an associated hidden word
    seed(1337)
    chosenWord = top50List[randint(0, 50)]
    hiddenWord = '_' * len(chosenWord)
    
    print("Let's play a word guessing game!")
    #Loop the game until '!' is inputted
    while(True):
        #Check if score drops below 0
        if(userScore < 0):
            print("You're out of points! Game over")
            exit()
        
        # Check & Handle if solved
        if('_' not in hiddenWord):
            print(hiddenWord)
            print("You solved it!\n")
            print("Current score: ", userScore, '\n')
            print("Guess another word")
            chosenWord = top50List[randint(0, 50)]
            hiddenWord = '_' * len(chosenWord)
            print(hiddenWord)
            
        print(hiddenWord)
        print("Guess a letter:")
        
        # Get user-input and exit on '!'
        char = input()
        if (char == '!'):
            print("Exiting Game")
            exit()
        
        # Handle correct/incorrect input
        if char in chosenWord:
            userScore += 1
            print("Right! Score is ", userScore)
            
            #Update hidden characters in word
            for index, c in enumerate(chosenWord):
                if char is c:
                    hiddenWord = hiddenWord[:index] + char + hiddenWord[index + 1:]
        else:
            userScore -= 1
            print("Sorry, guess again,. Score is ", userScore)  
    
    
    
if __name__ == '__main__':
    # 1 - Check arguments, print error and exit if no file path
    if len(sys.argv) < 2:
        print("Error - Please enter a file path for the data as an system arg")
        exit()
    
    # Read input file as raw text 
    filePath = sys.argv[1]
    with open(os.path.join(os.getcwd(), filePath), 'r') as f:
        text_in = f.read()
        
    # 2 - Print the lexical diversity
    calcLexDiversity(text_in)
    
    # 3 - Call preprocessing function & store return vals
    tokens, nouns = preprocess(text_in)
    
    # 4 - Make a dictionary of noun:count of noun in tokens from the preprocess function
    pos_dict = {}
    
    # Assign dictionary values noun:count
    for word, nounType in nouns:
        pos_dict[word] = tokens.count(word)
    
    # Sort and print top 50
    sortedVals = sorted(pos_dict, key=pos_dict.get, reverse=True)[:50]
    
    for word in sortedVals:
        print(word, ':', pos_dict[word])
    print('\n')

    # 5 - Guessing Game
    guessingGame(sortedVals)
    