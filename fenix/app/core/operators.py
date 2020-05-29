def or_operator(dataframe, column_filter1, column_filter2, name="__or_filter"):
    if not str(column_filter1) in dataframe.columns:
        raise Exception("column column_filter1 not exist in dataframe")
    if not str(column_filter2) in dataframe.columns:
        raise Exception("column column_filter2 not exist in dataframe")
    name_filter = column_filter1.replace("_filter", "") +"__" + column_filter2.replace("_filter", "") + name
    dataframe[name_filter] = (dataframe[str(column_filter1)] | dataframe[str(column_filter2)])
    dataframe.drop([column_filter1, column_filter2], axis=1, inplace=True)
    return dataframe


def and_operator(dataframe, column_filter1, column_filter2, name=None):
    if not str(column_filter1) in dataframe.columns:
        raise Exception("column column_filter1 not exist in dataframe")
    if not str(column_filter2) in dataframe.columns:
        raise Exception("column column_filter2 not exist in dataframe")
    if name==None:
        name_filter = column_filter1.replace("_filter", "") +"__" + column_filter2.replace("_filter", "") + "__or_filter"
    else:
        name_filter = name + "_filter"
    dataframe[name_filter] = (dataframe[str(column_filter1)] & dataframe[str(column_filter2)])
    dataframe.drop([column_filter1, column_filter2], axis=1, inplace=True)
    return dataframe
