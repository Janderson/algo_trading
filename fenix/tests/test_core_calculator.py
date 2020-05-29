import unittest
import pandas as pd
from app.core.calculator import Calculator
from app.core.cdataframe import CDataFrame, COHLCDataFrame
from app.market_data.mt5.convert_csv_file import ConvertCSVFile
from app.indicators.indicators_factory import IndicatorsFactory


class TestCoreCalculator(unittest.TestCase):

    def setUp(self):
        self.cdataframe = ConvertCSVFile().from_csv("tests/test_core_calculator.csv")

    def test_calculator_add_indicator_and_calc(self):
        def no_sense_function(param1, param2):
            pass
        calculator = Calculator(self.cdataframe)

        indicator = IndicatorsFactory().build_from_dict({
            "indicator": "roc",
            "params": {
                "period": 2
            }
        })

        calculator.add_indicator(indicator)
        result_dataframe = calculator.calc()
        self.assertTrue(indicator.col_name() in result_dataframe.columns)
        self.assertTrue("roc_2" in result_dataframe.columns)

    def test_calculator_with_two_indicators_inside_should_return_each_column_to_each_indicator(self):
        def no_sense_function(param1, param2):
            pass
        calculator = Calculator(self.cdataframe)


        indicator_rets = IndicatorsFactory().build_from_dict({
            "indicator": "roc",
            "params": {
                "period": 2
            }
        })

        indicator_rsi = IndicatorsFactory().build_from_dict({
            "indicator": "rsi",
            "params": {
                "period": 5
            }
        })
        calculator.add_indicator(indicator_rets)
        calculator.add_indicator(indicator_rsi)
        result_dataframe = calculator.calc()
        self.assertTrue(indicator_rets.col_name() in result_dataframe.columns)
        self.assertTrue(indicator_rsi.col_name() in result_dataframe.columns)
        self.assertTrue("roc_2" in result_dataframe.columns)
        self.assertTrue("rsi_5" in result_dataframe.columns)

    def test_if_info_of_dataframe_is_keep_into_result(self):
        
        calculator = Calculator(self.cdataframe)

        indicator = IndicatorsFactory().build_from_dict({
            "indicator": "roc",
            "params": {
                "period": 2
            }
        })
        calculator.add_indicator(indicator)
        expected_info = {"timeframe":"D1"}
        self.cdataframe._info = expected_info

        result_dataframe = calculator.calc()
        self.assertEqual(result_dataframe.info, expected_info)
