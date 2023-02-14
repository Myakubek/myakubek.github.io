---
title: "Project-1 Data Pre-Processing"
excerpt: "Data Pre-Processing Project for NLP"
classes: wide
number: 2
---

## File

[Python File](https://github.com/Myakubek/myakubek.github.io/blob/master/Programs/NLP/Project-1/Homework1_mcy170000.py)

## Overview

### Description  

The program gets a CSV file of a list of employees and their first, middle, and last names as well as their associated ID's and phone numbers.
It processes and cleans the data, standardizing capitalization, phone numbers, and middle names to all be a "John C Doe ID1234 123-456-7890" format.
After cleaning and storing the data, the dictionary is saved as pickle file, then loaded and displayed.  

### How to run  

The program can be run with the following command:

> Python Homework1_mcy170000.py data/data.csv  

The argument is the relative data path, so it could be changed to fit where you're storing your CSV.  

### Strengths & Weaknesses of Python for text processing   

**Strengths**: Python is a very easy to learn, and quick to implement language. There is an abundance of documentation and libraries that support text processing and it's easy to write powerful scripts that process data.    

**Cons**: Because python is an interpreted language and higher level, it's less effecient than compiled lower-level ones. It's a trade-off between the ease of writing python code, the amount of libraries you can utilize and the performance. For what we're currently doing performance isn't really an issue, but for text processing on large scales, the slower runtime may make a noticable difference.

### Takeaways  

Some of the more basic implementations like dictionaries, strings, and regexes were reviews for me. I've worked with python for AI/ML applications before, but it has been a while so this assignment was a great refresher. I have also never worked with pickling before, being able to save and load a dictionary seems very valuable and was definitely something I was happy to learn about. In general lot of the program was string manipulation, functions, and regex which wasn't new but overall the program worked well for what it was meant for: ensuring we know basic python and preprocessing strings for NLP.

## Code

```python
import os
import sys
import re
import pickle

'''
Person Class:
Attributes: First, Middle, & Last Name. ID & Phone.
Functions: Display - Prints all attributes
'''
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone
        
    #Prints all data associated with person
    def display(self):
        print('Employee id:', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone)
        
'''
Function: Reads & cleans data from a csv
Arguments: filePath - A relatively filepath to a CSV file
Returns: Returns a dictionary where Key = ID and value = Person that has that ID
'''
def processFile(filePath):
    personDict = dict()
    
    #Read file into text_in
    with open(os.path.join(os.getcwd(), filePath), 'r') as f:
        text_in = f.read()
    
    #Split elements by line (each person is an element in the list)
    text_list = text_in.split('\n')
    text_list.pop(0)
    
    # Go through and clean & store the persons in a dictionary
    for person in text_list:
        #Split the peron's elements by comma
        text_elements = person.split(',')
        
        #Format first & last name
        lastName = text_elements[0].lower().capitalize()
        firstName = text_elements[1].lower().capitalize()
        
        #Store middle initial as single uppercase letter
        middleName = text_elements[2].upper()
        middleName = middleName[0] if len(middleName) > 0 else '' 
        
        #Regex to ensure in 2 letter-4 digit format
        ID = text_elements[3]
        while not re.match(r"[a-zA-Z]{2}[0-9]{4}", ID):
            print("ID invalid: ", text_elements[3])
            print("ID is two letters followed by 4 digits")
            print("Please enter a valid id:", end = " ")
            ID = input()
        
        #Strip all elements, check if 10 digit 0-9 else get input, then format and store
        phoneNum = text_elements[4]
        if not re.match(r"[0-9]{10}", phoneNum.replace(' ', '').replace ('.', '').replace('-', '')):
            while not re.match(r"[0-9]{3}-[0-9]{3}-[0-9]{4}", phoneNum):
                print("phone ", phoneNum, "is invalid")
                print("Enter phone number in form 123-456-7890")
                print("Enter phone number: ", end='')
                phoneNum = input()
        else:
            phoneNum = phoneNum.replace(' ', '').replace ('.', '').replace('-', '')
            phoneNum = phoneNum[0:3] + '-' + phoneNum[3:6] + '-' + phoneNum[6:]
        
        #store person in dictionary & check for duplicates
        currPerson = Person(lastName, firstName, middleName, ID, phoneNum)
        if ID not in personDict:
            personDict[ID] = currPerson
        else:
            print("Error - repeated ID: ", ID)
            
    return personDict

'''
Main Function: Process & format data from a CSV
Arguments: Takes a system argument for a relataive path of a CSV file
Returns: Will print a processed list of people from the file
'''
if __name__ == '__main__':
    
    #Check arguments, print error and exit if no file path
    if len(sys.argv) < 2:
        print("Error - Please enter a file path for the data as an system arg")
        exit()
    
    personDict = processFile(sys.argv[1])
    
    #Saving & Load pickle data
    pickle.dump(personDict, open('dict.p', 'wb'))  # write binary
    dict_in = pickle.load(open('dict.p', 'rb'))  # read binary
    
    #Run display for each person stored in dictionary
    print('\n\n')
    print("Employee List\n")
    for ID in dict_in:
        dict_in[ID].display()
        print()
```
