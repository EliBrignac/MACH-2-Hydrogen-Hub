import pandas as pd

# Function to load data or create a new dataframe if none exists
def load_data():
    try:
        df = pd.read_csv('validation_data.csv')
        # Ensure string fields are stripped of whitespace and have the correct case if necessary
        df['Value Chain'] = df['Value Chain'].str.strip()
        df['Technology'] = df['Technology'].str.strip()
        df['Core Occupation'] = df['Core Occupation'].str.strip()
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Value Chain", "Technology", "Core Occupation", "Validation Count"])


# Function to increment validation count
def increment_validation_count(value_chain, technology, core_occupation):
    df = load_data()
    
    # Ensure inputs are stripped of any leading/trailing whitespace
    value_chain = value_chain.strip()
    technology = technology.strip()
    core_occupation = core_occupation.strip()

    # Use mask to find the existing row
    mask = (df['Value Chain'] == value_chain) & (df['Technology'] == technology) & (df['Core Occupation'] == core_occupation)
    row_index = df.loc[mask].index

    if row_index.empty:
        # If the combination does not exist, add it with a count of 1
        new_row = pd.DataFrame({
            "Value Chain": [value_chain],
            "Technology": [technology],
            "Core Occupation": [core_occupation],
            "Validation Count": [1],
        })
        df = pd.concat([df, new_row], ignore_index=True)
        print("New row added")  
    else:
        # If it exists, increment the count
        df.loc[row_index, "Validation Count"] += 1
        print("Count incremented for row index", row_index)  # Debug statement

    
    df.to_csv('validation_data.csv', index=False)
    print("DataFrame saved to CSV.")  # Debug statement
