import pandas as pd

df = pd.read_csv('results.tsv', sep='\t')
print(len(df))
df = df.drop_duplicates()
print(len(df))
df.to_csv('results.tsv', sep='\t', index=False)
