from tkinter import *
from tkinter.font import Font
from tkinter.ttk import * 
from tkinter.messagebox import *
import os 
from utility import *
import numpy as np
import time
import sys
from websocket import create_connection
from threading import *

df , eq_df = readCSFunction()
eq_script_list =sorted(eq_df['Script'].dropna().unique().tolist())

new_df = pd.DataFrame()
new_df1 = pd.DataFrame()
new_df2 = pd.DataFrame()
new_df3 = pd.DataFrame()
canvasList=dict()

idx = 0
DataDict = dict()
script_list =sorted(df['Script'].dropna().unique().tolist())
strategy_list = ['Butterfly']
ratio_list = ['121' ,'143']

bg_color = None
lst = [['Script Name'  ,'Price'  ]]
script_name,  val = '' , 0 
client =None
sessionID = ""

class FuturesFrame(LabelFrame):
    def __init__(self , container , seg_selec):
        super().__init__(container)
        self['text'] = f'{seg_selec}'
        style = Style()
        style.map('TCombobox' , fieldbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectforeground=[('readonly' , 'black')])
        
        self.label_instrument = Label(self , background=bg_color , text='Instrument')
        self.combo_instrument = Combobox(self  , values=['FUTIDX' , 'FUTSTK'])
        self.combo_instrument['state'] = 'readonly'
        self.combo_instrument.bind('<<ComboboxSelected>>' , self.comboInstrument_selected) 

        self.label_script = Label(self , background=bg_color , text='Script')
        self.combo_script = AutocompleteCombobox(self)
        self.combo_script['state'] = 'readonly'
        self.combo_script.bind('<<ComboboxSelected>>' , self.comboScript_selected)

        self.label_expiry = Label(self , text='Expiry' , background=bg_color )
        self.combo_expiry = Combobox(self)
        self.combo_expiry['state'] = 'readonly'
        self.combo_expiry.bind('<<ComboboxSelected>>' , self.comboExpiry_selected)

        self.radio_button = Radiobutton(self , background=bg_color , text='Get data for all list values' , command = self.radioButtonChecked)

        self.label_instrument.grid(column=0 , row=0)
        self.combo_instrument.grid(column=1 , row=0 , padx=5,pady=5)

        self.label_script.grid(column=2 , row=0)
        self.combo_script.grid(column=3 , row=0 , padx=5,pady=5)

        self.label_expiry.grid(column=0 , row=1)
        self.combo_expiry.grid(column=1 , row=1, pady = 5 , padx = 5)

        self.radio_button.grid(column=3 , row=1,padx=5 , pady=5)

        self.grid(column=0 , row=1 , columnspan=4 , padx=5 , pady=5)
        self.grid_forget()
        
    def callback(self , var , idx , mode):
        try:
            if var.get() <= 0:
                print()
            else :
                var.get() 
        except :
            showerror('Error','Gap/Center cannot be zero or negative')

    def comboInstrument_selected(self ,event):
        self.instrument = event.widget.get()
        global new_df
        global new_df1
        global new_df3
        new_df = df[df['Instrument'] == self.instrument]
        new_df1 = new_df
        self.combo_script.set_completion_list(sorted(new_df['Script'].unique().tolist()))
        self.combo_expiry['values'] = sorted(np.unique([str(x).split(' ')[0] for x in new_df.sort_values(by='Expiry')['Expiry'].tolist()]).tolist())

    def comboScript_selected(self ,event):
        self.script_name = event.widget.get()
        global new_df
        global new_df1
        global script_name 
        script_name = self.script_name
        new_df1 = new_df[new_df['Script']==self.script_name]
        self.combo_expiry['values'] = sorted(np.unique([str(x).split(' ')[0] for x in new_df1.sort_values(by='Expiry')['Expiry'].tolist()]).tolist())

    def comboExpiry_selected(self ,event):
        self.exp = event.widget.get()
        global new_df3
        global new_df1
        try :
            new_df3 = new_df1[new_df1['Expiry']==self.exp]
            
        except:
            showerror('Please Select the Expiry correctly !!! ') 
    
    def radioButtonChecked(self):
        global new_df
        global new_df3
        try:
            new_df3 = new_df[new_df['Expiry']==self.exp]
        except :
            showerror("Select previous options")

