import json
from socket import *
from utils.config import *
from utils.fileChooser import fileChooser

clientSocket = socket(AF_INET, SOCK_STREAM)

def receiveHandler():
    clientSocket.send(terminateSignal)
    print("> Client Log: Waiting for the response...")

    modifiedMessage = clientSocket.recv(1024)
    response_json = json.loads(modifiedMessage.decode())
    print('> Response:', json.dumps(response_json, indent=4))

def sendHandler():
    with open(clientPath, 'rb') as f:
        while True:
            chunk = f.read(chunkSize)
            if not chunk:
                break
            clientSocket.send(chunk)

    print("> Client Log: Request sent to the server")

try:
    clientSocket.connect((serverName, serverPort))
    client_address = clientSocket.getsockname()

    clientPath = fileChooser()
    sendHandler()
    receiveHandler()

except Exception as e:
    receiveHandler()
    print(f"> Error: {e}")

finally:
    clientSocket.close()
