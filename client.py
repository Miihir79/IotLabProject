import socket
import threading
import random
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12129))

mean = [2, 500, 3]      # ph, tds, chlorine levels
deviation = [1, 550, 2]

idName = input("Choose a name: ")
mail = input("Enter mail for alert")


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
        # value generation using gaussian method
        valuePh = random.gauss(mean[0], deviation[0])
        valueTurbidity = random.gauss(mean[1], deviation[1])
        valueChlorine = random.gauss(mean[2], deviation[2])

        if 6.5 < valuePh < 8.5:
            client.send(f'Permissible ph level for drinking water {valuePh}'.encode("ascii"))
        elif valuePh > 8.5:
            client.send(f'Over the Permissible ph levels!!'.encode("ascii"))
        else:
            client.send(f'Under the Permissible ph levels!!{valuePh}'.encode("ascii"))

        if 100 < valueTurbidity < 1000:
            client.send(f'Permissible TDS Level for drinking water {valueTurbidity}'.encode("ascii"))
        else:
            client.send(f'TDS levels Not in the permissible range! '.encode("ascii"))

        if valueChlorine < 4:
            client.send(f'Chlorine levels in range {valuePh}'.encode("ascii"))
        else:
            client.send(f'Chlorine levels not in permissible range'.encode("ascii"))

        time.sleep(10)


recieveThread = threading.Thread(target=recieveMessage)
recieveThread.start()

sendThread = threading.Thread(target=sendMessage)
sendThread.start()