class EquityFrame(LabelFrame):
    def __init__(self , container , seg_selec ):
        super().__init__(container)
        self['text'] = f'{seg_selec}'
        
        style = Style()
        style.map('TCombobox' , fieldbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectforeground=[('readonly' , 'black')])
        
        self.label_instrument = Label(self , background=bg_color , text='Instrument')
        self.combo_instrument = Combobox(self  , values=['EQ'])
        self.combo_instrument['state'] = 'readonly'
        self.combo_instrument.set('EQ') 

        self.label_script = Label(self , background=bg_color , text='Script')
        self.combo_script = AutocompleteCombobox(self)
        self.combo_script.set_completion_list(eq_script_list)
        self.combo_script.bind('<<ComboboxSelected>>' , self.comboScript_selected)

        self.radio_button = Radiobutton(self , background=bg_color , text='Range' , command = self.radioButtonChecked)
        self.label1_ = Label(self , background=bg_color)

        self.label2 = Label(self , background=bg_color)
        self.label2_ = Label(self , background=bg_color)
        
        self.label3 = Label(self , background=bg_color)
        self.label3_ = Label(self , background=bg_color)
        
        self.label_instrument.grid(column=0 , row=0)
        self.combo_instrument.grid(column=1 , row=0 , padx=5,pady=5)

        self.label_script.grid(column=2 , row=0)
        self.combo_script.grid(column=3 , row=0 , padx=5,pady=5)

        self.radio_button.grid(column=0 , row=1)
        self.label1_.grid(column=1 , row=1 , pady = 5 , padx = 5)

        self.label2.grid(column=2 , row=1)
        self.label2_.grid(column=3 , row=1, pady = 5 , padx = 5)

        self.label3.grid(column=0 , row=2)
        self.label3_.grid(column=1 , row=2, pady = 5 , padx = 5)
        self.grid(column=0 , row=1 , columnspan=4 ,padx=0 , pady = 5 )

    def comboScript_selected(self , event):
        self.script_name = event.widget.get()
        global new_df3
        global script_name 
        script_name = self.script_name
        new_df3 = eq_df[eq_df['Script']==self.script_name]
        
    def radioButtonChecked(self ):
    	self.stringVar = StringVar()
    	self.label_startwith = Label(self, text='Start')
    	self.combo_startwith = Combobox(self , textvariable=self.stringVar)
    	self.alphabet_values = [chr(alb) for alb in range(ord('A') , ord('Z')+1)]
    	self.combo_startwith['values'] = self.alphabet_values
    	self.combo_startwith.bind("<<ComboboxSelected>>" , self.startswithSelected)

    	self.label_startwith.grid(column=2 , row=1)
    	self.combo_startwith.grid(column=3 , row=1, pady = 5 , padx = 5)

    def startswithSelected(self , event):
    	self.stringVar_end = StringVar()
    	self.label_endwith = Label(self, text='End')
    	self.combo_endwith = Combobox(self , textvariable=self.stringVar_end)
    	self.combo_endwith['values'] = self.alphabet_values[self.alphabet_values.index(self.combo_startwith.get())+1 :]
    	self.combo_endwith.bind("<<ComboboxSelected>>" , self.endswithSelected)

    	self.label_endwith.grid(column=0 , row=2)
    	self.combo_endwith.grid(column=1 , row=2, pady = 5 , padx = 5)

    def endswithSelected(self , event):
    	global new_df3
    	global scrip_name 
    	script_name = "List of values Selected"

    	new_df3 = eq_df[eq_df['Script'].str.contains(f'^[{self.combo_startwith.get()}-{self.combo_endwith.get()}].*' , regex=True)]

