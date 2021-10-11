import pyupbit

access = ""          # 본인 값으로 변경
secret = ""          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)


# 잔고조회
print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회 리플 보유수량
print(upbit.get_balance("KRW-BTC"))
print(upbit.get_balance("KRW"))         # 보유 현금 조회


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


#upbit.buy_market_order("KRW-DOT", 5000)
btc = upbit.get_balance("DOT")  # 현재 가지고 있는 BTC의 잔고를 가져옴
upbit.sell_market_order("KRW-DOT", btc*0.9995)
