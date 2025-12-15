from csv_reader import *
from table_filler import *

OUTPUT = "../data/out/"

def __main__():

    # Lecture des fichiers CSV et remplissage des DataFrames
    patients_df = read_csv_to_dataframe(folder_path + "patients.csv")
    print(patients_df.head())
    admissions_df = read_csv_to_dataframe(folder_path + "admissions.csv")
    print(admissions_df.head())
    microbiology_df = read_csv_to_dataframe(folder_path + "microbiologyevents.csv")
    print(microbiology_df.head())
    prescriptions_df = read_csv_to_dataframe(folder_path + "prescriptions.csv")
    print(prescriptions_df.head())

    mapping_df = read_csv_to_dataframe(folder_path + "mapping_voc_usagi.csv")

    # Fill tester
    PERSON = fill_person_table(patients_df, mapping_df)
    print("PERSON:", PERSON)
    DEATH = fill_death_table(patients_df)
    print("DEATH:", DEATH)
    VISIT_OCCURENCE = fill_visit_occurrence_table(admissions_df)
    print("VISIT_OCCURENCE:", VISIT_OCCURENCE)
    MEASUREMENT = fill_measurement_table(microbiology_df, mapping_df)
    print("MEASUREMENT:", MEASUREMENT)
    DRUG_EXPOSURE = fill_drug_exposure_table(prescriptions_df, mapping_df)
    print("DRUG_EXPOSURE:", DRUG_EXPOSURE)

    # Garder uniquement les IDs présents dans MEASUREMENT et DRUG_EXPOSURE
    ids_measurement = set(MEASUREMENT['person_id'])
    ids_drug = set(DRUG_EXPOSURE['person_id'])
    ids_to_keep = ids_measurement.union(ids_drug)

    PERSON = PERSON[PERSON['person_id'].isin(ids_to_keep)]
    DEATH = DEATH[DEATH['person_id'].isin(ids_to_keep)]
    VISIT_OCCURENCE = VISIT_OCCURENCE[VISIT_OCCURENCE['person_id'].isin(ids_to_keep)]

    PERSON.to_csv(OUTPUT + "PERSON.csv", index=False)
    DEATH.to_csv(OUTPUT + "DEATH.csv", index=False)
    VISIT_OCCURENCE.to_csv(OUTPUT + "VISIT_OCCURENCE.csv", index=False)
    MEASUREMENT.to_csv(OUTPUT + "MEASUREMENT.csv", index=False)
    DRUG_EXPOSURE.to_csv(OUTPUT + "DRUG_EXPOSURE.csv", index=False)

if __name__ == "__main__":
    __main__()