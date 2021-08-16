from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
import tkinter as tk
import tkinter.font as tkFont
from math import *
import random
import time
import pandas as pd
from threading import Thread

df = pd.DataFrame(columns=['Open' ,'High', 'Low' , 'Close'])

PADDING = dict(padx=0, pady=0)
class GridView(Frame):
    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.labels = []
        style = ttk.Style()
        style.configure("red.TLabel", background='red')
        style.configure("green.TLabel", background='green')
        style.configure("header.TLabel", font = '-weight bold')

    def set(self, df):
        self.clear()
        for col, name in enumerate(df.columns):
            lbl = ttk.Label(self, text=name, style='header.TLabel')
            lbl.grid(row=0, column=col, **PADDING)
            self.labels.append(lbl)

        for row, values in enumerate(df.itertuples(), 1):
            for col, value in enumerate(values[1:]):
                lbl = ttk.Entry(self, style=self.get_style(value))
                lbl.insert(tk.END, value)
                lbl.grid(row=row, column=col, **PADDING)
                self.labels.append(lbl)

    @staticmethod
    def get_style(value):
        if value > 70:
            return "red.TLabel"
        elif value < 30:
            return "green.TLabel"
        else:
            return None

    def clear(self):
        for lbl in self.labels:
            lbl.grid_forget()
        self.labels = []

def myFunc(tree):
    for i in range(20):
        children = tree.get_children()
        for child in children:
            first = tree.item(child)['values'][0]
            tree.item(child , values=(first , random.randint(0,30) , random.randint(0,30) , 
                                    random.randint(0,30) , random.randint(0,30)))
        time.sleep(2) 


class rootFrame(Frame):
    def __init__(self , parent=None , **kwargs):
        Frame.__init__(self , parent , **kwargs)
        global df
        self.tree = GridView(self)
        self.tree.pack()
        self.tree.set(df)

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
                if self.carryOn:
                    self.add_column([f"{self.entryColName.get()}"] , anchor='center')
                    self.carryOn = False
                else :
                    showinfo("Info" , "Only 1 Expression is allowed")
            else :
                showerror("Error" , "No Expression to evaluate")
        else : 
            showerror("Error" , "Column name is empty")
        top.destroy()


    def add_column(self, columns, **kwargs):
        print(self.entryData.get())
        try:
            print(eval(self.entryData.get().lower() , {"__builtins__":None},{'open':0 , "high":0 , "low":0 , "close":0 , "sqrt":sqrt , "pow":pow}))
            current_columns = list(self.tree['columns'])
            current_columns = {key:self.tree.heading(key) for key in current_columns}

            self.tree['columns'] = list(current_columns.keys()) + list(columns)
            for key in columns:
                self.tree.heading(key, text=key, **kwargs)

            for key in current_columns:
                state = current_columns[key].pop('state')
                self.tree.heading(key, **current_columns[key] )

            simulator = dict()
            for i in self.tree.get_children():
                item = self.tree.item(i)
                data = item['values']
                simulator[i] = data

            for i in simulator:
                data = simulator[i]
                self.tree.item(i , values = (data[0], data[1] , data[2] , data[3] , data[4] , eval(self.entryData.get().lower() , {'open':data[1] , "high":data[2] , "low":data[3] , "close":data[4], "sqrt":sqrt , "pow":pow})))

        except Exception as e:
            showerror("Error" , f"{e}")


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Testing ... ")
        self.geometry('1200x500')
    #     self.protocol('WM_DELETE_WINDOW' , self.onClose)

    # def onClose(self):
    #     if askokcancel("Quit" , "Are you sure you want to exit"):
    #         global run 
    #         run = False
    #         self.destroy()
      
if __name__ == "__main__":
    app = App()
    rootFrame(app)
    app.mainloop()

# root = Tk()

# f = Frame(root)
# f.pack()

# frame = Canvas(f)
# frame.pack()


# xscroll= Scrollbar(f , orient='horizontal' , command=frame.xview)
# xscroll.pack(side='bottom' , fill=X)

# yscroll = Scrollbar(f , orient='vertical' , command=frame.yview)
# yscroll.pack(side='right' , fill=Y)
# w = 9
# options = {'padx':0 , "pady":0}

# def callback(var , i , j):
#     global vars
#     spl = [i for i in var.get()]
    
#     if len(spl)==0:
#         print("#")
#     elif spl[0]=='=':
#         spl = spl[1:]
#         string = ''
#         for i in spl:
#             string+= i
#         try :

#             print(eval(string))
#         except:
#             pass
#     else :
#         print('#')

# def addColumn():
#     global counter , i , j , w
#     j += 1
#     lbl = Label(frame , text=f'Heading {j+1}' , width=w)
#     lbl.grid(row=0 , column=j ,**options)
#     for k in range(i+1):
#         vars[counter][0].trace("w" , lambda name , index , mode , var=vars[counter][0] ,c=counter : callback(var  , c))
#         entries[counter] = Entry(frame , width=w , textvariable=vars[counter])
#         entries[counter].grid(row=k+1 , column=j , **options)
#         counter+=1

# for j in range(16):
#     lbl = Label(frame , text=f'heading {j+1}' , width=w)
#     lbl.grid(row=0 , column=j , **options)

# for i in range(20):
#     for j in range(16):
#         vars.append(StringVar())
#         vars[0].append(StringVar())
#         vars[1].append("")
#         vars[counter][0].trace("w" , lambda name , index , mode , var=vars[counter][0] ,i=i ,j=j : callback(var  , i,j))
#         entries[counter] = tk.Entry(frame  , width=w , textvariable=vars[counter][0] , borderwidth=0)
#         entries[counter].grid(row=i+1 , column=j , **options)
#         counter +=1

# btn = Button(frame , text='Add Column' , command=addColumn)
# btn.grid(row= i+3 , column=j+3 )

# root.mainloop()

# root = Tk()

# headers = ['A' , 'B' ,'C' , 'D' , 'E']
# r , c = 0, 0 # initial rows and columns

# entryGrid = []
# entryVars = []

# def varCallback(var , c ,r):
#     global entryVars
#     spl = [i for i in var.get()]
#     if len(spl)==0:
#         pass
#     elif spl[0]=='=':
#         spl = spl[1:]
#         string = ''
#         for i in spl:
#             string+= i
#         try :
#             entryVars[c]['old'][r] = entryVars[c]['new'][r].get()
#             entryVars[c]['new'][r].set(eval(string))
#         except Exception as e:
#             print(e)

# f = Frame(root)
# f.pack()

# canvas = Canvas(f, width=100 , height=100)
# canvas.pack()


# def create_grid(rows=10 , columns=5):
#     global r , c,headers , entryGrid , entryVars
#     for i in range(columns):
#         grid = [None]
#         vars = {"new":[None] , 'old':[None]}
#         for j in range(rows+1):
#             if j==0:
#                 lbl = Label(canvas , text=headers[i])
#                 lbl.grid(row=j , column=i)
#             else :
#                 vars['new'].append(StringVar())
#                 vars['old'].append("")
#                 # vars['new'][j].trace('w' , lambda name , index ,mode , var= vars['new'][j] , i=i, j=j: varCallback(var , i ,j))
#                 grid.append(Entry(canvas ,textvariable=vars['new'][j]))
#                 grid[j].bind("<Return>" ,lambda event  , var=vars['new'][j] , i=i , j=j: varCallback( var , i , j))
#                 grid[j].grid(row=j , column=i)
#         # print(vars)

#         entryGrid.append(grid)
#         entryVars.append(vars)

#     r = j+1
#     c= i+1

# create_grid()
