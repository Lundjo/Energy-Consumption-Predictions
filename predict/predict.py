import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import preprocessing.preprocessing as pp
import database.database
import scorer


def preprocessing(df, training_data):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['month'] = df['datetime'].dt.month
    df['weekday'] = df['datetime'].dt.weekday
    df['hour'] = df['datetime'].dt.hour
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

    df['date'] = df['datetime'].dt.date
    daily_avg_temp = df.groupby('date')['temp'].mean()
    df['prev_day_avg_temp'] = df['date'].map(daily_avg_temp.shift(1))
    df['prev_day_avg_temp'] = df['prev_day_avg_temp'].fillna(df['temp'])

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

    df['load'] = training_data['load'].median()

    df.drop(columns=['datetime', 'uvindex', 'conditions', 'snowdepth', 'sealevelpressure', 'winddir', 'solarenergy', 'preciptype', 'severerisk',
                     'humidity', 'dew', 'hour', 'precip', 'snow', 'name', 'precipprob', 'windgust', 'solarradiation', 'weekday', 'month', 'cloudcover'], inplace=True)
    df = df[
        ['temp', 'windspeed', 'prev_day_avg_temp', 'season',
         'hour_sin', 'hour_cos', 'month_sin', 'month_cos', 'day_of_week_sin', 'day_of_week_cos', 'load']]

    return df


def test(start, end, city, model_type):
    # Učitavanje sačuvanog modela
    if(model_type == "standard"):
        model = load_model('D:/Energy-Consumption-Predictions/model.keras')
    else:
        model = load_model('D:/Energy-Consumption-Predictions/newmodel.keras')

    new_dataframe = database.database.get_data_in_range('weather_data', start, end, 'datetime')

    # Učitavanje novih podataka
    training_data = pp.dataPreprocesing('2018-01-01T00:00:00', '2021-09-06T00:00:00')
    #training_data.to_csv('training.csv', index=False)
    new_dataframe = preprocessing(new_dataframe, training_data)

    # Priprema skalera (isti kao tokom treniranja)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit_transform(training_data)

    # Normalizacija podataka
    new_data_values = new_dataframe.values.astype('float32')
    new_data_scaled = scaler.transform(new_data_values)

    # Priprema ulaznih podataka (X) za predikciju
    look_back = 11
    X_new = []
    for i in range(len(new_data_scaled)):
        a = new_data_scaled[i, 0:look_back - 1]
        X_new.append(a)
    X_new = np.array(X_new)
    X_new = np.reshape(X_new, (X_new.shape[0], 1, X_new.shape[1]))

    # Predikcija
    predictions_scaled = model.predict(X_new)

    X_new = np.reshape(X_new, (X_new.shape[0], X_new.shape[2]))

    # Promena dimenzije predikcija sa (n_samples, 1) u (n_samples, )
    predictions_scaled = np.reshape(predictions_scaled, (predictions_scaled.shape[0], 1))

    # Spajanje predikcija sa podacima
    new_data_scaled = np.concatenate((X_new, predictions_scaled), axis=1)

    # Inverzna transformacija podataka
    data_original = scaler.inverse_transform(new_data_scaled)

    predictions = data_original[:, -1]
    data = database.database.get_data_in_range('weather_data', start, end, 'datetime')

    df = data[['datetime']].copy()
    df['predicted_load'] = predictions
    df['name'] = city
    df.to_csv('predicted_load.csv', index=False)
    database.database.insert_data(df, 'predicted_loads')
    scorer.score(df, city)