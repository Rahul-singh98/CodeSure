from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import tkinter.font as tkFont
from math import *

# class rootFrame(Frame):
#     def __init__(self , parent):
#         super().__init__()
        
    #     self.tree = Treeview(parent)
    #     self.carryOn = True
    #     self.tree["columns"] = ("Name" ,"Open", "High", "Low" ,"Close")

    #     self.tree.column("#0",   width=0, stretch="no")
    #     self.tree.column("Name", width=100, anchor='center')
    #     self.tree.column("Open", width=100, anchor='center')
    #     self.tree.column("High", width=100, anchor='center')
    #     self.tree.column("Low",  width=100, anchor='center')
    #     self.tree.column("Close",  width=100, anchor='center')
    #     self.xscroll = Scrollbar(parent ,orient='horizontal' , command=self.tree.xview)
    #     self.yscroll = Scrollbar(parent ,orient='vertical', command=self.tree.yview)
    #     self.xscroll.pack(side='bottom' , fill='x')
    #     self.yscroll.pack(side='right' , fill='y')

    #     self.tree.heading("#0",   text="")
    #     self.tree.heading("Name",   text="Name")
    #     self.tree.heading("Open", text="Open")
    #     self.tree.heading("High", text="High")
    #     self.tree.heading("Low",  text="Low")
    #     self.tree.heading("Close",  text="Close")

    #     self.tree.insert("","end",iid = 1, text = "1",
    #                      values = ("Nifty", 10 , 13 , 6 , 9))
    #     self.tree.insert("","end",iid = 2, text = "2" ,
    #                      values = ("BankNifty",15 , 16, 6, 62))
    #     self.tree.insert("","end",iid = 3, text = "3",
    #                      values = ("FinNifty",16 , 25 ,9 , 12))
    #     self.tree.insert("","end",iid = 4, text = "4",
    #                      values = ("Axis",10 , 13 , 6 , 9))
    #     self.tree.insert("","end",iid = 5, text = "5" ,
    #                      values = ("BankOfBaroda",15 , 16, 6, 62))
    #     self.tree.insert("","end",iid = 6, text = "6",
    #                      values = ("IndusIndBank",16 , 25 ,9 , 12))
    #     self.tree.insert("","end",iid = 7, text = "7",
    #                      values = ("SBI",10 , 13 , 6 , 9))
    #     self.tree.insert("","end", iid = 8,text = "8" ,
    #                      values = ("Zomato",15 , 16, 6, 62))
    #     self.tree.insert("","end",iid = 9, text = "9",
    #                      values = ("AdaniPort",16 , 25 ,9 , 12))
    #     self.tree.insert("","end", iid = 10,text = "10",
    #                      values = ("MindTree",10 , 13 , 6 , 9))
    #     self.tree.insert("","end", iid = 11,text = "11" ,
    #                      values = ("PNB",15 , 16, 6, 62))
    #     self.tree.insert("","end",iid = 12, text = "12",
    #                      values = ("DLF",16 , 25 ,9 , 12))
    #     self.tree.pack(fill="both" , expand=True)

    #     self.tree.bind("<Button-3>" , self.showEntry)

    # def showEntry(self , event):
    #     self.entryData = StringVar()
    #     self.entryColName = StringVar()
    #     top = Toplevel(self)
    #     top.geometry('300x120')
    #     lbl1 = Label(top , text='Column Name : ')
    #     lbl2 = Label(top , text='Expression : ')

    #     entry = Entry(top , textvariable=self.entryData)
    #     col = Entry(top , textvariable=self.entryColName)
    #     button = Button(top , text="submit" , command=lambda : self.submit(top))

    #     lbl1.grid(row=0 , column=0 , padx=5 , pady=5)
    #     lbl2.grid(row=1 , column=0 , padx=5 , pady=5)
    #     col.grid(row=0 , column=1 , padx=5 , pady=5)
    #     entry.grid(row=1 , column=1 , padx=5 , pady=5)
    #     button.grid(row=2 , column=0 , columnspan=2, padx=5 , pady=5)
        

    # def submit(self ,top ):
    #     if self.entryColName.get():
    #         if self.entryData.get():
    #             if self.carryOn:
    #                 self.add_column([f"{self.entryColName.get()}"] , anchor='center')
    #                 self.carryOn = False
    #             else :
    #                 showinfo("Info" , "Only 1 Expression is allowed")
    #         else :
    #             showerror("Error" , "No Expression to evaluate")
    #     else : 
    #         showerror("Error" , "Column name is empty")
    #     top.destroy()


    # def add_column(self, columns, **kwargs):
    #     try:
    #         print(eval(self.entryData.get().lower() , {"__builtins__":None},{'open':0 , "high":0 , "low":0 , "close":0 , "sqrt":sqrt , "pow":pow}))
    #         current_columns = list(self.tree['columns'])
    #         current_columns = {key:self.tree.heading(key) for key in current_columns}

    #         self.tree['columns'] = list(current_columns.keys()) + list(columns)
    #         for key in columns:
    #             self.tree.heading(key, text=key, **kwargs)

    #         for key in current_columns:
    #             state = current_columns[key].pop('state')
    #             self.tree.heading(key, **current_columns[key] )

    #         simulator = dict()
    #         for i in self.tree.get_children():
    #             item = self.tree.item(i)
    #             data = item['values']
    #             simulator[i] = data

    #         for i in simulator:
    #             data = simulator[i]
    #             self.tree.item(i , values = (data[0], data[1] , data[2] , data[3] , data[4] , eval(self.entryData.get().lower() , {'open':data[1] , "high":data[2] , "low":data[3] , "close":data[4], "sqrt":sqrt , "pow":pow})))

    #     except Exception as e:
    #         showerror("Error" , f"{e}")

view = dict()

class rootFrame(Frame):
    def __init__(self , parent):
        super().__init__()
        

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Testing ... ")
        self.geometry('1200x500')
      
if __name__ == "__main__":
    app = App()
    rootFrame(app)
    app.mainloop()