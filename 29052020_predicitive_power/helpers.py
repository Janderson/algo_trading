import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import qgrid
import warnings
warnings.filterwarnings("ignore")
import os, sys, json

sys.path.append(os.path.abspath("../fenix"))
from app.tools.predictive_power import CPredictivePower
from app.market_data.mt5.get_data import CMT5MarketData
from app.core.calculator import Calculator
from app.indicators.indicators_factory import IndicatorsFactory    


def build_predictive_power_for_group_stocks_and_indicators(cdataframes, indicators):
    ppowers = []
    for cohcl in cdataframes.collection:
        calculator = Calculator(cohcl)
        for indicator in indicators:
            calculator.add_indicator(indicator)
            ppower = CPredictivePower(calculator.calc(), indicator)
            ppower.estimate()
            stats = ppower.info
            stats["ticker"] = cohcl.info["ticker"]
            stats["timeframe"] = cohcl.info["timeframe"]
            ppowers.append(stats)

    results = pd.DataFrame([pp for pp in ppowers])
    results["indicator_period"] = results.indicator_params.astype(str).str.replace("'", "")
    return results
    
def indicators_names():
    with open("indicators.v1.0.names", "r") as f: 
        return json.loads(f.read())
