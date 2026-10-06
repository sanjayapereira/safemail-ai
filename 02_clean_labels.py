import pandas as pd

df = pd.read_csv("data/emails_raw.csv")

# Drop any rows with missing text or label
df = df.dropna(subset=['text', 'label'])

# Convert label from float (1.0/0.0) to clean integer (1/0)
df['label'] = df['label'].astype(int)

# Sanity check before saving
print("Final shape:", df.shape)
print(df['label'].value_counts())
print(df.head())

df.to_csv("data/emails_labeled.csv", index=False)
print("\nSaved to data/emails_labeled.csv")