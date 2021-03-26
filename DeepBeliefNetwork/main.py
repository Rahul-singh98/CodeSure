import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.metrics._regression import r2_score, mean_squared_error

from dbn import SupervisedDBNRegression as SR
import time
import tensorflow as tf
import os
import argparse

def main(path):
    try:
        df = pd.read_csv(path)
        dt = []
        for i in range(len(df)):
            dt.append(df['Date'][i]+ " " +df['Time'][i])


        df['DateTime'] = dt
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df.index = df['DateTime']

        df.drop(df[df['Volume']==0].index , axis=0 ,inplace=True)
        idx = df[df['Low']==df['High']].index
        df.drop(idx , axis=0 , inplace=True)

        df['Date'] = pd.to_datetime(df['Date'])
        df.index = df['Date']
        data = df['Close'].copy()

        # Training and testing data
        train_size = int(len(data) * 0.80)
        train = data[:train_size]
        test = data[train_size :]

        # Data scaling
        scaled_train = np.array(train)
        # Preparing training data
        X_train , y_train = [] , []
        for i in range(60 , len(scaled_train)):
            X_train.append(scaled_train[i-60 : i])
            y_train.append(scaled_train[i])

        # Training
        X_train = np.array(X_train)
        y_train = np.array(y_train)


        # Test
        # scaled_test = scaler.transform(np.array(test).reshape(-1,1))
        scaled_test = np.array(test)
        X_test , y_test = [] , []
        for i in range(60 , len(scaled_test)):
            X_test.append(scaled_test[i-60: i])
            y_test.append(scaled_test[i ])

        X_test = np.array(X_test)
        y_test = np.array(y_test)
        print(X_test.shape)

        regressor = SR(hidden_layers_structure=[1470 , 735],
                                    learning_rate_rbm=0.001,
                                    learning_rate=0.001,
                                    n_epochs_rbm=100,
                                    n_iter_backprop=2000,
                                    batch_size=32,
                                    activation_function='relu')

        gpu = tf.config.list_physical_devices('GPU')
        if gpu:
            proc = '/GPU:0'
            
        else :
            proc = '/CPU:0'
            
            
        with tf.device(proc):
            start_time = time.time()
            regressor.fit(X_train , y_train)
            end_time = time.time()
            print("Total time consumed : {} seconds ".format(end_time - start_time))

        os.mkdir('./models')
        model_name = 'regressor{}'.format(time.time())
        regressor.save('./models/{}'.format(model_name))
        print('Model is Saved ----- > {}'.format(model_name))

        train_preds = regressor.predict(X_train)
        test_preds = regressor.predict(X_test)

        plt.figure(figsize=(20,10))
        plt.plot(train_preds.reshape(-1,1) , label = 'Training Predictions')
        plt.plot(y_train.reshape(-1 ,1) , label='train labels')
        plt.plot(test_preds.reshape(-1 ,1 ) , label = 'Testing Predictions')
        plt.plot(y_test.reshape(-1 , 1) , label = 'Testing Labels')
        plt.legend()
        plt.show()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser('DBN GPU Training')

    parser.add_argument('--p' , default='./data/NIFTY1.csv' , type=str)
    
    args = parser.parse_args()
    main(args.p)