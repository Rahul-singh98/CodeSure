from tkinter import *
from tkinter.ttk import * 
from tkinter.messagebox import *
import datetime
import time
import pandas as pd
import os 
from utility import *
from utilFrames import *
from threading import Thread

df , eq_df = readCSFunction()
eq_script_list =sorted(eq_df['Script'].dropna().unique().tolist())

new_df = pd.DataFrame()
new_df1 = pd.DataFrame()
new_df2 = pd.DataFrame()
new_df3 = pd.DataFrame()

idx = 0
DataDict = dict()
script_list =sorted(df['Script'].dropna().unique().tolist())
strategy_list = ['Butterfly']
ratio_list = ['121' ,'143']

bg_color = None
lst = [['Script Name'  ,'Price'  ]]
script_name,  val = '' , 0 

client = WebSocketClient()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop = asyncio.get_event_loop()
connection = loop.run_until_complete(client.connect())

class AddContract(Toplevel):
    def __init__(self,container):
        super().__init__(container)
        # self.DataDict = dict()
        self.geometry('560x200+300+300')
        self.title('Add Contract')
        self.resizable(False , False)
        options = {'padx': 10, 'pady': 5}

        self.var = StringVar()
        style = Style()
        style.map('TCombobox' , fieldbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectforeground=[('readonly' , 'black')])

        self.exchangeLabel = Label(self , text='Exchange')
        self.exchangeCombo =  Combobox(self, values=['NSE'])
        self.exchangeCombo.current(0)
        self.exchangeCombo['state'] = 'readonly'

        self.segmentLabel = Label(self , text='Segment')
        self.segmentCombo = Combobox(self ,textvariable=self.var, values=['Equity' , 'Futures' , 'Options'])
        self.segmentCombo.current(0)
        self.segmentCombo.bind('<<ComboboxSelected>>', self.change_frame )
        self.segmentCombo['state'] = 'readonly'

        self.exchangeLabel.grid(column=0 , row=0 ,sticky=W, **options )
        self.exchangeCombo.grid(column=1 , row=0 ,sticky=W , **options)
        self.segmentLabel.grid(column=2 , row=0 ,sticky=W , **options)
        self.segmentCombo.grid(column=3 , row=0 ,sticky=W , **options)

        self.frames = {}

        self.frames['Futures'] = FuturesFrame(self , 'Futures')
        self.frames['Options'] = OptionsFrame(self , 'Options')
        self.frames['Equity'] = EquityFrame(self , 'Equity')

        self.add_button = Button(self , text='Add',command=self.add)
        self.add_button.grid(column=0 , row=3 ,columnspan=4 , sticky=W+E+N+S , **options )

    def change_frame(self , event):
        frame = self.frames[str(self.var.get())]
        for f in self.frames.values():
        	if f == frame:
        		f.grid(column=0 , row=1 , columnspan=4 ,padx=0 , pady = 5 )
        	else:
        		f.grid_forget()
        frame.tkraise()
        
    def fileReceive(self , tokenNo , idx , DataGrid , DataDict):
    #     client = WebSocketClient()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        connection = loop.run_until_complete(client.connect())
        # Start listener and heartbeat 
        tasks = [
            asyncio.ensure_future(client.heartbeat(connection , tokenNo)),
            asyncio.ensure_future(client.receiveMessage(connection, tokenNo, DataGrid ,idx , DataDict)),
        ]

        try:
            loop.run_until_complete(asyncio.wait(tasks) )
        except Exception as e  :
            print(f"Coroutine error {e}")
        finally:
            loop.close()
            loop.stop()

    def add(self):
        try:
            del(new_df)
            del(new_df1)
            del(new_df2)
        except Exception as e:
            pass

        global new_df3
        new_df3 = new_df3.reset_index(drop=True )
        
        self.rootNotebook = self.master.winfo_children()[1]

        self.DataGrid = self.rootNotebook.winfo_children()[1].winfo_children()[0]
        token = new_df3.loc[0 , 'Token No']
        global idx
        global DataDict
        self.DataGrid.insert(parent="" , index=idx ,iid = idx, values=(0 ,0,0 ,0,0 ,0,0 ,0,0 ,0,0 ,0,0 ,0,0 ,0 ))

        # self.display_notebook.add(self.nifty_tab , text=f"{new_df3['Script'].unique()[0]}")
        # self.ltpLabel = Label(self.nifty_tab)
        # self.ltpLabel.pack()
        # self.display_notebook.pack()

        # self.contract_frame = self.rootNotebook.winfo_children()[0]
        # global script_name  ,val ,lst
        # lst.append([script_name ,val  ])
        # for i in range(len(lst)):
        #     for j in range(len(lst[0])):
        #         self.entry = Entry(self.contract_frame , width=16 , font=('Arial' , 10 , 'bold'))
        #         self.entry.grid(row=i+3 , column=j ,sticky=N+S+E+W)
        #         self.entry.insert(END , lst[i][j])
        
        # await asyncio.gather(self.fileReceive(token , idx))
        guiThread = Thread(target=self.fileReceive , args=[token , idx , self.DataGrid ,DataDict ])
        guiThread.start()
        # guiThread.join()
        idx+=1
        self.destroy()
        
