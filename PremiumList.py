import sys
from binance.client import Client
from PyQt5.QtCore import QTime, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pykorbit
import time
import binanceTrading
import UpbitTrading
# qtdesigner ui 불러오기
form_class = uic.loadUiType("UI.ui")[0]

tickers =['BTC', 'ETH','XLM','DOT','XRP','TRX','ADA','NEO','QTUM','EOS','IOTA','GAS','BTT','WAXP','QKC','SC','STEEM','HIVE','ICX']

class Worker(QThread):
    # 시그널 객체를 생성합니다.
    finished =pyqtSignal(dict,dict,dict,dict)
    def run(self):
        while True:
            binance_data ={}
            upbit_data ={}
            price_btc ={}
            Premium = {}
            # get data from binance market.
            for ticker in tickers:
                binance_data[ticker] = binanceTrading.get_current_price(ticker)

                # get data from upbit market.
                upbit_data[ticker] = UpbitTrading.get_current_price(ticker)
                # get price in BTC
                price_btc[ticker] = UpbitTrading.get_current_price_in_BTC(ticker)
                #get Premium result
                Premium[ticker] = binanceTrading.calculate_premium(ticker)

                # 시그널을 발생시킵니다. data 객체를 전송합니다.
                self.finished.emit(binance_data, upbit_data,price_btc,Premium)





class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.worker = Worker()
        # finished 시그널이 emit 되면 update_table_widget 메서드가 호출되도록 설정
        self.worker.finished.connect(self.update_table_widget)
        self.worker.start()
        # 타이머 만들기
        #timer = QTimer(self)
        # 5초마다 timeout이 발생하게 한다.
        #timer.start(5000)
        #timer.timeout.connect(self.timeout)

    def update_table_widget(self,binance_data, upbit_data, price_BTC,Premium):

        try:
            # display binance currencies price
            for ticker,price in binance_data.items():
                index = tickers.index(ticker)
                self.tableWidget.setItem(index, 0, QTableWidgetItem(str(price)))

            # display upbit currencies price
            for ticker,price in upbit_data.items():
                index = tickers.index(ticker)
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(price)))
            # display upbit currencies in BTC
            for ticker, price in price_BTC.items():
                index = tickers.index(ticker)
                #display price in BTC
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(format(price,'.8f'))))
            for ticker, premium in Premium.items():

                index = tickers.index(ticker)
                #display price in BTC
                self.tableWidget.setItem(index, 3, QTableWidgetItem(str(premium)))
        except:
            pass
# UI 실행시키기
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()