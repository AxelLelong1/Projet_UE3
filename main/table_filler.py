import pandas as pd

# Définir les examens microbiologiques d'intérêt
allowed_specs = ["BLOOD CULTURE", "URINE", "STOOL"]

# Définir les bactéries d'intérêt 
allowed_orgs = [
    "ESCHERICHIA COLI",
    "KLEBSIELLA PNEUMONIAE",
    "PSEUDOMONAS AERUGINOSA",
    "STAPH AUREUS COAG +",
    "ENTEROCOCCUS FAECALIS",
    "ENTEROCOCCUS FAECIUM",
    "CLOSTRIDIUM DIFFICILE"]

allowed_drugs = [
    "VANCOMYCIN",
    "CEFTRIAXONE",
    "AMOXICILLIN",
    "PIPERACILLIN-TAZOBACTAM"
]

def fill_person_table(data, mapping):
    # Remplissage de la table person
    PERSON = pd.DataFrame()
    PERSON['person_id'] = data['subject_id']
    PERSON['gender_concept_id'] = data['gender'].map(dict(zip(mapping['source_code'], mapping['target_concept_id'])))
    PERSON['year_of_birth'] = pd.to_datetime(data['anchor_year'] - data['anchor_age']).dt.year
    PERSON['race_concept_id'] = 0
    PERSON['ethnicity_concept_id'] = 0

    return PERSON

def fill_death_table(data: pd.DataFrame):

    DEATH = pd.DataFrame()
    
    # Garde les person_id existants dans PERSON
    data = data[data['dod'].notnull()]

    # Remplissage de la table death
    DEATH['person_id'] = data['subject_id']
    DEATH['death_date'] = pd.to_datetime(data['dod'])
    DEATH['death_type_concept_id'] = 38003569  # Valeur par défaut
    
    return DEATH

def fill_visit_occurrence_table(data: pd.DataFrame):

    VISIT_OCCURENCE = pd.DataFrame()
    # Remplissage de la table visit_occurrence
    VISIT_OCCURENCE['visit_occurrence_id'] = data['hadm_id']
    VISIT_OCCURENCE['person_id'] = data['subject_id']

    VISIT_OCCURENCE['visit_start_date'] = pd.to_datetime(data['admittime'])
    VISIT_OCCURENCE['visit_end_date'] = pd.to_datetime(data['dischtime'])

    VISIT_OCCURENCE['visit_concept_id'] = 9201 
    VISIT_OCCURENCE['visit_type_concept_id'] = 32817 

    return VISIT_OCCURENCE

def fill_measurement_table(data: pd.DataFrame, mapping: pd.DataFrame):

    MEASUREMENT = pd.DataFrame()

    # Filtrer les données pour ne garder que les examens et bactéries d'intérêt
    filtered_data = data[
        (data['spec_type_desc'].isin(allowed_specs)) & 
        (data['org_name'].isin(allowed_orgs)) &
        (data['hadm_id'].notnull())
    ].reset_index(drop=True)

    MEASUREMENT['measurement_id'] = filtered_data.index
    MEASUREMENT['person_id'] = filtered_data['subject_id']
    MEASUREMENT['visit_occurrence_id'] = filtered_data['hadm_id']
    
    MEASUREMENT['measurement_date'] = pd.to_datetime(filtered_data['chartdate'])

    MEASUREMENT['measurement_concept_id'] = filtered_data['spec_type_desc'].map(dict(zip(mapping['source_code'], mapping['target_concept_id'])))
    MEASUREMENT['value_as_concept_id'] = filtered_data['org_name'].map(dict(zip(mapping['source_code'], mapping['target_concept_id'])))
    MEASUREMENT['measurement_type_concept_id'] = 32817

    MEASUREMENT['measurement_source_value'] = filtered_data['spec_type_desc']
    MEASUREMENT['value_source_value'] = filtered_data['org_name']

    return MEASUREMENT

def fill_drug_exposure_table(data: pd.DataFrame, mapping: pd.DataFrame):

    filtered_data = data[
        ((data['drug']).str.upper().isin(allowed_drugs)) & 
        (data['hadm_id'].notnull())
    ].reset_index(drop=True)

    DRUG_EXPOSURE = pd.DataFrame()
    # Remplissage de la table drug_exposure
    DRUG_EXPOSURE['drug_exposure_id'] = filtered_data.index
    DRUG_EXPOSURE['person_id'] = filtered_data['subject_id']
    DRUG_EXPOSURE['visit_occurrence_id'] = filtered_data['hadm_id']

    DRUG_EXPOSURE['drug_exposure_start_date'] = pd.to_datetime(filtered_data['starttime'])
    DRUG_EXPOSURE['drug_exposure_end_date'] = pd.to_datetime(filtered_data['stoptime'])

    DRUG_EXPOSURE['drug_concept_id'] = filtered_data['drug'].map(dict(zip(mapping['source_code'], mapping['target_concept_id'])))
    DRUG_EXPOSURE['drug_source_value'] = filtered_data['drug']
    DRUG_EXPOSURE['drug_type_concept_id'] = 32817

    return DRUG_EXPOSURE