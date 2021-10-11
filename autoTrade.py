import time
import pyupbit
import datetime

access = ""          
secret = ""         


def get_target_price(ticker, k):  # ticker:코인 이름 k:변동값
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    # [close] 종가 ==> 다음날 시가
    target_price = df.iloc[0]['close'] + \
        (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day",
                           count=1)  # ohlcy day로 조회하면 일봉을 가져올 수 있고
    start_time = df.index[0]  # 가장 첫번째가 시작 시간 값임
    return start_time  # 일봉의 조회시간은 9시니까 요약하면 9시를 가져오는 것임.


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")  # 9:00
        end_time = start_time + datetime.timedelta(days=1)  # 9시+1일 다음날 9시

        # 9시< 현재 < 8시59분50초
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)  # 매수목표가 설정
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")  # 현재 가지고 있는 원화를 가져옴
                if krw > 5000:  # 잔고가 최소거래 금액 5천원 이상인 경우
                    1
                    #  upbit.buy_market_order("KRW-BTC", krw*0.9995)  # 비트코인 매수
        else:
            btc = get_balance("BTC")  # 현재 가지고 있는 BTC의 잔고를 가져옴
            if btc > 0.00008:  # 현재 시간 기준으로 대략 5천원
                # 당일 종가에 비트코인을 전량 매도 / 수수료를 제외하고 매도
                1
                #upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
