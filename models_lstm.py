import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

FEATURES = ["RSI", "MACD", "SMA_50", "SMA_200", "EMA_20", "EMA_50", "ATR"]

def prepare_lstm_data(df, time_steps=60):
    scaler = MinMaxScaler()
    data = scaler.fit_transform(df[FEATURES])
    X, y = [], []
    for i in range(time_steps, len(data) - 1):
        X.append(data[i-time_steps:i])
        y.append(1 if df["Target"].iloc[i] == 1 else 0)
    X, y = np.array(X), np.array(y)
    return X, y, scaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

def train_lstm(df, epochs=30, batch_size=32):
    X, y, scaler = prepare_lstm_data(df)
    if len(X) == 0:
        raise ValueError("Not enough data for LSTM training")
    split = int(len(X) * 0.8)
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]
    model = build_lstm_model((X.shape[1], X.shape[2]))
    early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
              validation_data=(X_val, y_val), callbacks=[early_stop], verbose=0)
    val_acc = model.evaluate(X_val, y_val, verbose=0)[1]
    return model, scaler, val_acc

def predict_lstm(model, scaler, recent_data):
    data_scaled = scaler.transform(recent_data[FEATURES])
    X = np.expand_dims(data_scaled, axis=0)  # (1, time_steps, features)
    pred = model.predict(X)
    return "BUY" if pred[0][0] > 0.5 else "SELL"
