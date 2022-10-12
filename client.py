import socket
import threading
import random
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12129))
mean = 2
deviation = 2
idName = input("Choose a name: ")
mail = input("Enter mail for aleart")


def recieveMessage():
    while True:  # infinite loop
        try:
            message = client.recv(1024).decode('ascii')
            if message == "RequestIdName":
                client.send(idName.encode('ascii'))

            elif message == "RequestMail":
                client.send(mail.encode('ascii'))
            else:
                print(message)

        except:
            print("An error occurred!")
            client.close()
            break


def sendMessage():
    while True:
        value = random.gauss(mean, deviation)
        if 1 < value < 5:
            client.send(f'Permissible level for drinking water {value}'.encode("ascii"))
        elif value > 5:
            client.send(f'Over the Permissible levels!!'.encode("ascii"))
        else:
            client.send(f'Under the Permissible levels!!{value}'.encode("ascii"))
        time.sleep(1)


recieveThread = threading.Thread(target=recieveMessage)
recieveThread.start()

sendThread = threading.Thread(target=sendMessage)
sendThread.start()
