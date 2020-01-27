#
# import socket #import the socket module
# import keyboard
#
# s = socket.socket() #Create a socket object
# port = 12397 # Reserve a port for your service
# s.bind(('',port)) #Bind to the port
#
# s.listen(1) #Wait for the client connect
# c, addr = s.accept()
# while True:
#     message = input("Enter message here:")
#     c.sendto(message.encode(), addr)

import socket

HOST = ''
PORT = 12397
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = 0
print('Socket created')

#managing error exception
try:
    s.bind((HOST, PORT))
    s.listen(1)
    print('Socket awaiting messages')
    conn, addr = s.accept()
    print('Connected')
except socket.error:
    print ('Bind failed')

# awaiting for message
while True:
    data = (conn.recv(1024)).decode()
    print('I sent a message back in response to: ' + data)
    reply = ''

    if data == 'Hello':
        reply = 'Hi, back!'
    elif data == 'This is important':
        reply = 'OK, I have done the important thing you have asked me!'

    elif data == 'quit':
        conn.send('Terminate'.encode())
        break
    else:
        reply = 'Unknown command'

    conn.send(reply.encode())
conn.close()
