import sqlite3
import pandas as pd

DB_PATH = "D:/Energy-Consumption-Predictions/database/my_database.db"

def createDB():
    # Povezivanje sa bazom podataka (ako baza ne postoji, biće kreirana)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Kreiranje prve tabele za vremenske podatke
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        datetime DATETIME,
        temp REAL,
        feelslike REAL,
        dew REAL,
        humidity REAL,
        precip REAL,
        precipprob REAL,
        preciptype TEXT,
        snow REAL,
        snowdepth REAL,
        windgust REAL,
        windspeed REAL,
        winddir INTEGER,
        sealevelpressure REAL,
        cloudcover REAL,
        visibility REAL,
        solarradiation INTEGER,
        solarenergy REAL,
        uvindex INTEGER,
        severerisk INTEGER,
        conditions TEXT
        UNIQUE(datetime)
    )
    ''')

    # Kreiranje druge tabele za podatke o opterećenju
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS load_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_stamp DATETIME,
        time_zone TEXT,
        name TEXT,
        ptid INTEGER,
        load REAL
        UNIQUE(time_stamp, name)
    )
    ''')

    # Tabela sa predikcijama
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predicted_loads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime DATETIME,
            name TEXT,
            predicted_load REAL            
            UNIQUE(datetime, name)
        )
        ''')

    # Čuvanje promena i zatvaranje konekcije
    conn.commit()
    conn.close()

def insert_data(df, table):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Uzimamo nazive kolona iz DataFrame-a
    column_names = df.columns.tolist()

    # Priprema SQL query-a
    placeholders = ", ".join(["?" for _ in column_names])
    sql_query = f'INSERT OR REPLACE INTO {table} ({", ".join(column_names)}) VALUES ({placeholders})'

    # Uzimanje vrednosti iz DataFrame-a kao liste torki
    values = df.itertuples(index=False, name=None)

    cursor.executemany(sql_query, values)

    conn.commit()
    conn.close()

def clear_database():
    """ Briše sve podatke iz svih tabela u bazi """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Dohvati sve tabele u bazi
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DELETE FROM {table_name}")  # Briše podatke iz tabele
        cursor.execute(
            f"UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = '{table_name}'")  # Resetuje AUTO_INCREMENT, ako postoji

    conn.commit()
    conn.close()

    print("Baza je uspešno obrisana.")

import sqlite3
import pandas as pd

def get_data_in_range(table, start_date, end_date, date_column, city_column=None, city=None):
    conn = sqlite3.connect(DB_PATH)

    # SQL upit za filtriranje podataka na osnovu datuma i grada
    query = f'''
    SELECT * FROM {table}
    WHERE {date_column} >= ? AND {date_column} <= ?
    '''

    # Dodajte grad u upit ako je prosleđen
    params = [start_date, end_date]
    if city_column and city:
        query += f' AND {city_column} = ?'
        params.append(city)

    # Izvršavanje upita sa parametrima
    df = pd.read_sql_query(query, conn, params=params)

    conn.close()
    return df