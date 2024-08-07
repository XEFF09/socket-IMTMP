import json
import os
import threading
from socket import *
from utils.config import * 
from utils.aiModel import imageDesc

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
filePath = 'app/ser_image/'

def sendHandler(description: str, status: str, connectionSocket: socket):
    json_response = json.dumps(
        {
            'status': status,
            'message': description
        }
    ).encode()
    connectionSocket.send(json_response)
    print(f'> Server Log: Confirmation sent to {connectionSocket.getpeername()}')

def receiveHandler(serverPath: str):
    with open(serverPath, 'wb') as f:
            while True:
                data = connectionSocket.recv(chunkSize)

                if not data:
                    break

                if terminateSignal in data:
                    f.write(data[:data.find(terminateSignal)])
                    break
                f.write(data)

def handleClient(connectionSocket: socket, clientAddress: tuple):
    print(f'> Server Log: Connection established with {clientAddress}')

    try:
        serverPath = os.path.join(filePath, f'{clientAddress[1]}.jpg')
        
        receiveHandler(serverPath)
        sendHandler(imageDesc(serverPath), '200 OK', connectionSocket)

    except Exception as e:
        print(f"> Error: {e}")
        sendHandler('', '400 Bad Request', connectionSocket)

    finally:
        connectionSocket.close()
        if os.path.exists(serverPath):
            os.remove(serverPath)

        print(f'> Server Log: Connection closed with {clientAddress}')

serverSocket.listen(10)
print('> Server Log: Listening...')

while True:
    connectionSocket, clientAddress = serverSocket.accept()
    clientThread = threading.Thread(target=handleClient, args=(connectionSocket, clientAddress))
    clientThread.start()
