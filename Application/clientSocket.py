import socket
import sys

TCP_IP= '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20 


def initConnect():

    s = socket.socket()
    s.connect(('', TCP_PORT))
    return s

def sendMessage(s, sentence):
    s.send( sentence )
    data = s.recv(1024)
    print data


s = initConnect()
x= s.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)

while True: 
   
    sendMessage(s,"connected")
