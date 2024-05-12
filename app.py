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


# with st.form("my_form"):
#     value_chain = st.selectbox('Value Chain:', ['Select'] + list(data['value_chain'].unique()))
#     technology = st.selectbox('Technology:', ['Select'] + list(data[data['value_chain'] == value_chain]['technology'].unique()))
#     core_occupation = st.selectbox('Core Occupation:', ['Select'] + list(data[data['technology'] == technology]['core_occupation'].unique()))
    
#     # Every form must have a submit button.
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write("Submitted")


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







with st.expander("Fill out form below to validate the model"):
    with st.form(key='validation_form'):
        # static text for showing the user what filters they are validating
        st.markdown(f"""
Validating model for:
- **Value Chain**: {value_chain}
- **Technology**: {technology}
- **Core Occupation**: {core_occupation}
""", unsafe_allow_html=True)



        name = st.text_input("Name")
        contact_info = st.text_input("Contact Information")
        qualifications = st.text_area("Your Qualifications")
        strengths = st.text_area("Describe strengths of the current model")
        improvements = st.text_area("Suggest areas for improvement")
        submit_button = st.form_submit_button(label='Submit Validation')

        if submit_button:
            form_data = {
                "Name": name,
                "Contact Information": contact_info,
                "Qualifications": qualifications,
                "Strengths": strengths,
                "Improvements": improvements,
                "Value Chain": value_chain,
                "Technology": technology,
                "Core Occupation": core_occupation
            }
            df = pd.DataFrame([form_data])
            df.to_csv('validation_data.csv', mode='a', header=not pd.io.common.file_exists('validation_data.csv'), index=False)
            st.success("Thank you for your feedback!")




            # Process the validation feedback as needed


# base_url = "https://your-deployment-url.com/validate_form"  # Change this to the URL where your validation form is deployed
# params = {
#     "value_chain": value_chain,
#     "technology": technology,
#     "core_occupation": core_occupation
# }
# query_string = urllib.parse.urlencode(params)
# validation_url = f"{base_url}?{query_string}"

# # Button that opens the validation form in a new tab
# button_html = f'<a target="_blank" href="{validation_url}" style="text-decoration: none;"><button style="color: white; background-color: blue; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Validate Model</button></a>'
# st.markdown(button_html, unsafe_allow_html=True)

