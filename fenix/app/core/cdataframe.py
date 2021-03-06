from abc import ABC, abstractmethod


DATAFRAME_COLUMNS = ["time", "open", "high", "low", "close", "volume"]


class CDataFrame(ABC):
    def __init__(self, dataframe, info={}):
        self.__dataframe = dataframe
        self._info = info
        if self.is_valid():
            self.parse()
    
    @property
    def dataframe(self):
        return self.__dataframe

    @property
    def info(self):
        return self._info

    def get(self):
        return self.__dataframe.copy()
    
    def set(self, dataframe):
        self.__dataframe = dataframe

    @abstractmethod
    def parse(self):
        pass

    def is_valid(self):
        return all([
            len(set(DATAFRAME_COLUMNS)-set(list(self.dataframe.columns)))==0
        ])

    @property
    def columns(self):
        return list(self.dataframe.columns)
    
    @staticmethod
    def is_type_obj(obj):
        return any([
            isinstance(obj, CDataFrame),
            issubclass(obj.__class__, CDataFrame)
        ])


class COHLCDataFrame(CDataFrame):
    def __init__(self, dataframe, info={}):
        super().__init__(dataframe, info=info)

    def parse(self):
        if "ticker" in self.dataframe.columns:
            self._info["ticker"] = self.dataframe.ticker.iloc[0]
        if "timeframe" in self.dataframe.columns:
            self._info["timeframe"] = self.dataframe.timeframe.iloc[0]
        self.set(self.dataframe[DATAFRAME_COLUMNS].sort_values(["time"], ascending=True))


class CCalcDataFrame(CDataFrame):
    def __init__(self, dataframe, info={}):
        super().__init__(dataframe, info=info)

    def parse(self):
        pass
