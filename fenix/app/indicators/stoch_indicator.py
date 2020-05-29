from ta.momentum import RSIIndicator, StochasticOscillator
from app.indicators.base_indicator import BaseIndicator

class StochIndicator(BaseIndicator):
    def calc(self, dataframe):
        stoch = StochasticOscillator(
            close=dataframe.close, 
            low=dataframe.low, 
            high=dataframe.high, 
            n=self.params.get("period"),
            d_n=self.params.get("d_period"))
        dataframe["{}_k".format(self.col_name())] = stoch.stoch()
        return dataframe
    
    def name(self):
        return "stoch"
    
    def col_name(self):
        p = self.params
        return "stoch_{}_{}".format(p.get("period"), p.get("d_period"))
    
    def base_params(self):
        return {"period": 14, "d_period": 3, "signal_line": False}


