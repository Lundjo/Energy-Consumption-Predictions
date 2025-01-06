import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy import stats

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
            df[col] = df[col].interpolate(method='linear', limit_direction='both', axis=0).fillna(method='ffill')  # Interpolacija na osnovu susednih vrednosti
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
for i in ['temp', 'feelslike', 'windspeed', 'visibility', 'Load']:
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
df['day'] = df['datetime'].dt.day
df['weekday'] = df['datetime'].dt.weekday
df['hour'] = df['datetime'].dt.hour

df['date'] = df['datetime'].dt.date  # Ekstrahovanje samo datuma
daily_avg_temp = df.groupby('date')['temp'].mean()  # Računanje prosečne temperature po datumu
df['prev_day_avg_temp'] = df['date'].map(daily_avg_temp.shift(1))  # Dodavanje prosečne temperature prethodnog dana
df['prev_day_avg_temp'] = df['prev_day_avg_temp'].fillna(df['temp'])
# Prosečna vrednost 'Load' iz prethodnih 7 dana
df['prev_week_avg_load'] = df['date'].map(df.groupby('date')['Load'].transform(lambda x: x.shift(7).mean()))

# Maksimalna vrednost 'Load' iz prethodnih 7 dana
df['prev_week_max_load'] = df['date'].map(df.groupby('date')['Load'].transform(lambda x: x.shift(7).max()))

# Minimalna vrednost 'Load' iz prethodnih 7 dana
df['prev_week_min_load'] = df['date'].map(df.groupby('date')['Load'].transform(lambda x: x.shift(7).min()))

# Razlika između trenutnog i prosečnog opterećenja prethodnog dana
df['daily_load_difference'] = df['Load'] - df['prev_day_avg_temp']

# Uklanjanje privremene kolone 'date' (ako nije potrebna)
df.drop(columns=['date'], inplace=True)

def get_part_of_day(hour):
    if 5 <= hour < 12:
        return 1
    elif 12 <= hour < 17:
        return 2
    elif 17 <= hour < 21:
        return 3
    else:
        return 4

df['part_of_day'] = df['hour'].apply(get_part_of_day)

def get_season(month):
    if month in [12, 1, 2]:
        return 1
    elif month in [3, 4, 5]:
        return 2
    elif month in [6, 7, 8]:
        return 3
    else:
        return 4

df['season'] = df['month'].apply(get_season)

df['snow'] = df['snow'].apply(lambda x: 1 if x > 0 else 0)

# Dodavanje vikenda
df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)
df.drop(columns=['datetime'], inplace=True)
df.drop(columns=['uvindex'], inplace=True)
df.drop(columns=['conditions', 'snowdepth', 'sealevelpressure', 'cloudcover', 'winddir', 'humidity', 'dew', 'weekday'], inplace=True)

df['lag_1'] = df['Load'].shift(1)
df['lag_24'] = df['Load'].shift(24)
df['lag_168'] = df['Load'].shift(168)
df['diff_hour'] = df['Load'] - df['Load'].shift(1)
df['diff_day'] = df['Load'] - df['Load'].shift(24)
df['lag_week'] = df['Load'].shift(7 * 24)  # Pre nedelju dana
df['lag_year'] = df['Load'].shift(365 * 24)  # Pre godinu dana
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

df['lag_1'] = df['lag_1'].fillna(df['Load'])
df['lag_24'] = df['lag_24'].fillna(df['Load'])
df['lag_168'] = df['lag_168'].fillna(df['Load'])
df['diff_hour'] = df['diff_hour'].fillna(df['Load'])
df['diff_day'] = df['diff_day'].fillna(df['Load'])
df['lag_week'] = df['lag_week'].fillna(df['Load'])
df['lag_year'] = df['lag_year'].fillna(df['Load'])

# Definišite prag za minimalni broj nenedostajućih vrednosti
threshold = int(0.7 * len(df))  # Zadržava kolone koje imaju najmanje 70% nenedostajućih podataka

# Uklonite kolone koje imaju previše nedostajućih podataka
df = df.dropna(axis=1, thresh=threshold)

dummy = pd.get_dummies(data=df, columns=['name'], drop_first=True)
load_column = dummy.pop('Load')  # Izvlači kolonu 'Load' iz DataFrame-a
dummy['Load'] = load_column      # Dodaje kolonu 'Load' kao poslednju
print(dummy.head().to_string())
dummy.to_csv("C:/Energy-Consumption-Predictions/new_output.csv", index=False)