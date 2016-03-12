
# coding: utf-8

# In[5]:

import QuestionClassification 
targets_sentences = QuestionClassification.readData("train_5500.label")
QuestionClassifier = QuestionClassification.trainMachine(targets_sentences[0], targets_sentences[1])


test_sentence = ["How many people do live in Istanbul"]

print QuestionClassification.classify_question(QuestionClassifier,test_sentence)



# In[2]:

import os,sys
import nltk


# In[ ]:



