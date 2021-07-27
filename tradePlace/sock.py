from websocket import WebSocketApp

url = "ws://122.160.79.135:10771/Broadcast"
sessionID = ""

def on_message(ws , message):
    global sessionID
    print(message)
    if type(message) != bytes:
        sessionID=message

def on_error(ws , error):
    print(error)

def on_connect(ws):
    print("connected")

    ws.send(f'{sessionID}_rahul@thecodesure.com_159753')

    ws.send(f'{sessionID}_rahul@thecodesure.com_52173')

def on_close(ws, status_code , message):
    ws.send(f'{sessionID}_rahul@thecodesure.com_147258')
    print(f"Connection closed successfully {message} : {status_code}")


client = WebSocketApp(url , on_open=on_connect , on_message=on_message , on_close=on_close)
client.run_forever()
