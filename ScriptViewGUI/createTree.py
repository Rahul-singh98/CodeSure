# import tkinter as tk
# from tkinter import ttk
# import pandas as pd
# from random import randrange

# PADDING = dict(padx=0, pady=0)
# df = pd.DataFrame(columns=['One' , 'Two' , 'Three' ,'Four'])

# class GridView(tk.Frame):
#     def __init__(self, master=None, **kwargs):
#         tk.Frame.__init__(self, master, **kwargs)
#         self.labels = []
#         style = ttk.Style()
#         style.configure("red.TLabel", background='red')
#         style.configure("green.TLabel", background='green')
#         style.configure("header.TLabel", font = '-weight bold')

#     def set(self, df):
#         self.clear()
#         for col, name in enumerate(df.columns):
#             lbl = ttk.Label(self, text=name, style='header.TLabel')
#             lbl.grid(row=0, column=col, **PADDING)
#             self.labels.append(lbl)

#         for row, values in enumerate(df.itertuples(), 1):
#             for col, value in enumerate(values[1:]):
#                 lbl = ttk.Entry(self, style=self.get_style(value))
#                 lbl.insert(tk.END, value)
#                 lbl.grid(row=row, column=col, **PADDING)
#                 self.labels.append(lbl)

#     @staticmethod
#     def get_style(value):
#         if value > 70:
#             return "red.TLabel"
#         elif value < 30:
#             return "green.TLabel"
#         else:
#             return None

#     def clear(self):
#         for lbl in self.labels:
#             lbl.grid_forget()
#         self.labels = []

# class GUI(tk.Frame):
#     def __init__(self, master=None, **kwargs):
#         tk.Frame.__init__(self, master, **kwargs)
#         global df
#         self.table = GridView(self)
#         self.table.pack()
#         self.table.set(df)
#         btn = ttk.Button(self, text="Add Row", command=self.populate)
#         btn.pack()
#         btn = ttk.Button(self, text="Add Column", command=self.column)
#         btn.pack()
#         btn = ttk.Button(self, text="clear", command=self.table.clear)
#         btn.pack()
#         self.idx=0

#     def populate(self):
#         global df
#         df.loc[len(df.index)] = [randrange(100) for _ in range(len(df.columns))]
#         self.table.set(df)

#     def column(self):
#         global df
#         df[f'{self.idx}'] = 0
#         self.table.set(df)
#         self.idx+=1

# def main():
#     root = tk.Tk()
#     win = GUI(root)
#     win.pack()
#     root.mainloop()

# def new_rand_df():
#     width = 5
#     height = 5
#     return pd.DataFrame([[randrange(100) for _ in range(width)] for _ in range(height)], columns = list('abcdefghijklmnopqrstuvwxyz'[:width]))

# if __name__ == '__main__':
#     main()

from tkinter import *
from tkinter.ttk import *
import tkinter as tk

root = Tk()
headers = ['A' , 'B' ,'C' , 'D' , 'E']
r , c = 0, 0 # initial rows and columns
entryGrid = []
entryVars = []
def varCallback(var , c ,r):
    global entryVars
    spl = [i for i in var.get()]
    if len(spl)==0:
        pass
    elif spl[0]=='=':
        spl = spl[1:]
        string = ''
        for i in spl:
            string+= i
        try :
            entryVars[c]['old'][r] = entryVars[c]['new'][r].get()
            entryVars[c]['new'][r].set(eval(string))
        except Exception as e:
            print(e)
f = Frame(root)
f.pack()
canvas = Canvas(f, width=100 , height=100)
canvas.pack()
def create_grid(rows=10 , columns=5):
    global r , c,headers , entryGrid , entryVars
    for i in range(columns):
        grid = [None]
        vars = {"new":[None] , 'old':[None]}
        for j in range(rows+1):
            if j==0:
                lbl = Label(canvas , text=headers[i])
                lbl.grid(row=j , column=i)
            else :
                vars['new'].append(StringVar())
                vars['old'].append("")
                # vars['new'][j].trace('w' , lambda name , index ,mode , var= vars['new'][j] , i=i, j=j: varCallback(var , i ,j))
                grid.append(Entry(canvas ,textvariable=vars['new'][j]))
                grid[j].bind("<Return>" ,lambda event  , var=vars['new'][j] , i=i , j=j: varCallback( var , i , j))
                grid[j].grid(row=j , column=i)
        # print(vars)
        entryGrid.append(grid)
        entryVars.append(vars)
    r = j+1
    c= i+1
create_grid()

root.mainloop()