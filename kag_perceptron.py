import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
import string
from pattern.en import singularize
import math

#GLOBAL
trainingFile = "Headline_Trainingdata.csv"
testingFile = "Headline_Testingdata.csv"


def main():
	global trainingFile
	global totals
	trainingMatrix, validationMatrix = getFileMatrix(trainingFile, 100)
	testMatrix, junk = getFileMatrix(testingFile, 100)
	cleanData(trainingMatrix)
	cleanData(validationMatrix)
	cleanData(testMatrix)

	# wordDictionary = createDictionary(trainingMatrix)
	# wordDictionary, bias = train(wordDictionary, trainingMatrix, [3,4], 200)
	# accuracy = validate(wordDictionary, bias, validationMatrix, [3,4])
	# print(accuracy)
	# exit()
	remainingLabels = [0,1,2,3,4]

	classifiedTestPoints = []
	classifiedTrainingPoints = []
	print("length of training matrix = {}".format(len(trainingMatrix)))
	d = None

	for i in range(0, 4):
		splitLabel, maxAccuracy, maxWordDictionary, maxBias = findSplit(remainingLabels, trainingMatrix, trainingMatrix)
		print("splitLabel = {}  maxAccuracy = {}".format(splitLabel, maxAccuracy))
		# printList(maxWordDictionary)
		# exit()
		remainingLabels.remove(splitLabel)
		positivePoints, testMatrix = splitTestingMatrix(splitLabel, testMatrix, maxWordDictionary, maxBias)
		classifiedTestPoints = classifiedTestPoints + positivePoints

		trainingMatrix, newlyClassifiedTraining = splitTrainingMatrix(splitLabel, trainingMatrix, maxWordDictionary, maxBias)
		classifiedTrainingPoints = classifiedTrainingPoints + newlyClassifiedTraining
		print("length of training matrix = {}".format(len(trainingMatrix)))

	print("final length of test: {}".format(len(testMatrix)))

	for line in testMatrix:
		line.append(remainingLabels[0])
		classifiedTestPoints.append(line)

	for line in trainingMatrix:
		line.append(remainingLabels[0])
		classifiedTrainingPoints.append(line)

	print(calcAccuracy(classifiedTrainingPoints))
	writeTestingOutput(classifiedTestPoints)
	#printList(classifiedTestPoints)


def writeTestingOutput(classifiedTestPoints):
	f = open("solution_perceptron.csv", "w+")
	f.write("id,sentiment\n")
	#printList(classifiedTestPoints)
	classifiedTestPoints.sort(key=lambda x: x[0])
	for line in classifiedTestPoints:
		#print(line)
		predicted = line[3]
		sentenceID = line[0]
		s = str(sentenceID) + "," + str(predicted) + "\n"
		f.write(s)
	f.close()


def calcAccuracy(matrix):
	sum = 0.0
	for line in matrix:
		if line[4] == line[2]:
			sum += 1

	return (sum / float(len(matrix)))

def splitTrainingMatrix(splitLabel, trainingMatrix, wordDictionary, bias):
	remainingPoints = []
	classifiedPoints = []
	for line in trainingMatrix:
		sentence_array = line[3]
		predicted = calcFunction(sentence_array, wordDictionary, bias)
		if predicted == False:
			remainingPoints.append(line)
		else:
			line.append(splitLabel)
			classifiedPoints.append(line)

	return remainingPoints, classifiedPoints

def splitTestingMatrix(splitLabel, testMatrix, wordDictionary, bias):
	positivePoints = []
	negativePoints = []
	for line in testMatrix:
		sentence_array = line[2]
		predicted = calcFunction(sentence_array, wordDictionary, bias)
		if predicted == True:
			line.append(splitLabel)
			positivePoints.append(line)
		else:
			negativePoints.append(line)

	return positivePoints, negativePoints

def findSplit(remainingLabels, trainingMatrix, validationMatrix):
	maxAccuracy = -1.0
	splitLabel = -1
	maxWordDictionary = None
	maxBias = None
	for i in remainingLabels:
		wordDictionary = createDictionary(trainingMatrix)
		wordDictionary, bias = train(wordDictionary, trainingMatrix, [i], 200)
		accuracy = validate(wordDictionary, bias, validationMatrix, [i])
		if accuracy > maxAccuracy:
			maxAccuracy = accuracy
			splitLabel = i
			maxWordDictionary = wordDictionary
			maxBias = bias

	return splitLabel, maxAccuracy, maxWordDictionary, maxBias

