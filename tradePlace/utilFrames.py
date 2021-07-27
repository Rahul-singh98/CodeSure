from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from utility import AutocompleteCombobox

bg_color = None

class FuturesFrame(LabelFrame):
    def __init__(self , container , seg_selec):
        super().__init__(container)
        self['text'] = f'{seg_selec}'
        style = Style()
        style.map('TCombobox' , fieldbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectforeground=[('readonly' , 'black')])
        
        self.label_instrument = Label(self , background=bg_color , text='Instrument')
        self.combo_instrument = Combobox(self  , values=['FUTIDX' , 'FUTSTK'])
        self.combo_instrument['state'] = 'readonly'
        self.combo_instrument.bind('<<ComboboxSelected>>' , self.comboInstrument_selected) 

        self.label_script = Label(self , background=bg_color , text='Script')
        self.combo_script = AutocompleteCombobox(self)
        self.combo_script['state'] = 'readonly'
        self.combo_script.bind('<<ComboboxSelected>>' , self.comboScript_selected)

        self.label_expiry = Label(self , text='Expiry' , background=bg_color )
        self.combo_expiry = Combobox(self)
        self.combo_expiry['state'] = 'readonly'
        self.combo_expiry.bind('<<ComboboxSelected>>' , self.comboExpiry_selected)

        self.label_instrument.grid(column=0 , row=0)
        self.combo_instrument.grid(column=1 , row=0 , padx=5,pady=5)

        self.label_script.grid(column=2 , row=0)
        self.combo_script.grid(column=3 , row=0 , padx=5,pady=5)

        self.label_expiry.grid(column=0 , row=1)
        self.combo_expiry.grid(column=1 , row=1, pady = 5 , padx = 5)

        self.grid(column=0 , row=1 , columnspan=4 , padx=5 , pady=5)
        self.grid_forget()
        
    def callback(self , var , idx , mode):
        try:
            if var.get() <= 0:
                print()
            else :
                var.get() 
        except :
            showerror('Error','Gap/Center cannot be zero or negative')

    def comboInstrument_selected(self ,event):
        self.instrument = event.widget.get()
        global new_df
        new_df = df[df['Instrument'] == self.instrument]
        self.combo_script.set_completion_list(sorted(new_df['Script'].unique().tolist()))

    def comboScript_selected(self ,event):
        self.script_name = event.widget.get()
        global new_df
        global new_df1
        global script_name 
        script_name = self.script_name
        new_df1 = new_df[new_df['Script']==self.script_name]
        self.combo_expiry['values'] = sorted(np.unique([str(x).split(' ')[0] for x in new_df1.sort_values(by='Expiry')['Expiry'].tolist()]).tolist())

    def comboExpiry_selected(self ,event):
        self.exp = event.widget.get()
        global new_df3
        global new_df1
        try :
            new_df3 = new_df1[new_df1['Expiry']==self.exp]
            
        except:
            showerror('Please Select the Expiry correctly !!! ') 

class EquityFrame(LabelFrame):
    def __init__(self , container , seg_selec):
        super().__init__(container)
        self['text'] = f'{seg_selec}'
        
        style = Style()
        style.map('TCombobox' , fieldbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectforeground=[('readonly' , 'black')])
        
        self.label_instrument = Label(self , background=bg_color , text='Instrument')
        self.combo_instrument = Combobox(self  , values=['EQ'])
        self.combo_instrument['state'] = 'readonly'
        self.combo_instrument.set('EQ') 

        self.label_script = Label(self , background=bg_color , text='Script')
        self.combo_script = AutocompleteCombobox(self)
        self.combo_script.set_completion_list(eq_script_list)
        self.combo_script.bind('<<ComboboxSelected>>' , self.comboScript_selected)

        self.radio_button = Radiobutton(self , background=bg_color , text='Range' , command = self.radioButtonChecked)
        self.label1_ = Label(self , background=bg_color)

        self.label2 = Label(self , background=bg_color)
        self.label2_ = Label(self , background=bg_color)
        
        self.label3 = Label(self , background=bg_color)
        self.label3_ = Label(self , background=bg_color)
        
        self.label_instrument.grid(column=0 , row=0)
        self.combo_instrument.grid(column=1 , row=0 , padx=5,pady=5)

        self.label_script.grid(column=2 , row=0)
        self.combo_script.grid(column=3 , row=0 , padx=5,pady=5)

        self.radio_button.grid(column=0 , row=1)
        self.label1_.grid(column=1 , row=1 , pady = 5 , padx = 5)

        self.label2.grid(column=2 , row=1)
        self.label2_.grid(column=3 , row=1, pady = 5 , padx = 5)

        self.label3.grid(column=0 , row=2)
        self.label3_.grid(column=1 , row=2, pady = 5 , padx = 5)
        self.grid(column=0 , row=1 , columnspan=4 ,padx=0 , pady = 5 )

    def comboScript_selected(self , event):
        self.script_name = event.widget.get()
        global new_df3
        global script_name 
        script_name = self.script_name
        new_df3 = eq_df[eq_df['Script']==self.script_name]
        
    def radioButtonChecked(self ):
    	self.stringVar = StringVar()
    	self.label_startwith = Label(self, text='Start')
    	self.combo_startwith = Combobox(self , textvariable=self.stringVar)
    	self.alphabet_values = [chr(alb) for alb in range(ord('A') , ord('Z')+1)]
    	self.combo_startwith['values'] = self.alphabet_values
    	self.combo_startwith.bind("<<ComboboxSelected>>" , self.startswithSelected)

    	self.label_startwith.grid(column=2 , row=1)
    	self.combo_startwith.grid(column=3 , row=1, pady = 5 , padx = 5)

    def startswithSelected(self , event):
    	self.stringVar_end = StringVar()
    	self.label_endwith = Label(self, text='End')
    	self.combo_endwith = Combobox(self , textvariable=self.stringVar_end)
    	self.combo_endwith['values'] = self.alphabet_values[self.alphabet_values.index(self.combo_startwith.get())+1 :]
    	self.combo_endwith.bind("<<ComboboxSelected>>" , self.endswithSelected)

    	self.label_endwith.grid(column=0 , row=2)
    	self.combo_endwith.grid(column=1 , row=2, pady = 5 , padx = 5)

    def endswithSelected(self , event):
    	global new_df3
    	global scrip_name 
    	script_name = "List of values Selected"

    	new_df3 = eq_df[eq_df['Script'].str.contains(f'^[{self.combo_startwith.get()}-{self.combo_endwith.get()}].*' , regex=True)]
    	new_df3.drop('Type' , axis=1 , inplace=True)

