from app.market_data.mt5.connection import MT5Connection


def get_dict_of_historical_data(stocks, timeframe="D1", qtd_bars=5000):
    bars = {}
    with MT5Connection() as mt5_con:
        for ticker in stocks:
            df = mt5_con.get_bars_to_df(ticker, timeframe, qtd=qtd_bars)
            bars[ticker] = df
    return bars

def build_a_dataframe_from_dict_of_historical(dict_of_bars_df):
    prices_df = pd.DataFrame()
    for ticker in dict_of_bars_df.keys():
        stock_df = dict_of_bars_df[ticker]
        series_close = stock_df[["close", "time"]]
        series_close.rename({"close": ticker}, axis=1, inplace=True)
        series_close.time = pd.to_datetime(series_close.time)
        if len(prices_df.columns)==0:
            prices_df = series_close
        else:
            prices_df = pd.merge(prices_df, series_close, how='outer', on='time')
    return prices_df


