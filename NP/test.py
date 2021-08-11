import os
import pandas as pd 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from threading import Thread

observer = None
stringVar = None
run = True
cols = [i for i in range(27)]
df = pd.read_csv('./0809AUTOTRD.txt' , names = cols)
data = dict()
price = dict()
temp = dict()
temp2 = dict()
users = [i for i in df[17].unique()]

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == "./samplefile.txt" :
            stringVar.set(event.src_path)
        else :
            print(event.src_path)
            print("Kya bhai, kya change krr diya")

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


class AppFrame(Frame):
    def __init__(self , container):
        super().__init__(container)
        global stringVar 
        stringVar = StringVar()
        var2 = StringVar()
        self.combo_list = Listbox(container , selectmode='multiple')
        for i in df[17].unique():
            self.combo_list.insert(END , i)
        # self.combo_list.bind("<<ComboboxSelected>>" , self.ComboSeleted)
        self.combo_list.pack()

        self.butn = Button(container , text="Add user" , command=self.addUser)
        self.butn.pack()

        # self.lab = Label(container , text ="hello")
        # self.lab.pack()
        # self.label = Label(container , textvariable=stringVar)
        # self.label.pack()
        # t = Thread(target=myThread)
        # t.start()

    def addUser(self):
        global users
        cur = self.combo_list.curselection()

        for i in cur:
            if self.combo_list.get(i) not in users:
                users.append(self.combo_list.get(i))    
        
        for user in users:
            pass
        
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("MyUniqueTitle")
        self.geometry('500x300')
        self.protocol("WM_DELETE_WINDOW" , self.onDelete)
    
    def onDelete(self ):
        if askokcancel("Quit" , "Are you sure you want to exit !!"):    
            global run 
            run  = False
            self.destroy()


if __name__ == "__main__":
    app = App()
    AppFrame(app)
    app.mainloop()

# from tkinter import *
  
# window = Tk()
# window.title('Multiple selection')
  
# # for scrolling vertically
# yscrollbar = Scrollbar(window)
# yscrollbar.pack(side = RIGHT, fill = Y)
  
# label = Label(window,
#               text = "Select the languages below :  ",
#               font = ("Times New Roman", 10), 
#               padx = 10, pady = 10)
# label.pack()
# list = Listbox(window, selectmode = "multiple", 
#                yscrollcommand = yscrollbar.set)
  
# # Widget expands horizontally and 
# # vertically by assigning both to
# # fill option
# list.pack(padx = 10, pady = 10,
#           expand = YES, fill = "both")
  
# x =["C", "C++", "C#", "Java", "Python",
#     "R", "Go", "Ruby", "JavaScript", "Swift",
#     "SQL", "Perl", "XML"]
  
# selValues = []
# def do():
#     cs = list.curselection()
#     for i in cs:
#         selValues.append(list.get(i))
#     print(selValues)

# for each_item in range(len(x)):
      
#     list.insert(END, x[each_item])
#     list.itemconfig(each_item, bg = "lime")

# but1 = Button(window , text='submit' , command=do)
# but1.pack(padx = 10, pady = 10,
#           expand = YES, fill = "both")


# # Attach listbox to vertical scrollbar
# yscrollbar.config(command = list.yview)
# window.mainloop()
# print(selValues)