class OptionsFrame(LabelFrame):
    def __init__(self , container , seg_selec):
        super().__init__(container)
        self['text'] = f'{seg_selec}'
        style = Style()
        style.map('TCombobox' , fieldbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectforeground=[('readonly' , 'black')])
        
        self.label_instrument = Label(self , background=bg_color , text='Instrument')
        self.combo_instrument = Combobox(self  , values=['OPTIDX' , 'OPTSTK'])
        self.combo_instrument['state'] = 'readonly'
        self.combo_instrument.bind('<<ComboboxSelected>>' , self.comboInstrument_selected) 

        self.label_script = Label(self , background=bg_color , text='Script')
        self.combo_script = AutocompleteCombobox(self)
        self.combo_script['state'] = 'readonly'
        self.combo_script.bind('<<ComboboxSelected>>' , self.comboScript_selected)

        self.label_option = Label(self , text='Option Type', background=bg_color )
        self.combo_option = Combobox(self)
        self.combo_option['values'] = ['CE' ,'PE']
        self.combo_option['state'] = 'readonly'
        self.combo_option.bind('<<ComboboxSelected>>' , self.comboOption_selected)

        self.label_expiry = Label(self , text='Expiry' , background=bg_color )
        self.combo_expiry = Combobox(self)
        self.combo_expiry['state'] = 'readonly'
        self.combo_expiry.bind('<<ComboboxSelected>>' , self.comboExpiry_selected)

        self.label_lowerR = Label(self , text='Strike', background=bg_color )
        self.combo_lowerR = Combobox(self)
        self.combo_lowerR['state'] = 'readonly'
        self.combo_lowerR.bind('<<ComboboxSelected>>' , self.comboLowerR_selected)

        self.label_instrument.grid(column=0 , row=0)
        self.combo_instrument.grid(column=1 , row=0 , pady = 5 , padx= 5)

        self.label_script.grid(column=2 , row=0)
        self.combo_script.grid(column=3 , row=0 , pady = 5 , padx= 5)

        self.label_option.grid(column=0 , row=1)
        self.combo_option.grid(column=1 , row=1 , pady = 5 , padx = 5)

        self.label_expiry.grid(column=2 , row=1)
        self.combo_expiry.grid(column=3 , row=1, pady = 5 , padx = 5)

        self.label_lowerR.grid(column=0 , row=2)
        self.combo_lowerR.grid(column=1 , row=2, pady = 5 , padx = 5)
        
        self.grid(column=0 , row=1 , columnspan=4 , padx=5 , pady=5)
        self.grid_forget()

    def callback(self , var , idx , mode):
        try:
            if var.get() <= 0:
                print()
            else :
                var.get() 
        except :
            showerror('Error','Gap/Center cannot be zero or negative')

    def comboInstrument_selected(self ,event):
        self.instument = event.widget.get()
        global new_df
        new_df = df[df['Instrument'] == self.instument]
        self.combo_script.set_completion_list(sorted(new_df['Script'].unique().tolist()))

    def comboScript_selected(self ,event):
        self.script_name = event.widget.get()
        global new_df
        global script_name 
        script_name = self.script_name
        new_df = df[df['Script']==self.script_name]

    def comboOption_selected(self ,event):
        self.option = event.widget.get()
        global new_df
        global new_df1
        try :
            new_df1 = new_df[new_df['Type'] == self.option]
            self.combo_expiry['values'] = sorted(np.unique([str(x).split(' ')[0] for x in new_df1.sort_values(by='Expiry')['Expiry'].tolist()]).tolist())
        except :
            showerror("Please select the Script Correctly !!! ")

    def comboExpiry_selected(self ,event):
        self.exp = event.widget.get()
        global new_df1
        global new_df2
        try :
            new_df2 = new_df1[new_df1['Expiry']==self.exp]
            self.combo_lowerR['values'] = sorted(new_df2['Price'].tolist())

        except:
            showerror('Please the Expiry correctly !!! ')

    def comboLowerR_selected(self ,event):
        global val
        global new_df3
        global new_df3
        self.val = event.widget.get()
        new_df3 = new_df2[new_df2['Price'] == int(self.val)] 


