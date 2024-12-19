import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

df = pd.read_csv("final_output.csv")

#imena svih kolona iz csv i njihovi tipovi
#print(df.info())

#procenat podataka koji fale
#print(df.isnull().sum()/df.shape[0]*100)

#broj dupliranih vrednosti
#print(df.duplicated().sum())

'''
for i in df.select_dtypes(include="object").columns:
    print(df[i].value_counts())
    print("***" * 10)
    '''

#informacije o podacima u svim kolonama
#print(df.describe().T.to_string())

#sve kolone sa numerickim vrednostima
#print(df.select_dtypes(include="number").columns)

"""
#iscrtavanje grafika zavisnosti svake vrednosti pojedinacno u odnosu na zavisnu load
for i in ['temp', 'feelslike', 'dew', 'humidity', 'precip', 'precipprob',
       'preciptype', 'snow', 'snowdepth', 'windgust', 'windspeed', 'winddir',
       'sealevelpressure', 'cloudcover', 'visibility', 'solarradiation',
       'solarenergy', 'uvindex', 'severerisk']:
    sns.scatterplot(data=df, x=i, y='Load')
    plt.show()
    """

"""
#korelacija medju svim vrednostima
s=df.select_dtypes(include="number").corr()
plt.figure(figsize=(15, 15))
sns.heatmap(s, annot=True)
plt.show()
"""

'''
#popunjavanje nedostajucih vrednosti
print(df.isnull().sum())
columns_to_fill = ["feelslike", "dew", "humidity", "precip", "windspeed", "winddir", "sealevelpressure", "cloudcover", "visibility"]

for col in columns_to_fill:
    if col in df.columns:  # Provera da li kolona postoji
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Konverzija u numerički format
        if df[col].notna().any():  # Provera da li postoje nenull vrednosti
            median_value = df[col].median()  # Izračunajte median
            df[col] = df[col].fillna(median_value)  # Popunite NaN vrednosti
        else:
            print(f"Kolona '{col}' sadrži samo NaN vrednosti.")
    else:
        print(f"Kolona '{col}' ne postoji u DataFrame-u.")
print(df.isnull().sum())
'''