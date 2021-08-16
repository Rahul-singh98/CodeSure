import tkinter as tk
from tkinter import ttk
import pandas as pd
from random import randrange

PADDING = dict(padx=0, pady=0)
class GridView(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
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

class GUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.table = GridView(self)
        self.table.pack()
        btn = ttk.Button(self, text="populate", command=self.populate)
        btn.pack()
        btn = ttk.Button(self, text="clear", command=self.table.clear)
        btn.pack()

    def populate(self):
        self.table.set(new_rand_df())

def main():
    root = tk.Tk()
    win = GUI(root)
    win.pack()
    root.mainloop()

def new_rand_df():
    width = 5
    height = 5
    return pd.DataFrame([[randrange(100) for _ in range(width)] for _ in range(height)], columns = list('abcdefghijklmnopqrstuvwxyz'[:width]))

if __name__ == '__main__':
    main()