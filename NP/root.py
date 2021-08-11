import os
import pandas as pd 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import * 
from tkinter.messagebox import *
from threading import Thread

observer = None
stringVar = None
run = True
cols = [i for i in range(27)]
df = pd.read_csv('./0809AUTOTRD.txt' , names = cols)
users = [i for i in df[17].unique()]
remUsers = []
data = dict()
price = dict()
temp = dict()
temp2 = dict()
idx = 0

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == "./samplefile.txt" :
            stringVar.set(event.src_path)
        else :
            print(event.src_path)

def myThread():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=True)
    observer.start()
    try:
        while run:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()


class AddUser(Toplevel):
    def __init__(self,container , tree):
        super().__init__(container)
        global users
        self.tree = tree
        self.geometry('500x300+300+300')
        self.title('Add User')
        self.resizable(False , False)
        options = {'padx': 10, 'pady': 5}

        self.info = Label(self ,text='To add users select from below list :')
        self.info.pack(expand=True , fill='both')

        self.listUsers = Listbox(self , selectmode='multiple')
        for i in users:
            self.listUsers.insert(END , i)
        
        self.listUsers.pack(expand=True , fill='both' )
        self.submit = Button(self , text='Add' , command=self.listSelected)
        self.submit.pack(expand=True)
    
    def listSelected(self):
        global users
        global remUsers
        cur = self.listUsers.curselection()

        for i in cur:
            v = self.listUsers.get(i)
            remUsers.append(v)
            users.remove(v)      

        updateTree(self.tree)
        self.destroy()

def updateTree(tree):
    children = tree.get_children()
    for child in children:
        tree.delete(child)

    global idx
    for user in remUsers:
        df1 = df[df[17]==user]
        contracts = [i for i in df1[7].unique()]
        for cont in contracts:
            df2= df1[df1[7]==cont]
            for each , row in df2.iterrows():
                if row[13]== 2:
                    temp[cont] = row[14]
                    try:
                        data[user][cont] -= temp[cont] 
                    except:
                        data[user] = temp
                else :
                    temp[cont] = row[14]
                    try:
                        data[user][cont] += temp[cont] 
                    except:
                        data[user] = temp
            temp2[cont] = df2[15].mean()
            price[user] = temp2

    for user in remUsers:
        for cont in data[user]:
            if data[user][cont] >0:
                p =  price[user][cont]
                q = data[user][cont]
                tree.insert(parent="" ,index=idx , values=(user , cont , q ,p ,q*p ))
                idx+=1

class DeleteUser(Toplevel):
    def __init__(self,container , tree):
        super().__init__(container)
        global remUsers
        self.tree = tree
        self.geometry('500x300+300+300')
        self.title('Add Contract')
        self.resizable(False , False)
        options = {'padx': 10, 'pady': 5}

        self.info = Label(self ,text='To delete users select from below list :')
        self.info.pack(expand=True , fill='both')

        self.listUsers = Listbox(self , selectmode='multiple')
        for i in remUsers:
            self.listUsers.insert(END , i)
        
        self.listUsers.pack(expand=True  , fill='both')
        self.submit = Button(self , text='Delete' , command=self.listSelected)
        self.submit.pack(expand=True , fill='both')
    
    def listSelected(self):
        global users
        global remUsers
        cur = self.listUsers.curselection()

        for i in cur:
            v = self.listUsers.get(i)
            users.append(v)
            remUsers.remove(v)

        updateTree(self.tree)
        self.destroy()
        
class RootFrames(Frame):
    def __init__(self , container):
        super().__init__(container)
        self.notebook = Notebook(container , width= container.winfo_screenwidth() , height=container.winfo_screenheight()-90)
        self.notebook.place(x=0 , y=0)
        self.general_tab = Frame(self.notebook)
        self.display_tab = Frame(self.notebook , height=self.notebook.winfo_screenheight())
        options = {'padx':10 , 
                    'pady':10 }

        self.add_user = Button(self.general_tab , text='ADD USER',command=lambda :AddUser(container , self.DataGrid))
        self.delete_user = Button(self.general_tab , text="Delete User" , command=lambda : DeleteUser(container , self.DataGrid))
        self.add_user.grid(column=0 , row=0 ,**options)
        self.delete_user.grid(column=1 , row=0 ,**options)

        self.DataGrid = Treeview(self.display_tab , height=self.display_tab.winfo_screenheight())

        self.scrollBarY = Scrollbar(self.display_tab  , orient='vertical' , command=self.DataGrid.yview)
        self.scrollBarY.pack(side='right', fill="y" )


        self.scrollBarX = Scrollbar(self.display_tab  , orient='horizontal' , command=self.DataGrid.xview)
        self.scrollBarX.pack(side='bottom' ,fill="x" )
        self.DataGrid.configure(xscrollcommand=self.scrollBarX.set , yscrollcommand=self.scrollBarY.set)

        self.DataGrid['columns'] = ["User" , 'Contracts' ,'Quantity' ,'Price' ,'Position']
        self.DataGrid.column('#0', width=0 , stretch=NO)
        self.DataGrid.column('User', anchor=CENTER, width=80)
        self.DataGrid.column("Contracts" ,anchor=CENTER , width=200)
        self.DataGrid.column('Quantity', anchor=CENTER, width=100)        
        self.DataGrid.column('Price', anchor=CENTER, width=100)
        self.DataGrid.column('Position', anchor=CENTER, width=80)
        
        self.DataGrid.heading('#0', anchor=CENTER , text="")
        self.DataGrid.heading('User' , anchor=CENTER ,text ='User')
        self.DataGrid.heading('Contracts' , anchor=CENTER ,text ='Contracts')
        self.DataGrid.heading('Quantity' , anchor=CENTER ,text ='Quantity')
        self.DataGrid.heading('Price', anchor=CENTER, text='Price')
        self.DataGrid.heading('Position', anchor=CENTER, text='Position')

        self.DataGrid.pack(side='left' , fill='both' , expand=True)        
        self.general_tab.pack()
        self.display_tab.pack()

        self.notebook.add(self.general_tab , text='General')
        self.notebook.add(self.display_tab , text='Watch')

        # self.url = "ws://122.160.79.135:10771/Broadcast"
        # global client 
        # global sessionID
        # client = create_connection(self.url ,timeout=21650000)
        # sessionID = client.recv()
        # client.send(f'{sessionID}_rahul@thecodesure.com_159753')
        # myThread = Thread(target=recvMessage , args=[self.DataGrid] )
        # myThread.start()

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
        t = Thread(target=myThread)
        t.start()
    
    def onDelete(self ):
        if askokcancel("Quit" , "Are you sure you want to exit !!"):    
            global run 
            run  = False
            self.destroy()
        
if __name__ == "__main__":
    app = App()
    RootFrames(app)
    app.mainloop()