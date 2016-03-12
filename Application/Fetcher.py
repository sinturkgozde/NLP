from bs4 import BeautifulSoup

from nltk.corpus import wordnet as wn

import urllib2

wiki_link_first_part = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="
wiki_link_end_part = "&rvprop=content&redirects=true&format=json"

def fetchDataForProcessing(NAME):
    
    data = urllib2.urlopen(wiki_link_first_part+NAME+wiki_link_end_part).read().decode('utf8')
    return data

def fetcherSynonym(word):
    url = "http://thesaurus.altervista.org/thesaurus/v1?key=rokG4BhtuF68i0G6qU8G&word="+word+"&language=en_US&output=json"
    data = urllib2.urlopen(url).read().decode('iso-8859-9').encode('utf-8',',ignore')
    return json.loads(data)["response"]


url = "https://en.wikipedia.org/wiki/Mahatma_Gandhi"

def myGetForTest():
    html = urllib2.urlopen(url).read().decode('iso-8859-9').encode('utf-8',',ignore')
    soup = BeautifulSoup(html,"html.parser")
    raw = soup.get_text()
    return raw[:raw.index("References\n\n")]


def creatingSynonymThearus(word):
    similar_words = []
    for element in fetcherSynonym(word):
         for word in element["list"]["synonyms"].split("|"):
            similar_words.append(word)
            
    return similar_words

def generateSynonymList(word):
 allSynonym = []
 for x in creatingSynonymThearus(word):
    for el in wn.synsets(x):
        allSynonym.append(el)
 result = []       
 for element in allSynonym:   
    for el in element.lemma_names():
        if el not in result:
         result.append(el)
 return result

def makeHyponyms(word):
    return wn.synset(word+'.v.01').hyponyms()