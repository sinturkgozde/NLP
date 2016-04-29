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
import exceptions


print "Model is loading..."
model = Word2Vec.load("our.model")
print "Model is loaded"
stop_words = stopwords.words("english")

print "training question"
arr = Qc.readData("train_5500.label")
classifier = Qc.trainMachine(arr[0],arr[1])
print "question is loaded"

def possingData(sentence):
	stems = []
	wl =WordNetLemmatizer()
	for word in sentence.split(" "):
		if word not in stop_words:
			stems.append(wl.lemmatize(word))
		else:
			stems.append(word)
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



def extractRelations(splitted_sentence,classifier_tag,resultArray):
	before = False
	togather=""
	for i in range(0,len(splitted_sentence)):
		if classifier_tag in splitted_sentence[i]:
			before=True
			if before:
			 togather = togather +" "+ splitted_sentence[i][:splitted_sentence[i].index("/")]
		else:
			if togather != "":
				if togather not in resultArray:
					resultArray.append(togather)
			before=False
			togather = ""
	if togather != "":
		resultArray.append(togather)
	return resultArray










def extractPossible(noun,searchNoun):
	content = ""
	try:
		searchNounTitle = wikipedia.page(searchNoun).title
		nounTitle = wikipedia.page(noun).title
		if len(wikipedia.search(noun)) > 0 and searchNoun != wikipedia.search(noun)[0] and searchNounTitle != nounTitle:
			content = wikipedia.page(noun).content
	except Exception:
		pass
	return content

def isExistinWikipedia(name):
	try:
		wikipedia.page(name).content
		return True
	except Exception:
		pass
	return False

def contentOfRelations(arr):
	return map(lambda x:extractPossible(x),arr)

def searchTermInDoc(doc,term,title):
	counter  = 0
	dict = {}
	sentences = doc.split(".")
	for sentence in sentences:
		if term in sentence:
			counter = counter+1
	return str({title:counter})


def countSucessful(array,searchNoun):
	return map(lambda x:searchTermInDoc(extractPossible(x,searchNoun),searchNoun,x),array)





#url = "https://en.wikipedita.org/wiki/Mahatma_Gandhi"
#html = urllib2.urlopen(url).read().decode('iso-8859-9').encode('utf-8',',ignore')
#soup = BeautifulSoup(html,"html.parser")
#raw = soup.get_text()
#second_data = raw[:raw.index("References\n\n")].split(".")




def filterArray(array,noun):
    resultArray = []
    found = False
    counter = 1
    titled = wikipedia.page(noun).title
    while counter < len(array):
        if isExistinWikipedia(array[counter]) and noun != array[counter] and wikipedia.page(array[counter]).title == titled:
            array.pop(counter)
            found = True
        else:
            counter = counter+1
    return array



def resultAnswers(testArray):
 resultArray = []
 for element in testArray:
    resultArray = filterArray(testArray,element)
    print resultArray
 return resultArray


def extractWithStanfordNer(question):
	resultArray = []
	#data = extractNounAndVerb(question)
	text =  searchContext(question)
	#print text
	result = extractSimilarSentences(text[1],text[2],text[0],question)
	#print result
	classifier_tag = Qc.classify_question(classifier,[question])
	lastResult = []
	a = []
	for sentence in result:
		recieved_data_from_server = clientSocket.analyzeSentence(sentence)
		checkInfo = searchAnswer.checkIfTag(classifier_tag,recieved_data_from_server)
		if checkInfo[0]:
			splitted_sentence = recieved_data_from_server.split(" ")
			a = extractRelations(splitted_sentence,checkInfo[2],resultArray)
			lastResult.append(a)
	return countSucessful(a,text[1])




def searchContext(sentence):
	stemmer2 = PorterStemmer()
	posed_data = possingData(sentence)
	verb = [element for element in posed_data if  'VB' in element[1] and element[0] not in stop_words ]
	verb =  stemmer2.stem(verb[0][0])
	nlist = findingPossibleName(posed_data)
	name = nlist[0]
	return (myGetForTest(nlist), name , verb)




#question = "Where was Gandhi assassinated?"
#print possingData(question)
#print extractSimilarSentences("Gandhi","kill",second_data,model)[4]
#print (x for x in extractSimilarSentences("Gandhi","kill",second_data,model))



#model = Word2Vec.load("our.model")

#arr = Fetcher.merge_Hyp_Sys("kill")

#result_hyponym2 = filter(lambda x:model.similarity(x,"kill")>0.0 and x in model.vocab,arr)
#print arr
#print result_hyponym2
#print  extractNounAndVerb("When was Bilgi University found?")
#print map(lambda x:str(x),Fetcher.merge_Hyp_Sys("kill"))
