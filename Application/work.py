#!/usr/bin/env python
 # -*- coding: utf-8 -*-
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
import urllib
import simplejson
import time
import cProfile
import ptest

###################################################################
'''
    our.model adli modelimizde, kelimelerin birbirine yakinligi
    ve semantik analizi gerceklestirilir.
	
	Gensim kutuphanesinin icinde bulunan Word2Vec yardimiyla modelimiz yuklenir.
'''
print "Model is loading..."
model = Word2Vec.load("our.model")
print "Model is loaded"
#####################################################################



#####################################################################
'''
	Nltk kutuphanesinin stop words adli moduludur., 
	Ingilizce'de  kullanildigi cumlede anlam degistirmeyen kelimeleri elde ederiz.
	Ornek: the, a, of, there vb.
	Bu kelimeleri elememiz cumlede anlam aramamizda dogruluk payimizi artiracaktir.
'''
stop_words = stopwords.words("english")


#######################################################################



#######################################################################
'''
	Train 5550 modelimizde, Ingilizce bircok soru ve etiketlendirilmesi vardir. 
	Ornek : HUM:ind Who killed Gandhi ?
	Sorunun siniflandirilmasi icin bu modelin egitilmesi gerekmektedir.
	Gerekli ayrintilar QuestionClassification dosyasinda anlatilmistir.
'''
print "We are training question model..."
arr = Qc.readData("train_5500.label")
classifier = Qc.trainMachine(arr[0],arr[1])
print "Question model is loaded!"


#########################################################################


#########################################################################
'''

	Possing Data methodunda amac gelen soru cumlesini WordNet'in Lemmatizer adli modulu yardimiyla kelime kelime ayirmak,
	koklerini bulmak ve pos adi verilen isim, sifat, fiil vb etiketlendirilmesi yapilmasidir. Pos tagging islemi Nltk yardimiyla 
	gerceklestirilir.
	Ornek Soru Cumlesi : "Who directed A Clockwork Orange?"
	Cikti              : ([('Who', 'WP'), ('directed', 'VBD'),('A', 'NNP'), ('Clockwork', 'NNP'), ('Orange', 'NNP')]

	
	WP: Wh-pronoun (What, Who)
	VBD: Verb, past tense
	NNP: Proper noun, sing
	
	
'''

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


#############################################################################








#############################################################################
'''
	Finding Possible Name methodunun amaci, possing data methodunda etiketlendirdigimiz kelimeleri kullanarak cumledeki isim ya da isim tamlamalarini bulmaktir.
	"Who directed A Clockwork Orange?" sorusunda gitmemiz gereken baslik "A Clockwork Orange" oldugu uzere, ngram yolu ile etiketinde 'NN' gecen kelimelerle
	farkli tamlamalar olusturulur.(A, A Clockwork, A Clockwork Orange vb)

'''


def findingPossibleName(posed_data):
	noun = []
	nlist = []
	
	for element in posed_data:
		if "NN" in element[1]:
			
			noun.append(element[0])
			
	if len(noun) <= 1:
		return noun
	
	for i in range(0,len(noun)+1):
		aa = ngrams(noun, i+1)
		for a in aa:
			st = ""
			for i in range(0,len(a)):
				st = st + " " + a[i]
			nlist.append(st)	
	return nlist


''''
	Dondurulen isim tamlamalarinin Wikipedia'da basligi var mi diye kontrolu yapilir. A Clockwork Orange basligi aranilan isim tamlamasi alternatiflerinden 
	en mantikli olani oldugu icin asil aranilan isim olarak "name" olarak tutulur. 
	
	wiki, wikipedia uzerinden "name" olarak etiketlendirdigimiz A Clockwork Orange filminin sayfasina gider, ve butun icerigi ceker.
'''
import datetime

def start_process2():
	print multiprocessing.current_process().name
def findWiki(nlist):
	nameList = []
	for i in nlist:
		try:
			main_title = wikipedia.page(i).title		
			main_search = wikipedia.search(i)
			name = threadWiki(main_search, main_title)
			for el in name:
				if el != None:
					nameList.append(el)
		except:
			pass
	name = max(nameList, key=len)
	wiki =wikipedia.page(name).content.replace("\n","").replace("=","").replace('\\',"").split(".")
	org_name = wikipedia.page(name).title.decode('iso-8859-9').encode('utf-8',',ignore')	
	if "(" in org_name:
		org_name_index= org_name[0:org_name.index(" (")]
	else:
		org_name_index = org_name
	
	return (wiki,org_name_index) 


def threadWiki(nlist,main_title):
	func = partial(wikipedia_search, main_title)
	pool_size =multiprocessing.cpu_count() * 2
	#pool_size = multiprocessing.Pool(len(array))
	pool =multiprocessing.Pool(processes=pool_size,initializer=start_process2 ) 
	results = pool.map(func, nlist)

	pool.close()
	pool.join()
	
	return results

