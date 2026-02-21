import pandas as pd
import numpy as np  # <--- fondamentale

# -----------------------------
# Percorso del file CSV originale
# -----------------------------
file_path = "/Users/antonio/Desktop/globalterrorismdb_0718dist.csv"

# -----------------------------
# Elenco delle colonne di interesse
# -----------------------------
columns_of_interest = [
    "eventid", "country_txt", "region_txt", "provstate", "city", "latitude", "longitude",
    "crit1", "crit2", "crit3",
    "attacktype1_txt", "weaptype1_txt", "weapsubtype1_txt", "suicide", "success",
    "targtype1_txt", "targsubtype1_txt", "corp1", "natlty1_txt",
    "gname", "claimed", "nperps",
    "nkill", "nwound", "propvalue", "ishostkid", "ransomamt",
    "iyear", "imonth", "iday"
]

# -----------------------------
# Caricamento del dataset
# -----------------------------
df = pd.read_csv(file_path, usecols=columns_of_interest, encoding='ISO-8859-1', engine='python')

# -----------------------------
# CORREZIONE VALORI SCONOSCIUTI (-99 -> NaN)
# -----------------------------
numeric_cols_unknown = ["nkill", "nwound", "propvalue", "ransomamt", "nperps"]

for col in numeric_cols_unknown:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # Forza a numerico
    df[col] = df[col].replace(-99, np.nan)  # Sostituisci -99 con NaN

# -----------------------------
# CREAZIONE COLONNA DATA
# -----------------------------
def create_date(row):
    try:
        year = int(row['iyear'])
        month = int(row['imonth']) if row['imonth'] != 0 else 1
        day = int(row['iday']) if row['iday'] != 0 else 1
        return pd.Timestamp(year=year, month=month, day=day)
    except:
        return np.nan

df['date'] = df.apply(create_date, axis=1)

# Rimuovere le colonne originali anno/mese/giorno
df = df.drop(columns=['iyear', 'imonth', 'iday'])

# -----------------------------
# SALVATAGGIO DEL DATAFRAME PULITO
# -----------------------------
output_path = "/Users/antonio/Desktop/gtd_cleaned_CORRECT.csv"
df.to_csv(output_path, index=False, encoding='utf-8', float_format='%.0f')

print("Dataset corretto generato. I valori sconosciuti sono ora celle vuote, non zeri.")

# -----------------------------
# FILTRARE RECORD CON RAPIMENTI (ishostkid = 1 o 1.0)
# -----------------------------
hostkid_records = df[df['ishostkid'].isin([1, 1.0])]

# Numero totale di eventi unici (come fa Qlik)
unique_hostkid_events = hostkid_records['eventid'].nunique()
print(f"\nNumero totale di eventi unici con rapimento/ostaggi: {unique_hostkid_events}")

# Numero totale di righe con rapimento (tutte le righe)
print(f"\nNumero totale di righe con rapimento/ostaggi: {len(hostkid_records)}")

# Mostra i primi 5 record filtrati
print("\nEsempio di record con ishostkid=1:")
print(hostkid_records.head())

