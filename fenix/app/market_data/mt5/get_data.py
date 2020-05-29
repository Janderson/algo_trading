from app.market_data.mt5.connection import MT5Connection
from app.core.cdataframe import COHLCDataFrame
from app.core.cdataframe_collection import CDataFrameCollection

class CMT5MarketData:
    def get_stocks(self, stock_timeframes, qtd_bars = 5000):
        _collection = CDataFrameCollection()
        with MT5Connection() as mt5_conn:
            for ticker, timeframe in stock_timeframes:
                bars_df = mt5_conn.get_bars_to_df(ticker, timeframe, qtd=qtd_bars)
                _collection.add(COHLCDataFrame(bars_df, 
                    info={"ticker": ticker, "timeframe": timeframe}))
        return _collection
