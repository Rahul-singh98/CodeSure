from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import tkinter.font as tkFont

class rootFrame(Frame):
    def __init__(self , parent):
        super().__init__()
        self.tree = Treeview(parent)
        self.tree["columns"] = ("Open", "High", "Low" ,"Close")

        self.tree.column("#0",   width=100, anchor='center')
        self.tree.column("Open", width=100, anchor='center')
        self.tree.column("High", width=100, anchor='center')
        self.tree.column("Low",  width=100, anchor='center')
        self.tree.column("Close",  width=100, anchor='center')
        self.xscroll = Scrollbar(parent ,orient='horizontal' , command=self.tree.xview)
        self.yscroll = Scrollbar(parent ,orient='vertical', command=self.tree.yview)
        self.xscroll.pack(side='bottom' , fill='x')
        self.yscroll.pack(side='right' , fill='y')

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
        self.tree.insert("","end", text = "X",
                         values = (10 , 13 , 6 , 9))
        self.tree.insert("","end", text = "Y" ,
                         values = (15 , 16, 6, 62))
        self.tree.insert("","end", text = "Z",
                         values = (16 , 25 ,9 , 12))
        self.tree.insert("","end", text = "X",
                         values = (10 , 13 , 6 , 9))
        self.tree.insert("","end", text = "Y" ,
                         values = (15 , 16, 6, 62))
        self.tree.insert("","end", text = "Z",
                         values = (16 , 25 ,9 , 12))
        self.tree.insert("","end", text = "X",
                         values = (10 , 13 , 6 , 9))
        self.tree.insert("","end", text = "Y" ,
                         values = (15 , 16, 6, 62))
        self.tree.insert("","end", text = "Z",
                         values = (16 , 25 ,9 , 12))
        self.tree.pack(fill="both" , expand=True)

        self.tree.bind("<Button-3>" , self.showEntry)

    def showEntry(self , event):
        self.entryData = StringVar()
        self.entryColName = StringVar()
        top = Toplevel(self)
        top.geometry('300x120')
        lbl1 = Label(top , text='Column Name : ')
        lbl2 = Label(top , text='Expression : ')

        entry = Entry(top , textvariable=self.entryData)
        col = Entry(top , textvariable=self.entryColName)
        button = Button(top , text="submit" , command=lambda : self.submit(top))

        lbl1.grid(row=0 , column=0 , padx=5 , pady=5)
        lbl2.grid(row=1 , column=0 , padx=5 , pady=5)
        col.grid(row=0 , column=1 , padx=5 , pady=5)
        entry.grid(row=1 , column=1 , padx=5 , pady=5)
        button.grid(row=2 , column=0 , columnspan=2, padx=5 , pady=5)
        

    def submit(self ,top ):
        if self.entryColName.get():
            if self.entryData.get():
                self.add_column([f"{self.entryColName.get()}"] , anchor='center')
            else :
                showerror("Error" , "No Expression to evaluate")
        else : 
            showerror("Error" , "Column name is empty")
        top.destroy()


    def add_column(self, columns, **kwargs):
        try:
            eval(self.entryData.get().lower() , {'open':0 , "high":0 , "low":0 , "close":0})
            current_columns = list(self.tree['columns'])
            current_columns = {key:self.tree.heading(key) for key in current_columns}

            self.tree['columns'] = list(current_columns.keys()) + list(columns)
            for key in columns:
                self.tree.heading(key, text=key, **kwargs)

            for key in current_columns:
                state = current_columns[key].pop('state')
                self.tree.heading(key, **current_columns[key] )

            for i in self.tree.get_children():
                item = self.tree.item(i)
                data = item['values']
                self.tree.item(i , values = (data[0], data[1] , data[2] , data[3] , eval(self.entryData.get().lower() , {'open':data[0] , "high":data[1] , "low":data[2] , "close":data[3]})))
        except Exception as e:
            showerror("Error" , f"{e}")

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Testing ... ")
      
if __name__ == "__main__":
    app = App()
    rootFrame(app)
    app.mainloop()