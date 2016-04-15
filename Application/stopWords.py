import Fetcher
from gensim.models import Word2Vec
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import urllib2
from bs4 import BeautifulSoup

def extractNounAndVerb(sentence):
	stop_words = stopwords.words("english")
	tokenized_sentence = nltk.word_tokenize(sentence)
	wordnet_lemmatizer = WordNetLemmatizer()
	
	#stems = [str(wordnet_lemmatizer.lemmatize(element)) for element in nltk.word_tokenize(sentence)]
	stems = stemmer(sentence)
	question_tokenized = nltk.word_tokenize(' '.join(stems))
	posed_data = nltk.pos_tag(question_tokenized)	
	verb = [element for element in posed_data if  'VB' in element[1] and element[0] not in stop_words ]
	nnps = [element for element in posed_data if  'NNP' in element[1]]
	return {"verb": verb[0][0],"name":nnps[0][0]}

def stemmer(sentence):
	word_list = []
	stop_words = stopwords.words("english")
	wordnet_lemmatizer = WordNetLemmatizer()
	tok_sen = nltk.word_tokenize(sentence)
	for word in tok_sen:
		if word not in stop_words:
			word_list.append(wordnet_lemmatizer.lemmatize(word))
		else:
			word_list.append(str(word))

	return word_list

