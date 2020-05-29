from app.market_data.mt5.helpers import get_dict_of_historical_data
from app.indicators.indicators_factory import IndicatorsFactory    
from app.tools.predictive_power import CPredictivePower
from app.market_data.mt5.get_data import CMT5MarketData
from app.core.calculator import Calculator
from app.tools.backtester import BackTester
import pandas as pd
from itertools import product

global make_prediction
def make_prediction(**parameters):
    indicator = IndicatorsFactory().build_from_dict({
            "indicator": parameters.get("indicator"),
            "params": {
                "period": parameters.get("period")
            }
        })
    ohlc=parameters.get("ohlc")
    calculator = Calculator(ohlc)
    calculator.add_indicator(indicator)
    ppower = CPredictivePower(calculator.calc(), indicator)
    ppower.estimate()
    return ppower.info

total_results = []
def make_results(results, index, total):
    print("tested {} of {}".format(index, total))
    total_results.extend(list(results.values()))
    pd.DataFrame(total_results).to_csv("results.csv")


if __name__=="__main__":

    mt5 = CMT5MarketData() 
    stocks = ["VALE3", "PETR4", "ITUB4", "BBAS3", "WIN$N", "WDO$N", "ITSA4"]
    timeframes = ["D1", "H1", "M5", "M15"]
    collection = mt5.get_stocks(list(product(stocks, timeframes)))
    for data in collection.collection:
        print(data.info)
    backtester = BackTester(50)
    backtester.build_params(
        ohlc=collection.collection,
        period=range(2, 50),
        indicator=["rsi", "roc"]
    )
    backtester.callback(make_prediction)
    backtester.callback_results(make_results)
    backtester.run()