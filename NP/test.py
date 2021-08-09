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

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # print(event.src_path)
        if event.src_path == event.src_path :
            stringVar.set(event.src_path)
        else :
            print("Kya bhai, kya change krr diya")

def myThread():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
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
        self.label = Label(self , textvariable=var2)
        self.label.pack()
        t = Thread(target=myThread)
        t.start()
        

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("MyUniqueTitle")
        self.protocol("WM_DELETE_WINDOW" , self.onDelete)
    
    def onDelete(self ):
        if askokcancel("Quit" , "Are you sure you want to exit !!"):    
            global run 
            run  = False
            # try:
            #     if showinfo("Info","Server connection closed "):  
            #         self.destroy()
            # except :
            self.destroy()


if __name__ == "__main__":
    app = App()
    AppFrame(app)
    app.mainloop()