from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import tkinter.font as tkFont
from math import *
import random
import time
# from threading import Thread

# view = dict()

# def myFunc(tree):
#     for i in range(20):
#         children = tree.get_children()
#         for child in children:
#             first = tree.item(child)['values'][0]
#             tree.item(child , values=(first , random.randint(0,30) , random.randint(0,30) , 
#                                     random.randint(0,30) , random.randint(0,30)))
#         time.sleep(2) 


# class rootFrame(Frame):
#     def __init__(self , parent):
#         super().__init__()
        
#         self.tree = Treeview(parent)
#         self.carryOn = True
#         self.tree["columns"] = ("Name" ,"Open", "High", "Low" ,"Close")

#         self.tree.column("#0",   width=40, stretch="no" , anchor='center')
#         self.tree.column("Name", width=100, anchor='center')
#         self.tree.column("Open", width=100, anchor='center')
#         self.tree.column("High", width=100, anchor='center')
#         self.tree.column("Low",  width=100, anchor='center')
#         self.tree.column("Close",  width=100, anchor='center')
#         self.xscroll = Scrollbar(parent ,orient='horizontal' , command=self.tree.xview)
#         self.yscroll = Scrollbar(parent ,orient='vertical', command=self.tree.yview)
#         self.xscroll.pack(side='bottom' , fill='x')
#         self.yscroll.pack(side='right' , fill='y')

#         self.tree.heading("#0",   text="0")
#         self.tree.heading("Name",   text="Name")
#         self.tree.heading("Open", text="Open")
#         self.tree.heading("High", text="High")
#         self.tree.heading("Low",  text="Low")
#         self.tree.heading("Close",  text="Close")

#         self.tree.insert("","end",iid = "A", text = "A",
#                          values = ("Nifty", 10 , 13 , 6 , 9))
#         view.update({"A":("Nifty", 10 , 13 , 6 , 9)})                        
#         self.tree.insert("","end",iid = "B", text = "B" ,
#                          values = ("BankNifty",15 , 16, 6, 62))

#         view.update({"B":("BankNifty",15 , 16, 6, 62)})
#         self.tree.insert("","end",iid = "C", text = "C",
#                          values = ("FinNifty",16 , 25 ,9 , 12))
        
#         view.update({'C':("FinNifty",16 , 25 ,9 , 12)})
#         self.tree.insert("","end",iid = "D", text = "D",
#                          values = ("Axis",10 , 13 , 6 , 9))

#         view.update({'D':("Axis",10 , 13 , 6 , 9)})
#         self.tree.insert("","end",iid = "E", text = "E" ,
#                          values = ("BankOfBaroda",15 , 16, 6, 62))

#         view.update({"E":("BankOfBaroda",15 , 16, 6, 62)})
#         self.tree.insert("","end",iid = "F", text = "F",
#                          values = ("IndusIndBank",16 , 25 ,9 , 12))

#         view.update({"F":("IndusIndBank",16 , 25 ,9 , 12)})
#         self.tree.insert("","end",iid = "G", text = "G",
#                          values = ("SBI",10 , 13 , 6 , 9))

#         view.update({"G":("SBI",10 , 13 , 6 , 9)})
#         self.tree.insert("","end", iid = "H",text = "H" ,
#                          values = ("Zomato",15 , 16, 6, 62))

#         view.update({"H":("Zomato",15 , 16, 6 , 62)})
#         self.tree.insert("","end",iid = "I", text = "I",
#                          values = ("AdaniPort",16 , 25 ,9 , 12))

#         view.update({"I":("AdaniPort",16 , 25 ,9 , 12)})
#         self.tree.insert("","end", iid = "J",text = "J",
#                          values = ("MindTree",10 , 13 , 6 , 9))

#         view.update({"J":("MindTree",10 , 13 , 6 , 9)})
#         self.tree.insert("","end", iid = 'K',text = "K" ,
#                          values = ("PNB",15 , 16, 6, 62))

#         view.update({'K':("PNB",15 , 16, 6, 62)})
#         self.tree.insert("","end",iid = 'L', text = "L",
#                          values = ("DLF",16 , 25 ,9 , 12))

#         view.update({'L':("DLF",16 , 25 ,9 , 12)})
#         self.tree.pack(fill="both" , expand=True)
#         print(view)

#         t = Thread(target=myFunc ,args=[self.tree])
#         t.start()

#         self.tree.bind("<Button-3>" , self.showEntry)

#     def showEntry(self , event):
#         self.entryData = StringVar()
#         self.entryColName = StringVar()
#         top = Toplevel(self)
#         top.geometry('300x120')
#         lbl1 = Label(top , text='Column Name : ')
#         lbl2 = Label(top , text='Expression : ')

#         entry = Entry(top , textvariable=self.entryData)
#         col = Entry(top , textvariable=self.entryColName)
#         button = Button(top , text="submit" , command=lambda : self.submit(top))

#         lbl1.grid(row=0 , column=0 , padx=5 , pady=5)
#         lbl2.grid(row=1 , column=0 , padx=5 , pady=5)
#         col.grid(row=0 , column=1 , padx=5 , pady=5)
#         entry.grid(row=1 , column=1 , padx=5 , pady=5)
#         button.grid(row=2 , column=0 , columnspan=2, padx=5 , pady=5)

#     def submit(self ,top ):
#         if self.entryColName.get():
#             if self.entryData.get():
#                 if self.carryOn:
#                     self.add_column([f"{self.entryColName.get()}"] , anchor='center')
#                     self.carryOn = False
#                 else :
#                     showinfo("Info" , "Only 1 Expression is allowed")
#             else :
#                 showerror("Error" , "No Expression to evaluate")
#         else : 
#             showerror("Error" , "Column name is empty")
#         top.destroy()


#     def add_column(self, columns, **kwargs):
#         print(self.entryData.get())
#         try:
#             print(eval(self.entryData.get().lower() , {"__builtins__":None},{'open':0 , "high":0 , "low":0 , "close":0 , "sqrt":sqrt , "pow":pow}))
#             current_columns = list(self.tree['columns'])
#             current_columns = {key:self.tree.heading(key) for key in current_columns}

#             self.tree['columns'] = list(current_columns.keys()) + list(columns)
#             for key in columns:
#                 self.tree.heading(key, text=key, **kwargs)

#             for key in current_columns:
#                 state = current_columns[key].pop('state')
#                 self.tree.heading(key, **current_columns[key] )

#             simulator = dict()
#             for i in self.tree.get_children():
#                 item = self.tree.item(i)
#                 data = item['values']
#                 simulator[i] = data

#             for i in simulator:
#                 data = simulator[i]
#                 self.tree.item(i , values = (data[0], data[1] , data[2] , data[3] , data[4] , eval(self.entryData.get().lower() , {'open':data[1] , "high":data[2] , "low":data[3] , "close":data[4], "sqrt":sqrt , "pow":pow})))

#         except Exception as e:
#             showerror("Error" , f"{e}")


# class App(Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Testing ... ")
#         self.geometry('1200x500')
      
# if __name__ == "__main__":
#     app = App()
#     rootFrame(app)
#     app.mainloop()

root = Tk()

frame = Frame(root)
frame.pack()
for i in range(20):
    for j in range(15):
        lbl = Entry(frame  , width=10 )
        lbl.insert(END , f'{i}*{j}')
        lbl.grid(row=i , column=j)

ent = frame.children["!entry250"]
ent.delete(0,END)
ent.insert(END , 'newText')

root.mainloop()