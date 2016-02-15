# very (very) basic test script
# takes three arguments -- server (hostname), port, and file to request
# Example:
#  python3 Simple_Client.py www.cs.utexas.edu 80 /~dbryan/simple.html
#
# sends a minimum legal HTTP request for the file

# import the socket library, system library 
from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

message = 'GET ' + filename + ' HTTP/1.1' + '\r\n'
message += 'Host: www.cs.utexas.edu\r\n\r\n'  
clientSocket.send(message.encode())

# only handle 8192 bytes here. Lots of ways to fix that...
response = clientSocket.recv(8192)
print ('From Server:' + response.decode())
clientSocket.close()
