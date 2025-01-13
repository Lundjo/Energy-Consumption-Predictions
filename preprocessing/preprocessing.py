import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("C:/Energy-Consumption-Predictions/final_output.csv")
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

#brisanje praznika
holidays = pd.read_excel("C:/Energy-Consumption-Predictions/US Holidays 2018-2021.xlsx")
datetime_values_to_remove = pd.to_datetime(holidays.iloc[:, 2])
df_filtered = df[~df['datetime'].dt.date.isin(datetime_values_to_remove)]

df = df.drop_duplicates(subset=['datetime'], keep=False)

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
for i in ['temp', 'feelslike', 'precip', 'snow', 'windspeed', 'visibility', 'Load']:
    lw, uw = wisker(df[i])  # Izračunavanje granica

    # Zamena outliera sa NaN
    df[i] = df[i].where((df[i] >= lw) & (df[i] <= uw), np.nan)

    # Interpolacija za zamenu NaN vrednosti
    df[i] = df[i].interpolate(method='linear', limit_direction='both', axis=0).fillna(method='ffill').fillna(method='bfill')

# Pretvaranje datetime u korisne atribute
df['datetime'] = pd.to_datetime(df['datetime'])
df['year'] = df['datetime'].dt.year
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
    if 7 <= hour <= 23:
        return 0
    else:
        return 1

#df['is_night'] = df['hour'].apply(get_part_of_day)

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

df['lag_1'] = df['Load'].shift(1)
df['lag_24'] = df['Load'].shift(24)
df['lag_168'] = df['Load'].shift(168)
'''df['diff_hour'] = df['Load'] - df['Load'].shift(1)
df['diff_day'] = df['Load'] - df['Load'].shift(24)
df['lag_week'] = df['Load'].shift(7 * 24)  # Pre nedelju dana
df['lag_year'] = df['Load'].shift(365 * 24)  # Pre godinu dana'''
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
df['day_of_week_sin'] = np.sin(2 * np.pi * df['weekday'] / 7)
df['day_of_week_cos'] = np.cos(2 * np.pi * df['weekday'] / 7)
#df['season_sin'] = np.sin(2 * np.pi * df['season'] / 4)
#df['season_cos'] = np.cos(2 * np.pi * df['season'] / 4)

df['lag_1'] = df['lag_1'].fillna(df['Load'])
df['lag_24'] = df['lag_24'].fillna(df['Load'])
df['lag_168'] = df['lag_168'].fillna(df['Load'])
'''df['diff_hour'] = df['diff_hour'].fillna(df['Load'])
df['diff_day'] = df['diff_day'].fillna(df['Load'])
df['lag_week'] = df['lag_week'].fillna(df['Load'])
df['lag_year'] = df['lag_year'].fillna(df['Load'])'''

df.drop(columns=['datetime', 'uvindex', 'conditions', 'snowdepth', 'sealevelpressure', 'cloudcover', 'winddir', 'humidity', 'dew', 'hour', 'month', 'precip',
                 'snow', 'year', 'weekday', 'day'], inplace=True)

# Definišite prag za minimalni broj nenedostajućih vrednosti
threshold = int(0.7 * len(df))  # Zadržava kolone koje imaju najmanje 70% nenedostajućih podataka

# Uklonite kolone koje imaju previše nedostajućih podataka
df = df.dropna(axis=1, thresh=threshold)

dummy = pd.get_dummies(data=df, columns=['name'], drop_first=True)
load_column = dummy.pop('Load')  # Izvlači kolonu 'Load' iz DataFrame-a
dummy['Load'] = load_column      # Dodaje kolonu 'Load' kao poslednju
dummy = np.round(dummy, 3)


print(dummy.head().to_string())


dummy.to_csv("C:/Energy-Consumption-Predictions/new_output.csv", index=False)