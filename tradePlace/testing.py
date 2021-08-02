# from tkinter import ttk
# import tkinter as tk

# root = tk.Tk()
# tree = ttk.Treeview(root)
# tree.pack()
# tree.insert('', 'end', text='This is critical message', tags=('critical',))
# # tree.insert(c, 'end', text='This is child of critical message', tags=('critical',))
# for i in range(5):
#     tree.insert('', 'end', text='This is non-critical message')
# tree.tag_configure('critical', background='red',foreground="white")

# root.mainloop()

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        #1. Create Treeview with binding
        self.tree = ttk.Treeview(parent, columns=("size", "modified"))
        self.tree["columns"] = ("date", "time", "loc")

        self.tree.column("#0",   width=100, anchor='center')
        self.tree.column("date", width=100, anchor='center')
        self.tree.column("time", width=100, anchor='center')
        self.tree.column("loc",  width=100, anchor='center')

        self.tree.heading("#0",   text="Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("loc",  text="Location")

        self.tree.insert("","end", text = "Grace",
                         values = ("2010-09-23","03:44:53","Garden"))
        self.tree.insert("","end", text = "John" ,
                         values = ("2017-02-05","11:30:23","Airport"))
        self.tree.insert("","end", text = "Betty",
                         values = ("2014-06-25","18:00:00",""))

        self.tree.grid()
        self.tree.bind('<ButtonRelease-1>', self.selectItem)

        #2. Create a Canvas Overlay to show selected Treeview cell 
        sel_bg = '#ecffc4'
        sel_fg = '#05640e'
        self.setup_selection(sel_bg, sel_fg)


    def setup_selection(self, sel_bg, sel_fg):
        self._font = tkFont.Font()

        self._canvas = tk.Canvas(self.tree,
                                 background=sel_bg,
                                 borderwidth=0,
                                 highlightthickness=0)

        self._canvas.text = self._canvas.create_text(0, 0,
                                                     fill=sel_fg,
                                                     anchor='w')

    def selectItem(self, event):
        # Remove Canvas overlay from GUI
        self._canvas.place_forget()

        # Local Parameters
        x, y, widget = event.x, event.y, event.widget
        item = widget.item(widget.focus())
        itemText = item['text']
        itemValues = item['values']
        iid = widget.identify_row(y)
        column = event.widget.identify_column(x)
        print ('\n&&&&&&&& def selectItem(self, event):')
        print ('item = ', item)
        print ('itemText = ', itemText)
        print('itemValues = ',itemValues)
        print ('iid = ', iid)
        print ('column = ', column)

        #Leave method if mouse pointer clicks on Treeview area without data
        if not column or not iid:
            return

        #Leave method if selected item's value is empty
        if not len(itemValues): 
            return

        #Get value of selected Treeview cell
        if column == '#0':
            self.cell_value = itemText
        else:
            self.cell_value = itemValues[int(column[1]) - 1]
        print('column[1] = ',column[1])
        print('self.cell_value = ',self.cell_value)

        #Leave method if selected Treeview cell is empty
        if not self.cell_value: # date is empty
            return

        #Get the bounding box of selected cell, a tuple (x, y, w, h), where
        # x, y are coordinates of the upper left corner of that cell relative
        #      to the widget, and
        # w, h are width and height of the cell in pixels.
        # If the item is not visible, the method returns an empty string.
        bbox = widget.bbox(iid, column)
        print('bbox = ', bbox)
        if not bbox: # item is not visible
            return

        # Update and show selection in Canvas Overlay
        self.show_selection(widget, bbox, column)

        print('Selected Cell Value = ', self.cell_value)


    def show_selection(self, parent, bbox, column):
        """Configure canvas and canvas-textbox for a new selection."""
        print('@@@@ def show_selection(self, parent, bbox, column):')
        x, y, width, height = bbox
        fudgeTreeColumnx = 19 #Determined by trial & error
        fudgeColumnx = 15     #Determined by trial & error

        # Number of pixels of cell value in horizontal direction
        textw = self._font.measure(self.cell_value)
        print('textw = ',textw)

        # Make Canvas size to fit selected cell
        self._canvas.configure(width=width, height=height)

        # Position canvas-textbox in Canvas
        print('self._canvas.coords(self._canvas.text) = ',
              self._canvas.coords(self._canvas.text))
        if column == '#0':
            self._canvas.coords(self._canvas.text,
                                fudgeTreeColumnx,
                                height/2)
        else:
            self._canvas.coords(self._canvas.text,
                                (width-(textw-fudgeColumnx))/2.0,
                                height/2)

        # Update value of canvas-textbox with the value of the selected cell. 
        self._canvas.itemconfigure(self._canvas.text, text=self.cell_value)

        # Overlay Canvas over Treeview cell
        self._canvas.place(in_=parent, x=x, y=y)



if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()