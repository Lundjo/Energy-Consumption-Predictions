import pandas as pd
import database.database

def score(predicted_df):
    # Učitajmo podatke iz fajlova
    start = predicted_df['datetime'].iloc[0]
    end = predicted_df['datetime'].iloc[-1]
    actual_df = database.database.get_data_in_range('load_data', start, end, 'time_stamp')

    # Osiguravamo da su kolone datetime u istom formatu za spajanje
    predicted_df['datetime'] = pd.to_datetime(predicted_df['datetime'])
    actual_df['datetime'] = pd.to_datetime(actual_df['time_stamp'])
    actual_df = actual_df[actual_df['name'] == 'N.Y.C.']

    # Spajanje na osnovu datetime kolone
    merged_df = predicted_df.merge(actual_df[['datetime', 'load']], on='datetime', how='left')

    # Preimenujemo kolonu load iz new_output.csv u actual_load
    merged_df.rename(columns={'load': 'actual_load'}, inplace=True)

    # Proverimo da li postoje prazne vrednosti u actual_load
    if merged_df['actual_load'].isnull().any():
        print("Upozorenje: Neki zapisi nemaju odgovarajuće actual_load vrednosti!")

    # Izračunavanje MAPE
    merged_df['absolute_percentage_error'] = (
                abs(merged_df['predicted_load'] - merged_df['actual_load']) / merged_df['actual_load'] * 100).round(2)
    mape = merged_df['absolute_percentage_error'].mean()

    print(merged_df.to_string())
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")