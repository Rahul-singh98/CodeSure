from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

a = None
expression= None
b = None

class EntryWidget(Toplevel):
    def __init__(self  , parent):
        super().__init__()
        self.parent = parent
        self.geometry('300x300')
        self.title('Custom Columns')
        self.entryData = StringVar()
        self.entry = Entry(self , textvariable=self.entryData)
        self.button = Button(self , text="submit" , command=self.submit)
        self.button.grid(row= 2 , column=1)
        self.entry.grid(row=1 , column=1)

    def submit(self ):
        global expression ,a , b
        expression = self.entryData.get()
        print(expression)
        a , expression , b = expression.split(" ")
        self.destroy()
        return True


class rootFrame(Frame):
    def __init__(self , parent):
        super().__init__()
        self.tree = Treeview(parent, columns=("size", "modified"))
        self.tree["columns"] = ("Open", "High", "Low" ,"Close")

        self.tree.column("#0",   width=100, anchor='center')
        self.tree.column("Open", width=100, anchor='center')
        self.tree.column("High", width=100, anchor='center')
        self.tree.column("Low",  width=100, anchor='center')
        self.tree.column("Close",  width=100, anchor='center')

        self.tree.heading("#0",   text="Name")
        self.tree.heading("Open", text="Open")
        self.tree.heading("High", text="High")
        self.tree.heading("Low",  text="Low")
        self.tree.heading("Close",  text="Close")

        self.tree.insert("","end", text = "X",
                         values = (10 , 13 , 6 , 9))
        self.tree.insert("","end", text = "Y" ,
                         values = (15 , 16, 6, 62))
        self.tree.insert("","end", text = "Z",
                         values = (16 , 25 ,9 , 12))

        self.tree.pack()

        self.tree.bind("<Button-3>" , self.showEntry)

    def showEntry(self , event):
        print(EntryWidget(self))

    def add_column(self, columns, **kwargs):
        global a , expression , b
        current_columns = list(self.tree['columns'])
        current_columns = {key:self.tree.heading(key) for key in current_columns}

        self.tree['columns'] = list(current_columns.keys()) + list(columns)
        for key in columns:
            self.tree.heading(key, text=key, **kwargs)

        for key in current_columns:
            state = current_columns[key].pop('state')
            self.tree.heading(key, **current_columns[key])

        for i in self.tree.get_children():
            item = self.tree.item(i)
            data = item['values']
            self.tree.item(i , values = (data[0], data[1] , data[2] , data[3] , data[a] + expression + data[b]))

class App(Tk):
    def __init__(self):
        super().__init__()
        width = 1100
        height = 250
        self.geometry(f'{width}x{height}')
      
if __name__ == "__main__":
    app = App()
    rootFrame(app)
    app.mainloop()