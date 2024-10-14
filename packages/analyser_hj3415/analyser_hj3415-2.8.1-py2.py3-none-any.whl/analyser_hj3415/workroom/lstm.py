import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# 1. 데이터 다운로드 (애플 주식 데이터를 사용)
#stock_data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')
# 삼성전자 주식 데이터 가져오기 (KOSPI 상장)
#stock_data = yf.download('005930.KS', start='2019-01-01', end='2024-10-11')
# 크래프톤 주식 데이터 가져오기 (KOSPI 상장)
stock_data = yf.download('259960.KS', start='2020-01-01', end='2024-10-11')
# 하이닉스 주식 데이터 가져오기 (KOSPI 상장)
#stock_data = yf.download('000660.KS', start='2019-01-01', end='2024-10-11')


# 2. 필요한 열만 선택 (종가만 사용)
data = stock_data['Close'].values.reshape(-1, 1)

# 3. 데이터 정규화 (0과 1 사이로 스케일링)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# 4. 학습 데이터 생성
# 주가 데이터를 80%는 학습용, 20%는 테스트용으로 분리하는 코드
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]


# 학습 데이터에 대한 입력(X)과 출력(y)를 생성
def create_dataset(data, time_step=60):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:i + time_step, 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)


X_train, y_train = create_dataset(train_data)
X_test, y_test = create_dataset(test_data)

# LSTM 모델 입력을 위해 데이터를 3차원으로 변환
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# 5. LSTM 모델 생성
model = Sequential()
model.add(LSTM(units=200, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=50))
model.add(Dropout(0.3))
model.add(Dense(units=1))

# 6. 모델 컴파일 및 학습
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=20, batch_size=32)

# 7. 테스트 데이터 예측
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)  # 스케일링 복원

# 8. 미래 30일 예측
# 마지막 60일간의 데이터를 기반으로 미래 30일을 예측
future_days = 30
last_60_days = test_data[-60:]
last_60_days = last_60_days.reshape(1, -1, 1)

future_predictions = []
for _ in range(future_days):
    predicted_price = model.predict(last_60_days)
    future_predictions.append(predicted_price[0][0])

    # 예측값을 다시 입력으로 사용하여 새로운 예측을 만듦
    predicted_price_reshaped = np.reshape(predicted_price, (1, 1, 1))  # 3D 배열로 변환
    last_60_days = np.append(last_60_days[:, 1:, :], predicted_price_reshaped, axis=1)

# 예측된 주가를 다시 스케일링 복원
future_predictions = np.array(future_predictions).reshape(-1, 1)
future_predictions = scaler.inverse_transform(future_predictions)

# 9. 날짜 생성 (미래 예측 날짜)
last_date = stock_data.index[-1]
future_dates = pd.date_range(last_date, periods=future_days + 1).tolist()[1:]

# 10. 시각화
plt.figure(figsize=(10, 6))

# 실제 주가
plt.plot(stock_data.index, stock_data['Close'], label='Actual Price')

# 미래 주가 예측
plt.plot(future_dates, future_predictions, label='Future Predicted Price', linestyle='--')

plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.title('Apple Stock Price Prediction with LSTM')
plt.show()

# 8. 시각화
plt.figure(figsize=(10, 6))
plt.plot(stock_data.index[train_size + 60:], data[train_size + 60:], label='Actual Price')
plt.plot(stock_data.index[train_size + 60:], predictions, label='Predicted Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.title('Apple Stock Price Prediction with LSTM')
plt.show()