def validate(wordDictionary, bias, validationMatrix, classLabel):
	truePositive = 0.0
	trueNegative = 0.0
	falsePositive = 0.0
	falseNegative = 0.0
	for line in validationMatrix:
		sentence_array = line[3]
		predicted = calcFunction(sentence_array, wordDictionary, bias)
		actual = int(line[2])
		#print(line)
		#print("actual = {}   predicted = {}\n".format(actual, predicted))
		if predicted == True and actual in classLabel:
			truePositive += 1
		elif predicted == True and actual not in classLabel:
			falsePositive += 1
		elif predicted == False and actual in classLabel:
			falseNegative += 1
		elif predicted == False and actual not in classLabel:
			trueNegative += 1

	#print("truePositive = {}".format(truePositive))
	#print("trueNegative = {}".format(trueNegative))
	#print("falsePositive = {}".format(falsePositive))
	#print("falseNegative = {}".format(falseNegative))

	#print("accuracy = {}".format((truePositive + trueNegative) / float(len(validationMatrix))))

	return ((truePositive + trueNegative) / float(len(validationMatrix)))


def train(wordDictionary, trainingMatrix, classLabel, iterations):
	bias = 0
	for j in range(0, iterations):
		for line in trainingMatrix:
			sentence_array = line[3]
			predicted = calcFunction(sentence_array, wordDictionary, bias)
			actual = int(line[2])
			if predicted == True and actual in classLabel:
				pass
			elif predicted == False and actual not in classLabel:
				pass
			else:
				error = 0.0
				if predicted == True and actual not in classLabel:
					error = -1
				else:
					error = 1
				bias += error

				for word in sentence_array:
					wordDictionary[word] += error

				for i in range(0, len(sentence_array) - 1):
					newPhrase = sentence_array[i] + " " + sentence_array[i+1]
					wordDictionary[newPhrase] += error

				# for i in range(0, len(sentence_array) - 2):
				# 	newPhrase = sentence_array[i] + " " + sentence_array[i+1] + " " + sentence_array[i+2]
				# 	wordDictionary[newPhrase] += error

	return wordDictionary, bias


def calcFunction(sentence_array, wordDictionary, bias):
	score = 0.0
	for word in sentence_array:
		if word in wordDictionary:
			score += wordDictionary[word]

	for i in range(0, len(sentence_array) - 1):
		newPhrase = sentence_array[i] + " " + sentence_array[i+1]
		if newPhrase in wordDictionary:
			score += wordDictionary[newPhrase]
			#print(newPhrase)
			#exit()

	for i in range(0, len(sentence_array) - 2):
		newPhrase = sentence_array[i] + " " + sentence_array[i+1] + " " + sentence_array[i+2]
		if newPhrase in wordDictionary:
			score += wordDictionary[newPhrase]

	score += bias

	if score >= 0:
		return True
	return False

def printList(l):
	print(type(l))
	for item in l:
		if type(l) is dict:
			print("{} : {}".format(item, l[item]))
		else:
			print(item)

def createDictionary(trainingMatrix):
	wordDictionary = {}
	for line in trainingMatrix:
		sentence_array = line[3]
		for word in sentence_array:
			if word in wordDictionary:
				pass
			else:
				wordDictionary[word] = 0

		for i in range(0, len(sentence_array) - 1):
			newPhrase = sentence_array[i] + " " + sentence_array[i+1]
			if newPhrase in wordDictionary:
				pass
			else:
				wordDictionary[newPhrase] = 0

		for i in range(0, len(sentence_array) - 2):
			newPhrase = sentence_array[i] + " " + sentence_array[i+1] + " " + sentence_array[i+2]
			if newPhrase in wordDictionary:
				pass
			else:
				wordDictionary[newPhrase] = 0

	return wordDictionary


def cleanData(data_matrix):
	printable = set(string.printable)
	#prepositions = [" is ", " a ", " at ", " the ", " which ", " on ", " to ", " bln "]
	prepositions = [" is ", " a ", " the ", " which ", " on ", " to ", " bln "]

	for line in data_matrix:
		line[1] = line[1].replace("UPDATE 5-", "")
		line[1] = line[1].replace("UPDATE 1-", "")
		line[1] = line[1].replace("UPDATE ", "")
		line[1] = line[1].replace("UPDATE: ","")

		line[1] = line[1].replace("Companies", "")
		line[1] = line[1].replace("Insight - ", "")
		line[1] = line[1].replace(" - Quick Facts", "")
		line[1] = line[1].replace(" ...", "")
		line[1] = line[1].replace(" bn ", " ")

		line[1] = filter(lambda x: x in printable, line[1])
		line[1] = line[1].lower()
		line[1] = line[1].translate(None, string.punctuation)

		line[1] = ''.join([i for i in line[1] if not i.isdigit()])


		for prep in prepositions:
			line[1] = line[1].replace(prep, " ")

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

main()
