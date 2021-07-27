import pandas as pd
import datetime
import websockets , asyncio

def readCSFunction(contract_filepath = '../Data/contract.txt' ,equity_filepath = '../Data/security.txt' ):
    cols = [i for i in range(0,70)]

    try:
        df = pd.read_csv(contract_filepath , sep='|' , skiprows=1 , names=cols)

        df= df[[0,2,3,6,7,8]]
        df.columns = ['Token No','Instrument','Script', 'Expiry' , 'Price' , 'Type']
        df.dropna(inplace=True)
        df['Price'] = df['Price'].apply(lambda x: (x/100)).astype('int')
        dChange =int(datetime.datetime(1980, 1,1,0,0).timestamp())
        df['Expiry'] = df['Expiry'].apply(lambda x: datetime.datetime.fromtimestamp(dChange + x).strftime('%d-%m-%Y')).astype('datetime64')
        df.reset_index(drop=True ,inplace=True)

    except :
        df = pd.DataFrame()
        print(f"contract file is not present at : {contract_filepath}")

    cols = [i for i in range(55)] 

    try:    
        eq_df = pd.read_csv(equity_filepath , sep='|' , skiprows=1 , names=cols)     
        eq_df = eq_df[[0,1,2]]
        eq_df = eq_df[eq_df[2] == "EQ"]
        eq_df.columns = ['Token No' , 'Script' ]
        eq_df.reset_index(drop=True ,inplace=True)
    except:
        eq_df = pd.DataFrame()
        print(f"equity file is not present at : {equity_filepath}")

    if not df.empty and not eq_df.empty:
        return [df , eq_df]
    elif df.empty :
        return [None,eq_df]
    elif eq_df.empty:
        return [df , None]
    else :
        return [None,None]

class WebSocketClient():

    def __init__(self):
        pass

    async def connect(self):
        '''
            Connecting to webSocket server

            websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
        '''
        self.connection = await websockets.connect('ws://122.160.79.135:10771/Broadcast')
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            # Send greeting
            self.sessionID = await self.connection.recv()
            print(self.sessionID)
            self.message = f'{self.sessionID}_rahul@thecodesure.com_159753'
            print(self.message)

            await self.sendMessage(self.message)
            return self.connection


    async def sendMessage(self, message):
        '''
            Sending message to webSocket server
        '''
        await self.connection.send(message)

    async def receiveMessage(self, connection ,tokenNo, DataGrid , idx , DataDict):
        '''
            Receiving all server messages and handling them
        '''
        print('[DEBUG]:: receiveMessage')
        while True:
            try:
                message = await connection.recv()
                # myToken = int.from_bytes(message[2:6] , 'little')
                if  tokenNo in DataDict.keys():
                    # selected = DataGrid.focus()
                    # DataGrid.item(selected , 'values')
                    # print(f'DataDictionary index: {DataDict[myToken]}')
                    if int.from_bytes(message[2:6] , 'little') in DataDict.keys():
                        DataGrid.item(DataDict[int.from_bytes(message[2:6] , 'little')] ,values=(int.from_bytes(message[2:6] , 'little') , 
                            int.from_bytes(message[6:10] , 'little')/100 , 
                            int.from_bytes(message[10:14] , 'little'), 
                            int.from_bytes(message[14:18] , 'little')/100 ,
                            int.from_bytes(message[18:22] , 'little') ,
                            int.from_bytes(message[22:26] , 'little') ,
                            int.from_bytes(message[26:30] , 'little') ,
                            int.from_bytes(message[30:34] , 'little')/100 ,
                            int.from_bytes(message[34:38] , 'little')/100 ,
                            int.from_bytes(message[38:42] , 'little') /100,
                            int.from_bytes(message[42:46] , 'little')/100 ,
                            (datetime.datetime.fromtimestamp(int(datetime.datetime(1980, 1,1,0,0).timestamp()) + 
                                int.from_bytes(message[46:50] , 'little'))).strftime('%d-%m-%Y') ,
                            int.from_bytes(message[50:54] , 'little') /100,
                            int.from_bytes(message[54:58] , 'little') /100,
                            int.from_bytes(message[58:62] , 'little') ,
                            int.from_bytes(message[62:66] , 'little')/100))

                else :
                    DataDict.update({tokenNo : idx})
                    print(f'DataDictionary updated... {tokenNo} and \n{DataDict}')
                    
            except Exception as e:
                print('receiveMessage Connection with server closed')
                break

    async def heartbeat(self, connection , tokenNo):
        '''
        Sending heartbeat to server every 5 seconds
        Ping - pong messages to verify connection is alive
        '''
        print('[DEBUG]:: heartbeat')
        try:
            await connection.send(f"{self.sessionID}_rahul@thecodesure.com_{tokenNo}")
            print('Messsage Sent')
        except websockets.exceptions.ConnectionClosed:
            print('hearbeat Connection with server closed')


class AutocompleteCombobox(Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(INSERT), END)
                        self.position = self.index(END)
                if event.keysym == "Left":
                        if self.position < self.index(END): # delete the selection
                                self.delete(self.position, END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, END)
                if event.keysym == "Right":
                        self.position = self.index(END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()


if __name__ == "__main__":
    readCSFunction() , WebSocketClient() , AutocompleteCombobox()