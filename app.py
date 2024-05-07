import streamlit as st
import pandas as pd

# Load the data
data = pd.read_csv('comma_fixed.csv')  # Replace 'your_data.csv' with the path to your CSV file
st.markdown(
    """
    <style>
    .element-container.st-eb .st-fc {
        margin-bottom: 0.5rem !important;
    }
    .sidebar .sidebar-content {
        width: 20%;
        margin-left: 80%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Hydrogen Technology Requirements Explorer")

# Select Boxes
value_chain = st.selectbox('Value Chain:', ['Select'] + list(data['value_chain'].unique()))
if value_chain != 'All':
    filtered_data = data[data['value_chain'] == value_chain]
else:
    filtered_data = data

technology = st.selectbox('Technology:', ['Select'] + list(filtered_data['technology'].unique()))
if technology != 'All':
    filtered_data = filtered_data[filtered_data['technology'] == technology]

core_occupation = st.selectbox('Core Occupation:', ['All'] + list(filtered_data['core_occupation'].unique()))
if core_occupation != 'All':
    filtered_data = filtered_data[filtered_data['core_occupation'] == core_occupation]

# Display the results
st.subheader(f"Requirements for:")
signature = f'<p style="color:grey; font-size: 20px;">{value_chain} - {technology} - {core_occupation}</p>'
st.markdown(signature, unsafe_allow_html=True)

if len(filtered_data) > 0:
    requirements = filtered_data['unique_requirements_for_hydrogen'].iloc[0]
    requirements_bullets = [f'- {requirement.strip()}' for requirement in requirements.split('.')]
    st.markdown('\n'.join(requirements_bullets))
else:
    st.write("No data available for the selected criteria.")
