import MetaTrader5 as mt5
import pandas as pd

class MT5Connection:
    def __init__(self):
        pass
    
    def open(self):
        return mt5.initialize()

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        mt5.shutdown()
        if exc_type:
            print("exit: {}, {}, {}".format(exc_type, exc_val, exc_tb))
        return True

    def get_bars(self, symbol, timeframe, start_index=0, qtd=10):
        return mt5.copy_rates_from_pos(symbol, 
                                       self.str_timeframe_to_mt5(timeframe), 
                                       start_index, 
                                       qtd)
    
    def get_bars_to_df(self, symbol, timeframe, start_index=0, qtd=1):
        rates = self.get_bars(symbol, 
                              timeframe, start_index=start_index, qtd=qtd)
        columns=['time', 'open', 'low', 'high', 'close', 'tick_volume', 'spread', 'real_volume']
        rates_dataframe = pd.DataFrame(rates,columns=columns)

        rates_dataframe['time'] = pd.to_datetime(rates_dataframe['time'], unit="s")
        return rates_dataframe

    def str_timeframe_to_mt5(self, tf_str):
        if tf_str == "D1":
            return mt5.TIMEFRAME_D1

        elif tf_str == "H1":
            return mt5.TIMEFRAME_H1

        elif tf_str == "M30":
            return mt5.TIMEFRAME_M30

        elif tf_str == "M15":
            return mt5.TIMEFRAME_M15

        elif tf_str == "M5":
            return mt5.TIMEFRAME_M5

        elif tf_str == "M1":
            return mt5.TIMEFRAME_M1
