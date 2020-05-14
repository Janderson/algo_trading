import pandas as pd
import numpy as np


def build_d1_bar(dataframe):
    dataframe = dataframe.copy()
    dataframe["time"] = pd.to_datetime(dataframe["time"])
    dataframe.sort_values(["time"], ascending=True, inplace=True)
    
    dataframe["start_bar_sign"] = dataframe.time.dt.day != dataframe.time.dt.day.shift(1)
    dataframe["end_bar_sign"] = (dataframe.start_bar_sign.shift(-1)) | \
                                (dataframe.index == dataframe.index[-1])
    dataframe["open_bar"] = np.where(dataframe.start_bar_sign,
                                     dataframe.open, np.nan)
    dataframe["close_bar"] = dataframe.close
    dataframe.fillna(method="ffill", inplace=True)
    columns = ["time","open", "close", "open_bar", "close_bar", "start_bar_sign", "end_bar_sign"]
    dataframe = dataframe[columns]
    return dataframe.rename({"close": "close_lower", "open": "open_lower", "open_bar": "open", "close_bar": "close"}, axis=1)

def build_dataframe(df_win, df_bova):
    return build_d1_bar(df_win).set_index("time").join(build_d1_bar(df_bova).set_index("time"), lsuffix="_fut", rsuffix="_etf").reset_index()


def get_a_sample(dataframe, query_exp, start_of=0, minus=5, plus=6):
    indexing = dataframe.query(query_exp).index
    return dataframe.iloc[indexing[start_of]-minus:indexing[start_of]+plus].tail(minus+plus+1)


def get_stats(dataframe, params={}):
    """
        function: get_stats
        calculate statistics
    """
    cum_profit = dataframe.cum_profit.iloc[-1]
    final_pnl = cum_profit
    #cum_cost = opt_df.cum_cost.iloc[-1]
    total_trades = dataframe[(dataframe.signal!=0)&(dataframe.signal!=np.inf)].shape[0]
    winners = dataframe[(dataframe.profit>0)].shape[0]
    profit_by_trade = 0 
    win_ratio = 0
    sharpe_ratio = 0
    sortino_ratio = 0
    loss_means = 0
    win_means = 0
    if total_trades>0:
        trades_df = dataframe[dataframe.signal.shift(1)!=0]
        win_ratio = winners / total_trades
        profit_by_trade = final_pnl / total_trades
        sharpe_ratio = np.mean(trades_df.profit) / np.std(trades_df.profit) *np.sqrt(252)    
        sortino_ratio = np.mean(trades_df.profit) / np.std(trades_df.profit)*np.sqrt(252)
        loss_means = trades_df[trades_df.profit<0].profit.mean()
        win_means = trades_df[trades_df.profit>0].profit.mean()
    returns_dict = {
        "final_pnl": final_pnl,
        "cum_profit": cum_profit,
        "total_trade": total_trades,
        "win_ratio": win_ratio,
        "profit_by_trade": profit_by_trade,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "loss_means": loss_means,
        "win_means": win_means,
        "total_trades": total_trades
    }
    return returns_dict


def calculate_pnl(dataframe, size=1):
    """
        calculate a PNL Curve from a BackTest
    """
    dataframe["fut_points"] = 0
    dataframe["fut_points"] = np.where(
        ((dataframe.end_trade) & (dataframe.signal_carry.shift(1)==1)), 
        (dataframe.close_fut-dataframe.entry_price), dataframe.fut_points)
    dataframe["fut_points"] = np.where(
        (dataframe.end_trade) & (dataframe.signal_carry.shift(1)==-1), 
        (dataframe.entry_price-dataframe.close_fut), dataframe.fut_points)
    
    #dataframe["fut_points"] = np.where(dataframe.end_trade, (dataframe.close_fut-dataframe.entry_price), 0)
    dataframe["fut_profit"] = dataframe.fut_points*0.2*size
    dataframe["profit"] = dataframe.fut_profit
    dataframe["cum_profit"] = dataframe.profit.cumsum()
    return dataframe

