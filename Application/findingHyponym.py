from nltk.stem.porter import *
import Fetcher
from string import letters
       
        
strl = """Mohandas Karamchand Gandhi was the preeminent leader of the Indian independence movement in British-ruled India. Born and raised in a Hindu merchant caste family in coastal Gujarat, western India, and trained in law at the Inner Temple. After his return to India in 1915, he set about organising peasants, farmers, and urban labourers to protest against excessive land-tax and discrimination. Some Indians thought Gandhi was too accommodating.[11][12] Nathuram Godse, a Hindu nationalist, assassinated Gandhi on 30 January 1948 by firing three bullets into his chest at point-blank range"""

question2 = "When has been Microsoft founded?"




stemmer = PorterStemmer()

stems = [str(stemmer.stem(element)) for element in nltk.word_tokenize(question2)]



question_tokenized = nltk.word_tokenize(' '.join(stems))


posed_data = nltk.pos_tag(question_tokenized)

print posed_data

VERBS = [element for element in posed_data if  'VB' in element[1]]

similarity_research_word =  VERBS[0][0]


gozde = Fetcher.myGetForTest()
splitted_gozde = gozde.split(" ")





closest_6 =  Fetcher.makeHyponyms(similarity_research_word)[0:]

hyponymArray = []
for element in closest_6:
     hyponymArray.append(str(element.name())[0:str(element.name()).index(".")])

print hyponymArray