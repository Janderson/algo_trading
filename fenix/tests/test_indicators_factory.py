import unittest
from app.indicators.base_indicator import BaseIndicator
from app.indicators.indicators_factory import IndicatorsFactory


class TestIndicatorsFactory(unittest.TestCase):
    def test_create_a_indicator_from_factory(self):
        indicator = IndicatorsFactory().build_from_dict({
            "indicator": "roc",
            "params": {
                "period": 2
            }
        })

        self.assertTrue(BaseIndicator.is_type_obj(indicator))
        self.assertEqual(indicator.name(), "roc")
        self.assertEqual(indicator.params.get("period"), 2)

    def test_create_a_indicator_from_factory_with_default_parameters(self):
        indicator = IndicatorsFactory().build_from_dict({
            "indicator": "stoch",
            "params": {
                "period": 2
            }
        })

        self.assertTrue(BaseIndicator.is_type_obj(indicator))
        self.assertEqual(indicator.name(), "stoch")
        self.assertEqual(indicator.params.get("period"), 2)
        self.assertEqual(indicator.params.get("d_period"), 3)

    def test_create_a_rsi_indicator_from_factory(self):
        expected_period = 15
        indicator = IndicatorsFactory().build_from_dict({
            "indicator": "rsi",
            "params": {
                "period": expected_period
            }
        })

        self.assertTrue(BaseIndicator.is_type_obj(indicator))
        self.assertEqual(indicator.name(), "rsi")
        self.assertEqual(indicator.col_name(), "rsi_{}".format(expected_period))
        self.assertEqual(indicator.params.get("period"), expected_period)

    def test_create_a_stoch_indicator_from_factory(self):
        expected_period = 14
        default_d_period = 3
        indicator = IndicatorsFactory().build_from_dict({
            "indicator": "stoch",
            "params": {
                "period": expected_period
            }
        })

        self.assertTrue(BaseIndicator.is_type_obj(indicator))
        self.assertEqual(indicator.name(), "stoch")
        self.assertEqual(indicator.col_name(), "stoch_{}_{}".format(expected_period, default_d_period))
        self.assertEqual(indicator.params.get("period"), expected_period)

    def test_create_a_indicators_from_list_factory(self):
        expected_period = 14
        default_d_period = 3
        indicators = IndicatorsFactory().build_from_dict([{
            "indicator": "stoch",
            "params": {
                "period": expected_period
            }
        },{
            "indicator": "stoch",
            "params": {
                "period": expected_period+1
            }
        }])

        self.assertTrue(BaseIndicator.is_type_obj(indicators[0]))
        self.assertEqual(indicators[0].name(), "stoch")
        self.assertEqual(indicators[0].col_name(), "stoch_{}_{}".format(expected_period, default_d_period))
        self.assertEqual(indicators[0].params.get("period"), expected_period)

