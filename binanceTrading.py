from binance.client import Client
import UpbitTrading
# API key 값 가져오기

with open("binancekey.txt") as f:
    lines = f.readlines()

con_key = lines[0].strip()
sec_key = lines[1].strip()

# binance 클래스 객체를 생성하는데 초기화자로 키값을 전달합니다.
client = Client(api_key=con_key, api_secret=sec_key)
tickers = client.get_all_tickers()


# get_curremt price
def get_current_price(ticker):
    try:
        if(ticker == 'BTC'):
            return client.get_symbol_ticker(symbol='BTCUSDT')['price']
        currency = client.get_symbol_ticker(symbol=ticker+'BTC')

        price = currency['price']
        return price
    except:
        return None
def calculate_premium(ticker):
    try:
        if(ticker =='BTC'):
            return '0%'
        binance_price = float(get_current_price(ticker))

        upbit_price = float(UpbitTrading.get_current_price_in_BTC(ticker))

        premium = (upbit_price - binance_price) / binance_price *100
        return format(premium,'.3f') +'%'
    except:
        return None
    return None


