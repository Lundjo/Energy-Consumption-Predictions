import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("New York City, ... 2018-01-01 to 2018-12-31.csv")
#print(df.isnull().sum()/df.shape[0]*100)
#print(df.duplicated().sum())

for i in df.select_dtypes(include="object").columns:
    counts = df[i].value_counts()
    repeated_values = counts[counts >= 2]

    if not repeated_values.empty:
        print(f"Kolona: {i}")
        print(repeated_values)
        print("***" * 10)