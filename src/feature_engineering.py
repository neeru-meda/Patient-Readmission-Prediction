import pandas as pd


def map_icd_to_category(icd):
    try:
        code = float(icd)

        if 390 <= code <= 459 or code == 785:
            return 'Circulatory'

        if 460 <= code <= 519 or code == 786:
            return 'Respiratory'

        if 520 <= code <= 579 or code == 787:
            return 'Digestive'

        if str(icd).startswith('250'):
            return 'Diabetes'

        if 800 <= code <= 999:
            return 'Injury'

        if 710 <= code <= 739:
            return 'Musculoskeletal'

        if 580 <= code <= 629:
            return 'Genitourinary'

        if 140 <= code <= 239:
            return 'Neoplasms'

        return 'Other'

    except:
        return 'Other'


def create_features(df):

    df = df.copy()

    df['total_prior_visits'] = (
        df['number_outpatient']
        + df['number_emergency']
        + df['number_inpatient']
    )

    df['treatment_changed'] = (
        df['change'] == 'Ch'
    ).astype(int)

    df['diag1_category'] = (
        df['diag_1']
        .apply(map_icd_to_category)
    )

    df['lab_intensity'] = (
        df['num_lab_procedures']
        / (df['time_in_hospital'] + 1)
    )

    df['med_intensity'] = (
        df['num_medications']
        / (df['time_in_hospital'] + 1)
    )

    return df

if __name__ == "__main__":
    df = pd.read_csv('d:\\Codes\\Patient_Readmission_Prediction\\data\\processed\\diabetic_data_cleaned.csv')
    df = create_features(df)
    print("Feature engineering completed.")
    print(df.head())

    df.to_csv('d:\\Codes\\Patient_Readmission_Prediction\\data\\processed\\diabetic_data_with_features.csv', index=False)