import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout
import pandas as pd
from matplotlib import pyplot as plt

from sklearn.preprocessing import StandardScaler
import seaborn as sns
from flask import jsonify
import os
from os.path import exists
import matplotlib
matplotlib.use('Agg')
np.random.seed(1337)

def process(df, db_connection):
    train_dates = pd.to_datetime(df['Date'])
    cols = list(df)[1:6]
    df_for_training = df[cols].astype(float)

    scaler = StandardScaler()
    scaler = scaler.fit(df_for_training)
    df_for_training_scaled = scaler.transform(df_for_training)

    trainX = []
    trainY = []

    n_future = 90   # Number of days we want to predict into the future
    n_past = 14     # Number of past days we want to use to predict the future

    for i in range(n_past, len(df_for_training_scaled) - n_future +1):
        trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
        trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 0])

    trainX, trainY = np.array(trainX), np.array(trainY)

    print('trainX shape == {}.'.format(trainX.shape))
    print('trainY shape == {}.'.format(trainY.shape))


    # define Autoencoder model

    model = Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(LSTM(32, activation='relu', return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(trainY.shape[1]))

    model.compile(optimizer='adam', loss='mse')
    model.summary()


    # fit model
    history = model.fit(trainX, trainY, epochs=20, batch_size=32, validation_split=0.1, verbose=1)

    #Forecasting...
    #Start with the last day in training date and predict future...
    n_future=90  #Redefining n_future to extend prediction dates beyond original n_future dates...
    forecast_period_dates = pd.date_range(list(train_dates)[-1], periods=n_future, freq='1d').tolist()

    n_future=90  #Redefining n_future to extend prediction dates beyond original n_future dates...
    forecast_period_dates = pd.date_range(list(train_dates)[-1], periods=n_future, freq='1d').tolist()

    forecast = model.predict(trainX[-n_future:]) #forecast 

    #Perform inverse transformation to rescale back to original range
    #Since we used 5 variables for transform, the inverse expects same dimensions
    #Therefore, let us copy our values 5 times and discard them after inverse transform
    forecast_copies = np.repeat(forecast, df_for_training.shape[1], axis=-1)
    y_pred_future = scaler.inverse_transform(forecast_copies)[:,0]


    # Convert timestamp to date
    forecast_dates = []
    for time_i in forecast_period_dates:
        forecast_dates.append(time_i.date())
        
    df_forecast = pd.DataFrame({'Date':np.array(forecast_dates), 'Open':y_pred_future})
    df_forecast['Date']=pd.to_datetime(df_forecast['Date'])

    original = df[['Date', 'Open']]
    original['Date']=pd.to_datetime(original['Date'])
    # original = original.loc[original['Date'] >= '2021-1-27']
    original = original.loc[original['Date'] >= '2019-12-1']

    if exists("stock/open_stock_app/src/output.png"):
        print("file existsssss")
        os.remove("stock/open_stock_app/src/output.png")
    else:
        print("no fileeeeeee")

    ax = sns.lineplot(original['Date'], original['Open'])
    ax = sns.lineplot(df_forecast['Date'], df_forecast['Open'])
    fig = ax.get_figure()
    
    
    
    fig.savefig('stock/open_stock_app/src/output.png')

    df_forecast.to_sql(con=db_connection, name='forecast_table', if_exists='replace')

    # return len(df_forecast)
    return jsonify({"forecast": df_forecast.to_json(), "Training_loss": history.history['loss'], "validation_loss": history.history['val_loss'], "Model": "LSTM : Multivariate Time Series"})