import socket
import sys





TCP_IP= '127.0.0.1'
TCP_PORT= 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello"




s = socket.socket()

s.bind(('', TCP_PORT))

s.listen(1)



while 1:

    c,addr = s.accept() #Establish a connection with the client
    print "Got connection from", addr
    c.send("Thank you for connecting!")
    c.close()

c.close()






