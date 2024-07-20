import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LayerNormalization, MultiHeadAttention, Dropout, GlobalAveragePooling1D
import yfinance as yf

def train_transformer_model(ticker):
    data = yf.download(ticker, start="2010-01-01", end="2024-07-17")[['Close']].values
    if data.size == 0:
        raise ValueError("Downloaded dataframe is empty or contains all NaN values.")
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)

    def create_dataset(dataset, time_step=1):
        dataX = [dataset[i:(i + time_step), 0] for i in range(len(dataset) - time_step - 1)]
        return np.array(dataX)

    time_step = 100
    train_data = data_scaled[:int(len(data_scaled) * 0.8)]  # Increase training data ratio
    test_data = data_scaled[int(len(data_scaled) * 0.8):]
    
    X_train = create_dataset(train_data, time_step).reshape(-1, time_step, 1)
    X_test = create_dataset(test_data, time_step).reshape(-1, time_step, 1)

    inputs = Input(shape=(X_train.shape[1], X_train.shape[2]))
    x = transformer_encoder(inputs, head_size=256, num_heads=4, ff_dim=4, dropout=0.1)
    x = GlobalAveragePooling1D(data_format='channels_first')(x)
    x = Dropout(0.1)(x)
    x = Dense(20, activation="relu")(x)
    outputs = Dense(1, activation="linear")(x)

    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer="adam", loss="mean_squared_error")
    
    # Added validation split and increased epochs
    model.fit(X_train, X_train[:, 0, :], validation_split=0.1, epochs=100, batch_size=64, verbose=1)

    return model, scaler

def get_transformer_predictions(model, scaler, ticker, latest_stock_price=None):
    data = yf.download(ticker, start="2010-01-01", end="2022-07-17")[['Close']].values
    data_scaled = scaler.transform(data)

    time_step = 100
    future_data = data_scaled[-time_step:].reshape(1, time_step, 1)
    future_predictions = []
    
    for _ in range(60):
        future_prediction = model.predict(future_data)[0]
        future_predictions.append(future_prediction)
        future_data = np.append(future_data[:, 1:, :], [[future_prediction]], axis=1)

    future_predictions_unscaled = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    if latest_stock_price is not None:
        adjustment = latest_stock_price - future_predictions_unscaled[0][0]
        future_predictions_unscaled += adjustment

    return future_predictions_unscaled

def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
    x = LayerNormalization(epsilon=1e-6)(inputs)
    x = MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(x, x)
    x = Dropout(dropout)(x)
    res = x + inputs

    x = LayerNormalization(epsilon=1e-6)(res)
    x = Dense(ff_dim, activation="relu")(x)
    x = Dropout(dropout)(x)
    x = Dense(inputs.shape[-1])(x)
    return x + res
