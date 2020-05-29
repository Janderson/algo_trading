from ta.momentum import RSIIndicator as ta_RSI, StochasticOscillator
from app.indicators.base_indicator import BaseIndicator


class RSIIndicator(BaseIndicator):
    def calc(self, dataframe):
        rsi = ta_RSI(close=dataframe.close, n=self.params.get("period"))
        dataframe[self.col_name()] = rsi.rsi()
        return dataframe
        
    def name(self):
        return "rsi"
    
    def col_name(self):
        return "rsi_{}".format(self.params.get("period"))

    def base_params(self):
        return {"period": 14}
