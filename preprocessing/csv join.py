import pandas as pd
import os
import database.database

database.database.createDB()

# Naziv foldera sa CSV fajlovima za df i dn
df_folder = "D:/Energy-Consumption-Predictions/Training Data/NYS Weather Data"
dn_folder = "D:/Energy-Consumption-Predictions/Training Data/NYS Load  Data"

# Kreirajte prazan DataFrame za spajanje svih df fajlova
df_list = []
dn_list = []

# Prođite kroz sve df fajlove u glavnom folderu i poddirektorijumima
for root, dirs, files in os.walk(df_folder):
    for file_name in files:
        if file_name.endswith(".csv"):  # Samo CSV fajlovi
            file_path = os.path.join(root, file_name)
            temp_df = pd.read_csv(file_path)
            df_list.append(temp_df)

# Spojite sve df fajlove u jedan DataFrame
df = pd.concat(df_list, ignore_index=True)

# Pretvorite datetime kolonu
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['datetime'] = df['datetime'].astype(str)

for root, dirs, files in os.walk(dn_folder):
    for file_name in files:
        if file_name.endswith(".csv"):  # Samo CSV fajlovi
            file_path = os.path.join(root, file_name)
            temp_dn = pd.read_csv(file_path)
            dn_list.append(temp_dn)

dn = pd.concat(dn_list, ignore_index=True)
dn['Time Stamp'] = pd.to_datetime(dn['Time Stamp'], errors='coerce')
dn['Time Stamp'] = dn['Time Stamp'].astype(str)
dn.columns = [col.lower().replace(" ", "_") for col in dn.columns]

database.database.insert_data(df, 'weather_data')
database.database.insert_data(dn, 'load_data')