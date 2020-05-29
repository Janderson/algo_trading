from app.indicators.base_indicator import BaseIndicator
from ta.momentum import ROCIndicator as ta_ROCIndicator


class ROCIndicator(BaseIndicator):
    def calc(self, dataframe):
        roc = ta_ROCIndicator(close=dataframe.close, n=self.params.get("period"))
        dataframe[self.col_name()] = roc.roc()
        return dataframe
    
    def name(self):
        return "roc"
    
    def base_params(self):
        return {"period": 1}

    def col_name(self):
        return "roc_{}".format(self.params.get("period"))

