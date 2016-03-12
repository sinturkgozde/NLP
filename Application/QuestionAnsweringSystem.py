
# coding: utf-8

# In[79]:

import nltk

import os,sys
from nltk.corpus import gutenberg
import urllib2
import re

from bs4 import BeautifulSoup


def extract(lst):
    if extractUnproperDateFromData(lst):
        return extractUnproperDateFromData(lst)
    elif  extractProperDateFromData(lst): 
        return  extractProperDateFromData(lst)
    return "Enter a person name"

def extractUnproperDateFromData(lst):
    
 for i in range(0,len(lst[0])):
        if lst[0][i] == "date" and lst[0][i+1] == "of" and lst[0][i+2] == "birth":
            return lst[0][i+4]+" "+ lst[0][i+5]+ " " +lst[0][i+6]
 return False
        
def extractProperDateFromData(lst):    
 for i in range(0,len(lst[0])):
    if "age|" in lst[0][i]:
        return lst[0][i].replace("|"," ")[lst[0][i].index("|"):]
 return False

    
def prepareDataForProccessing(NAME):
    
    data = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+ NAME + "&rvprop=content&redirects=true&format=json").read().decode('utf8')
    tokenized_data = nltk.word_tokenize(str(data).lower())
    #print tokenized_data
    converted_data = nltk.Text(tokenized_data)
    mydata=  nltk.ConcordanceIndex(converted_data.tokens, key = lambda s: s.lower())
    concordance_txt = ([converted_data.tokens[map(lambda x: x-5 if (x-10)>0 else 0,[offset])[0]:offset+10]
                        for offset in mydata.offsets("birth")])
    #print converted_data.tokens[map(lambda x: x-5 if (x-10)>0 else 0,[offset])[0]:offset+10]
    return concordance_txt

dataPrepared= prepareDataForProccessing("Barış_Manço")
dataPrepared2= prepareDataForProccessing("David_Bowie")
dataPrepared3= prepareDataForProccessing("Wes_Anderson")
dataPrepared4= prepareDataForProccessing("peter_jackson")
dataPrepared5= prepareDataForProccessing("Steven_Spielberg")
dataPrepared6= prepareDataForProccessing("Kazim_Karabekir")


print dataPrepared
print "boşluk"
print dataPrepared2
print "boşluk"
print dataPrepared3
print "boşluk"
print dataPrepared4
print "boşluk"
print dataPrepared5
print "boşluk"
print extract(dataPrepared5)





# In[1]:

import nltk

def extractVerb(possed_data):
    for element in possed_data:
        if element[1] == 'VBD' or element[1] == 'VBZ':
            return element[0]

def extractNoun(possed_data):
    result =""
    for element in possed_data:
        if element[1] == 'NNP':
          result +=   element[0] + "_" 
    return result[0:len(result)-1]
            

question = "Who is Bill Gates?"

question2 = "Where is colorado?"

print nltk.pos_tag(nltk.word_tokenize(question2))


def processQuestion(questionSentence): 
    tokenized_data = nltk.word_tokenize(questionSentence)
    possed_data = nltk.pos_tag(tokenized_data)
    return (extractVerb(possed_data),extractNoun(possed_data))



print nltk.help.upenn_tagset('WRB')


processQuestion(question2)


# In[164]:




# In[ ]:




# In[ ]:



