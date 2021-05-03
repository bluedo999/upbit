import time
import pyupbit
import datetime
import requests

access = "EL13IF46ku47ex7AxnynmmxHu31Pawiz20CIj7eu"
secret = "zuuaqx3R3PNn6KpJd3UIQSgpivA2kxX1Jurw6xIJ"
myToken = "xoxb-2015723902582-2009813660199-vB3IuINgQDiRMZSzz4nORgof"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=9)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=9)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=30)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(coin):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#upbit", "autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-MFT")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-MFT", 0.5)
            ma15 = get_ma15("KRW-MFT")
            current_price = get_current_price("KRW-MFT")
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-MFT", krw*0.9995)
                    post_message(myToken,"#upbit", "MFT buy : " +str(buy_result))
        else:
            btc = get_balance("MFT")
            if btc > 0.00008:
                sell_result = upbit.sell_market_order("KRW-MFT", btc*0.9995)
                post_message(myToken,"#upbit", "MFT buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#upbit", e)
        time.sleep(1)