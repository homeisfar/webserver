import filecmp
import socket
import sys

# Text color modifiers
class textColor:
	RESET = "\033[0m"
	GRAY = "\033[90m"
	RED = "\033[91m"
	GREEN = "\033[92m"
	YELLOW = "\033[93m"
	BLUE = "\033[94m"
	PURPLE = "\033[95m"
	CYAN = "\033[96m"

def display(header, content, color, resultType, result):
	if (resultType):
		print (color + "============================================================")
		print ("{:^60}".format("Test: " + result))
		print ("============================================================" + textColor.RESET)
	else:
		print (color + "============================================================")
		print ("{:^60}".format(header + " " + socket.gethostbyname(serverName)))
		print ("============================================================")
		print (content + textColor.RESET)

# Define the server name and port
serverName, serverPort = "localhost", int(sys.argv[1])

# Create socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tells kernel to reuse a local socket in the TIME_WAIT state
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Get request filename from command line
inputfile = "".join(sys.argv[2])

# Get expected result filename from command line
if (len(sys.argv) == 4):
	expectedfile = "".join(sys.argv[3])

# Open request file
try:
	inputfd = open(inputfile, "r")
except IOError as exception:
	print ("\nException:\n{}\n".format(exception))
	sys.exit(1)

# Split request filename to create output filename
fname, ftype = inputfile.split(".")
outputfile = fname + ".out"

try:
	# Connect to server
	clientSocket.connect((serverName, serverPort))

	# Read request from file
	request = ""
	for line in inputfd:
		request += line.strip() + "\r\n"

	# Display request
	display("Request to", request, textColor.CYAN, False, "")

	# Send request to server
	clientSocket.send(bytes(request, "utf-8"))

	# Receive response from server
	responseMsg = clientSocket.recv(8192)
	index = responseMsg.find(b"\r\n\r\n")
	response = str(responseMsg[:index], "utf-8")

	# Display response
	display("Response from", response + "\r\n\r\n", textColor.CYAN, False, "")
	msgContent = responseMsg[index + 4:]

	# Store result
	try:
		outputfd = open(outputfile, "wb")
		outputfd.write(msgContent)
		outputfd.close()
	except IOError as exception:
		print ("\nException:\n{}\n".format(exception))

	# Compare files for correctness
	if (len(sys.argv) == 4):
		if (filecmp.cmp(expectedfile, outputfile)):
			display("", "", textColor.GREEN, True, "PASSED")
		else:
			display("", "", textColor.RED, True, "FAILED")

finally:
	# Close connection to server
	# display("Client closing connection to", "", textColor.GRAY, False, "")
	clientSocket.close()
	inputfd.close()