class OptionsFrame(LabelFrame):
    def __init__(self , container , seg_selec):
        super().__init__(container)
        self['text'] = f'{seg_selec}'
        style = Style()
        style.map('TCombobox' , fieldbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectbackground=[('readonly' , 'white')])
        style.map('TCombobox' , selectforeground=[('readonly' , 'black')])
        
        self.label_instrument = Label(self , background=bg_color , text='Instrument')
        self.combo_instrument = Combobox(self  , values=['OPTIDX' , 'OPTSTK'])
        self.combo_instrument['state'] = 'readonly'
        self.combo_instrument.bind('<<ComboboxSelected>>' , self.comboInstrument_selected) 

        self.label_script = Label(self , background=bg_color , text='Script')
        self.combo_script = AutocompleteCombobox(self)
        self.combo_script['state'] = 'readonly'
        self.combo_script.bind('<<ComboboxSelected>>' , self.comboScript_selected)

        self.label_option = Label(self , text='Option Type', background=bg_color )
        self.combo_option = Combobox(self)
        self.combo_option['values'] = ['CE' ,'PE']
        self.combo_option['state'] = 'readonly'
        self.combo_option.bind('<<ComboboxSelected>>' , self.comboOption_selected)

        self.label_expiry = Label(self , text='Expiry' , background=bg_color )
        self.combo_expiry = Combobox(self)
        self.combo_expiry['state'] = 'readonly'
        self.combo_expiry.bind('<<ComboboxSelected>>' , self.comboExpiry_selected)

        self.label_lowerR = Label(self , text='Price', background=bg_color )
        self.combo_lowerR = Combobox(self)
        self.combo_lowerR['state'] = 'readonly'
        self.combo_lowerR.bind('<<ComboboxSelected>>' , self.comboLowerR_selected)

        self.label_instrument.grid(column=0 , row=0)
        self.combo_instrument.grid(column=1 , row=0 , pady = 5 , padx= 5)

        self.label_script.grid(column=2 , row=0)
        self.combo_script.grid(column=3 , row=0 , pady = 5 , padx= 5)

        self.label_option.grid(column=0 , row=1)
        self.combo_option.grid(column=1 , row=1 , pady = 5 , padx = 5)

        self.label_expiry.grid(column=2 , row=1)
        self.combo_expiry.grid(column=3 , row=1, pady = 5 , padx = 5)

        self.label_lowerR.grid(column=0 , row=2)
        self.combo_lowerR.grid(column=1 , row=2, pady = 5 , padx = 5)
        
        self.grid(column=0 , row=1 , columnspan=4 , padx=5 , pady=5)
        self.grid_forget()

    def callback(self , var , idx , mode):
        try:
            if var.get() <= 0:
                print()
            else :
                var.get() 
        except :
            showerror('Error','Gap/Center cannot be zero or negative')

    def comboInstrument_selected(self ,event):
        self.instument = event.widget.get()
        global new_df
        new_df = df[df['Instrument'] == self.instument]
        self.combo_script.set_completion_list(sorted(new_df['Script'].unique().tolist()))

    def comboScript_selected(self ,event):
        self.script_name = event.widget.get()
        global new_df
        global script_name 
        script_name = self.script_name
        new_df = df[df['Script']==self.script_name]

    def comboOption_selected(self ,event):
        self.option = event.widget.get()
        global new_df
        global new_df1
        try :
            new_df1 = new_df[new_df['Type'] == self.option]
            self.combo_expiry['values'] = sorted(np.unique([str(x).split(' ')[0] for x in new_df1.sort_values(by='Expiry')['Expiry'].tolist()]).tolist())
        except :
            showerror("Please select the Script Correctly !!! ")

    def comboExpiry_selected(self ,event):
        self.exp = event.widget.get()
        global new_df1
        global new_df2
        try :
            new_df2 = new_df1[new_df1['Expiry']==self.exp]
            self.combo_lowerR['values'] = sorted(new_df2['Price'].tolist())

        except:
            showerror('Please the Expiry correctly !!! ')

    def comboLowerR_selected(self ,event):
        global val
        global new_df3
        global new_df3
        self.val = event.widget.get()
        new_df3 = new_df2[new_df2['Price'] == int(self.val)] 

if __name__ == "__main__":
    FuturesFrame() , EquityFrame() ,OptionsFrame()