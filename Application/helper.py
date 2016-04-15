import wikipedia
from nltk.corpus import wordnet as wn
import nltk
import urllib2


def generateSynonymList(word):
 result=[]
 for array in wn.synsets(word):
    for element in array.lemma_names():
        result.append(str(element)) if element not in result else ""
 return result

def makeHyponyms(word):
  result = []
  try:
    return wn.synset(word+'.v.01').hyponyms()
  except nltk.corpus.reader.wordnet.WordNetError:
    result.append(word)
    return result 
    
    
def prepareHyponyms(word):
  result = []
  try:
    data = makeHyponyms(word)
    if len(data) > 0:
      for element in data:
        if hasattr(element,"name"):
          result.append(str(element.name())[0:])
        return map(lambda x:x[0:x.index(".")],result) 
    else:
      return result
  except nltk.corpus.reader.wordnet.WordNetError:
    result.append(word) 
    return result
  
  
def merge_Hyp_Sys(word):
 return prepareHyponyms(word)+generateSynonymList(word) 