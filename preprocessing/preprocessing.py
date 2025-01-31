import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import database.database

def dataPreprocesing():
    df = database.database.get_data('weather_data')
    dn = database.database.get_data('load_data')
    dn_nyc = dn[dn['name'] == "N.Y.C."]
    df = df.merge(dn_nyc[['time_stamp', 'load']], left_on='datetime', right_on='time_stamp', how='left')
    df = df.drop(columns=['time_stamp'])
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    # brisanje praznika
    holidays = pd.read_excel("D:/Energy-Consumption-Predictions/US Holidays 2018-2021.xlsx")
    datetime_values_to_remove = pd.to_datetime(holidays.iloc[:, 2])
    df_filtered = df[~df['datetime'].dt.date.isin(datetime_values_to_remove)]

    df = df.drop_duplicates(subset=['datetime'], keep=False)

    # popunjavanje nedostajucih vrednosti
    columns_to_check = ["temp", "feelslike", "windspeed", "visibility", "load"]
    df = df.dropna(subset=columns_to_check)
    df = df.drop(df.columns[0], axis=1)

    print(df.to_string())

    # trazenje outliera
    def wisker(col):
        q1, q3 = np.percentile(col, [25, 75])
        iqr = q3 - q1
        lw = q1 - 1.5 * iqr
        uw = q3 + 1.5 * iqr
        return lw, uw

    # menjanje outliera minimalnim dopustivim vrednostima
    for i in ['temp', 'feelslike', 'precip', 'snow', 'windspeed', 'visibility']:
        lw, uw = wisker(df[i])  # Izračunavanje granica

        # Zamena outliera sa NaN
        df[i] = df[i].where((df[i] >= lw) & (df[i] <= uw), np.nan)

        # Interpolacija za zamenu NaN vrednosti
        df[i] = df[i].interpolate(method='linear', limit_direction='both', axis=0).fillna(method='ffill').fillna(
            method='bfill')

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

    df.drop(columns=['date'], inplace=True)

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
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['day_of_week_sin'] = np.sin(2 * np.pi * df['weekday'] / 7)
    df['day_of_week_cos'] = np.cos(2 * np.pi * df['weekday'] / 7)

    df = df.groupby(['weekday', 'hour', 'month'], as_index=False).agg({
        'temp': 'mean',
        'windspeed': 'mean',
        'prev_day_avg_temp': 'mean',
        'season': 'mean',
        'hour_sin': 'mean',
        'hour_cos': 'mean',
        'month_sin': 'mean',
        'month_cos': 'mean',
        'day_of_week_sin': 'mean',
        'day_of_week_cos': 'mean',
        'load': 'mean'
    }).round(4)

    df.drop(columns=['month', 'hour', 'weekday'], inplace=True)

    return df