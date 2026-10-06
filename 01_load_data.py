import pandas as pd

df = pd.read_csv("data/emails_raw.csv")
print(df.shape)
print(df.columns)
print(df.head())
print(df.iloc[:, -1].value_counts())