def wikipedia_search(main_title,element):
	try:
		if main_title == wikipedia.page(element).title:
			return main_title
	except:
		pass
	


############################################################################





#############################################################################

'''
	Search Context methodunda amac Possing Data'dan itibaren yazdigimiz methodlari birlestirir.
	cikti : Wikipedia icerigi, Isim(A Clockwork Orange), Fiil (directed)

'''
def searchContext(sentence):
	stemmer2 = PorterStemmer()
	posed_data = possingData(sentence)
	
	verb = [element for element in posed_data if  'VB' in element[1]] 
	if len(verb) <= 1 and str(verb[0][0]) in stop_words:
		verbs = verb[0][0]
		
	else:
		for element in verb:
			if str(element[0]) not in stop_words:
				verbs =  stemmer2.stem(element[0])
		    
		
	
	nlist = findingPossibleName(posed_data)
	
	noun_data = findWiki(nlist)
	
	return (noun_data[0], noun_data[1] , verbs)
	
	
#############################################################################




#############################################################################
'''
	Girdiler: Isim, fiil, wiki datasi, soru
	
	Eger fiilimiz stopwords icinde degilse, helper classindaki merge_Hyp_Sys methodu ile, fiilimizin yakin ve esanlamlilarini bulur.
	Yakinlilik orani 0.35 in altinda olan fiiller filtrelenir. 
	
	
	Ikinci kisimda Wikipedia'da ilgili basliktan cektigimiz datanin icinde,  yukarida elde ettigimiz fiil listesini arar ilgili cumleleri tutariz.
	
	
'''


def extractSimilarSentences(noun,verb,data,question):
	stemmer = PorterStemmer()
	wordnet_lemmatizer = WordNetLemmatizer()
	result_array=[]
	if verb not in stop_words:
		sim_hyp_verb= helper.merge_Hyp_Sys(verb)
		sim_hyp_verb= filter(lambda x: x in model.vocab, sim_hyp_verb)
		similarity_checking= filter(lambda x:model.similarity(x,verb) > 0.35, sim_hyp_verb)
		
		for sentence in data:
			for word in nltk.word_tokenize(sentence):
				if stemmer.stem(word) in map(lambda x:stemmer.stem(x),similarity_checking) :
					result_array.append(sentence)
		 
		return result_array					
	elif verb in stop_words:
		for elem in data:
			result_array.append(elem)
		
		return result_array
	


############################################################################
'''
	

'''

def extractRelations(splitted_sentence,classifier_tag,resultArray):
	before = False
	together=""
	for i in range(0,len(splitted_sentence)):
		if classifier_tag in splitted_sentence[i]:
			before=True
			if before:
			 together = together +" "+ splitted_sentence[i][:splitted_sentence[i].index("/")]
		else:
			if together != "":
				if together not in resultArray:
					resultArray.append(together)
			before=False
			together = ""
	if together != "":
		resultArray.append(together)
	return resultArray


################################################################################################
'''
	Wikipedia'daki butun ilgili icerigi doner.

'''

def extractPossible(searchNoun ,noun):
    content = ""
    try:
        searchNounTitle = wikipedia.page(searchNoun).title
        nounTitle = wikipedia.page(noun).title
        if len(wikipedia.search(noun)) > 0 and searchNoun != wikipedia.search(noun)[0] and searchNounTitle != nounTitle:
            content = wikipedia.page(noun).content
    except Exception:
        pass
    return content

	
##########################################################################################



#############################################################################################

'''
	Count Succesful methodu Stanford NER'den donen olasi "Who directed A Clockwork Orange" cevaplarinin(bir dizi insan ismi) wikipedia sayfalarinda
	soruda asil gecen ismi arar ve siklik taramasina gore yakinligi test eder. Multiprocessing ile ayni anda farkli isimlerin wikipedialarinda A CLockwork Orange
	ismi aranir. En cok siklik donduren isimler, dogru cevap olarak alinir.
	
	
'''


def start_process():
    print 'Starting', multiprocessing.current_process().name
	
def countSuccessful(array,searchNoun):
	func = partial(extractPossible, searchNoun)
	pool_size =multiprocessing.cpu_count() * 2
	#pool_size = multiprocessing.Pool(len(array))
	pool =multiprocessing.Pool(processes=pool_size,initializer=start_process )                          
                                
	
	results = pool.map(func, array)
	
	mainResult = []
	for i in range(0, len(array)):
		
		mainResult.append(searchTermInDoc(results[i],searchNoun,array[i]))
	
	pool.close()
	pool.join()
    
	pool.terminate()
	
	return mainResult	

#####  Dokuman icinde siklik taramasini gerceklestirir.###########
def searchTermInDoc(doc,term,title):
	counter  = 0
	dict = {}
	sentences = doc.split(".")
	for sentence in sentences:
		if term in sentence:
			counter = counter+1
	return {title:counter}

###################################################################





