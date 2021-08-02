from websocket import WebSocketApp , create_connection
from threading import Thread , Lock

url = "ws://122.160.79.135:10771/Broadcast"

client = create_connection(url)
sessionID = client.recv()
print(sessionID)

client.send(f'{sessionID}_rahul@thecodesure.com_159753')
# client.send(f'{sessionID}_rahul@thecodesure.com_147258')

def recvMessage():
    while True:
        try:
            message = client.recv()
            if type(message)== str:
                print(f"String message : {message}")
            else:
                n = int.from_bytes(message[0:2],'little')
                print("Length : " , len(message))
                print("No. of packates : ", n)
                
                message =message[2:]
                val =[]
                for i in range(0,len(message),4):
                    val.append(int.from_bytes(message[i:i+4] ,'little'))
                for i in range(n):
                    print("Packet No. " ,i," contains ",val[i*16:(i*16)+16])
            
        except WebSocketConnectionClosedException:
            print("Connection deactivated")
            

def addToken(token):
    for t in token:
        client.send(f'{sessionID}_rahul@thecodesure.com_{t}')


t1 = Thread(target=recvMessage)
t1.start()

try:
    while True :
        string = input(">>> ")
        if string == 'EXIT':
            t1.join()
            client.send(f"{sessionID}_rahul@thecodesure.com_147258")
            client.close()
            print("Exit Successfully")
        token = string.split(",")
        addToken(token)

except:
    t1.join()
    client.close()
    print("Except Exit")
