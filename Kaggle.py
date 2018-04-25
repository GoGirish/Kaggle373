import pandas as pd
import sys


def main(args = sys.argv):
    trainingFile = args[1]
    file = open(trainingFile, "r")
    data = file.readline()
    data = file.readlines()
    file.close()
    train = []

    for line in data:
    	temp = []
    	#line = line.replace("\"", "")
    	line = line.replace("\n", "")
    	line = line.replace("?", " ?")
    	s = line.split(",\"")
    	temp.append(s[0])
    	s = s[1].split("\",")
    	temp.append(s[0])
    	temp.append(s[1])
        train.append(temp)
    
    #print train

    # trainingdata = pd.read_csv(args[1],sep=',',quotechar='"',header = 0, engine = 'python')
    # X = trainingdata.as_matrix()
    # print X
    # exit()
    	#print(s)

    training = splitMatrix(train)
    #print training

    sentiments = findSent(training)
    #print sentiments

    final = findSentperWord(sentiments)
    print final

    full = fullSent(train,final)
    print full


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

    for i in range(0,len(sentiments)):
        for j in range(0,len(sentiments[i])):
            if(len(finalSents)>0):
                found = findSentFinal(finalSents,sentiments[i][j][0])
            if found == -1:
                for k in range(0,len(sentiments)):
                    index = findIndex(sentiments,k,sentiments[i][j][0])
                    if index != -1:
                        total += sentiments[k][index][1]
                        sum += k*sentiments[k][index][1]
                finalSents.append([sentiments[i][j][0],int(round(sum/total))])
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

def fullSent(train,final):
    sentenceSent = []
    sum = 0.0
    majority =[]
    
    for i in range(0,len(train)):
        for j in range(0,len(train[i][3])):
            found = findSentFinal(final,train[i][3][j])
            sum += final[found][1]
            majority.append(final[found][1])
        sentenceSent.append([train[i][1],int(round(sum/len(train[i][3]))),find_majority(majority)])
        majority = []
        sum = 0.0
    
    return sentenceSent

    


main()