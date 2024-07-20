import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

def train_lstm_model(ticker):
    df = yf.download(ticker, period='2y')
    if df.empty or df['Close'].isnull().all():
        raise ValueError("Downloaded dataframe is empty or contains all NaN values.")
    
    y = df['Close'].fillna(method='ffill').values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    y = scaler.fit_transform(y)

    n_lookback = 400
    n_forecast = 60

    X = []
    Y = []

    for i in range(n_lookback, len(y) - n_forecast + 1):
        X.append(y[i - n_lookback: i])
        Y.append(y[i: i + n_forecast])

    X = np.array(X)
    Y = np.array(Y)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(n_lookback, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(n_forecast))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, Y, epochs=100, batch_size=32, verbose=0)

    return model, scaler

def get_lstm_predictions(model, scaler, ticker, latest_stock_price=None):
    df = yf.download(ticker, period='2y')
    y = df['Close'].fillna(method='ffill').values.reshape(-1, 1)
    y = scaler.transform(y)

    n_lookback = 400
    X_ = y[-n_lookback:].reshape(1, n_lookback, 1)
    Y_ = model.predict(X_).reshape(-1, 1)
    Y_ = scaler.inverse_transform(Y_)

    if latest_stock_price is not None:
        adjustment = latest_stock_price - Y_[0][0]
        Y_ += adjustment

    return Y_
