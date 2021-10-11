import pyupbit
import numpy as np

# count일 동안의 ohlcv (open, high, low, close, volumne)로 당일 시가,고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-BTC", count=7)

# 변동성 돌파 전략
# 어제의 고가와 어제의 저가의 변동폭 차이의 k배만큼 증가했을때 구매

# 변동폭 * k 계산, (고가-저가)*k값
df['range'] = (df['high'] - df['low']) * 0.5  # k를 0.5로 잡음
print(df['range'])
# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
print(df['range'].shift(1))
print(df['open'])
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.05  # 수수료
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
# df.to_excel("dd.xlsx")
