import socket 
import threading
import datetime
import os
import time 

HOST = '127.0.1.1'
PORT = 5000

ADDRESS = (HOST , PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 4096

client = socket.socket()

print(f'Connecting ...')
client.connect(ADDRESS)
print(f'Connected to {HOST}:{PORT}')
FILENAME = 'data.json'
FILENAME = os.path.basename(FILENAME)
def fileReceive():
	client.send('NIFTY|CE|2021-05-20|12900|13150'.encode(FORMAT))
	FILESIZE = client.recv(1024).decode(FORMAT)
	client.send(f'received'.encode(FORMAT))
	with open(FILENAME ,'wb') as f:
		bytes_read = client.recv(int(FILESIZE))
		print(bytes_read)
		f.write(bytes_read)

		f.close()
	print('Sleeping for 5 seconds')
	time.sleep(5)

# while (datetime.datetime.now().strftime('%H:%M') >=datetime.time(9,30).strftime('%H:%M')) and (datetime.datetime.now().strftime('%H:%M') <= datetime.time(15,30).strftime('%H:%M')):
fileReceive()

client.close()
