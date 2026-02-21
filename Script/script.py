import pandas as pd
import numpy as np  # <--- AGGIUNTA FONDAMENTALE

# Percorso del file CSV
file_path = "/Users/antonio/Desktop/globalterrorismdb_0718dist.csv"

# Elenco delle colonne di interesse (INVARIATO)
columns_of_interest = [
    "eventid", "country_txt", "region_txt", "provstate", "city", "latitude", "longitude",
    "crit1", "crit2", "crit3",
    "attacktype1_txt", "weaptype1_txt", "weapsubtype1_txt", "suicide", "success",
    "targtype1_txt", "targsubtype1_txt", "corp1", "natlty1_txt",
    "gname", "claimed", "nperps",
    "nkill", "nwound", "propvalue", "ishostkid", "ransomamt",
    "iyear", "imonth", "iday"
]

# Caricamento del dataset
df = pd.read_csv(file_path, usecols=columns_of_interest, encoding='ISO-8859-1', engine='python')

# --- INIZIO CORREZIONE ---

# Colonne numeriche dove -99 significa "Sconosciuto"
# NOTA: nperps (numero terroristi) a -99 non può essere 0.
numeric_cols_unknown = ["nkill", "nwound", "propvalue", "ransomamt", "nperps"]

# Sostituisci -99 con NaN (Valore nullo reale). NON SOSTITUIRE I NaN CON 0!
for col in numeric_cols_unknown:
    # Prima converti in numerico per sicurezza, forzando errori a NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')
    # Sostituisci il codice errore -99 con NaN
    df[col] = df[col].replace(-99, np.nan)

# --- FINE CORREZIONE ---

# Funzione per costruire la data (Questa va bene, è un compromesso accettabile per la BI)
def create_date(row):
    try:
        year = int(row['iyear'])
        # Se mese o giorno sono 0, li forziamo a 1 per avere una data valida nei grafici temporali
        month = int(row['imonth']) if row['imonth'] != 0 else 1
        day = int(row['iday']) if row['iday'] != 0 else 1
        return pd.Timestamp(year=year, month=month, day=day)
    except:
        return np.nan # Se c'è un errore grave nella data, meglio nullo che sbagliato

df['date'] = df.apply(create_date, axis=1)

# Rimuovere le colonne originali
df = df.drop(columns=['iyear', 'imonth', 'iday'])

# Salvare il DataFrame pulito
output_path = "/Users/antonio/Desktop/gtd_cleaned_CORRECT.csv"
# float_format='%.0f' serve per non avere decimali brutti (es. 1.0 invece di 1) se ci sono NaN
df.to_csv(output_path, index=False, encoding='utf-8')

print("Dataset corretto generato. I valori sconosciuti sono ora celle vuote, non zeri.")
