import re
import requests
import codecs
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize

'''
Run a delay with Selenium to ensure dynamic elements are loaded
'''
def render_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    #driver.quit()
    return r

'''
Chunk elements of the list to fit into a data frame (step is the number of elements in each sub array)
'''
def chunk_list(str_list):
    start = 0
    end = len(str_list)
    step = 7
    formattedList = []
    
    for i in range(start, end, step):
        x = i
        formattedList.append(str_list[x:x+step])
    return formattedList

'''
Return the paragraph data of the URL given
'''
def scrapeParagraphs(url):
    r = requests.get(url, timeout=40)
    soup = BeautifulSoup(r.content, "html.parser")
    
    str = ""
    
    if soup is not None:
        for paragraph in soup.find_all('p'):
            str += paragraph.text
            str += '\n'
            
    return str

'''
Function to write text to a given filename
'''
def writeToFile (fileName, text):
    file = codecs.open(fileName, "w", "utf-8")
    file.write(u'\ufeff')
    file.write(text)
    file.close()

'''
Clean data by removing newlines and tabs
'''
def cleanData (text):
    return text.replace('\n', '').replace('\t', '')

#Initliaze soup
url = "https://squeezingputin.com"
r = render_page(url)
soup = BeautifulSoup(r, "html.parser")

#Load data into aggregate table
aggregateTable = []
rows = soup.find_all('tr')

#Loop through companies and scrape table data
for company in rows:
    for attribute in company:
        aggregateTable.append(attribute.text)
    
    #Find links to sources & add them
    url = company.find('a')
    if url:
        aggregateTable.append(url.get('href'))
    else:
        aggregateTable.append("None")

'''
Extract important terms from list of tokenized words (TF)
To get most or least important terms can just [:15] or [-15:]
'''
def extractImportantTerms(tokens):
    tfDict = {}
    # get term frequencies
    for t in tokens:
        if t in tfDict:
            tfDict[t] += 1
        else:
            tfDict[t] = 1
            
    # get term frequencies in a more Pythonic way
    token_set = set(tokens)
    tfDict = {t:tokens.count(t) for t in token_set}
    
    # normalize tf by number of tokens
    for t in tfDict.keys():
        tfDict[t] = tfDict[t] / len(tokens)
    
    # Change dict into 2D list and sort from most common to least common
    tfList = list(tfDict.items())
    tfList.sort(key=lambda x: x[1], reverse=True)
    
    return tfList



#Call chunk function to split data by company & table
aggregateTable = chunk_list(aggregateTable)

# Extract text from 15 good URLs and store them as raw text and tokenized by sentence
paragraphItems = []             #Holds list of text from the saved articles
cleanedParagraphItems = []      #Holds list of text from the saved articles that has no tabs or newlines
URLindexes = [1, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 18, 19, 21, 22, 23, 24, 26, 28]

for item in URLindexes:
    url = aggregateTable[item][-1]
    name = aggregateTable[item][0]
    if url != "None":
        try:
            print("Name - ", name, "Index - ", item)
            text = scrapeParagraphs(url)
            #textIndexes.append(item)

            #Write regular file
            writeToFile('RawText - ' + name + ".txt", text)
            paragraphItems.append(text)
            
            #Write cleaned and tokenized data
            cleanedParagraphItems.append(cleanData(text))
            sentences = sent_tokenize(text)
            sentenceText = ""
            for sentence in sentences:
                sentenceText += sentence + '\n'
            writeToFile('Sentences - ' + name + ".txt", sentenceText)
        except:
            paragraphItems.append("Error Scraping URL")
        
#Extract 25 least important terms from pages using an importance measure (TF) and lower case, remove stopwords and punctuation
stopwords = stopwords.words('english')
importantTerms = []

for text in cleanedParagraphItems:
    #Remove punctuation and lowercase
    text = re.sub(r'[^\w\s]',' ', text.lower())
    tokens = word_tokenize(text)
    #Remove stopwords
    tokens_content = [t for t in tokens if t not in stopwords]
    
    #Store and print most important terms
    importantTerms.append(extractImportantTerms(tokens_content))
    print("\n\n25 Least important terms: ", extractImportantTerms(tokens_content)[-15:], '\n')
    print("\nTop 25 most important terms: ", extractImportantTerms(tokens_content)[:15], '\n\n')

# Create new column to add to dataframe
size = len(aggregateTable)-1
importanceColumn = [None for x in range(size)]

for index in URLindexes:
    importanceColumn[index-1] = importantTerms.pop(0)

#Enter into dataframe and export to CSV
df = pd.DataFrame(aggregateTable)
df.columns = ['Company Name', 'Summary', 'Comments', 'Date', 'Source', 'Donations', 'Source URL']
df = df.drop([0])
df.loc[:, "Words by Importance"] = importanceColumn
df.to_csv('SqueezingRussiaData.csv', header=True, index=False)

'''
#5: Manually determine the top 10 terms based on domain knowledge
1 - russia 
2 - ukraine
3 - global
4 - conflict
5 - company
6 - war
7 - media
8 - US
9 - support
10 - international
'''