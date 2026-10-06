import pandas as pd
from preprocessing import clean_text

df = pd.read_csv("data/emails_labeled.csv")
df['clean_text'] = df['text'].apply(clean_text)
df.to_csv("data/emails_clean.csv", index=False)
print(df[['text', 'clean_text']].head())