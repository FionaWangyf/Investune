import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from LS3 import train_lstm_model, get_lstm_predictions
from tran3 import train_transformer_model, get_transformer_predictions
from XG3 import train_prophet_model, get_prophet_predictions

def calculate_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    return mae, rmse

def compare_models(ticker):
    df = yf.download(ticker, start='2020-01-01', end='2024-07-17')
    if df.empty or df['Close'].isnull().all():
        raise ValueError("Downloaded dataframe is empty or contains all NaN values.")
    
    df.reset_index(inplace=True)
    df['SMA_15'] = df['Close'].rolling(window=15).mean().shift()
    df['SMA_30'] = df['Close'].rolling(window=30).mean().shift()
    df.dropna(inplace=True)
    historical_prices = df['Close'].values

    # Train models
    lstm_model, lstm_scaler = train_lstm_model(ticker)
    transformer_model, transformer_scaler = train_transformer_model(ticker)
    prophet_model = train_prophet_model(ticker)
    
    # Get predictions
    lstm_predictions = get_lstm_predictions(lstm_model, lstm_scaler, ticker).flatten()
    transformer_predictions = get_transformer_predictions(transformer_model, transformer_scaler, ticker).flatten()
    prophet_predictions = get_prophet_predictions(prophet_model, ticker)['yhat'].values
    
    # Ensure predictions are aligned for comparison
    min_len = min(len(historical_prices), len(lstm_predictions), len(transformer_predictions), len(prophet_predictions))
    historical_prices = historical_prices[-min_len:]
    lstm_predictions = lstm_predictions[-min_len:]
    transformer_predictions = transformer_predictions[-min_len:]
    prophet_predictions = prophet_predictions[-min_len:]
    
    # Calculate metrics
    lstm_mae, lstm_rmse = calculate_metrics(historical_prices, lstm_predictions)
    transformer_mae, transformer_rmse = calculate_metrics(historical_prices, transformer_predictions)
    prophet_mae, prophet_rmse = calculate_metrics(historical_prices, prophet_predictions)
    
    print(f"LSTM - MAE: {lstm_mae:.4f}, RMSE: {lstm_rmse:.4f}")
    print(f"Transformer - MAE: {transformer_mae:.4f}, RMSE: {transformer_rmse:.4f}")
    print(f"Prophet - MAE: {prophet_mae:.4f}, RMSE: {prophet_rmse:.4f}")
    
    fig, ax = plt.subplots(figsize=(15, 8))
    history_length = 100

    # Plotting the results
    ax.figure(figsize=(14, 7))
    ax.plot(df['Date'][-min_len:], historical_prices, label='Actual Prices', color='black', linewidth=2)
    ax.plot(df['Date'][-min_len:], lstm_predictions, label='LSTM Predictions', linestyle='--')
    ax.plot(df['Date'][-min_len:], transformer_predictions, label='Transformer Predictions', linestyle='--')
    ax.plot(df['Date'][-min_len:], prophet_predictions, label='Prophet Predictions', linestyle='--')
    ax.xlabel('Date')
    ax.ylabel('Stock Price')
    ax.title(f'Stock Price Predictions Comparison for {ticker}')
    ax.legend()
    ax.show()

    lstm_data = lstm_mae, lstm_rmse
    transformer_data = transformer_mae, transformer_rmse
    prophet_data = prophet_mae, prophet_rmse
    
    return fig, lstm_data, transformer_data, prophet_data

def read_comparison_data(file_path):
    best_models = {}
    with open(file_path, 'r') as file:
        data = file.readlines()
        current_ticker = None
        for line in data:
            line = line.strip()  # 去掉首尾的空白字符
            if "comparison" in line:
                current_ticker = line.split()[0]
                best_models[current_ticker] = {'model': None, 'mae': float('inf')}
            elif current_ticker and ' - ' in line:
                try:
                    model, metrics = line.split(' - ')
                    mae = float(metrics.split(', ')[0].split(': ')[1])
                    if mae < best_models[current_ticker]['mae']:
                        best_models[current_ticker] = {'model': model, 'mae': mae}
                except ValueError:
                    print(f"Error parsing line: {line}")
                    continue
    return best_models

best_models = read_comparison_data('./comparison/comparison_data.txt')

def choose_best_model(ticker):
    fig, lstm_data, transformer_data, prophet_data = compare_models(ticker)
    lstm_mae, lstm_rmse = lstm_data
    transformer_mae, transformer_rmse = transformer_data
    prophet_mae, prophet_rmse = prophet_data
    
    min_mae = min(lstm_mae, transformer_mae, prophet_mae)
    
    if min_mae == lstm_mae:
        best_model = 'LSTM'
        best_mae = lstm_mae
    elif min_mae == transformer_mae:
        best_model = 'Transformer'
        best_mae = transformer_mae
    else:
        best_model = 'Prophet'
        best_mae = prophet_mae

    print(f"Best model for {ticker} is {best_model} with MAE: {best_mae:.4f}")
    
    return best_model, best_mae



# Example usage
#ticker = input("Enter the stock ticker: ")
#compare_models(ticker)
