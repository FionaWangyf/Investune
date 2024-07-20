import pandas as pd
import yfinance as yf
from prophet import Prophet

def train_prophet_model(ticker):
    df = yf.download(ticker, start='2020-01-01', end='2024-07-11')
    if df.empty or df['Close'].isnull().all():
        raise ValueError("Downloaded dataframe is empty or contains all NaN values.")
    
    df_prophet = df[['Close']].rename_axis('Date').reset_index()
    df_prophet.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)

    model_prophet = Prophet(changepoint_prior_scale=0.05, yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model_prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    model_prophet.fit(df_prophet)

    return model_prophet

def get_prophet_predictions(model_prophet, ticker, latest_stock_price=None):
    df = yf.download(ticker, start='2020-01-01', end='2024-07-11')
    future = model_prophet.make_future_dataframe(periods=60)
    forecast = model_prophet.predict(future)
    prophet_predictions = forecast[['ds', 'yhat']].tail(60)

    if latest_stock_price is not None:
        adjustment = latest_stock_price - prophet_predictions['yhat'].iloc[0]
        prophet_predictions['yhat'] += adjustment

    return prophet_predictions
