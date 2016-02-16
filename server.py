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
serverSocket.bind((HOST,PORT))
serverSocket.listen(1)
filename = None


class CustomError(Exception):
    def __init__(self, arg):
        # Set some exception infomation
        self.msg = arg

print	('The	server	 is	ready	to	receive')

while	1:
    connectionSocket,	 addr =	serverSocket.accept()
    print ('new connection established from ' + str(addr))
    sentence = ''
    # while 1:
    #     sentencebite = connectionSocket.recv(2048)
    #     try:
    #         sentence = sentence + sentencebite.decode()
    #     except UnicodeDecodeError:
    #         break
    #     if (sentence.endswith('\r\n\r\n')):
    #         break


    sentencebite = connectionSocket.recv(2048)
    # try:
    sentence = sentence + sentencebite.decode()
    # except UnicodeDecodeError:
        # break
        # if (sentence.endswith('\r\n\r\n')):
            # break

    txtsentence =	sentence
    capitalizedSentence =	txtsentence.upper()
    txtsentence = txtsentence.replace('\r\n', ' ')
    parts = txtsentence.split(' ')
    print (repr(sentence))
    print (repr(txtsentence))
    print(capitalizedSentence)
    contents = None
    date = datetime.datetime.utcnow()

    try:
        filename = parts[1][1:]
        version = parts[2]
        request = parts[0]
        # host = parts[3] + ' ' + parts[4]
        ifModifiedIndex = -1
        hostIndex = -1
        try:
            ifModifiedIndex = parts.index("If-Modified-Since:")
        except ValueError:
            pass

        try:
            hostIndex = parts.index("Host:")
        except ValueError:
            pass

        ifModifiedRequestString = None
        host = None
        if (ifModifiedIndex > -1):
            ifModifiedRequestString = parts[ifModifiedIndex+2] + ' ' + parts[ifModifiedIndex+3] + ' ' + parts[ifModifiedIndex+4] + ' ' + parts[ifModifiedIndex+5] + ' ' + parts[ifModifiedIndex+6]

        if (hostIndex > -1):
            host = parts[hostIndex] + ' ' + parts[hostIndex+1]

        print ("HOST")
        print (host)
        print (parts)
        print (version)
        filepath, file_ext = os.path.splitext(filename)
        print (filepath)
        print (file_ext)
        binfile = 0
        MIME = None

        if ('\r' in txtsentence or '\n' in txtsentence):
            response = 'HTTP/1.1 400 Bad Request\r\n400 Bad Request. Malformed request.\r\n\r\n'
            connectionSocket.send(response.encode())
            raise CustomError('400 Bad Request')


        if (request != 'GET'):
            response = 'HTTP/1.1 501 Not Implemented\r\n501 Not Implemented. Only GET.\r\n\r\n'
            connectionSocket.send(response.encode())
            raise CustomError('501 error occurred')

        if (version != 'HTTP/1.1'):
            response = 'HTTP/1.1 505 HTTP Version Not Supported\r\n505 HTTP Version Not Supported\r\n\r\n'
            connectionSocket.send(response.encode())
            raise CustomError('505 error occurred')

        print ("host: " + host)

        if (not host.startswith("Host: ")):
            response = 'HTTP/1.1 400 Bad Request\r\n400 Bad Request. Malformed request.\r\n\r\n'
            connectionSocket.send(response.encode())
            raise CustomError('400 Bad Request')


        if (file_ext == '.txt'):
            inputfile = open (filename, 'r')
            contents = inputfile.read()
            MIME = 'text/plain'

        if (file_ext == '.htm' or file_ext == '.html'):
            inputfile = open (filename, 'r')
            contents = inputfile.read()
            MIME = 'text/html'

        if (file_ext == '.jpg' or file_ext == '.jpeg'):
            inputfile = open (filename, 'rb')
            contents = inputfile.read()
            binfile = 1
            MIME = 'image/jpeg'

        if contents is not None:
            file_stats = os.stat(filename)
            response = 'HTTP/1.1 200 OK\r\n'
            # connectionSocket.send(response.encode())
            response = response + date.strftime("Date: %a, %d %b %Y %I:%M:%S GMT\r\n")
            # connectionSocket.send(response.encode())
            response = response + 'Server: Ali H Server\r\n'
            # connectionSocket.send(response.encode())
            response = response + 'Content-Length: ' + str(file_stats.st_size) + '\r\n'
            # connectionSocket.send(response.encode())
            modifiedstamp = datetime.datetime.utcfromtimestamp(file_stats.st_mtime)
            response = response + modifiedstamp.strftime("Last-Modified: %a, %d %b %Y %I:%M:%S GMT\r\n")
            # connectionSocket.send(response.encode())
            response = response + 'Content-Type: ' + MIME + '\r\n'
            # connectionSocket.send(response.encode())
            response = response + '\r\n'
            # connectionSocket.send(response.encode())

            #NEED TO COMPARE MODIFIED DATES
            if (ifModifiedIndex > -1):
                try:
                    ifModifiedTimeObject = time.strptime(ifModifiedRequestString, "%d %b %Y %H:%M:%S %Z")
                except ValueError:
                    ifModifiedTimeObject = time.strptime(ifModifiedRequestString, "%d %b %Y %H:%M:%S")

                # modifiedstamp = modifiedstamp.replace(second=0)
                print ("FILE NOT MODIFIED?")
                print (time.mktime(ifModifiedTimeObject) - time.mktime(modifiedstamp.timetuple()))

                print (str(ifModifiedTimeObject))
                print (str(modifiedstamp.timetuple()))

                if (time.mktime(ifModifiedTimeObject) == time.mktime(modifiedstamp.timetuple())):
                    response = 'HTTP/1.1 304 Not Modified\r\n'
                    response = response + date.strftime("Date: %a, %d %b %Y %I:%M GMT\r\n")
                    response = response + 'Server: Ali H Server\r\n\r\n'
                    binfile = 2

            print("unencoded response:\n" + response)
            if (binfile == 0):
                response = response + contents
                connectionSocket.send(response.encode())
            elif (binfile == 1):
                response = response.encode()
                response = response + contents
                connectionSocket.send(response)
            else:
                response = response.encode()
                connectionSocket.send(response)
        else:
            connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
            connectionSocket.send('404 File not found'.encode())
            print ('File Not Found')
    except IOError:
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send('404 File not found'.encode())
        print ("URL Not Found")

    except IndexError:
        connectionSocket.send('HTTP/1.1 500 Internal Server Error\r\n\r\n'.encode())
        connectionSocket.send('500 Internal Server Error'.encode())
        print ("malformed request")

    except CustomError as custom:
        print ('Error: ' + custom.msg)

    except UnicodeDecodeError:
        print ("Some wild text came in closing connection")

    print('Closing connection from' +str(addr))
    connectionSocket.close()
