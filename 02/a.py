import pandas as pd

df = pd.read_csv('input', delim_whitespace=True, header=None);
maxs = df.max(axis=1)
mins = df.min(axis=1)
print (maxs - mins).sum()


