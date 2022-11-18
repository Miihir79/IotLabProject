import smtplib
import threading
import socket

host = "127.0.0.1"  # local host
port = 12129
clientsList = []
IdentityName = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
email = "mihirrshah02@gmail.com"


def broadCastMessage(message):
    for client in clientsList:
        client.send(message)


def handleClient(client):
    while True:  # endless loop
        try:
            value = client.recv(1024).decode('utf-8')  # packet size
            print(value)
            if value == "Over the Permissible ph levels!!":
                send_alert("ph")
            elif value == "TDS levels Not in the permissible range!":
                send_alert("tds")
            elif value == "Chlorine levels not in permissible range":
                send_alert("chlorine")

        except:
            index = clientsList.index(client)
            clientsList.remove(client)
            client.close()
            identity = IdentityName[index]
            broadCastMessage(f'{identity} left the chat'.encode('utf-8'))
            IdentityName.remove(identity)
            break


def recieveMessage():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("RequestIdName".encode('utf-8'))  # message for client to give a name
        identityName = client.recv(1024).decode('utf-8')
        IdentityName.append(identityName)
        clientsList.append(client)

        print(f'Identity Name of client is {identityName}')
        broadCastMessage(f'{identityName} joined the system!'.encode('utf-8'))  # for all the clients
        client.send('Connected to the server'.encode('utf-8'))  # for the particular client
        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()


def send_alert(whatsWrong):
    serverMail = smtplib.SMTP('smtp.gmail.com', 587)
    serverMail.ehlo()
    serverMail.starttls()
    serverMail.ehlo()
    serverMail.login('mihirrshah02@gmail.com', 'ygjcrdbiahryuylb')

    subject_mail = 'Issue in water'

    body_mail = f'Hey there, your water system reported abnormal levels of {whatsWrong} \n'
    msg = f"Subject: {subject_mail}\n\n{body_mail}"

    serverMail.sendmail('mihirrshah02@gmail.com', email, msg)

    print('The user has been alerted')

    serverMail.quit()


recieveMessage()
