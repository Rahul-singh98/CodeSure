from tkinter import *
from tkinter.ttk import * 
import datetime
import pandas as pd
import numpy as np
import time
import warnings
warnings.simplefilter('ignore')

bg_color = '#ff952b'
# csv_filepath = filedialog.askopenfilename(
#     # initialdir="C:/Users/MainFrame/Desktop/", 
#     title="Open Text file", 
#     filetypes=(("Text Files", "*.txt"),)
#     )
csv_filepath = './contract'

cols = [i for i in range(0,70)]

pdread = pd.read_csv(csv_filepath , sep='|' , skiprows=1 , names=cols)
stk = pdread[pdread[2] == 'OPTSTK' ]
idx = pdread[pdread[2] == 'OPTIDX']

df = pd.concat([stk , idx ] , axis=0)

del(stk)
del(idx)
del(pdread)

df= df[[3,6,7,8]]
df.columns = ['Script', 'Expiry' , 'Price' , 'Type']
df['Price'] = df['Price'].apply(lambda x: (x/100)).astype('int')
dChange =int(datetime.datetime(1980, 1,1,0,0).strftime('%s'))
df['Expiry'] = df['Expiry'].apply(lambda x: datetime.datetime.fromtimestamp(dChange + x).strftime('%d-%m-%Y')).astype('datetime64')
df.reset_index(drop=True ,inplace=True)

new_df = pd.DataFrame()
new_df1 = pd.DataFrame()
new_df2 = pd.DataFrame()
new_df3 = pd.DataFrame()

script_list =sorted(df['Script'].dropna().unique().tolist())
strategy_list = ['Butterfly']
option_type_list = sorted(['CE' , 'PE'])
ratio_list = ['121' ,'143']


def popup(msg):
	pop = Tk()
	def leave():
		pop.destroy()
	label = Label(pop , text=msg , background=bg_color)
	btn = Button(pop ,text='Okay',command=leave)
	label.pack()
	btn.pack(side='bottom' , padx=3 , pady=3)
	pop['bg'] = bg_color
	pop.mainloop()

