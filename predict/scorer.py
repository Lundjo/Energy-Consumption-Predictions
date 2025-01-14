import pandas as pd

# Učitajmo podatke iz fajlova
predicted_df = pd.read_csv('predicted_load.csv')
actual_df = pd.read_csv('C:/Energy-Consumption-Predictions/final_output.csv')

# Osiguravamo da su kolone datetime u istom formatu za spajanje
predicted_df['datetime'] = pd.to_datetime(predicted_df['datetime'])
actual_df['datetime'] = pd.to_datetime(actual_df['datetime'])

# Spajanje na osnovu datetime kolone
merged_df = predicted_df.merge(actual_df[['datetime', 'Load']], on='datetime', how='left')

# Preimenujemo kolonu load iz new_output.csv u actual_load
merged_df.rename(columns={'Load': 'actual_load'}, inplace=True)

# Proverimo da li postoje prazne vrednosti u actual_load
if merged_df['actual_load'].isnull().any():
    print("Upozorenje: Neki zapisi nemaju odgovarajuće actual_load vrednosti!")

# Izračunavanje MAPE
merged_df['absolute_percentage_error'] = (abs(merged_df['predicted_load'] - merged_df['actual_load']) / merged_df['actual_load'] * 100).round(2)
mape = merged_df['absolute_percentage_error'].mean()

print(merged_df.to_string())
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")