class AddContract(Toplevel):
    def __init__(self,container ):
        super().__init__(container)
        self.geometry('560x200+300+300')
        self.title('Add Contract')
        self.resizable(False , False)
        self.client = client
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
        
    def sendToken(self , tokenList):
        for token in tokenList:
            client.send(f'{sessionID}_rahul@thecodesure.com_{token}')


    def add(self):
        try:
            global new_df , new_df1 , new_df2
            del(new_df)
            del(new_df1)
            del(new_df2)
        except Exception as e:
            pass

        global new_df3
        if new_df3.empty:
            showerror("Try Again")
            self.destroy()

        else:
            new_df3 = new_df3.reset_index(drop=True)
            self.rootNotebook = self.master.winfo_children()[1]
            self.DataGrid = self.rootNotebook.winfo_children()[1].winfo_children()[0]
            token_list = new_df3['Token No'].to_list()
            script_list = new_df3['Script'].to_list()
            iType = new_df3['Type'].unique()[0]

            if new_df3['Type'].unique() !='EQ':
                inst =new_df3['Instrument'].unique()[0]
                exp = new_df3['Expiry'].unique()[0]
                           
            else :
                inst = "XX"
                exp = 'XX'
                iType = 'XX'
            global idx
            global DataDict
            for i in range(len(script_list)):
                self.DataGrid.insert(parent="" , index=token_list[i] ,iid = token_list[i], values=( token_list[i] ,script_list[i] ,inst ,exp,iType,0 ,0,0 ,0,0 ,0,0 ,0,0 ,0,0 ,0,0 ,0 ,0))
                _canvas = Canvas(self.DataGrid,background="#1818b8",
                                 borderwidth=0,
                                 highlightthickness=0)
                _canvas.text = _canvas.create_text(0,0,fill='#050505' , anchor='nw')
                canvasList.update({token_list[i]:_canvas})
                idx+=1

            self.sendToken(token_list)
            new_df3 = pd.DataFrame()
            self.destroy()

run = True
def recvMessage(DataGrid , _canvasList , _font):
    while run:  
        try:
            message = client.recv()
            if type(message)== str:
                pass
            else :
                n = int.from_bytes(message[:2],'little')
                message = message[2:]
                child = DataGrid.get_children()

                val = []
                for i in range(0,len(message),4):
                    val.append(int.from_bytes(message[i:i+4] ,'little'))
                for i in range(n):
                    val[i*16:(i*16)+16]
                    idx =i*16

                    if str(val[idx]) in child:
                        item = DataGrid.item(str(val[idx]))
                        _canvas = canvasList[val[idx]]
                        _canvas.place_forget()
                        bbox = DataGrid.bbox(str(val[idx]) , '#6')
                        if bbox == "":
                            continue
                        x ,y , height , width = bbox

                        _canvas.configure(width=height, height=width)
                        token , name ,inst ,exp , tp= item['values'][0:5]
                        if (val[idx+10]/100 > val[idx+1]/100):
                            _canvas.configure(bg='#b30517')
                        elif  val[idx+10]/100 < val[idx+1]/100:
                            _canvas.configure(bg='#2aa112')
                        else :
                            _canvas.configure(bg="#e6f8fa")
                        DataGrid.item(str(val[idx]) ,values=(token, name , inst, exp , tp,val[idx+1]/100 ,val[idx+2],val[idx+3]/100 ,val[idx+4] ,val[idx+5] ,val[idx+6] ,val[idx+7]/100 ,val[idx+8]/100 ,val[idx+9]/100,val[idx+10]/100 ,
                            (datetime.datetime.fromtimestamp(int(datetime.datetime(1980, 1,1,0,0).timestamp()) + val[idx+11])).strftime('%d-%m-%Y') ,val[idx+13] /100,val[idx+14]/100,val[idx+15]))

                        textw = _font.measure(val[idx+1]/100)
                        _canvas.coords(_canvas.text,15,3)
                        _canvas.itemconfigure(_canvas.text, text= str(val[idx+1]/100))
                        _canvas.place(in_=DataGrid , x=x , y=y)
        except Exception as e:
            # sys.exit()
            print('receiveMessage Connection with server closed: ' , e)
            break

    sys.exit()
        
