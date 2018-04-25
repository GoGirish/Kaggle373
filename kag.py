#Wolseley says Nicholls won't join as finance chief

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
from pattern.en import singularize
import string
#GLOBALS
trainingFile = "Headline_Trainingdata.csv"
OK_words = "Announce"

def main():
    #read in my file
    file = open(trainingFile, "r")
    data = file.readline()
    data = file.readlines()
    data_matrix = []


    for line in data:
    	temp = []
    	#line = line.replace("\"", "")
    	line = line.replace("\n", "")
    	line = line.replace("?", "")
    	line = line.replace(".", "")
    	s = line.split(",\"")
    	temp.append(s[0])
    	s = s[1].split("\",")
    	temp.append(s[0])
    	temp.append(s[1])
    	data_matrix.append(temp)
    	print(temp)

    print("hello")
    trainingData = clean(data_matrix)

def clean(matrix):
	Capitalized_Words = []
	printable = set(string.printable)
	#get rid of pronouns
	for line in matrix:
		#get the actual headline
		headline = line[1]
		#start trimming
		#print(headline)
		headline = headline.replace(", ", " ")
		headline = headline.replace("UPDATE: ", "")
		headline = headline.replace("UPDATE ", "")
		headline = headline.replace("'s ", " ")
		headline = filter(lambda x: x in printable, headline)
		print("")
                print(headline)
		
                tokens = nltk.word_tokenize(headline)
                tagged = nltk.pos_tag(tokens)
                s = trimSentence(tagged)
                line = toSent(s)
                print(line)



def toSent(array):
    delimiter = ' '
    sentence = delimiter.join(array)

    return sentence

def trimSentence(word_POS):
    sentence_array = []
    for word in word_POS:
        if word[1] == "IN":
            #do nothing
            pass
        elif word[1] == "TO":
            pass
        elif word[1] == "$":
            pass
        elif word[1] == "CD":
            pass
        elif word[1] == "CC":
            pass
        elif word[1] == ":":
            pass
        elif word[0] == "%":
            pass
        elif word[0] == "pct" or word[0] == "percent":
            pass
        elif word[0] == "second": #######
            pass
        elif word[0] == "wo":
            sentence_array.append("will")
        elif word[0] == "n't":
            sentence_array.append("not")
        #if its a verb, add the base of that verb
        elif word[1] == "VB" or word[1] == "VBD" or word[1] == "VBG" or word[1] == "VBN" or word[1] == "VBP" or word[1] == "VBZ":
            base = WordNetLemmatizer().lemmatize(word[0], 'v')
            sentence_array.append(base)
        else:
            #add
            sentence_array.append(singularize(word[0]))
    return sentence_array

def printList(l):
	for item in l:
		print(item)

main()
