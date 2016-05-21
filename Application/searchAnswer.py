import QuestionClassification as Qc
import clientSocket




'''

	Bu method work.py sinifinin extractWithStanfordNer methodunda cagirilir.
	Stanford NER'den aldigimiz etiketleri(Person,  Location, Organization) 
	train_5500 modelinin icinde QuestionClassification methodu ile
	etiketlendirdigimiz labellari eslestirir(Hum, Enty, Desc, Loc, Num).
	
		
'''

def checkIfTag(classifier_tag,recieved_data_from_server):
	if classifier_tag[0] == "HUM":
		return ("/PERSON" in recieved_data_from_server,recieved_data_from_server,"/PERSON")
	elif classifier_tag[0] == "ENTY":
		return ("/ORGANIZATION" in recieved_data_from_server,recieved_data_from_server,"/ORGANIZATION" )
	elif classifier_tag[0] == "DESC":
		return ("/ORGANIZATION" in recieved_data_from_server,recieved_data_from_server,"/ORGANIZATION")
	elif classifier_tag[0] == "LOC":
		return ("/LOCATION" in recieved_data_from_server,recieved_data_from_server,"/LOCATION")


