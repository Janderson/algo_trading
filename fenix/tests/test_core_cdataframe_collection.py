import unittest
from app.core.cdataframe_collection import CDataFrameCollection
from app.core.cdataframe import CDataFrame, COHLCDataFrame
import pandas as pd

class TestCoreCDataFrameCollection(unittest.TestCase):
    def test_create_a_collection_of_indicators_should_only_accept_indicators(self):
        collection = CDataFrameCollection()

        df = pd.DataFrame([{"open": 1, "high":5, "low": 2, "close":3, "volume": 15000, 
                "time": pd.to_datetime("2020-05-18"), "ticker": "PETR4"}
        ])
        cdataframe = COHLCDataFrame(df)
        self.assertTrue(cdataframe.is_valid())

        self.assertTrue(collection.add(cdataframe))
        with self.assertRaises(Exception):
            collection.add("should not accept string")
