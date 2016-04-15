
import helper
from gensim.models import Word2Vec
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
import nltk
import urllib2
from nltk.corpus import stopwords
import wikipedia


def myGetForTest(name):
    data = wikipedia.page(name)
    raw_text = data.content
    return raw_text.replace("\n","").replace("=","").replace('\\',"").split(".")

url = "https://en.wikipedia.org/wiki/Mahatma_Gandhi"


def extractNounAndVerb(sentence):
	stemmer2 = PorterStemmer()
	wordnet_lemmatizer = WordNetLemmatizer()	
	stop_words = stopwords.words("english")
	stems = stemmer(sentence)
	question_tokenized = nltk.word_tokenize(' '.join(stems))
	posed_data = nltk.pos_tag(question_tokenized)	
	verb = [element for element in posed_data if  'VB' in element[1] and element[0] not in stop_words ]
	verb =  stemmer2.stem(verb[0][0])
	nnps = [element for element in posed_data if  'NN' in element[1]]
	return {"verb": verb.decode('utf8'),"name":nnps[0][0]}
	

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

def loadModel(modelLink=0):
	return Word2Vec.load_word2vec_format('/Users/Kerem/Downloads/GoogleNews-vectors-negative300.bin', binary=True)

def loadModel_two(name):
	return Word2Vec.load(name)

def extractSimilarSentences(noun,verb,data,model):
	stemmer = PorterStemmer()
	wordnet_lemmatizer = WordNetLemmatizer()
	sim_hyp_verb= helper.merge_Hyp_Sys(verb)
	print noun
	sim_hyp_verb= filter(lambda x: x in model.vocab, sim_hyp_verb)
	similarity_checking= filter(lambda x:model.similarity(x,verb) > 0.35, sim_hyp_verb)
	sentence_no = 0
	result_array=[]
	for sentence in data:
		for word in nltk.word_tokenize(sentence):
			if stemmer.stem(word) in map(lambda x:stemmer.stem(x),similarity_checking) and noun in sentence	: 
				result_array.append(str(sentence_no) +" "+sentence+"<br><br>")
		sentence_no = sentence_no+1
	print sentence_no

	return result_array








#data = extractNounAndVerb("Who discoverd America?")

#result =  myGetForTest(data["name"]) 


model = Word2Vec.load("our.model")



#url = "https://en.wikipedita.org/wiki/Mahatma_Gandhi"
#html = urllib2.urlopen(url).read().decode('iso-8859-9').encode('utf-8',',ignore')
#soup = BeautifulSoup(html,"html.parser")
#raw = soup.get_text()
#second_data = raw[:raw.index("References\n\n")].split(".")
#print extractSimilarSentences(data["name"],data["verb"],result,model)
#print extractSimilarSentences("Gandhi","kill",second_data,model)[4]
#print (x for x in extractSimilarSentences("Gandhi","kill",second_data,model))  



#model = Word2Vec.load("our.model")

#arr = Fetcher.merge_Hyp_Sys("kill")

#result_hyponym2 = filter(lambda x:model.similarity(x,"kill")>0.0 and x in model.vocab,arr)
#print arr
#print result_hyponym2
#print  extractNounAndVerb("When was Bilgi University found?")
#print map(lambda x:str(x),Fetcher.merge_Hyp_Sys("kill"))