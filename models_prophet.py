from prophet import Prophet
import pandas as pd

def prepare_prophet_data(df):
    df_prophet = pd.DataFrame()
    df_prophet["ds"] = df.index
    df_prophet["y"] = df["Close"]
    return df_prophet

def train_prophet(df):
    df_prophet = prepare_prophet_data(df)
    model = Prophet(daily_seasonality=True)
    model.fit(df_prophet)
    return model

def predict_prophet_trend(model, periods=5):
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    forecast_period = forecast.tail(periods)
    trend = (forecast_period["yhat"].iloc[-1] - forecast_period["yhat"].iloc[0]) / forecast_period["yhat"].iloc[0]
    return trend
