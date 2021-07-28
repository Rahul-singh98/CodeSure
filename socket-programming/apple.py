# # import websockets
# # import asyncio
# # from tkinter import * 
# # from tkinter.ttk import *
# # import datetime , time
# # from threading import Thread

# # class WebSocketClient():

# #     def __init__(self):
# #         pass

# #     async def connect(self):
# #         '''
# #             Connecting to webSocket server

# #             websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
# #         '''
# #         self.connection = await websockets.client.connect('ws://122.160.79.135:10771/Broadcast')
# #         if self.connection.open:
# #             print('Connection stablished. Client correcly connected')
# #             # Send greeting
# #             self.sessionID = await self.connection.recv()
# #             # print(self.sessionID)
# #             self.message = f'{self.sessionID}_rahul@thecodesure.com_159753'
# #             # print(self.message)

# #             await self.sendMessage(self.message)
# #             return self.connection


# #     async def sendMessage(self, message):
# #         '''
# #             Sending message to webSocket server
# #         '''
# #         await self.connection.send(message)

# #     async def receiveMessage(self, connection , ltp ):
# #         '''
# #             Receiving all server messages and handling them
# #         '''
# #         # print('[DEBUG]:: receiveMessage')
# #         while True:
# # 	        try:
# # 	            message = await connection.recv()
# #          #        ltp.config(text=str([int.from_bytes(message[i:i+4] , 'little') for i in range(2,67,4)]))

# # 	        # except websockets.exceptions.ConnectionClosed:
# # 	        #     print('receiveMessage Connection with server closed')
# # 	        #     break

# #     async def heartbeat(self, connection):
# #         '''
# #         Sending heartbeat to server every 5 seconds
# #         Ping - pong messages to verify connection is alive
# #         '''
# #         # print(f'[DEBUG]:: heartbeat {self.sessionID}')
# #         try:
# #             await connection.send(f"{self.sessionID}_rahul@thecodesure.com_35009")
# #             # print('Messsage Sent')
# #         except websockets.exceptions.ConnectionClosed:
# #             print('hearbeat Connection with server closed')

# # class App(Tk):
# #     def __init__(self):
# #         super().__init__()

# #         self.title('CodeSure Software Solution Pvt Ltd')
# #         self.geometry(f'300x200')
# #         # titleImage = PhotoImage(file = 'CodeSurelogo.png')
# #         # self.iconphoto(True , titleImage)
# #         self.ltpLabel = Label(self , text="LTP").pack()
# #         self.ltpEntry = Label(self , text='0')
# #         self.ltpEntry.pack()
# #         client = WebSocketClient()
# #         loop = asyncio.new_event_loop()
# #         asyncio.set_event_loop(loop)
# #         loop = asyncio.get_event_loop()
# #         connection = loop.create_connection(client)

# #         self.b1 = Button(self, text='Add' , command = self.add).pack()

# #     def _threadWorker(self):      
# #     	loop.run_coroutine_threadsafe()
# #     	tasks = [asyncio.ensure_future(client.heartbeat(connection)),asyncio.ensure_future(client.receiveMessage(connection , self.ltpEntry)),]
# #     	loop.run_until_complete(asyncio.wait(tasks))


# #     def add(self):
# #     	myThread = Thread(target=self._threadWorker)
# #     	myThread.start()

# # if __name__ == "__main__":
# #     app = App()
# #     app.mainloop()



# # #################################################################################################
# # # import asyncio as aio
# # # import random

# # # @aio.coroutine
# # # def async_eval(input_, sec):
# # #   yield from aio.sleep(sec)
# # #   print("")
# # #   try:
# # #     result = eval(input_)
# # #   except Exception as e:
# # #     print("< {!r} does not compute >".format(input_))
# # #   else:  
# # #     print("< {!r} = {} >".format(input_, result))

# # # @aio.coroutine
# # # def main(loop):
# # #   while True:
# # #     input_ = yield from loop.run_in_executor(None, input, "> ")

# # #     if input_ == "quit":
# # #       break
# # #     elif input_ == "":
# # #       continue
# # #     else:
# # #       sec = random.uniform(5, 10)
# # #       print("< {!r} scheduled for execution in {:.02} sec>".format(input_, sec))
# # #       aio.async(async_eval(input_, sec))

# # # loop = aio.get_event_loop()

# # # loop.run_until_complete(main(loop))
# # # loop.close()


# # #################################################################################################
# # # import asyncio
# # # from threading import Thread


# # # loop = asyncio.new_event_loop()
# # # running = True


# # # def evaluate(future):
# # #     global running
# # #     stop = future.result()
# # #     if stop:
# # #         print("press enter to exit...")
# # #         running = False


# # # def side_thread(loop):
# # #     asyncio.set_event_loop(loop)
# # #     loop.run_forever()


# # # thread = Thread(target=side_thread, args=(loop,), daemon=True)
# # # thread.start()


# # # async def display(text):
# # #     await asyncio.sleep(5)
# # #     print("echo:", text)
# # #     return text == "exit"


# # # while running:
# # #   text = input("enter text: ")
# # #   future = asyncio.run_coroutine_threadsafe(display(text), loop)
# # #   future.add_done_callback(evaluate)


# # # print("exiting")

# import asyncio
# from threading import *

# async def production_task():
#     i = 0 
#     while True:
#         asyncio.run_coroutine_threadsafe(consumption(i) , thread_loop)
#         await asyncio.sleep(1)
#         i +=1 

# async def consumption(i):
#     while True:
#         print(f"Executing : {i}")
#         await asyncio.sleep(1)

# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()

# thread_loop = asyncio.new_event_loop()
# run_loop_thread = Thread(target=start_loop , args=[thread_loop,])
# run_loop_thread.start()

# advocate_loop = asyncio.get_event_loop()
# advocate_loop.run_until_complete(production_task())
from tkinter import *
from websocket import * 
from threading import *
from math import *

master = Tk()
master.wm_title("Team Black Client")
master.withdraw()
minwidth = master.winfo_screenwidth()/4*3
minheight = master.winfo_screenheight()/4*3
master.minsize(width=ceil(minwidth), height=ceil(minheight))
x = ceil((master.winfo_screenwidth() - minwidth)/2)
y = ceil((master.winfo_screenheight() - minheight)/2)
master.geometry("200x200")
master.deiconify()
master.resizable(0,0)

text = Text(master)
text.pack(expand=True,fill=BOTH)

def on_message(ws, message):
   text.insert(END, message+"\n")
   print("Received: "+message)
   return

def on_error(ws, error):
   text.insert(END, error+"\n")
   print( error)
   return

def on_close(ws):
   text.insert(END, "### closed ###\n")
   print( "### closed ###")
   return

def on_open(ws):
   _id = ws.recv()
   print(_id)
   return

def connection():
#    enableTrace(True)
   ws = WebSocketApp("ws://echo.websocket.org/", on_message = on_message, on_error = on_error, on_close = on_close)
   ws.on_open = on_open

   ws.run_forever()
   return

t = Thread(target=connection)
t.start()

master.mainloop()