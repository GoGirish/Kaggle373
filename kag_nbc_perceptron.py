import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
import string
from pattern.en import singularize
import math

#GLOBAL
trainingFile = "Headline_Trainingdata.csv"
testingFile = "Headline_Testingdata.csv"
totals = []
sentiments = []
bias = 0.0

def main():
	global totals
	global sentiments
	trainingMatrix, testMatrix = getFileMatrix(trainingFile, 100)
	cleanData(trainingMatrix)
	cleanData(testMatrix)
	calcProbabilities(trainingMatrix)

	trainData(trainingMatrix)
	# for i in range(0, 2):
	# 	trainData(trainingMatrix)
	checkTrainingOnTraining(trainingMatrix)
	# checkTrainingOnTraining(testMatrix)


def trainData(trainingMatrix):
	global sentiments
	global totals
	for line in trainingMatrix:
		sentence_array = line[3]
		actualSentiment = line[2]
		trainSentence(sentence_array, int(actualSentiment))

def checkTrainingOnTraining(trainingMatrix):
	global totals
	global sentiments
	sum = 0
	for line in trainingMatrix:
		#print(line)
		array = line[3]
		scores, predicted = calcPredictedScores(array)
		print(line)
		print("predicted = {}  actual = {}".format(predicted, line[2]))
		print("")
		if predicted == line[2]:
			sum += 1

	print(float(sum) / float(len(trainingMatrix)))

def trainSentence(sentence_array, actualSentiment):
	global sentiments
	global totals
	global bias
	predictedScores, predictedSentiment = calcPredictedScores(sentence_array)
	print("actual = {}  predicted = {}".format(actualSentiment, predictedSentiment))
	k = predictedScores[predictedSentiment] / predictedScores[actualSentiment]
	print(k)
	if k != 1.0:
		for word in sentence_array:
			#print("before = {}".format(sentiments[actualSentiment][word][0]))
			sentiments[actualSentiment][word][1] *= k
		bias += k
			#print("after = {}".format(sentiments[actualSentiment][word][0]))


	# if predictedSentiment == actualSentiment:
	# 	#do nothing
	# 	pass
	# else:
	# 	diff = predictedScores[predictedSentiment]  - predictedScores[actualSentiment]
	# 	for word in sentence_array:
	# 		sentiments[actualSentiment][word][0] += float(diff)/float(len(sentence_array))

# def calcPredictedScores(sentence_array):
# 	global sentiments
# 	global totals
# 	global bias
# 	scores = []
# 	for i in range(0,5):
# 		numerator = 1.0
# 		denominator = 1.0
# 		for j in range(len(sentence_array)):
# 			word = sentence_array[j]
# 			if word in sentiments[i]:
# 				numerator += (sentiments[i][word][0] + 1)
# 			else:
# 				numerator += 1
# 		denominator *= totals[i]
# 		scores.append(float(numerator)/float(denominator))
# 	print(scores)
# 	return scores, scores.index(max(scores))

def calcPredictedScores(sentence_array):
	global sentiments
	global totals
	global bias
	#print(sentiments)
	scores = []
	for i in range(0,5):
		score = 1.0
		for j in range(len(sentence_array)):
			word = sentence_array[j]
			if word in sentiments[0]:
				score *= sentiments[0][word][1]
			else:
				score *= 1.0/float(totals[i])
		scores.append(score + bias)

	return scores, scores.index(max(scores))

def calcProbabilities(data_matrix):
	global totals
	global sentiments
	totals = [0 for t in range(0,5)]
	train = data_matrix
	sentiments = [{} for i in range(0,5)]

	for i in range(0, len(data_matrix)):
		if (int(data_matrix[i][2]) == 0):
			totals[0] += 1
			for j in range(0, len(train[i][3])):
				if train[i][3][j] in sentiments[0]:
					sentiments[0][train[i][3][j]][0] += 1
				else:
					sentiments[0][train[i][3][j]] = [1,0.0]
		elif (int(data_matrix[i][2]) == 1):
			totals[1] += 1
			for j in range(0, len(train[i][3])):
				if train[i][3][j] in sentiments[1]:
					sentiments[1][train[i][3][j]][0] += 1
				else:
					sentiments[1][train[i][3][j]] = [1,0.0]
		elif (int(data_matrix[i][2]) == 2):
			totals[2] += 1
			for j in range(0, len(train[i][3])):
				if train[i][3][j] in sentiments[2]:
					sentiments[2][train[i][3][j]][0] += 1
				else:
					sentiments[2][train[i][3][j]] = [1,0.0]
		elif (int(data_matrix[i][2]) == 3):
			totals[3] += 1
			for j in range(0, len(train[i][3])):
				if train[i][3][j] in sentiments[3]:
					sentiments[3][train[i][3][j]][0] += 1
				else:
					sentiments[3][train[i][3][j]] = [1,0.0]
		elif (int(data_matrix[i][2]) == 4):
			totals[4] += 1
			for j in range(0, len(train[i][3])):
				if train[i][3][j] in sentiments[4]:
					sentiments[4][train[i][3][j]][0] += 1
				else:
					sentiments[4][train[i][3][j]] = [1,0.0]

	for i in range(0,5):
		for key in sentiments[i]:
			sentiments[i][key][1] = sentiments[i][key][0] / float(totals[i])


def findIndex(sentiments,index,value):
    #print(sentiments[index])
    for i in range(0,len(sentiments[index])):
        if sentiments[index][i][0].lower()== value.lower():
            return i
    return -1

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

		line[1] = line[1].replace("-"," ")

		line[1] = ''.join([i for i in line[1] if not i.isdigit()])

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
	print(type(l))
	for item in l:
		if type(l) is dict:
			print("{} : {}".format(item, l[item]))
		else:
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
