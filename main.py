import threading
import socket

host = "127.0.0.1"  # local host
port = 12129
clientsList = []
IdentityName = []
upperLimits = [5, ]
lowerLimits = [1, ]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


def broadCastMessage(message):
    for client in clientsList:
        client.send(message)


def handleClient(client):
    while True:  # endless loop
        try:
            value = client.recv(1024).decode('ascii')  # packet size
            if 1 < value < 5:
                client.send("Permissible level for drinking water")
            elif value > upperLimits[0]:
                client.send("Over the Permissible levels!!")
            else:
                client.send("Under the Permissible levels!!")

        except:
            index = clientsList.index(client)
            clientsList.remove(client)
            client.close()
            identity = IdentityName[index]
            broadCastMessage(f'{identity} left the chat'.encode('ascii'))
            IdentityName.remove(identity)
            break


def recieveMessage():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("RequestIdName".encode('ascii'))  # message for client to give a name
        identityName = client.recv(1024).decode('ascii')
        IdentityName.append(identityName)
        clientsList.append(client)

        print(f'Identity Name of client is {identityName}')
        broadCastMessage(f'{identityName} joined the channel!'.encode('ascii'))  # for all the clients
        client.send('Connected to the server'.encode('ascii'))  # for the particular client

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()


recieveMessage()