class AutocompleteCombobox(Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, Tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(INSERT), END)
                        self.position = self.index(END)
                if event.keysym == "Left":
                        if self.position < self.index(END): # delete the selection
                                self.delete(self.position, END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, END)
                if event.keysym == "Right":
                        self.position = self.index(END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()


class Userinterface:
	def __init__(self, root) :
		self.l1 = Label(root , background=bg_color , text='Script')
		self.c1 = AutocompleteCombobox(root)
		self.c1.set_completion_list(script_list)
		self.c1.bind('<<ComboboxSelected>>' , self.c1_selected)


		self.l2 = Label(root , text='Option Type', background=bg_color )
		self.c2 = Combobox(root)
		self.c2['values'] = option_type_list
		self.c2.bind('<<ComboboxSelected>>' , self.c2_selected)

		self.l3 = Label(root , text='Expiry' , background=bg_color )
		self.c3 = Combobox(root)
		self.c3.bind('<<ComboboxSelected>>' , self.c3_selected)

		self.l4 = Label(root , text='Lower Range', background=bg_color )
		self.c4 = Combobox(root)
		self.c4.bind('<<ComboboxSelected>>' , self.c4_selected)

		self.l5 = Label(root , text='Upper Range', background=bg_color )
		self.c5 = Combobox(root)
		self.c5.bind('<<ComboboxSelected>>' , self.c5_selected)

		self.sst1 = StringVar()
		self.l6 = Label(root , text= 'Strategy', background=bg_color )
		self.c6 = Combobox(root , values = strategy_list , textvariable=self.sst1)

		self.center1 = IntVar()
		self.l7 = Label(root , text='Center', background=bg_color )
		self.c7 = Entry(root , textvariable=self.center1)
		
		self.gap1 = IntVar()
		self.l8 = Label(root , text='Gap', background=bg_color )
		self.c8 = Entry(root , textvariable=self.gap1)


		self.l9 = Label(root , text='Ratio', background=bg_color )
		self.c9 = Combobox(root ,values= ratio_list)
		self.c9.bind('<<ComboboxSelected>>' , self.c9_selected)

		self.btn = Button(root ,text='Start', command=self.submit )
		self.btn1 = Button(root , text='Stop' , command =lambda: root.destroy())

		# self.l10 = Label(root , text="" , background=bg_color )
		self.l10 = Text(root)
		self.l10['bg'] = bg_color

		self.l1.grid(column=0 , row=0)
		self.c1.grid(column=1 , row=0 , pady = 5 , padx= 5)

		self.l2.grid(column=2 , row=0)
		self.c2.grid(column=3 , row=0 , pady = 5 , padx = 5)

		self.l3.grid(column=0 , row=1)
		self.c3.grid(column=1 , row=1, pady = 5 , padx = 5)

		self.l4.grid(column=2 , row=1)
		self.c4.grid(column=3 , row=1, pady = 5 , padx = 5)

		self.l5.grid(column=0 , row=2)
		self.c5.grid(column=1 , row=2, pady = 5 , padx = 5)

		self.l6.grid(column=2 , row=2)
		self.c6.grid(column=3 , row=2, pady = 5 , padx = 5)

		self.l7.grid(column=0 , row=3)
		self.c7.grid(column=1 , row=3, pady = 5 , padx = 5)

		self.l8.grid(column=2 , row=3)
		self.c8.grid(column=3 , row=3, pady = 5 , padx = 5)

		self.l9.grid(column=0 , row=4)
		self.c9.grid(column=1 , row=4, pady = 5 , padx = 5)


		self.btn.grid(column=1 , row=5 , padx=5  , pady=5)
		self.btn1.grid(column=3 , row=5, pady = 5 , padx = 5)

		self.l10.grid(column=0 , row=6 , columnspan=4 , pady = 5 , padx = 5)

	def c1_selected(self ,event):
	    script_name = event.widget.get()
	    global new_df
	    new_df = df[df['Script']==script_name]

	def c2_selected(self ,event):
	    option = event.widget.get()
	    global new_df
	    global new_df1
	    try :
	    	new_df1 = new_df[new_df['Type'] == option]
	    	self.c3['values'] = sorted(np.unique([str(x).split(' ')[0] for x in new_df1.sort_values(by='Expiry')['Expiry'].tolist()]).tolist())
	    except :
	    	popup("You have not seleted the Script Correctly !!! ")
	    
	def c3_selected(self ,event):
	    exp = event.widget.get()
	    global new_df1
	    global new_df2
	    new_df2 = new_df1[new_df1['Expiry']==exp]
	    self.c4['values'] = sorted(new_df2['Price'].tolist())

	def c4_selected(self ,event):
	    global val
	    self.val = event.widget.get()
	    l = self.c4['values']
	    new_list = l[l.index(self.val)+1:]
	    self.c5['values'] = new_list
	    
	def c5_selected(self ,event):
	    global new_df2
	    global new_df3

	    new_df3 = new_df2.sort_values(by=['Price']).reset_index(drop=True)
	    new_df3 = new_df3[new_df3['Price']>= int(self.val)]
	    end = new_df3[new_df3['Price'] == int(event.widget.get())].index
	    new_df3 = new_df3[:end[0]]
	    
	def c9_selected(self ,event):
	    global ratio
	    self.ratio = event.widget.get()
	    
	def submit(self):
	    gap = self.gap1.get()
	    center = self.center1.get()
	    sst = self.sst1.get()
	    global ratio
	    global new_df3
	    new_df3 = new_df3.reset_index(drop=True)


	    # def empty_box(n,start , end , gap ):
	    # 	fstart = start
	    # 	label_text = """SPOT   BS    SS   MAX \n"""
	    # 	# self.l10.delete('1.0' , END)
	    # 	# self.l10.insert(END, f'SPOT   BS    SS   MAX \n')
	    # 	for i in range(n):
	    # 		if start<=end:
	    # 			break
	    # 		bid = [np.random.randint(10 , 30 ) for _ in range(3)]
	    # 		ask = [np.random.randint(bid[x]-1 , bid[x]+1) for x in range(3)]
	    # 		bs = ask[0] * ratio[0] - bid[1] * ratio[1] + ask[2] * ratio[2]
	    # 		ss = -(bid[0] * ratio[0]) + ask[1] * ratio[1] + bid[2] * ratio[2]
	    # 		label_text+= "".join(f'{start}   {bs}   {ss}    {max(bs , ss)} \n')
	    # 		# self.l10.insert(END , f'{start}   {bs}   {ss}    {max(bs , ss)} \n')

	    # 		start += gap 

	    # 	self.l10.configure(text= label_text)

	    # 	root.after(10000 , empty_box(n,fstart , end , gap))
	    
	    if sst == 'Butterfly':
	        ratio = [int(d) for d in self.ratio]
	        start = new_df3.loc[0 , 'Price']
	        n = len(new_df3)-1
	        end = new_df3.loc[n ,'Price']
	        fstart = start

	        self.l10.insert(END , f'SPOT   BS    SS   MAX \n')

	        while start <= end:
	        	bid = [np.random.randint(10,30) for _ in range(3)]
	        	ask = [np.random.randint(bid[x]-1 , bid[x]+1) for x in range(3)]
	        	bs = ask[0] * ratio[0] - bid[1] * ratio[1] + ask[2] * ratio[2]
	        	ss = -(bid[0] * ratio[0])+ ask[1] * ratio[1] - bid[2] * ratio[2]
	        	self.l10.insert(END , f'{start}   {bs}    {ss}   {max(bs , ss)} \n')

	        	start += gap 

	        # root.after(1 , empty_box(n,start , end , gap))


root  = Tk()
r = Userinterface(root)
root.geometry('655x615')
root['bg'] = bg_color
root.title('Codesure')

root.bind('<Control-Q>' , lambda event=None : root.destroy())
root.bind('<Control-q>' , lambda event=None : root.destroy())
root.mainloop()
