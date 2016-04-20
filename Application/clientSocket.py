import socket
import sys

TCP_IP= '127.0.0.1'
TCP_PORT = 3150
BUFFER_SIZE = 20 
total_data = []

def initConnect():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)
    s.connect(('', TCP_PORT))
    return s

def sendMessage(s, sentence):
	s.send( sentence.encode('utf-8'))
	data = s.recv(2048)
	return data
		



def analyzeSentence(sentence):
	s = initConnect()
	data =  sendMessage(s,sentence+"\n")
	return data









#while True:
#		data = s.recv(2048)
#		print not data
#		if not data: 
#			break
#		total_data.append(data)
#	print not data
#		print total_data
#	return ''.join(total_data)



