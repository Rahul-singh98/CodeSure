from tkinter import *
from tkinter.ttk import * 
from tkinter.messagebox import *
import datetime
import time
import pandas as pd
import numpy as np
from pandastable import Table , TableModel
import socket 
import threading
import sys
import warnings
warnings.simplefilter('ignore')

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
dChange =int(datetime.datetime(1980, 1,1,0,0).timestamp())
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

bg_color = None
lst = [['Script Name' , 'Option Type' , 'Expiry' , 'Lower Price' ,'Ratio' , 'Center' , 'Gap']]

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("[+] Socket successfully created")
except socket.error as err: 
    print ("[+] socket creation failed with error %s" %(err))
  
# default port for socket 
# port = 10771
port = 5000
  
try: 
    # host_ip = socket.gethostbyname('ws://122.160.79.135:10771/Broadcast')
    # host_ip = socket.gethostbyname("122.160.79.135")
    host_ip = socket.gethostbyname(socket.gethostname()) 
except socket.gaierror: 
  
    # this means could not resolve the host 
    print ("[+] there was an error resolving the host")
    sys.exit() 
  
#connecting to the server 
s.connect((host_ip, port))
print (f"[+] the socket has successfully connected to codesure on port {host_ip}:{port}") 

def popup(msg):
	pop = Toplevel(root)
	pop.wm_title('Info')
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

# class Table:
# 	def __init__(self , root):
# 		for i in range(len(lst)):
# 			for j in range(len(lst[0])):
# 				self.entry = Entry(root , width=12 , font=('Arial' , 10 , 'bold'))
# 				self.entry.grid(row=i , column=j)
# 				self.entry.insert(END , lst[i][j])

