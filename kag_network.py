import pandas as pd
import numpy as numpy
import matplotlib.pyplot as pyplot
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer

trainingFile = "Headline_Trainingdata.csv"
testingFile = "Headline_Testingdata.csv"

def main():
	cols_training = ['id','text','sentiment']
	df = pd.read_csv(trainingFile, header=0, names=cols_training)
	print(df.head())
	skipLines(1)
	print(df.sentiment.value_counts())


def cleanData(matrix):
	for i in range(len(matrix)):
		line[1] = headline_cleaner(line[1])

	return matrix


def headline_cleaner(text):
	tok = WordPunctTokenizer()
	soup = BeautifulSoup(text, 'lxml')
	souped = soup.get_text()
	try:
		clean = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
	except:
		clean = souped
	letters_only = re.sub("[^a-zA-Z]", " ", clean)
	lower_case = letters_only.lower()
	words = tok.tokenize(lower_case)

	return(" ".join(words)).strip()

def skipLines(numSkips):
	for i in range(0, numSkips):
		print("\n")

main()