import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12129))
mean = 2
deviation = 3
idName = input("Choose a name: ")


def recieveMessage():
    while True:  # infinite loop
        try:
            message = client.recv(1024).decode('ascii')
            if message == "RequestIdName":
                client.send(idName.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def sendMessage():
    while True:
        value = random.gauss(mean, deviation)
        message = f'{value}'
        client.send(message.encode('ascii'))


recieveThread = threading.Thread(target=recieveMessage)
recieveThread.start()

sendThread = threading.Thread(target=sendMessage)
sendThread.start()
