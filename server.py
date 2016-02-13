from socket import *
import sys
import time
import datetime
import re
import os
import signal

PORT = int(sys.argv[1])
HOST = ''

serverSocket =	socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',PORT))
serverSocket.listen(1)
filename = None

def day_of_week_convert(arg):
    switcher = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun"
    }
    return switcher.get(arg, "Invalid")

print	('The	server	 is	ready	to	receive')

while	1:
    connectionSocket,	 addr =	serverSocket.accept()
    print ('new connection established from ' + str(addr))

    sentence	 =	connectionSocket.recv(2048)
    txtsentence =	sentence.decode()
    capitalizedSentence =	txtsentence.upper()

    parts = txtsentence.split(' ')
    print(capitalizedSentence)
    contents = None
    date = datetime.datetime.utcnow()
    dayofweek = day_of_week_convert(date.weekday())


    try:
        filename = parts[1][1:]
        filepath, file_ext = os.path.splitext(filename)
        print (filepath)
        print (file_ext)
        binfile = 0
        if (file_ext == '.txt' or file_ext == '.htm' or file_ext == '.html'):
            inputfile = open (filename, 'r')
            contents = inputfile.read()

        if (file_ext == '.jpg' or file_ext == '.jpeg'):
            inputfile = open (filename, 'rb')
            contents = inputfile.read()
            binfile = 1

        if contents is not None:
            response = 'HTTP/1.1 200 OK\r\nDate: '+ dayofweek +', '+ str(date.strftime('%b')) +' '+ str(date.year) +' ' + str(date.hour) + ':' + str(date.minute) + ':' + str(date.second) + ' GMT' +'\r\n'
            connectionSocket.send(response.encode())
            response = 'Server: Ali H Server\r\n'
            connectionSocket.send(response.encode())
            response = '\r\n'
            connectionSocket.send(response.encode())
            if (binfile == 0):
                connectionSocket.send(contents.encode())
            else:
                connectionSocket.send(contents)
        else:
            connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
            connectionSocket.send('404 File not found'.encode())
            print ('File Not Found')
    except IOError:
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send('404 File not found'.encode())
        print ("URL Not Found")


    # connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()


def http_ver_check(arg):
    pass
