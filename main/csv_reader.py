import pandas as pd

folder_path = "../data/hosp/"

# Lecture d'un fichier CSV et conversion en DataFrame
def read_csv_to_dataframe(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
        return pd.DataFrame()