class RootFrames(Frame):
    def __init__(self , container):
        super().__init__(container)
        self.notebook = Notebook(container , width= container.winfo_screenwidth() , height=container.winfo_screenheight())
        self.notebook.place(x=0 , y=0)
        self.contract_tab = Frame(self.notebook)
        self.display_tab = Frame(self.notebook )
        options = {'padx':10 , 
                    'pady':10 }

        self.add_contract = Button(self.contract_tab , text='ADD CONTRACT',command=lambda :AddContract(container))
        self.add_contract.grid(column=0 , row=0 ,**options)

        self.show_open_contracts = Frame(self.contract_tab)
        self.show_open_contracts.grid(column=0 ,columnspan=15, row=1 , **options)

        self.DataGrid = Treeview(self.display_tab , height=self.display_tab.winfo_screenheight() )
        self.DataGrid['columns'] = ['Token No' , 'LTP' ,'LTQ' ,'ATP' ,'VolTraded' ,'BuyQty' , 
        'SellQty' ,'Open' , 'High' , 'Low' , 'Close' ,'LTT' ,'Bid' , 'Ask' ,'OI' , 'Spot']
        self.DataGrid.column('#0', width=0 , stretch=NO)
        self.DataGrid.column('Token No', anchor=CENTER, width=80)
        self.DataGrid.column('LTP', anchor=CENTER, width=80)
        self.DataGrid.column('LTQ', anchor=CENTER, width=80)
        self.DataGrid.column('ATP', anchor=CENTER, width=80)
        self.DataGrid.column('VolTraded', anchor=CENTER, width=80)
        self.DataGrid.column('BuyQty', anchor=CENTER, width=80)
        self.DataGrid.column('SellQty', anchor=CENTER, width=80)
        self.DataGrid.column('Open', anchor=CENTER, width=80)
        self.DataGrid.column('High', anchor=CENTER, width=80)
        self.DataGrid.column('Low', anchor=CENTER, width=80)
        self.DataGrid.column('Close', anchor=CENTER, width=80)
        self.DataGrid.column('LTT', anchor=CENTER, width=80)
        self.DataGrid.column('Bid', anchor=CENTER, width=80)
        self.DataGrid.column('Ask', anchor=CENTER, width=80)
        self.DataGrid.column('OI', anchor=CENTER, width=80)
        self.DataGrid.column('Spot', anchor=CENTER, width=80)
        
        self.DataGrid.heading('#0', anchor=CENTER , text="")
        self.DataGrid.heading('Token No', anchor=CENTER, text='Token No')
        self.DataGrid.heading('LTP', anchor=CENTER, text='LTP')
        self.DataGrid.heading('LTQ', anchor=CENTER, text='LTQ')
        self.DataGrid.heading('ATP', anchor=CENTER, text='ATP')
        self.DataGrid.heading('VolTraded', anchor=CENTER, text='VolTraded')
        self.DataGrid.heading('BuyQty', anchor=CENTER, text='BuyQty')
        self.DataGrid.heading('SellQty', anchor=CENTER,text='SellQty' )
        self.DataGrid.heading('Open', anchor=CENTER, text='Open')
        self.DataGrid.heading('High', anchor=CENTER, text='High')
        self.DataGrid.heading('Low', anchor=CENTER, text='Low')
        self.DataGrid.heading('Close', anchor=CENTER, text='Close')
        self.DataGrid.heading('LTT', anchor=CENTER, text='LTT')
        self.DataGrid.heading('Bid', anchor=CENTER, text='Bid')
        self.DataGrid.heading('Ask', anchor=CENTER, text='Ask')
        self.DataGrid.heading('OI', anchor=CENTER, text='OI')
        self.DataGrid.heading('Spot', anchor=CENTER, text='Spot')
        
        self.DataGrid.pack()
        self.contract_tab.pack()
        self.display_tab.pack()

        self.notebook.add(self.contract_tab , text='General')
        self.notebook.add(self.display_tab , text='Watch')


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('CodeSure Software Solution Pvt Ltd')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{width}x{height}')
        titleImage = PhotoImage(file = '../Data/CodeSurelogo.png')
        self.iconphoto(True , titleImage)
        self.protocol("WM_DELETE_WINDOW", on_closing)

def on_closing():
    try:
        loop = asyncio.get_event_loop()
        loop.close()
        loop.stop()
    except Exception as e:
        print("HEre is EXceptions : "  , e)

if __name__ == "__main__":
    app = App()
    RootFrames(app)
    app.mainloop()
