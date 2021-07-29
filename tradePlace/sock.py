from websocket import WebSocketApp , create_connection
from threading import Thread

url = "ws://122.160.79.135:10771/Broadcast"

client = create_connection(url)
sessionID = client.recv()
print(sessionID)

client.send(f'{sessionID}_rahul@thecodesure.com_159753')

def recvMessage():
    while True:
        try:
            message = client.recv()
            n = int.from_bytes(message[0:2],'little')
            print("Length : " , len(message))
            print("No. of packates : ", n)
            
            message =message[2:]
            val =[]
            for i in range(0,len(message),4):
                val.append(int.from_bytes(message[i:i+4] ,'little'))
            for i in range(n):
                print("Packet No. " ,i," contains ",val[i*16:(i*16)+16])
            
        except :
            t1.join()
            

def addToken(token):
    for t in token:
        client.send(f'{sessionID}_rahul@thecodesure.com_{t}')


t1 = Thread(target=recvMessage)
t1.start()

while True :
    string = input(">>> ")
    if string == 'EXIT':
        client.send(f"{sessionID}_rahul@thecodesure.com_147258")
        client.close()
        t1.join()
        print("Exit Successfully")
    token = string.split(",")
    addToken(token)


# def on_message(ws , message):
#     global sessionID
#     # print(f"{message}: of type : {type(message)}")
#     if type(message) != bytes:
#         sessionID=message
#         print(sessionID)

# def on_error(ws , error):
#     print(error)

# def on_connect(ws):
#     print("connected")

#     # if sessionID != "":
#     #     ws.send(f'{sessionID}_rahul@thecodesure.com_159753')
#     #     print('Session Sent')
#     #     ws.send(f'{sessionID}_rahul@thecodesure.com_52173')

# def on_close(ws, status_code , message):
#     ws.send(f'{sessionID}_rahul@thecodesure.com_147258')
#     print(f"Connection closed successfully {message} : {status_code}")


# client = WebSocketApp(url , on_open=on_connect , on_message=on_message , on_close=on_close)
# client.run_forever()
