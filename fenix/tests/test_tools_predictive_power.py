import unittest
import pandas as pd
from app.core.calculator import Calculator
from app.core.cdataframe import COHLCDataFrame
from app.tools.predictive_power import CPredictivePower, DEFAULT_PARAMS
from app.indicators.indicators_factory import IndicatorsFactory


class TestToolsPredictivePower(unittest.TestCase):
    def setUp(self):
        dataframe1 = pd.DataFrame([
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000, 
                "time": pd.to_datetime("2020-05-18"), "ticker": "PETR4", "timeframe": "M15"},
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000, 
                "time": pd.to_datetime("2020-05-19"), "ticker": "PETR4", "timeframe": "M15"},
            {"open": 14, "high":14, "low": 14, "close":14, "volume": 14, 
                "time": pd.to_datetime("2020-05-14"), "ticker": "PETR4", "timeframe": "M15"},
            {"open": 14, "high":14, "low": 14, "close":5, "volume": 14, 
                "time": pd.to_datetime("2020-05-20"), "ticker": "PETR4", "timeframe": "M15"},
            {"open": 14, "high":14, "low": 14, "close":8, "volume": 14, 
                "time": pd.to_datetime("2020-05-21"), "ticker": "PETR4", "timeframe": "M15"},
        ])
        cdataframe = COHLCDataFrame(dataframe1)
        self.indicator = IndicatorsFactory().build_from_dict({
            "indicator": "roc",
            "params": {
                "period": 2
            }
        })
        self.indicator1 = IndicatorsFactory().build_from_dict({
            "indicator": "roc",
            "params": {
                "period": 1
            }
        })
        self.calculator = Calculator(cdataframe)

        self.calculator.add_indicator(self.indicator)
        self.calculator.add_indicator(self.indicator1)
        

    def test_predictive_power_estimate_and_get_a_return(self):
        ppower = CPredictivePower(self.calculator.calc(), self.indicator)
        ppower.estimate()
        print(ppower.stats.keys())
        self.assertTrue("max_returns" in ppower.stats.keys())
        self.assertTrue("indicator_name" in ppower.info)
        self.assertEqual(ppower.stats["indicator_name"], "roc")
        self.assertTrue(hasattr(ppower, "predictive_power"))


    def test_predictive_power_estimate_params(self):
        ppower = CPredictivePower(self.calculator.calc(), 
                    self.indicator, 
                    params={"num_bins": 15})
        self.assertEqual(ppower.num_bins, 15)
        
        ppower = CPredictivePower(self.calculator.calc(), 
                    self.indicator, 
                    params={"gain_ahead": 5})
        self.assertEqual(ppower.gain_ahead, 5)

        ppower = CPredictivePower(self.calculator.calc(), 
                    self.indicator, 
                    params={"lag": 2})
        self.assertEqual(ppower.lag, 2)

        ppower = CPredictivePower(self.calculator.calc(), 
                    self.indicator, 
                    params={"lag": 2})
        self.assertNotEqual(ppower.gain_ahead, 2, "should not be equal")
