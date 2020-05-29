from app.indicators.roc_indicator import ROCIndicator
from app.indicators.rsi_indicator import RSIIndicator
from app.indicators.stoch_indicator import StochIndicator


class IndicatorsFactory():
    def build_from_list(self, list_of_indicators_dict):
        indicators = []
        for indicator in list_of_indicators_dict:
            indicators.append(
                self.build_from_dict(indicator)
            )
        return indicators

    def build_from_dict(self, indicators_dict):
        if isinstance(indicators_dict, list):
            return self.build_from_list(indicators_dict)
        

        indicators = {
            # roc indicator
            ROCIndicator(indicators_dict["indicator"]).name(): ROCIndicator(indicators_dict["params"]),
            # rsi indicator
            RSIIndicator(indicators_dict["indicator"]).name(): RSIIndicator(indicators_dict["params"]),
            # stoch indicator
            StochIndicator(indicators_dict["indicator"]).name(): StochIndicator(indicators_dict["params"])
        }
        indicator = indicators.get(indicators_dict["indicator"])
        if indicator.is_valid():
            return indicator
        return None

    def build_single(self, indicator_dict):
        print("\n", indicators)
        return indicators.get(indicator_dict["name"])