def calculate_signals(dataframe, entry=2, period=20, allow_buy=True, allow_sell=True, calc_at_end_of_future=True):
    """
        calculate a signals for strategy
        Every strategy have a different type of signals generated

    """
    # should create columns in original dataframe to update after
    dataframe = dataframe.copy()
    dataframe["z"] = 0
    dataframe["signal"] = np.inf
    dataframe.close_etf.ffill(inplace=True)
    dataframe.open_etf.ffill(inplace=True)
    
    # get a sliced df to calculate in a up tf (D1)
    if calc_at_end_of_future:
        slice_df = dataframe.query("end_bar_sign_fut == True", inplace=False)
    else:
        slice_df = dataframe.query("end_bar_sign_etf == True", inplace=False)
        
    slice_df["signal"] = 0
    slice_df["A"] = slice_df.close_fut.pct_change()
    slice_df["B"] = slice_df.close_etf.pct_change()
    slice_df["dif"] = slice_df.A - slice_df.B
    slice_df["means"] = slice_df.dif.rolling(window=period).mean()
    slice_df["stddev"] = slice_df.dif.rolling(window=period).std(ddfo=0)
    
    slice_df["z"] = (slice_df.dif - slice_df.dif.rolling(window=period).mean())/slice_df.dif.rolling(window=period).std(ddfo=0)
    
    # calculate signal from z-score
    size = 1
    if allow_sell:
        slice_df["signal"] = np.where(slice_df.z>=entry, -1, slice_df.signal)
    # seems strange but z<z-entry means buy future
    if allow_buy:
        slice_df["signal"] = np.where(slice_df.z<=-entry, 1, slice_df.signal)
    dataframe.update(slice_df[["signal", "z"]])
    # calc carry signal
    dataframe["signal_carry"] = np.nan
    dataframe["signal_carry"] = np.where( (dataframe.signal != np.inf), dataframe.signal, dataframe.signal_carry)
    dataframe.signal_carry.ffill(inplace=True)
    dataframe.signal_carry.fillna(0, inplace=True)
    # calculate entry price / start trade
    dataframe["start_trade"] = False
    dataframe["end_trade"] = (dataframe.signal_carry!=0) & (dataframe.time.dt.hour==10) & (dataframe.time.dt.hour.shift(1)==9)
    dataframe["entry_price"] = np.nan
    dataframe["entry_price"] = np.where(dataframe.end_trade.shift(1), 0, dataframe.entry_price)
    dataframe["entry_price"] = np.where((dataframe.signal==np.inf).shift(2) & (dataframe.signal!=np.inf).shift(1), dataframe.open_lower_fut, dataframe.entry_price)
    #dataframe["entry_price"] = np.where((dataframe.signal_carry==0).shift(2) & (dataframe.signal_carry!=0).shift(1) & (dataframe.time.dt.hour==9), dataframe.open_A, 0)    
    dataframe.entry_price.ffill(inplace=True)
    
    return dataframe


def calculate_pnl(dataframe, size=1):
        
    dataframe["fut_points"] = 0
    dataframe["fut_points"] = np.where(
        ((dataframe.end_trade) & (dataframe.signal_carry.shift(1)==1)), 
        (dataframe.close_fut-dataframe.entry_price), dataframe.fut_points)
    dataframe["fut_points"] = np.where(
        (dataframe.end_trade) & (dataframe.signal_carry.shift(1)==-1), 
        (dataframe.entry_price-dataframe.close_fut), dataframe.fut_points)
    
    dataframe["fut_points"] = np.where((dataframe.entry_price==0) & (dataframe.end_trade==True), 0, dataframe.fut_points)
    #dataframe["fut_points"] = np.where(dataframe.end_trade, (dataframe.close_fut-dataframe.entry_price), 0)
    dataframe["fut_profit"] = dataframe.fut_points*0.2*size
    dataframe["profit"] = dataframe.fut_profit
    dataframe["cum_profit"] = dataframe.profit.cumsum()
    
    return dataframe


def optimization_process(df_win: pd.DataFrame, df_bova: pd.DataFrame, all_items: list):
    """
    it will call every step function to calculate a single backtest, but will iterate of possibilities
    """
    results = {}
    count=0
    for period, entry in all_items:
        opt_df = build_dataframe(df_win, df_bova)
        opt_df = calculate_signals(opt_df, entry=entry, period=period, allow_sell=False)
        opt_df = calculate_pnl(opt_df)
        stats = get_stats(opt_df)
        final_pnl = stats["final_pnl"]
        results["{}_{}".format(period, entry)] = {
            "p_entry": entry,
            "p_period": period,
            "final_pnl": stats["final_pnl"],
            "cum_profit": stats["cum_profit"],
            "total_trade": stats["total_trades"],
            "win_ratio": stats["win_ratio"],
            "profit_by_trade": stats["profit_by_trade"],
            "sharpe_ratio": stats["sharpe_ratio"],
            "sortino_ratio": stats["sortino_ratio"],
            "loss_means": stats["loss_means"],
            "win_means": stats["win_means"]
        }
        if (count % 12)==0:
            print("{} of {}\r".format(count, len(all_items)))
        count+=1
    return results
