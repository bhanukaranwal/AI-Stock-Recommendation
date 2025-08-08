from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import xgboost as xgb

FEATURES = ["RSI", "MACD", "SMA_50", "SMA_200", "EMA_20", "EMA_50", "ATR"]

def prepare_data(df):
    X = df[FEATURES]
    y = df["Target"]
    split = int(len(df) * 0.8)
    return X[:split], X[split:], y[:split], y[split:]

def train_random_forest(df):
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, acc

def train_xgboost(df):
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, acc

def predict_signal(model, latest_row):
    pred = model.predict(latest_row[FEATURES].values.reshape(1, -1))
    return "BUY" if pred[0] == 1 else "SELL"
