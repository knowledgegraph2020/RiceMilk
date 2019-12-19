import pandas as pd


def df_empty(df,col_name):
    if isinstance(df,pd.DataFrame):
        size = df[col_name].__len__()
