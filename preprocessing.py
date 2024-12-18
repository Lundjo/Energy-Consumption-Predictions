import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

'''
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

#print(df.describe().T.to_string())
#print(df.describe(include="object"))

#print(df.select_dtypes(include="number"))

dn = pd.read_csv("20180101pal.csv")
#print(dn.info())
#print(dn.isnull().sum()/df.shape[0]*100)

# Pretpostavimo da je naziv kolone sa timestamp-om 'timestamp'
dn['Time Stamp'] = pd.to_datetime(dn['Time Stamp'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
print(df.head())

dn_nyc = dn[dn['Name'] == "N.Y.C."]
df = df.merge(dn_nyc[['Time Stamp', 'Load']], left_on='datetime', right_on='Time Stamp', how='left')
df = df.drop(columns=['Time Stamp'])
print(df.tail())

'''

# Naziv foldera sa CSV fajlovima za df i dn
df_folder = "NYS Weather Data"
dn_folder = "NYS Load  Data"

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

for root, dirs, files in os.walk(dn_folder):
    for file_name in files:
        if file_name.endswith(".csv"):  # Samo CSV fajlovi
            file_path = os.path.join(root, file_name)
            temp_dn = pd.read_csv(file_path)
            dn_list.append(temp_dn)

dn = pd.concat(dn_list, ignore_index=True)
dn['Time Stamp'] = pd.to_datetime(dn['Time Stamp'], errors='coerce')

df.to_csv("df_output.csv", index=False)
dn.to_csv("dn_output.csv", index=False)

dn_nyc = dn[dn['Name'] == "N.Y.C."]
df = df.merge(dn_nyc[['Time Stamp', 'Load']], left_on='datetime', right_on='Time Stamp', how='left')
df = df.drop(columns=['Time Stamp'])

# Sačuvajte konačni rezultat
df.to_csv("final_output.csv", index=False)
print("Svi fajlovi su spojeni (uključujući poddirektorijume) i rezultat je sačuvan u 'final_output.csv'.")