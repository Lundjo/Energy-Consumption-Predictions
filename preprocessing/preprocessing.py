import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Energy-Consumption-Predictions/final_output.csv")
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

#brisanje praznika
holidays = pd.read_excel("C:/Energy-Consumption-Predictions/US Holidays 2018-2021.xlsx")
datetime_values_to_remove = pd.to_datetime(holidays.iloc[:, 2])
df_filtered = df[~df['datetime'].dt.date.isin(datetime_values_to_remove)]

#imena svih kolona iz csv i njihovi tipovi
#print(df.info())

#procenat podataka koji fale
#print(df.isnull().sum()/df.shape[0]*100)

#broj dupliranih vrednosti
#print(df.duplicated().sum())

df = df.drop_duplicates(subset=['datetime'], keep=False)

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


#popunjavanje nedostajucih vrednosti
print(df.isnull().sum())
columns_to_fill = ["feelslike", "dew", "humidity", "precip", "windspeed", "winddir", "sealevelpressure", "cloudcover", "visibility", "Load"]

for col in columns_to_fill:
    if col in df.columns:  # Provera da li kolona postoji
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Konverzija u numerički format
        if df[col].notna().any():  # Provera da li postoje nenull vrednosti
            df[col] = df[col].interpolate(method='linear', limit_direction='forward', axis=0)  # Interpolacija na osnovu susednih vrednosti
        else:
            print(f"Kolona '{col}' sadrži samo NaN vrednosti.")
    else:
        print(f"Kolona '{col}' ne postoji u DataFrame-u.")
print(df.isnull().sum())

#trazenje outliera
def wisker(col):
    q1, q3 = np.percentile(col, [25,75])
    iqr = q3 - q1
    lw = q1 - 1.5 * iqr
    uw = q3 + 1.5 * iqr
    return lw, uw

#menjanje outliera minimalnim dopustivim vrednostima
for i in ['temp', 'feelslike']:
    lw, uw = wisker(df[i])
    df[i] = np.where(df[i] < lw, lw, df[i])
    df[i] = np.where(df[i] > uw, uw, df[i])
'''
#prikaz nalazenja vrednosti sa outlierima
for i in ['temp', 'feelslike']:
    sns.boxplot(df[i])
    plt.show()
    '''

# Pretvaranje datetime u korisne atribute
df['datetime'] = pd.to_datetime(df['datetime'])
df['month'] = df['datetime'].dt.month
df['weekday'] = df['datetime'].dt.weekday
df['hour'] = df['datetime'].dt.hour

# Dodavanje vikenda
df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)
df.drop(columns=['datetime'], inplace=True)
df.drop(columns=['uvindex'], inplace=True)

# Definišite prag za minimalni broj nenedostajućih vrednosti
threshold = int(0.7 * len(df))  # Zadržava kolone koje imaju najmanje 70% nenedostajućih podataka

# Uklonite kolone koje imaju previše nedostajućih podataka
df = df.dropna(axis=1, thresh=threshold)

dummy = pd.get_dummies(data=df, columns=['name', 'conditions'], drop_first=True)
print(dummy.head().to_string())
dummy.to_csv("C:/Energy-Consumption-Predictions/new_output.csv", index=False)