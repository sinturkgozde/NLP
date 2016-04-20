import QuestionClassification as Qc
import clientSocket




test_question = "Where is the biggest city in the world"

arr = Qc.readData("train_5500.label")

classifier = Qc.trainMachine(arr[0],arr[1])

classifier_tag = Qc.classify_question(classifier,[test_question])







def checkIfTag(classifier_tag,recieved_data_from_server):
	if classifier_tag[0] == "HUM":
		return "/PERSON" in recieved_data_from_server
	elif classifier_tag[0] == "ENTIY":
		return "/ORGANIZATION" in recieved_data_from_server
	elif classifier_tag[0] == "LOC":
		return "/LOCATION" in recieved_data_from_server

#sentence = raw_input("Enter a sentence:")

#arr = ["Gandhi was killed by Nathuram Godse","Gandhi was killed by Nathuram Godse","Apple was founded by Steve Jobs", "Istanbul is the best city of Turkey "]

#for sentence in arr:
#	print sentence
#	recieved_data_from_server = clientSocket.analyzeSentence(sentence)
#	print checkIfTag(classifier_tag,recieved_data_from_server)

