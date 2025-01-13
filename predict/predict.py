import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def preprocessing(df, training_data):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['month'] = df['datetime'].dt.month
    df['day_of_week'] = df['datetime'].dt.weekday
    df['hour'] = df['datetime'].dt.hour
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df.drop(columns=['datetime', 'uvindex', 'conditions', 'snowdepth', 'sealevelpressure', 'winddir', 'solarenergy', 'preciptype', 'severerisk',
                     'humidity', 'dew', 'hour', 'precip', 'snow', 'name', 'feelslike', 'precipprob', 'windgust', 'solarradiation', 'visibility'], inplace=True)
    df = df[
        ['day_of_week', 'month', 'temp', 'windspeed', 'cloudcover', 'hour_sin', 'hour_cos', 'month_sin', 'month_cos']]
    df['load'] = training_data['load'].median()
    return df


# Učitavanje sačuvanog modela
model = load_model('C:/Energy-Consumption-Predictions/model.keras')

# Učitavanje novih podataka
new_data_path = 'C:/Energy-Consumption-Predictions/new_weather.csv'
training_data = pd.read_csv('C:/Energy-Consumption-Predictions/new_output.csv')
new_dataframe = pd.read_csv(new_data_path, engine='python', sep=',')
new_dataframe = preprocessing(new_dataframe, training_data)
if new_dataframe.isnull().any().any():
    print("Učitani podaci sadrže NaN vrednosti")
    print(new_dataframe.isnull().sum())
# Priprema skalera (isti kao tokom treniranja)
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit_transform(training_data)

# Normalizacija podataka
new_data_values = new_dataframe.values.astype('float32')
new_data_scaled = scaler.transform(new_data_values)

# Priprema ulaznih podataka (X) za predikciju
look_back = 10  # Pretpostavlja se da imate 9 kolona za ulaz
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

# Ispis rezultata
print("Predikcije na novim podacima:")
print(predictions)

new_dataframe = pd.read_csv(new_data_path, engine='python', sep=',')
df = new_dataframe[['datetime']].copy()
df['predicted_load'] = predictions
df.to_csv('predicted_load.csv', index=False)