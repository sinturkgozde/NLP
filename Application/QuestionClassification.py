import os,sys

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk

count_vectorizer = CountVectorizer()



data = open("train_5500.label").read().decode('iso-8859-9').encode('utf-8',',ignore')



data_fixed =  str(data)


sentences_data = data_fixed.split("\n")


sentences_data_fixed = map(lambda x:str(x),sentences_data)

sentences = map(lambda x:x[x.index(" "):][1:],sentences_data_fixed[0:len(sentences_data_fixed)-10])

meaning = map(lambda x:x[x.index(":"):x.index(" ")][1:],sentences_data[0:len(sentences_data)-10])

result_vector = map(lambda x:x[:x.index(":")],sentences_data[0:len(sentences_data)-10])


counts = count_vectorizer.fit_transform(sentences)


classifier = MultinomialNB()
target = result_vector
classifier.fit(counts,target)

test_sentence = ["How many people do live in Istanbul"]

vectorized_test = count_vectorizer.transform(test_sentence)


print classifier.predict(vectorized_test)
