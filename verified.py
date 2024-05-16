import os
import pandas as pd

def load_data():
    try:
        df = pd.read_csv('validation_data.csv')
        df['Value Chain'] = df['Value Chain'].str.strip()
        df['Technology'] = df['Technology'].str.strip()
        df['Core Occupation'] = df['Core Occupation'].str.strip()
    except KeyError as e:
        print(f"Column not found: {e}")
        df = pd.DataFrame(columns=['Value Chain', 'Technology', 'Core Occupation', 'Validation Count'])  # Create empty DataFrame with required columns
    except FileNotFoundError:
        print("File not found. Creating new file.")
        df = pd.DataFrame(columns=['Value Chain', 'Technology', 'Core Occupation', 'Validation Count'])
        df.to_csv('validation_data.csv', index=False)
    return df

def increment_validation_count(value_chain, technology, core_occupation):
    df = load_data()
    value_chain = value_chain.strip()
    technology = technology.strip()
    core_occupation = core_occupation.strip()
    mask = (df['Value Chain'] == value_chain) & (df['Technology'] == technology) & (df['Core Occupation'] == core_occupation)
    row_index = df.loc[mask].index

    if row_index.empty:
        new_row = pd.DataFrame({
            "Value Chain": [value_chain],
            "Technology": [technology],
            "Core Occupation": [core_occupation],
            "Validation Count": [1]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df.loc[row_index, "Validation Count"] += 1

    df.to_csv('validation_data.csv', index=False)
    return df

def handle_form_submission(form_data):
    df = pd.DataFrame([form_data])
    file_exists = os.path.exists('raw_forms.csv')
    df.to_csv('raw_forms.csv', mode='a', header=not file_exists, index=False)

def get_validation_count(value_chain, technology, core_occupation):
    df = load_data()  # Make sure this properly handles file reading and column stripping
    value_chain = value_chain.strip()
    technology = technology.strip()
    core_occupation = core_occupation.strip()

    # Use mask to filter the DataFrame
    mask = (df['Value Chain'] == value_chain) & (df['Technology'] == technology) & (df['Core Occupation'] == core_occupation)
    filtered_df = df.loc[mask]

    # Check if any row matches the filter
    if not filtered_df.empty:
        validation_count = filtered_df['Validation Count'].iloc[0]  # Access the first row's count
        return int(validation_count) + 1
    else:
        return 0  # Return 0 if no validations are recorded for this configuration
