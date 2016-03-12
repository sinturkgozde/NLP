
# coding: utf-8

# In[1]:

import os,sys

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk


import QuestionClassification 
targets_sentences = QuestionClassification.readData("train_5500.label")
QuestionClassifier = QuestionClassification.trainMachine(targets_sentences[0], targets_sentences[1])


test_sentence = ["How many people do live in Istanbul"]

print QuestionClassification.classify_question(QuestionClassifier,test_sentence)




# In[2]:

from nltk.stem.porter import *


        
        

question2 = "Who killed Gandhi?"




stemmer = PorterStemmer()

stems = [str(stemmer.stem(element)) for element in nltk.word_tokenize(question2)]



question_tokenized = nltk.word_tokenize(' '.join(stems))


posed_data = nltk.pos_tag(question_tokenized)

print posed_data

VERBS = [element for element in posed_data if  'VB' in element[1]]

nnps = [element for element in posed_data if  'NNP' in element[1]]



similarity_research_word =  VERBS[0][0]

research_nnp =  nnps[0][0]



print similarity_research_word,research_nnp







# In[3]:

import Fetcher
from bs4 import  BeautifulSoup
gozde = Fetcher.myGetForTest()

splitted_gozde = gozde.split(".")

index = 0


# In[14]:

#kerem
import Fetcher
from string import letters
from nltk.corpus import wordnet as wn
from nltk.stem.porter import *


closest_6 =  Fetcher.makeHyponyms(similarity_research_word)[0:]

hyponymArray = []
for element in closest_6:
     hyponymArray.append(str(element.name())[0:])



stemmer = PorterStemmer()

stemmed_hypononym = map(lambda x:stemmer.stem(x),hyponymArray)


cleaned_hyponym= stemmer.stem(stemmed_hypononym[0])
                              
cleaned_hyponym= cleaned_hyponym[0: cleaned_hyponym.index(".")]

result_hyponym = map(lambda x: stemmer.stem(x[0: x.index(".")]),stemmed_hypononym)


        
sentence_no = 0
for sentence in splitted_gozde:
    for word in nltk.word_tokenize(sentence):
       if stemmer.stem(word) in result_hyponym  and research_nnp in sentence  : 
            print "bu sentence gszel:",sentence_no," ",sentence
    sentence_no = sentence_no+1
        




# In[4]:



print gozde


# In[ ]:



