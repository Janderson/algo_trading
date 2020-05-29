import numpy as np
import pandasbt as pbt

def organize_columns(dataframe_columns):
    def remove_duplicate_without_sort(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    remove_to_remove = ["time", "open", "close", "high", "low", "tick_volume", "start_bar_sign", "close_bar_sign"]
    columns = ["time_bar", "open_bar", "high_bar", "low_bar", "close_bar"]
    columns.extend(dataframe_columns)
    for item in remove_to_remove:
        columns.remove(item)
    
    return remove_duplicate_without_sort(columns)

def begin_build_bars(dataframe, timeframe="D1"):
    return pbt.build_timeframe(dataframe, timeframe=timeframe, filter_at_end=False)


def end_build_bars(dataframe, default_operator="and"):
    dataframe = dataframe.copy()
    columns_filter = [item for item in dataframe.columns if "_filter" in item]
    if default_operator=="and":
        operator_str = "&"
    else:
        operator_str = "|"

    #print (columns_filter)
    if len(columns_filter)<=0:
        return dataframe[dataframe.close_bar_sign][organize_columns(dataframe.columns)]
    append_query_str = "==True {}".format(operator_str).join(columns_filter) + "==True"
    query_str = " close_bar_sign == True & ({}) ".format(append_query_str) 
    return dataframe.query(query_str)[organize_columns(dataframe.columns)]
