import os,sys

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk

count_vectorizer = CountVectorizer()


def readData(dataPath):
 data = open(dataPath).read().decode('iso-8859-9').encode('utf-8',',ignore')

 data_fixed =  str(data)
 sentences_data = data_fixed.split("\n")
 sentences_data_fixed = map(lambda x:str(x),sentences_data)
 sentences = map(lambda x:x[x.index(" "):][1:],sentences_data_fixed[0:len(sentences_data_fixed)-10])
 meaning = map(lambda x:x[x.index(":"):x.index(" ")][1:],sentences_data[0:len(sentences_data)-10])
 result_vector = map(lambda x:x[:x.index(":")],sentences_data[0:len(sentences_data)-10])
 return [sentences,result_vector]

def trainMachine(sentences,target):
 counts = count_vectorizer.fit_transform(sentences)
 classifier = MultinomialNB()
 classifier.fit(counts,target)
 return classifier


def classify_question(classifier,test_sentence):
    vectorized_test = count_vectorizer.transform(test_sentence)
    return classifier.predict(vectorized_test)

"""

arr = readData("train_5500.label")

classifier = trainMachine(arr[0],arr[1])


test_sentence = ["How many people do live in Istanbul"]

print classify_question(classifier,test_sentence)

"""
