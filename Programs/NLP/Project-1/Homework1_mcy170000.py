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