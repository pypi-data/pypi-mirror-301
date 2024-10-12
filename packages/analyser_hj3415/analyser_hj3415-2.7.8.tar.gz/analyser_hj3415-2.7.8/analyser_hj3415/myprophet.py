import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from prophet import Prophet
from sklearn.preprocessing import StandardScaler
from utils_hj3415 import utils
from typing import Optional
import plotly.graph_objs as go
from plotly.offline import plot
import matplotlib.pyplot as plt  # Matplotlib 수동 임포트
from db_hj3415 import myredis

class MyProphet:
    def __init__(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        self.raw_data = self.get_raw_data()

        self.scaler = StandardScaler()
        self.model = Prophet()

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        self.raw_data = self.get_raw_data()

    def get_raw_data(self) -> pd.DataFrame:
        """
        야후에서 해당 종목의 4년간 주가 raw data를 받아온다.
        :return:
        """
        # 오늘 날짜 가져오기
        today = datetime.today()

        # 4년 전 날짜 계산 (4년 = 365일 * 4)
        four_years_ago = today - timedelta(days=365 * 4)

        return yf.download(
            self.code + '.KS',
            start=four_years_ago.strftime('%Y-%m-%d'),
            end=today.strftime('%Y-%m-%d')
        )

    def preprocessing_for_prophet(self) -> pd.DataFrame:
        """
        Prophet이 사용할 수 있도록 데이터 준비
        ds는 날짜, y는 주가
        :return:
        """
        df = self.raw_data[['Close', 'Volume']].reset_index()
        df.columns = ['ds', 'y', 'volume']  # Prophet의 형식에 맞게 열 이름 변경

        # 추가 변수를 정규화
        df['volume_scaled'] = self.scaler.fit_transform(df[['volume']])
        return df

    def make_forecast(self) -> pd.DataFrame:
        # Prophet을 위한 dataframe 만들기
        df_for_prophet = self.preprocessing_for_prophet()

        # 정규화된 'volume_scaled' 변수를 외부 변수로 추가
        self.model.add_regressor('volume_scaled')

        self.model.fit(df_for_prophet)

        # 향후 180일 동안의 주가 예측
        future = self.model.make_future_dataframe(periods=180)

        # 미래 데이터에 거래량 추가 (평균 거래량을 사용해 정규화)
        future_volume = pd.DataFrame({'volume': [self.raw_data['Volume'].mean()] * len(future)})
        future['volume_scaled'] = self.scaler.transform(future_volume[['volume']])

        forecast = self.model.predict(future)
        return forecast

    def export_to(self, to="str") -> Optional[str]:
        """
        prophet과 plotly로 그래프를 그려서 html을 문자열로 반환
        :param to: str, png, htmlfile, show
        :return:
        """
        # 실제 데이터
        df = self.preprocessing_for_prophet()
        # 예측 데이터
        forecast = self.make_forecast()

        # Plotly를 사용한 시각화
        fig = go.Figure()

        # 실제 데이터
        fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], mode='markers', name='실제주가'))
        # 예측 데이터
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='예측치'))

        # 상한/하한 구간
        fig.add_trace(
            go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill=None, mode='lines', name='상한'))
        fig.add_trace(
            go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', mode='lines', name='하한'))

        fig.update_layout(
            title=f'{self.code} {self.name} 주가 예측 그래프(prophet)',
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis = dict(
                tickformat='%Y/%m',  # X축을 '연/월' 형식으로 표시
            ),
            yaxis = dict(
                tickformat=".0f",  # 소수점 없이 원래 숫자 표시
            )
        )

        if to == 'str':
            # 그래프 HTML로 변환 (string 형식으로 저장)
            graph_html = plot(fig, output_type='div')
            return graph_html
        elif to == 'png':
            # 그래프를 PNG 파일로 저장
            fig.write_image("plotly_graph.png")
        elif to == 'htmlfile':
            # 그래프를 HTML로 저장
            plot(fig, filename='graph_plotly.html', auto_open=False)
            return None
        elif to == 'show':
            # 예측 결과 출력
            print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
            # 예측 결과 시각화 (Matplotlib 사용)
            fig = self.model.plot(forecast)
            # 추세 및 계절성 시각화
            fig2 = self.model.plot_components(forecast)
            plt.show()  # 시각화 창 띄우기
        else:
            Exception("to 인자가 맞지 않습니다.")