class RootFrames(Frame):
    def __init__(self , container):
        super().__init__(container)
        self.notebook = Notebook(container , width= container.winfo_screenwidth() , height=container.winfo_screenheight()-90)
        self.notebook.place(x=0 , y=0)
        self.contract_tab = Frame(self.notebook)
        self.display_tab = Frame(self.notebook , height=self.notebook.winfo_screenheight())
        options = {'padx':10 , 
                    'pady':10 }

        self.add_contract = Button(self.contract_tab , text='ADD CONTRACT',command=lambda :AddContract(container))
        self.add_contract.grid(column=0 , row=0 ,**options)

        self.show_open_contracts = Frame(self.contract_tab)
        self.show_open_contracts.grid(column=0 ,columnspan=15, row=1 , **options)

        self.DataGrid = Treeview(self.display_tab ,selectmode='browse', height=self.display_tab.winfo_screenheight())

        self.scrollBarY = Scrollbar(self.display_tab  , orient='vertical' , command=self.DataGrid.yview)
        self.scrollBarY.pack(side='right', fill="y" )


        self.scrollBarX = Scrollbar(self.display_tab  , orient='horizontal' , command=self.DataGrid.xview)
        self.scrollBarX.pack(side='bottom' ,fill="x" )
        self.DataGrid.configure(xscrollcommand=self.scrollBarX.set , yscrollcommand=self.scrollBarY.set)

        self.DataGrid['columns'] = ["Token No" , 'Name' ,'Instrument' ,'Expiry' ,'Type' , 'LTP' ,'LTQ' ,'ATP' ,'VolTraded' ,'BuyQty' , 
        'SellQty' ,'Open' , 'High' , 'Low' , 'Close' ,'LTT' ,'Bid' , 'Ask' ,'OI' , 'Spot']
        self.DataGrid.column('#0', width=0 , stretch=NO)
        self.DataGrid.column('Token No', anchor=CENTER, width=80)
        self.DataGrid.column("Name" ,anchor=CENTER , width=150)
        self.DataGrid.column('Instrument', anchor=CENTER, width=100)        
        self.DataGrid.column('Expiry', anchor=CENTER, width=100)
        self.DataGrid.column('Type', anchor=CENTER, width=80)
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
        self.DataGrid.heading('Token No' , anchor=CENTER ,text ='Token No')
        self.DataGrid.heading('Name' , anchor=CENTER ,text ='Name')
        self.DataGrid.heading('Instrument' , anchor=CENTER ,text ='Instrument')
        self.DataGrid.heading('Expiry', anchor=CENTER, text='Expiry')
        self.DataGrid.heading('Type', anchor=CENTER, text='Type')
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

        self.DataGrid.pack(side='left')        
        self._font = Font()

        self.contract_tab.pack()
        self.display_tab.pack()

        self.notebook.add(self.contract_tab , text='General')
        self.notebook.add(self.display_tab , text='Watch')

        self.url = "ws://122.160.79.135:10771/Broadcast"

        global client 
        global sessionID
        client = create_connection(self.url ,timeout=21650000)
        sessionID = client.recv()
        client.send(f'{sessionID}_rahul@thecodesure.com_159753')
        myThread = Thread(target=recvMessage , args=[self.DataGrid , canvasList , self._font] )
        myThread.start()

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('CodeSure Software Solution Pvt Ltd')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{width}x{height}')
        titleImage = PhotoImage(file = '../Data/CodeSurelogo.png')
        self.iconphoto(True , titleImage)
        self.protocol("WM_DELETE_WINDOW" , self.onDelete)
    
    def onDelete(self ):
        if askokcancel("Quit" , "Are you sure you want to exit !!"):    
            global run 
            run  = False
            try:
                client.send(f'{sessionID}_rahul@thecodesure.com_147258') 
                if showinfo("Server connection closed "):  
                    self.destroy()

            except :
                self.destroy()
        
if __name__ == "__main__":
    app = App()
    RootFrames(app)
    app.mainloop()