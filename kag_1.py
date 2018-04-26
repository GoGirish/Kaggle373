#Wolseley says Nicholls won't join as finance chief

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
from pattern.en import singularize
import string
#GLOBALS
trainingFile = "Headline_Trainingdata.csv"
testingFile = "Headline_Testingdata.csv"
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
        #print(s)
    	temp.append(s[0])
    	temp.append(s[1])
    	data_matrix.append(temp)

    #print("hello")
    trainingData = clean(data_matrix)
    #printList(trainingData)
    #exit()
    training = splitMatrix(trainingData)

    sentiments = findSent(training)
    # printList(sentiments[0])
    # exit()
    #print sentiments

    final = findSentperWord(sentiments)
    #print final
    # printList(final)
    # exit()

    full = fullSent(trainingData,final)
    #full = fullSentMod(trainingData, final)
    printList(full)
    #calcAccuracy(full, 1,2)
    #exit()
    #printList(full)
    #exit()
   # printList(full)

    print(accuracy(full,trainingData))
    exit()

    file2 = open(testingFile, "r")
    data2 = file2.readline()
    data2 = file2.readlines()
    data_matrix2 = []
    for line in data2:
        temp = []
        #line = line.replace("\"", "")
        line = line.replace("\n", "")
        line = line.replace("?", "")
        line = line.replace(".", "")
        s = line.split(",\"")
        temp.append(s[0])
        s = s[1].split("\",")
        #print(s)
        temp.append(s[0])
        data_matrix2.append(temp)

    #print("hello")
    testingData = clean(data_matrix2)
    # printList(testingData)

    testing = splitMatrix(testingData)

    full = fullSent(testingData,final)
    printList(full)


def clean(matrix):
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
        #print("")
        #print(headline)

        tokens = nltk.word_tokenize(headline)
        tagged = nltk.pos_tag(tokens)
        s = trimSentence(tagged)
        line[1] = str(toSent(s))
        #print(line)

    return matrix

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

def splitMatrix(train):
    for i in range(0,len(train)):
        train[i].append(train[i][1].split(' '))
    return train

        
def findSent(train):
    sentiments = [[]for i in range(0,5)]
    for i in range(0,len(train)):
        #print(train[i][2])
        if(int(train[i][2]) == 0):
            for j in range(0,len(train[i][3])):
                found = findIndex(sentiments,0,train[i][3][j])
                if found != -1:
                    sentiments[0][found][1]+=1
                else:
                    sentiments[0].append([train[i][3][j],1])
        if(int(train[i][2]) == 1):
            for j in range(0,len(train[i][3])):
                found = findIndex(sentiments,1,train[i][3][j])
                if found != -1:
                    sentiments[1][found][1]+=1
                else:
                    sentiments[1].append([train[i][3][j],1])
        if(int(train[i][2]) == 2):
            for j in range(0,len(train[i][3])):
                found = findIndex(sentiments,2,train[i][3][j])
                if found != -1:
                    sentiments[2][found][1]+=1
                else:
                    sentiments[2].append([train[i][3][j],1])
        if(int(train[i][2]) == 3):
            for j in range(0,len(train[i][3])):
                found = findIndex(sentiments,3,train[i][3][j])
                if found != -1:
                    sentiments[3][found][1]+=1
                else:
                    sentiments[3].append([train[i][3][j],1])
        if(int(train[i][2]) == 4):
            for j in range(0,len(train[i][3])):
                found = findIndex(sentiments,4,train[i][3][j])
                if found != -1:
                    sentiments[4][found][1]+=1
                else:
                    sentiments[4].append([train[i][3][j],1])
            
    return sentiments

def findSentperWord(sentiments):
    finalSents = []
    found = -1
    sum = 0.0
    total = 0.0
    majority =[]

    for i in range(0,len(sentiments)):
    	#for every rating
        for j in range(0,len(sentiments[i])):
        	#for every word in each rating
            if(len(finalSents)>0):
                found = findSentFinal(finalSents,sentiments[i][j][0])
            if found == -1:
                for k in range(0,len(sentiments)):
                    index = findIndex(sentiments,k,sentiments[i][j][0])
                    if index != -1:
                        total += sentiments[k][index][1]
                        sum += k*sentiments[k][index][1]

                finalSents.append([sentiments[i][j][0],(sum/total), sum, total])
            sum = 0.0
            total = 0.0
            found = -1
    return finalSents

def findIndex(sentiments,index,value):
    #print(sentiments[index])
    for i in range(0,len(sentiments[index])):
        if sentiments[index][i][0].lower()== value.lower():
            return i
    return -1

def findSentFinal(finalSents,value):
    for i in range(0,len(finalSents)):
        if finalSents[i][0].lower() == value.lower():
            return i
    return -1

def find_majority(k):
    myMap = {}
    maximum = ( '', 0 ) # (occurring element, occurrences)
    for n in k:
        if n in myMap: 
            myMap[n] += 1
        else: 
            myMap[n] = 1

        # Keep track of maximum on the go
        if myMap[n] > maximum[1]: maximum = (n,myMap[n])

    return maximum[0]

def fullSentMod(train, final):
	print("fullSentMod")
	result = []

	for i in range(0, len(train)):
		#...for every sentence
		dataPoint = train[i]
		#print(dataPoint)
		words = dataPoint[3]

		#sum and total
		sum = 0.0
		total = 0.0
		for word in words:
			pSum, pTotal = lookupWord(final, word)
			sum += pSum
			total += pTotal

		predictedScore = sum / total
		result.append([dataPoint[1], dataPoint[2], predictedScore])

	return result

def calcAccuracy(matrix, ind1, ind2):
	sum = 0.0
	for line in matrix:
		if int(line[ind1]) == round(line[ind2]):
			sum += 1

	print sum/float(len(matrix))


def lookupWord(wordData, word):
	for w in wordData:
		if w[0] == word:
			return w[2], w[3]
	return 0,0

def fullSent(train,final):
    sentenceSent = []
    sum = 0.0
    majority =[]
    
    for i in range(0,len(train)):
        for j in range(0,len(train[i][3])):
            found = findSentFinal(final,train[i][3][j])
            sum += final[found][1]
            majority.append(final[found][1])
        sentenceSent.append([train[i][1],sum/len(train[i][3]),find_majority(majority),train[i][2]])
        majority = []
        sum = 0.0
    
    return sentenceSent

def accuracy(sentenceSent,train):
    sum = 0.0
    plusMinus = 0.0
    for i in range(0,len(sentenceSent)):
        if int(sentenceSent[i][3]) == int(round(sentenceSent[i][2])):
            sum += 1
        
            
            # for j in range(0,len(sentence))
        # elif abs(int(sentenceSent[i][3]) - (sentenceSent[i][2])) <= 1:
        #     print(sentenceSent[i])
            #plusMinus += 1.0
    return ((plusMinus+sum)/float(len(sentenceSent)))

def printList(l):
	for item in l:
		print(item)

main()
