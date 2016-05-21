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
import multiprocessing
from functools import partial
import wikipedia
from dateutil.parser import _timelex, parser
from nltk.util import ngrams


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





p = parser()
info = p.info

def timetoken(token):
  try:
    float(token)
    return True
  except ValueError:
    pass
  return any(f(token) for f in (info.jump,info.weekday,info.month,info.hms,info.ampm,info.pertain,info.utczone,info.tzoffset))

def timesplit(input_string):
  batch = []
  for token in _timelex(input_string):
    if timetoken(token):
      if info.jump(token):
        continue
      batch.append(token)
    else:
      if batch:
        yield " ".join(batch)
        batch = []
  if batch:
    yield " ".join(batch)

def extractDates(text):
    result = []
    for sentence in text:
        sentence = sentence[1:].encode('ascii', 'ignore').decode('ascii')
        for elem in timesplit(sentence):
			if elem != 's':
				result.append(sentence)
    return result


def findingPossibleName(posed_data):
	noun = []
	nlist = []
	print posed_data
	for element in posed_data:
		if "NN" in element[1]:
			print element
			noun.append(element[0])
	if len(noun) <= 1:
		return noun
	for i in range(0,len(noun)+1):
		aa = ngrams(noun, i+1)
		print "Yeter yeter"
		for a in aa:
			st = ""
			for i in range(0,len(a)):
				st = st + " " + a[i]
			nlist.append(st)
	print nlist
	return nlist

def findWiki(nlist):
	print "findWiki"
	nameList = []
	for i in nlist:
		try:
			for element in wikipedia.search(i):
				if wikipedia.page(i).title == wikipedia.page(element).title:
					nameList.append(i)
		except:
			pass
	print nameList
	name = max(nameList, key=len)
	print "findWiki" + name 
	wiki =wikipedia.page(name).content.replace("\n","").replace("=","").replace('\\',"").split(".")	
	org_name = wikipedia.page(name).title.decode('iso-8859-9').encode('utf-8',',ignore')	
	org_name_indexed = org_name[0:org_name.index(" (")]
	print "cokmedim burada" + org_name_indexed
	return (wiki,org_name_indexed) 




def myGetForTest(possibleNameList):
	for i in possibleNameList:
	 	if wikipedia.search(i) is not [] :
			return wikipedia.page(i).content.replace("\n","").replace("=","").replace('\\',"").split(".")

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


def extractSimilarSentences(noun,verb,data,question):
	stemmer = PorterStemmer()
	wordnet_lemmatizer = WordNetLemmatizer()
	result_array=[]
	print verb
	if verb not in stop_words:
		sim_hyp_verb= helper.merge_Hyp_Sys(verb)
		sim_hyp_verb= filter(lambda x: x in model.vocab, sim_hyp_verb)
		similarity_checking= filter(lambda x:model.similarity(x,verb) > 0.35, sim_hyp_verb)
		sentence_no = 0
		
		for sentence in data:
			#recieved_data_from_server = clientSocket.analyzeSentence(sentence)
			for word in nltk.word_tokenize(sentence):
				if stemmer.stem(word) in map(lambda x:stemmer.stem(x),similarity_checking) :
					result_array.append(str(sentence_no) +" "+sentence)
		return result_array					
	elif verb in stop_words:
		for elem in data:
			result_array.append(elem)
			
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




def extractPossible2(searchNoun ,noun):
    content = ""
    try:
        searchNounTitle = wikipedia.page(searchNoun).title
        nounTitle = wikipedia.page(noun).title
        if len(wikipedia.search(noun)) > 0 and searchNoun != wikipedia.search(noun)[0] and searchNounTitle != nounTitle:
            content = wikipedia.page(noun).content
    except Exception:
        pass
    return content
def start_process():
    print 'Starting', multiprocessing.current_process().name
	
def countSuccessful2(array,searchNoun):
	func = partial(extractPossible2, searchNoun)
	pool_size =multiprocessing.cpu_count() * 2
	#pool_size = multiprocessing.Pool(len(array))
	pool =multiprocessing.Pool(processes=pool_size,initializer=start_process )                          
                                
	
	results = pool.map(func, array)
	
	mainResult = []
	for i in range(0, len(array)):
		print i
		mainResult.append(searchTermInDoc(results[i],searchNoun,array[i]))
	
	pool.close()
	pool.join()
    
	pool.terminate()
	print results
	return mainResult	