class Main_window:
	def __init__(self , root):
		titleBarImage = PhotoImage(file = 'CodeSurelogo.png')
		root.iconphoto(True , titleBarImage)
		self.label_script = Label(root , background=bg_color , text='Script')
		self.combo_script = AutocompleteCombobox(root)
		self.combo_script.set_completion_list(script_list)
		self.combo_script.bind('<<ComboboxSelected>>' , self.comboScript_selected)
		# self.combo_script.set(script_list[113])


		self.label_option = Label(root , text='Option Type', background=bg_color )
		self.combo_option = Combobox(root)
		self.combo_option['values'] = option_type_list
		self.combo_option.bind('<<ComboboxSelected>>' , self.comboOption_selected)
		# self.c2.set(option_type_list[0])

		self.label_expiry = Label(root , text='Expiry' , background=bg_color )
		self.combo_expiry = Combobox(root)
		self.combo_expiry.bind('<<ComboboxSelected>>' , self.comboExpiry_selected)

		self.label_lowerR = Label(root , text='Lower Range', background=bg_color )
		self.combo_lowerR = Combobox(root)
		self.combo_lowerR.bind('<<ComboboxSelected>>' , self.comboLowerR_selected)

		self.label_upperR = Label(root , text='Upper Range', background=bg_color )
		self.combo_upperR = Combobox(root)
		self.combo_upperR.bind('<<ComboboxSelected>>' , self.comboUpperR_selected)

		self.strategy_var = StringVar()
		self.label_strategy = Label(root , text= 'Strategy', background=bg_color )
		self.combo_strategy = Combobox(root , values = strategy_list , textvariable=self.strategy_var)
		self.combo_strategy.set(strategy_list[0])

		self.center = IntVar()
		self.label_center = Label(root , text='Center', background=bg_color )
		self.entry_center = Entry(root , textvariable=self.center)
		# self.center.trace_add('write' ,self.callback)
		
		self.gap = IntVar()
		self.label_gap = Label(root , text='Gap', background=bg_color )
		self.entry_gap = Entry(root , textvariable=self.gap)
		# self.gap.trace_add('write' , self.callback)


		self.label_ratio = Label(root , text='Ratio', background=bg_color )
		self.combo_ratio = Combobox(root ,values= ratio_list)
		self.combo_ratio.bind('<<ComboboxSelected>>' , self.comboRatio_selected)

		self.add_button = Button(root ,text='Add', command=self.add )
		self.exit_button = Button(root , text='Exit' , command =lambda: root.destroy())

		# self.l10 = Label(root , text="" , background=bg_color )

		self.label_script.grid(column=0 , row=0)
		self.combo_script.grid(column=1 , row=0 , pady = 5 , padx= 5)

		self.label_option.grid(column=2 , row=0)
		self.combo_option.grid(column=3 , row=0 , pady = 5 , padx = 5)

		self.label_expiry.grid(column=0 , row=1)
		self.combo_expiry.grid(column=1 , row=1, pady = 5 , padx = 5)

		self.label_lowerR.grid(column=2 , row=1)
		self.combo_lowerR.grid(column=3 , row=1, pady = 5 , padx = 5)

		self.label_upperR.grid(column=0 , row=2)
		self.combo_upperR.grid(column=1 , row=2, pady = 5 , padx = 5)

		self.label_strategy.grid(column=2 , row=2)
		self.combo_strategy.grid(column=3 , row=2, pady = 5 , padx = 5)

		self.label_center.grid(column=0 , row=3)
		self.entry_center.grid(column=1 , row=3, pady = 5 , padx = 5)

		self.label_gap.grid(column=2 , row=3)
		self.entry_gap.grid(column=3 , row=3, pady = 5 , padx = 5)

		self.label_ratio.grid(column=0 , row=4)
		self.combo_ratio.grid(column=1 , row=4, pady = 5 , padx = 5)


		self.add_button.grid(column=1 , row=5 , padx=5  , pady=5)
		self.exit_button.grid(column=3 , row=5, pady = 5 , padx = 5)

	def callback(self , var , idx , mode):
		try:
			if var.get() <= 0:
				print()
			else :
				var.get() 
		except :
			showerror('Error','Gap/Center cannot be zero or negative')

	def comboScript_selected(self ,event):
	    self.script_name = event.widget.get()
	    global new_df
	    new_df = df[df['Script']==self.script_name]

	def comboOption_selected(self ,event):
	    self.option = event.widget.get()
	    global new_df
	    global new_df1
	    try :
	    	new_df1 = new_df[new_df['Type'] == self.option]
	    	self.combo_expiry['values'] = sorted(np.unique([str(x).split(' ')[0] for x in new_df1.sort_values(by='Expiry')['Expiry'].tolist()]).tolist())
	    except :
	    	popup("Please select the Script Correctly !!! ")
	    
	def comboExpiry_selected(self ,event):
	    self.exp = event.widget.get()
	    global new_df1
	    global new_df2
	    try :
	    	new_df2 = new_df1[new_df1['Expiry']==self.exp]
	    	self.combo_lowerR['values'] = sorted(new_df2['Price'].tolist())

	    except:
	    	popup('Please the Expiry correctly !!! ')

	def comboLowerR_selected(self ,event):
	    global val
	    self.val = event.widget.get()
	    l = self.combo_lowerR['values']
	    new_list = l[l.index(self.val)+1:]
	    self.combo_upperR['values'] = new_list
	    
	def comboUpperR_selected(self ,event):
	    global new_df2
	    global new_df3

	    new_df3 = new_df2.sort_values(by=['Price']).reset_index(drop=True)
	    new_df3 = new_df3[new_df3['Price']>= int(self.val)]
	    end = new_df3[new_df3['Price'] == int(event.widget.get())].index
	    new_df3 = new_df3[:end[0]]
	    
	def comboRatio_selected(self ,event):
	    # global ratio
	    self.ratio = event.widget.get()
	    
	def add(self):
		try:
			del(new_df)
			del(new_df1)
			del(new_df2)
		except Exception as e:
			pass

		global new_df3
		global lst 
		new_df3 = new_df3.reset_index(drop=True)
		lst.append([self.script_name , self.option  , self.exp , self.val , self.ratio , self.center.get() , self.gap.get()])
		# f = Frame(main)
		# f.pack(fill=BOTH , expand=1)

		for i in range(len(lst)):
			for j in range(len(lst[0])):
				entry = Entry(main , width=16 , font=('Arial' , 10 , 'bold'))
				entry.grid(row=i , column=j ,sticky=N+S+E+W)
				entry.insert(END , lst[i][j])
				# entry['text'] = lst[i][j]

		main.deiconify()
		main.mainloop()

root = Tk()
window = Main_window(root)
main = Toplevel(root)
# new_win = Table(main)	
main.withdraw()	
root.title('CodeSure')
root.mainloop()