from app.core.cdataframe import COHLCDataFrame
import pandas as pd


class ConvertCSVFile:
    def __init__(self):
        pass

    def from_csv(self, csv_path):
        return COHLCDataFrame(pd.read_csv(csv_path).rename({"tick_volume": "volume"}, axis=1))
