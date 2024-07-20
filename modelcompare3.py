import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from LS3 import train_lstm_model, get_lstm_predictions
from tran3 import train_transformer_model, get_transformer_predictions
from XG3 import train_prophet_model, get_prophet_predictions

def plot_predictions(ticker):
    try:
        df = yf.download(ticker, start='2020-01-01', end='2024-07-17')
        if df.empty or df['Close'].isnull().all():
            raise ValueError("Downloaded dataframe is empty or contains all NaN values.")
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
        return

    df.reset_index(inplace=True)
    latest_stock_price = df['Close'].iloc[-1]

    # Train models
    lstm_model, lstm_scaler = train_lstm_model(ticker)
    transformer_model, transformer_scaler = train_transformer_model(ticker)
    prophet_model = train_prophet_model(ticker)

    # Get predictions
    lstm_predictions = get_lstm_predictions(lstm_model, lstm_scaler, ticker, latest_stock_price)
    transformer_predictions = get_transformer_predictions(transformer_model, transformer_scaler, ticker, latest_stock_price)
    prophet_predictions = get_prophet_predictions(prophet_model, ticker, latest_stock_price)

    last_date = df['Date'].max()
    lstm_dates = pd.date_range(start=last_date, periods=len(lstm_predictions) + 1)[1:]
    transformer_dates = pd.date_range(start=last_date, periods=len(transformer_predictions) + 1)[1:]

    fig, ax = plt.subplots(figsize=(15, 8))
    history_length = 100

    ax.plot(df['Date'][-history_length:], df['Close'][-history_length:], label='Historical Data', linewidth=2)
    ax.plot(prophet_predictions['ds'], prophet_predictions['yhat'], 'b-', label='XGBoost Predicted', linewidth=2)
    ax.plot(lstm_dates, lstm_predictions, label='LSTM Forecast', linewidth=2)
    ax.plot(transformer_dates, transformer_predictions, label='Transformer Forecast', linewidth=2)
    ax.axvline(x=last_date, color='r', linestyle='--', label='Forecast Start')

    ax.set_ylim(bottom=0)
    ax.set_title(f'Stock Price Prediction Comparison for {ticker}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Price')
    ax.legend()

    return fig

# Example usage:
#ticker = input("Enter the stock ticker: ")
#plot_predictions(ticker)
