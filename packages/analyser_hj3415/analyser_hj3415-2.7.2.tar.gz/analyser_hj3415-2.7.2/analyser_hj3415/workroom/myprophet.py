# prophet 사용 공부

import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt  # Matplotlib 수동 임포트


# 애플 주식 데이터를 다운로드
#stock_data = yf.download('AAPL', start='2020-01-01', end='2024-10-09')
# 삼성전자 주식 데이터 가져오기 (KOSPI 상장)
#stock_data = yf.download('005930.KS', start='2020-01-01', end='2024-08-01')
# 크래프톤 주식 데이터 가져오기 (KOSPI 상장)
#stock_data = yf.download('259960.KS', start='2020-01-01', end='2024-10-08')
# 하이닉스 주식 데이터 가져오기 (KOSPI 상장)
stock_data = yf.download('000660.KS', start='2020-01-01', end='2024-10-08')


# Prophet이 사용할 수 있도록 데이터 준비
df = stock_data[['Close', 'Volume']].reset_index()
df.columns = ['ds', 'y', 'volume']  # Prophet의 형식에 맞게 열 이름 변경

from sklearn.preprocessing import StandardScaler

# 추가 변수를 정규화
scaler = StandardScaler()
df['volume_scaled'] = scaler.fit_transform(df[['volume']])

# Prophet 모델 생성 및 학습
model = Prophet()

# 정규화된 'volume_scaled' 변수를 외부 변수로 추가
model.add_regressor('volume_scaled')

model.fit(df)

# 향후 180일 동안의 주가 예측
future = model.make_future_dataframe(periods=180)

# 미래 데이터에 거래량 추가 (평균 거래량을 사용해 정규화)
future_volume = pd.DataFrame({'volume': [stock_data['Volume'].mean()] * len(future)})
future['volume_scaled'] = scaler.transform(future_volume[['volume']])


forecast = model.predict(future)



# 예측 결과 출력
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# 예측 결과 시각화 (Matplotlib 사용)
fig = model.plot(forecast)

# 추세 및 계절성 시각화
fig2 = model.plot_components(forecast)

plt.show()  # 시각화 창 띄우기
