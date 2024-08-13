import pandas as pd


def read_excel(path, sheet_name, skiprows):
    df = pd.read_excel(path, sheet_name=sheet_name, skiprows=skiprows)
    df["任课教师"] = df["任课教师"].fillna("空")
    df["上课地点"] = df["上课地点"].fillna("空")
    df["上课周次"] = df["上课周次"].fillna("空")
    return df
