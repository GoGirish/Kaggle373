import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
import string
from pattern.en import singularize

#GLOBAL
trainingFile = "Headline_Trainingdata.csv"
testingFile = "Headline_Testingdata.csv"
totals = []

def main():
	global totals
	trainingMatrix, testMatrix = getFileMatrix(trainingFile, 70)
	cleanData(trainingMatrix)
	cleanData(testMatrix)
	#splitMatrix(trainingMatrix)
	wordCounts = calcCounts(trainingMatrix)
	checkTrainingOnTraining(testMatrix, wordCounts)
	exit()
	testMatrix, junk = getFileMatrix(testingFile, 100)

	cleanData(testMatrix)
	outputTesting(testMatrix, wordCounts)

def outputTesting(testingMatrix, counts):
	global totals
	f = open("solution_revised_1.csv", "w+")
	f.write("id,sentiment\n")

	for line in testingMatrix:
		array = line[2]
		predicted = calcProb(array, counts, totals)
		s = str(line[0]) + "," + str(predicted) + "\n"
		f.write(s)
	f.close()


def checkTrainingOnTraining(trainingMatrix, counts):
	global totals
	sum = 0
	for line in trainingMatrix:
		array = line[3]
		predicted = calcProb(array, counts, totals)
		print(line)
		print("predicted = {}  actual = {}".format(predicted, line[2]))
		print("")
		if predicted == line[2]:
			sum += 1

	print(float(sum) / float(len(trainingMatrix)))


def findCount(list, word):
	for tup in list:
		if tup[0] == word:
			return tup[1]
	return 0

def calcProb(sentence_array, counts, totals):
	scores = [0 for x in range(0,5)]

	for i in range(0,5):
		numerator = 1	#totals[i]
		denominator = 1	#sum(totals)
		for j in range(len(sentence_array)):
			word = sentence_array[j]
			numerator *= (findCount(counts[i], word) + 1)
			# d = 1.0
			# for k in range(0,5):
			# 	d += (findCount(counts[k], word) + 1)
			# denominator *= d
		denominator *= totals[i]
		scores[i] = float(numerator) / float(denominator)

	return scores.index(max(scores))


def cleanData(data_matrix):
	printable = set(string.printable)
	prepositions = ["is", "a", "at", "the", "which", "on ", "to"]

	for line in data_matrix:
		line[1] = line[1].replace("UPDATE 5-", "")
		line[1] = line[1].replace("UPDATE 1-", "")
		line[1] = line[1].replace("UPDATE ", "")
		line[1] = line[1].replace("UPDATE: ","")

		line[1] = line[1].replace("Companies", "")
		line[1] = line[1].replace("Insight - ", "")
		line[1] = line[1].replace(" - Quick Facts", "")
		line[1] = line[1].replace(" ...", "")

		line[1] = filter(lambda x: x in printable, line[1])
		line[1] = line[1].lower()
		line[1] = line[1].translate(None, string.punctuation)

		# for prep in prepositions:
		# 	line[1] = line[1].replace(prep, "")

		sentence_array = nltk.word_tokenize(line[1])
		# for pr in prepositions:
		# 	try:
		# 		sentence_array.remove(pr)
		for i in range(len(sentence_array)):
			#sentence_array[i] = str(WordNetLemmatizer().lemmatize(sentence_array[i], 'v'))
			sentence_array[i] = str(singularize(sentence_array[i]))



		line.append(sentence_array)

def splitMatrix(train):
	for i in range(0,len(train)):
		train[i].append(train[i][1].split(' '))
	return train

def findIndex(sentiments,index,value):
    #print(sentiments[index])
    for i in range(0,len(sentiments[index])):
        if sentiments[index][i][0].lower()== value.lower():
            return i
    return -1

def calcCounts(data_matrix):
	global totals
	totals = [0 for t in range(0,5)]
	train = data_matrix
	sentiments = [[]for i in range(0,5)]
	for i in range(0,len(train)):
		#print(train[i][2])
		if(int(train[i][2]) == 0):
			totals[0] += 1
			for j in range(0,len(train[i][3])):
				found = findIndex(sentiments,0,train[i][3][j])
				if found != -1:
				    sentiments[0][found][1]+=1
				else:
				    sentiments[0].append([train[i][3][j],1])
		elif(int(train[i][2]) == 1):
			totals[1] += 1
			for j in range(0,len(train[i][3])):
				found = findIndex(sentiments,1,train[i][3][j])
				if found != -1:
				    sentiments[1][found][1]+=1
				else:
				    sentiments[1].append([train[i][3][j],1])
		elif(int(train[i][2]) == 2):
			totals[2] += 1
			for j in range(0,len(train[i][3])):
				found = findIndex(sentiments,2,train[i][3][j])
				if found != -1:
				    sentiments[2][found][1]+=1
				else:
				    sentiments[2].append([train[i][3][j],1])
		elif(int(train[i][2]) == 3):
			totals[3] += 1
			for j in range(0,len(train[i][3])):
				found = findIndex(sentiments,3,train[i][3][j])
				if found != -1:
				    sentiments[3][found][1]+=1
				else:
				    sentiments[3].append([train[i][3][j],1])
		elif(int(train[i][2]) == 4):
			totals[4] += 1
			for j in range(0,len(train[i][3])):
				found = findIndex(sentiments,4,train[i][3][j])
				if found != -1:
				    sentiments[4][found][1]+=1
				else:
				    sentiments[4].append([train[i][3][j],1])

	return sentiments

def getFileMatrix(fileName, percentage=100):
	file = open(fileName, "r")
	data = file.readline()
	data = file.readlines()

	data_matrix = []
	test = []
	length = int(float(len(data)) * float(percentage) / float(100))
	for i in range(0,length):
		line = data[i]
		temp = []
		s = line.split(",\"")
		temp.append(int(s[0]))

		s = s[1].split("\",")
		temp.append(str(s[0]))
		if len(s) == 2:
			temp.append(int(s[1]))
		data_matrix.append(temp)

	if percentage != 100:
		for i in range(length, len(data)):
			line = data[i]
			temp = []
			s = line.split(",\"")
			temp.append(int(s[0]))

			s = s[1].split("\",")
			temp.append(str(s[0]))
			temp.append(int(s[1]))
			test.append(temp)

	file.close()
	return data_matrix, test

def printList(l):
	for item in l:
		print(item)

main()

##########################################
##---------TRASH-----------------------###
##########################################

def nltkSentiment(data_matrix):
	sia = SentimentIntensityAnalyzer()

	for line in data_matrix:
		pol_score = sia.polarity_scores(line[1])
		print(line)
		print(pol_score)
