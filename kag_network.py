import pandas as pd
import numpy as numpy
import matplotlib.pyplot as pyplot
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
import re

trainingFile = "Headline_Trainingdata.csv"
testingFile = "Headline_Testingdata.csv"

def main():
	cols_training = ['id','text','sentiment']
	df = pd.read_csv(trainingFile, header=0, names=cols_training)
	print(df.head())
	skipLines(1)
	print(df.sentiment.value_counts())
	skipLines(1)
	clean_headlines_raw = cleanData(df)
	exit()
	clean_df = pd.DataFrame(clean_headlines_raw, columns=['text'])
	clean_df['target'] = df.sentiment
	print(clean_df.head())

def cleanData(matrix):
	printList(matrix)
	clean_headlines = []
	for i in range(len(matrix)):
		print(matrix[i])
		clean_headlines.append(headline_cleaner(matrix[i][1]))

	return clean_headlines

def printList(l):
	for item in l:
		print(item)

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