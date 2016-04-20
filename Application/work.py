
import helper
from gensim.models import Word2Vec
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
import wikipedia
import searchAnswer
import clientSocket
import QuestionClassification as Qc


print "Model is loading..."
model = Word2Vec.load("our.model")




def possingData(sentence):
	stems = []
	wl =WordNetLemmatizer()
	for word in sentence.split(" "):
		stems.append(wl.lemmatize(word))
	question_tokenized = nltk.word_tokenize(' '.join(stems))
	return nltk.pos_tag(question_tokenized)

def findingPossibleName(posed_data):
	noun = []
	for element in posed_data:
		if 'NN' in element[1]:
			noun.append(element[0])
	if len(noun)<= 1:
		return noun
	bigrams = nltk.bigrams(noun)
	nlist = []
	for grams in bigrams:
		noun = grams[0]+ " "+grams[1]
		nlist.append(noun)
	return nlist

def myGetForTest(possibleNameList):
	for i in possibleNameList:
	 	if wikipedia.search(i) is not [] :
			return wikipedia.page(i).content.replace("\n","").replace("=","").replace('\\',"").split(".")

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

def extractSimilarSentences(noun,verb,data,question):
	stemmer = PorterStemmer()
	wordnet_lemmatizer = WordNetLemmatizer()
	sim_hyp_verb= helper.merge_Hyp_Sys(verb)
	sim_hyp_verb= filter(lambda x: x in model.vocab, sim_hyp_verb)
	similarity_checking= filter(lambda x:model.similarity(x,verb) > 0.35, sim_hyp_verb)
	sentence_no = 0
	result_array=[]
	for sentence in data:
		#recieved_data_from_server = clientSocket.analyzeSentence(sentence)
		for word in nltk.word_tokenize(sentence):
			if stemmer.stem(word) in map(lambda x:stemmer.stem(x),similarity_checking) : 
				result_array.append(str(sentence_no) +" "+sentence+"<br><br>")
		sentence_no = sentence_no+1
	return result_array





#and searchAnswer.checkIfTag(classifier_tag,recieved_data_from_server)


 







#url = "https://en.wikipedita.org/wiki/Mahatma_Gandhi"
#html = urllib2.urlopen(url).read().decode('iso-8859-9').encode('utf-8',',ignore')
#soup = BeautifulSoup(html,"html.parser")
#raw = soup.get_text()
#second_data = raw[:raw.index("References\n\n")].split(".")

def extractWithStanfordNer(question):
	#data = extractNounAndVerb(question)
	text =  searchContext(question)
	result = extractSimilarSentences(text[1],text[2],text[0],question)
	arr = Qc.readData("train_5500.label")
	classifier = Qc.trainMachine(arr[0],arr[1])
	classifier_tag = Qc.classify_question(classifier,[question]) 
	lastResult = []
	for sentence in result:
		recieved_data_from_server = clientSocket.analyzeSentence(sentence)
		if searchAnswer.checkIfTag(classifier_tag,recieved_data_from_server):
			lastResult.append(sentence)
	return lastResult		



def searchContext(sentence):
	stemmer2 = PorterStemmer()
	stop_words = stopwords.words("english")
	posed_data = possingData(sentence)
	verb = [element for element in posed_data if  'VB' in element[1] and element[0] not in stop_words ]
	verb =  stemmer2.stem(verb[0][0])
	nlist = findingPossibleName(posed_data)
	name = nlist[0]
	return (myGetForTest(nlist), name , verb)






#print extractSimilarSentences("Gandhi","kill",second_data,model)[4]
#print (x for x in extractSimilarSentences("Gandhi","kill",second_data,model))  



#model = Word2Vec.load("our.model")

#arr = Fetcher.merge_Hyp_Sys("kill")

#result_hyponym2 = filter(lambda x:model.similarity(x,"kill")>0.0 and x in model.vocab,arr)
#print arr
#print result_hyponym2
#print  extractNounAndVerb("When was Bilgi University found?")
#print map(lambda x:str(x),Fetcher.merge_Hyp_Sys("kill"))