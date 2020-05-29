import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

DEFAULT_PARAMS = {
    "gain_ahead": 1,
    "lag": 0,
    "num_bins": 20,
    "method": "mean"
}

class CPredictivePower():
    def __init__(self, c_dataframe, indicator_to_predict, params = {}):
        self._indicator = indicator_to_predict
        self._dataframe = c_dataframe
        self.params = params
        self._stats = {}

    def estimate(self):
        result_df = self.build_a_new_dataframe()
        sorted_df = self.sort_and_binned_data(result_df)
        self._stats = self.calc_stats(sorted_df)

    def build_a_new_dataframe(self):
        close_series = self._dataframe.get().close
        col_name = self._indicator.col_name()
        indicator_series = self._dataframe.get()[col_name]
        dataframe = pd.DataFrame({
            "returns": close_series.pct_change(), 
            "indicator": indicator_series
        })
        dataframe["gain_ahead"] = dataframe["returns"].rolling(
            window=abs(self.gain_ahead)).sum().shift(-abs(self.gain_ahead))
        if self.lag>0:
            dataframe["indicator"] = dataframe.indicator.shift(self.lag)
        return dataframe

    def sort_data(self, dataframe):
        dataframe.sort_values(["indicator"], ascending=False, inplace=True)
        dataframe["indicator_grouped"] = pd.cut(dataframe.indicator, self.num_bins, labels=False)
        return dataframe

    def sort_and_binned_data(self, dataframe):
        dataframe = self.sort_data(dataframe)
        df_grouped = dataframe.groupby(["indicator_grouped"]).agg(
            {"gain_ahead": self.method, "indicator":["min", "max"]}).reset_index()
        df_grouped.columns = ["_".join(column) for column in df_grouped.columns.ravel()]
        return df_grouped

    def first_change_sign(self, dataframe):
        try:
            first_change_sign_ = dataframe[ 
                (np.sign(dataframe.gain_ahead_sum)==1) & (np.sign(dataframe.gain_ahead_sum).shift(-1)==-1)
            ].iloc[0]
        except:
            first_change_sign_ = dataframe.iloc[0]
        return first_change_sign_

    def calc_stats(self, dataframe):
        first_change = self.first_change_sign(dataframe)
        ols_model = ols("{} ~ indicator_grouped_".format(
                self.gain_ahead_col), 
                data=dataframe).fit()
        return {
            "selected_start_value": first_change.indicator_min,
            "selected_end_value": first_change.indicator_max,
            "selected_returns": first_change[self.gain_ahead_col],
            "max_returns": dataframe[self.gain_ahead_col].max(),
            "ols_r_squared": ols_model.rsquared
        }

    @property
    def gain_ahead_col(self):
        return "gain_ahead_{}".format(self.method)

    @property
    def gain_ahead(self):
        return self.params.get("gain_ahead", DEFAULT_PARAMS["gain_ahead"])

    @property
    def method(self):
        return self.params.get("method", DEFAULT_PARAMS["method"])

    @property
    def lag(self):
        return self.params.get("lag", DEFAULT_PARAMS["lag"])

    @property
    def predictive_power(self):
        return self._stats.get("ols_r_squared", 0)

    @property
    def num_bins(self):
        return self.params.get("num_bins", DEFAULT_PARAMS["num_bins"])

    @property
    def stats(self):
        return self._stats

    @property
    def info(self):
        info_dict = self.stats
        info_dict["data"] = self._dataframe.info
        info_dict["indicator_name"] = self._indicator.name()
        info_dict["indicator_params"] = self._indicator.params
        return info_dict