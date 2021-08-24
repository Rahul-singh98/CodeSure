import socket 
import threading
import datetime
import time
import os
import pandas as pd 

PORT = 5000
HOST = socket.gethostbyname(socket.gethostname())

ADDRESS = (HOST , PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 4096

clients = []

server = socket.socket()

server.bind(ADDRESS)

def sharing():
    print(f'Server is working on {HOST}:{PORT}')

    server.listen()

    # while datetime.datetime.now().strftime('%H:%M') <= datetime.time(15,30).strftime('%H:%M'):
    while True:
        conn , addr = server.accept()

        print(f'Connected {addr}')
        clients.append(conn)
        # fileShare()
        thread = threading.Thread(target = handle , args=(conn ,addr) )
        thread.start()

        print(f'Active Connections {threading.activeCount()-1}')

    for client in clients:
        client.close()
    server.close()

def handle(conn , addr):
    print(f'New Connection {addr}')
    # connected = True

    while True:
        received = conn.recv(1024).decode(FORMAT)
        script , o_type , expiry , lower , upper = received.split('|')
        fileShare(script,o_type , expiry , lower , upper)
        print('Waiting for 5 seconds')
        time.sleep(5)

    conn.close()


def fileShare(script , o_type , expiry , lower , upper):
    FILENAME = 'data.json'
    df = pd.read_json(FILENAME)
    dChange =int(datetime.datetime(1980, 1,1,0,0).timestamp())
    df['Expiry'] = df['Expiry'].apply(lambda x: datetime.datetime.fromtimestamp(dChange + x).strftime('%d-%m-%Y')).astype('datetime64')
    df = df[(df['Script'] ==script) & (df['Type']==o_type) & (df['Price']>= lower) & (df['Price'] <= upper) & (df['Expiry'] = expiry)]
    "Change Here"

    FILESIZE = os.path.getsize(FILENAME)
    for client in clients:
        client.send(f'{FILESIZE}'.encode(FORMAT))
        rec = client.recv(1024).decode()
    with open(FILENAME , 'rb') as f:
        bytes_read = f.read()
        print(bytes_read)

        for client in clients:
            client.sendall(bytes_read)

        f.close()

sharing()