def searchTermInDoc(doc,term,title):
	counter  = 0
	dict = {}
	sentences = doc.split(".")
	for sentence in sentences:
		if term in sentence:
			counter = counter+1
	return {title:counter}




#url = "https://en.wikipedita.org/wiki/Mahatma_Gandhi"
#html = urllib2.urlopen(url).read().decode('iso-8859-9').encode('utf-8',',ignore')
#soup = BeautifulSoup(html,"html.parser")
#raw = soup.get_text()
#second_data = raw[:raw.index("Refereinces\n\n")].split(".")

def findMaximumAnswer(listCountedName):
	print "findMaximumAnswer"
	maxValue = 0
	correctAnswer = {}
	max_key = ""
	print listCountedName
	for element in listCountedName:
		print element
		for key, value in element.iteritems():
			if value >= maxValue:
				print key, value
				maxValue = value
				correctAnswer = element
	print correctAnswer
	return correctAnswer

def extractCorrectAnswers(result):
	greatest = findMaximumAnswer(result)
	max_no = 0
	max_name = ""
	print "ExtractCorrectAnswer 1"
	for k,v in greatest.iteritems():
		max_no = v
		max_name = k
	potential = []
	potential.append(max_name)
	print "ExtractCorrectAnswer 2"
	for element in result:
		for key,value in element.iteritems():
			if value >= max_no*0.70 and key!=max_name:
				print value
				potential.append(key)
	print potential
	return potential
                

def extractWithStanfordNer(question):
	resultArray = []
	#data = extractNounAndVerb(question)
	text =  searchContext(question)
	print text
	result = extractSimilarSentences(text[1],text[2],text[0],question)
	
	
	classifier_tag = Qc.classify_question(classifier,[question])
	print classifier_tag
	if classifier_tag[0] == "NUM":
		
		print "burada cokuyor"
		
		return [extractDates(result), ""]
	
	
	elif  classifier_tag[0] == "HUM" or classifier_tag[0] == "LOC":
		lastResult = []
		a = []
		for i in range(0,len(result)):
			if ","  in result[i]:
				result[i]  = result[i].replace("," , " ,")
				
		
			recieved_data_from_server = clientSocket.analyzeSentence(result[i])
			checkInfo = searchAnswer.checkIfTag(classifier_tag,recieved_data_from_server)
			
			if checkInfo[0]:
				splitted_sentence = recieved_data_from_server.split(" ")
			
				a = extractRelations(splitted_sentence,checkInfo[2],resultArray)
				lastResult.append(a)
		print a
		print "niyeeeee"
		
		
		count_result =countSuccessful2(a,text[1])
		
		print "gelemedim buraya"
		print count_result
		
		
		
		correct_answer = extractCorrectAnswers(count_result)
		for i in range(0,len(correct_answer)):
			correct_answer[i] = correct_answer[i][1:]
		
		
		print correct_answer
		img = []
		for element in correct_answer:
			element_appended = findImage(element)
			if element_appended != None:
				img.append(element_appended)

		print  img
		
		return [correct_answer, img]
	elif classifier_tag[0] == "DESC" or classifier_tag[0] == "ENTY":
		text =text[1]
		img=findImage(text)
		print text
		mysummary = wikipedia.summary(text)
		print mysummary
		return [[mysummary],[img]]		
	else:
		return 	[["This is  not a proper question"], ""]



def searchContext(sentence):
	stemmer2 = PorterStemmer()
	posed_data = possingData(sentence)
	
	verb = [element for element in posed_data if  'VB' in element[1]] 
	if len(verb) <= 1 and verb[0][0] in stop_words:
		verbs = verb[0][0]
		
	else:
		verbs= [element for element in verb if element[0] not in stop_words]
		verbs =  stemmer2.stem(verb[0][0])        
	
	nlist = findingPossibleName(posed_data)
	noun_data = findWiki(nlist)
	print "name:" + noun_data[1]
	return (noun_data[0], noun_data[1] , verbs)


def findCorrectAnswer(listCountedName):
	maxim = 0
	correctAnswer = ""

	for element in listCountedName:
		for key,value in element.iteritems():
			if value >= maxim:
				maxim = value
				correctName = key
			elif value == maxim:
				correctName = correctName if len(correctName) > len(key) else key
	return correctName

def findImage(name):
        page = wikipedia.page(name).images
        splittedName = name.split(" ")
        for index in range(0,len(page)):
                for element in splittedName:
                        if element in page[index]:
							print element, index
							return page[index]


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
