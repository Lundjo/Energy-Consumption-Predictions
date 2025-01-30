import sqlite3

DB_NAME = "my_database.db"

def createDB():
    # Povezivanje sa bazom podataka (ako baza ne postoji, biće kreirana)
    conn = sqlite3.connect(DB_NAME)
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
    )
    ''')

    # Čuvanje promena i zatvaranje konekcije
    conn.commit()
    conn.close()

def insert_data(data, table):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    column_names = list(data[0].keys())
    placeholders = ", ".join(["?" for _ in column_names])
    sql_query = f'INSERT INTO {table} ({", ".join(column_names)}) VALUES ({placeholders})'
    values = [tuple(row[col] for col in column_names) for row in data]  # Priprema podataka za ubacivanje

    cursor.executemany(sql_query, values)

    conn.commit()
    conn.close()

def get_data(table):
    """ Vraća sve podatke iz tabele weather_data """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()

    conn.close()
    return rows


def clear_database():
    """ Briše sve podatke iz svih tabela u bazi """
    conn = sqlite3.connect(DB_NAME)
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