###################################################################
'''
	Siklik taramasinda en yuksek orandaki sonuclari %70 gibi bir yakinlik kistasiyla doner.

'''
def findMaximumAnswer(listCountedName):
	maxValue = 0
	correctAnswer = {}
	max_key = ""
	
	for element in listCountedName:
		
		for key, value in element.iteritems():
			if value >= maxValue:
				
				maxValue = value
				correctAnswer = element
	
	return correctAnswer



def extractCorrectAnswers(result):
	greatest = findMaximumAnswer(result)
	max_no = 0
	max_name = ""
	
	for k,v in greatest.iteritems():
		max_no = v
		max_name = k
	potential = []
	potential.append(max_name)
	
	for element in result:
		for key,value in element.iteritems():
			if value >= max_no*0.70 and key!=max_name:
				
				potential.append(key)
	
	return potential
	
	
	
######################################################################

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_location(noun):
    noun = noun.encode('utf-8')
    params = {
        'address': noun,
        'sensor': "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
    else:
        latitude, longitude = None, None

    return latitude, longitude


	
#########################################################################

	
'''
	Ana Method
	
	Kosullar sorunun siniflandirilmasina gore gerceklestirilir.
	Oc QuestionClassification classindan sorunun ilgili sinifini ceker.
	
	Ornek: "Who directed A Clockwork Orange?"
	Sonuc: [HUM]
	
	{Java Stanford Ner denilen Name Entity Recognizer bize Person etiketiyle (kisileri) doner.}
	
	Kosullar : /NUM(numerik) {Tarih vb numerik sonuclar}
			   /HUM(insan) 
	   		   /LOC(location)
		       /DESC(aciklama)
			   /ENTY(varlik)



'''    

def returnNameOrLoc(noun,verb,data,tag,result,flag):
	resultArray = []
	allSentences = []
	if verb in stop_words:
		try:
			pg = wikipedia.page(noun).summary
			img = findImage(noun)
			return [[pg],[img],tag,flag]
		except:
			pass
	lastResult=[]
	extracted=[]
	
	for i in range(0,len(result)):
		if ","  in result[i]:
			result[i]  = result[i].replace("," , " ,")
		
		recieved_data_from_server = clientSocket.analyzeSentence(result[i])
		checkInfo = searchAnswer.checkIfTag(tag,recieved_data_from_server)
						
			
		if checkInfo[0]:
			splitted_sentence = recieved_data_from_server.split(" ")
			extracted = extractRelations(splitted_sentence,checkInfo[2],resultArray)
			lastResult.append(extracted)
		
	count_result =countSuccessful(extracted,noun)
		
		
		
	correct_answer = extractCorrectAnswers(count_result)
	
	for i in result:
		for elem in correct_answer:
			if elem in i and i not in allSentences:
				allSentences.append(i)
	
	for i in range(0,len(correct_answer)):
		correct_answer[i] = correct_answer[i][1:]
	
		
	img = []
	for element in correct_answer:
		element_appended = findImage(element)
		if element_appended != None:
			img.append(element_appended)
	
	print allSentences
	print img
		
	return [allSentences, img, tag[0], flag]           

def extractWithStanfordNer(question):
	
	resultArray = []
	text =  searchContext(question)
	result = extractSimilarSentences(text[1],text[2],text[0],question)	
	allSentences =[]
	location_flag = False
	classifier_tag = Qc.classify_question(classifier,[question])
	
	if classifier_tag[0] == "NUM":
		
		return [extractDates(result), "", classifier_tag[0],location_flag]
	
	elif  classifier_tag[0] == "HUM":
		return returnNameOrLoc(text[1],text[2],text[0],classifier_tag,result,location_flag)
	elif classifier_tag[0] == "DESC" or classifier_tag[0] == "ENTY":
		text =text[1]
		img=findImage(text)
		mysummary = wikipedia.summary(text)
		
		return [[mysummary],[img],classifier_tag[0],location_flag]		
	
	
	elif classifier_tag[0] == "LOC":
		recieved_data_from_server = clientSocket.analyzeSentence(question)
		if "/LOCATION" in recieved_data_from_server:
			img=findImage(text[1])
			location_flag = True
			return [[get_location(text[1])],[img],classifier_tag[0],location_flag]
		else:
			return returnNameOrLoc(text[1],text[2],text[0],classifier_tag,result,location_flag)
	
	else:
		return 	[["This is  not a proper question"], "",classifier_tag[0],location_flag]





	
	
	
###############################################################################################

'''
	Find  Image methodu dondurdugumuz cevaplarin Wikipedia'daki ilgili resimlerini doner.

'''
def findImage(name):
    try:
       	page = wikipedia.page(name).images
        splittedName = name.split(" ")
        for index in range(0,len(page)):
                for element in splittedName:
                        if element in page[index]:
							return page[index]
    except:
        pass

#################################################################################################







########################################################################################################
'''
	Date parser icin gerekli implementasyonlar.
	
'''
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

########################################################################################################################
