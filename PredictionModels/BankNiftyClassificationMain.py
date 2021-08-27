import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from numpy.random import seed
from datetime import timedelta, date
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix,roc_auc_score, roc_curve
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.compat.v1 import set_random_seed
import tensorflow as tf

from py5paisa import FivePaisaClient

client = FivePaisaClient(email="52119099", passwd="#bhola@1996", dob="19840101")
client.login()

scriptDf = pd.read_csv('../HistoricalData/NSECashScripts.csv')

symbol = 'banknifty'
end = datetime.datetime.now() - datetime.timedelta(1)
start = end - datetime.timedelta(100)

scode = int(scriptDf[scriptDf['Name']==symbol.upper()]['Scripcode'])
data = client.historical_data('N' , 'C' , scode ,'1m', start ,end)
data.set_index('Datetime' , inplace=True)
data.index = pd.to_datetime(data.index)

initial_balance1 = data.between_time(start_time = '09:16:00', end_time = '10:15:00', include_end = True)
initial_balance2 = data.between_time(start_time = '14:31:00', end_time = '15:30:00', include_end = True)
initial_balance = pd.concat([initial_balance1,initial_balance2],axis=0)

initial_balance.dropna(inplace=True)

eod_returns = data.between_time(start_time = '09:16:00', end_time = '15:30:00', include_end = True)

conversion = {'Open' : 'first', 'High' : 'max', 'Low' : 'min', 'Close' : 'last'}
data2 = eod_returns.resample('1D').agg(conversion)
data2['target'] = data2['Open']/data2['Close'].shift(1)
data2.dropna(inplace=True)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


X = []
y = []

single_date = end
if single_date.strftime("%Y-%m-%d") in data2.index:
    curr = single_date.strftime("%Y-%m-%d")
    
    Xdelta = []
    for i in range(0,initial_balance.loc[curr].shape[0]):
        
        for j in range(0,4):
            Xdelta.append(initial_balance.loc[curr].iloc[i][j])
    if(len(Xdelta) == 480):
        X.append(Xdelta)
        y.append(data2.loc[curr].loc['target'])
    else:
        print('Excluded - ',curr,' Length: ',len(Xdelta))

cols = []
for i in range(0,120):
    for j in range(0,4):
        cols.append('f'+str(i)+str(j))
y = pd.Series(y)
X = pd.DataFrame(np.reshape(X,(y.shape[0],len(cols))), columns=cols)

X.dropna(inplace=True)
X = X.iloc[:,:-1]

scaler = StandardScaler()
X_scaled = scaler.transform(X)

model = load_model('./models/bestmodel')
y_pred = model.predict(X_scaled)
y_pred = (y_pred > 0.5)
if y_pred[-1][0]:
    print('Bullish Prediction')
else :
    print("Bearish Prediction")
