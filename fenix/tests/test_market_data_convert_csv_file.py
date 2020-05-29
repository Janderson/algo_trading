import unittest
from app.market_data.mt5.convert_csv_file import ConvertCSVFile


class TestMarketDataConvertCSV(unittest.TestCase):

    def test_convert_a_csv_file_from_mt5_and_convert_into_a_valid_format(self):
        cdataframe = ConvertCSVFile().from_csv("tests/test_market_data_convert_csv_file.csv")
        self.assertTrue(cdataframe.is_valid())
