import streamlit as st
import pandas as pd
from verified import load_data, increment_validation_count, handle_form_submission, get_validation_count


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


# ==============================================================================================================

# Select Boxes
value_chain = st.selectbox('Value Chain:', ['Select'] + list(data['value_chain'].unique()))
if value_chain != 'Select':
    filtered_data = data[data['value_chain'] == value_chain]
else:
    filtered_data = data
    

technology = st.selectbox('Technology:', ['Select'] + list(filtered_data['technology'].unique()))
if technology != 'Select':
    filtered_data = filtered_data[filtered_data['technology'] == technology]

core_occupation = st.selectbox('Core Occupation:', ['Select'] + list(filtered_data['core_occupation'].unique()))
if core_occupation != 'Select':
    filtered_data = filtered_data[filtered_data['core_occupation'] == core_occupation]

# Display Validation

st.write("Current Validation:", get_validation_count(value_chain, technology, core_occupation))


# Load the validation data
spell_checked_csv = pd.read_csv('comma_fixed.csv')

job_description_df = pd.read_excel(r'C:\Users\Eli Brignac\OneDrive\Desktop\Hydrogen\MACH-2-Hydrogen-Hub\given_files\Production_Electrolysis_Occupations.xlsx')
job_description_df = job_description_df.replace('\n', '', regex=True)
job_description_df = job_description_df.replace('_x000D_', '', regex=True)
job_description_df = job_description_df.replace('°', ' ', regex=True)
job_description_df = job_description_df.replace('_x0002_', ' ', regex=True)



# Display the validation count for the selected combination
if not (value_chain != 'Select' and technology != 'Select' and core_occupation != 'Select'):
    st.markdown(f"#### Please select a value chain, technology, and core occupation to view the requirements.")
else:
    st.markdown(f"#### Key Activities for {value_chain} - {technology} - {core_occupation}")
    activities = job_description_df[job_description_df['Value Chain'] == value_chain][job_description_df['Technology'] == technology][job_description_df['Core Occupation'] == core_occupation]['Key Activities']
    activities = list(activities)[0].split('•')
    for activity in activities:
        if activity.strip() != '':
            st.write(f'- {activity}')
    #st.write(activities)

    st.markdown(f"#### Hydrogen Related Requirements for {value_chain} - {technology} - {core_occupation}")
    if value_chain != 'Select' and technology != 'Select' and core_occupation != 'Select':
        sents = spell_checked_csv[spell_checked_csv['value_chain'] == value_chain][spell_checked_csv['technology'] == technology][spell_checked_csv['core_occupation'] == core_occupation]['unique_requirements_for_hydrogen']
        sents = list(sents)[0].split('.')
        for sent in sents:
            st.write(f'- {sent}')

# ==============================================================================================================



# with st.form("my_form"):
#     value_chain = st.selectbox('Value Chain:', ['Select'] + list(data['value_chain'].unique()))
#     technology = st.selectbox('Technology:', ['Select'] + list(data[data['value_chain'] == value_chain]['technology'].unique()))
#     core_occupation = st.selectbox('Core Occupation:', ['Select'] + list(data[data['technology'] == technology]['core_occupation'].unique()))
    
#     # Every form must have a submit button.
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write("Submitted")



# #df = load_data()
# df = pd.read_csv('validation_data.csv')

# # Display the validation count for the selected combination
# if value_chain != 'Select' and technology != 'Select' and core_occupation != 'Select':
#     row = df[(df['Value Chain'] == value_chain) & (df['Technology'] == technology) & (df['Core Occupation'] == core_occupation)]
#     if not row.empty:
#         validation_count = row['Validation Count'].iloc[0]
#         st.write(f"Current validation count for this configuration: {validation_count}")
#     else:
#         st.write("This configuration has not yet been validated.")

# # Display the results
# st.subheader(f"Requirements for:")
# signature = f'<p style="color:grey; font-size: 20px;">{value_chain} - {technology} - {core_occupation}</p>'
# st.markdown(signature, unsafe_allow_html=True)

# if len(filtered_data) > 0:
#     requirements = filtered_data['unique_requirements_for_hydrogen'].iloc[0]
#     requirements_bullets = [f'- {requirement.strip()}' for requirement in requirements.split('.')]
#     st.markdown('\n'.join(requirements_bullets))
# else:
#     st.write("No data available for the selected criteria.")






st.markdown("#### Form Validation Dropdown")
with st.expander("Fill out form below to validate the model"):
    with st.form(key='validation_form'):
        st.markdown(f"""
        Validating model for:
        - **Value Chain**: {value_chain}
        - **Technology**: {technology}
        - **Core Occupation**: {core_occupation}
        """, unsafe_allow_html=True)

        isValid = st.checkbox("Is the current model accurate to your knowledge?")
        st.write("\n")
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
                "Is Valid": isValid,
                "Strengths": strengths,
                "Improvements": improvements,
                "Value Chain": value_chain,
                "Technology": technology,
                "Core Occupation": core_occupation
            }
            # Write form data to CSV
            handle_form_submission(form_data)

            # Call the increment function and use the returned DataFrame to get the updated count
            updated_df = increment_validation_count(value_chain, technology, core_occupation, isValid)
            if (isValid):
                row = updated_df[(updated_df['Value Chain'] == value_chain) & (updated_df['Technology'] == technology) & (updated_df['Core Occupation'] == core_occupation)]
                if not row.empty:
                    validation_count = row['Validation Count'].iloc[0]
                    st.write(f"Updated validation count for this configuration: {validation_count}")
                else:
                    st.write("This configuration has now been validated for the first time.")
            else:
                st.write("Model Invalid")



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



# Most relevant requirements

st.markdown("## Analytics Summary")
st.markdown("#### Most Relevant Requirements")


st.markdown("""
- Selecting, designing, and maintaining electrolyzers, vessels, compressors, piping systems, and fittings for reliable hydrogen operation.
- Focus on appropriate material selection, design, and maintenance to withstand high-pressure hydrogen environments, particularly in fuel tanks and related infrastructure.
- knowledge of materials, coatings, and inhibitors aimed at protecting against hydrogen corrosion and embrittlement.
- Ensuring the durability and safety of equipment and systems in handling hydrogen under various pressures and temperatures.
- Knowledge of hydrogen related regulations, standards and codes and keeping up-to-date with the latest changes.
- Understanding of combined-cycle power generation using hydrogen blending, electrochemical reactions, PEM electrolyzers, hydrogen compression processes

""")


import streamlit.components.v1 as components
from jinja2 import Template
def render_file():
    # Your dynamic data
    app_title = "My Streamlit App"
    items = ["Item 1", "Item 2", "Item 3"]

    # Load the Jinja2 template
    path_to_html = r"cluster_viz_plot.html" 

    with open(path_to_html, "r",  encoding='utf-8') as template_file:
        template_content = template_file.read()
        jinja_template = Template(template_content)

    # Render the template with dynamic data
    rendered_html = jinja_template.render(title=app_title, items=items)

    # Display the HTML in Streamlit app
    components.html(rendered_html, height=800, width=1200, scrolling=True)
render_file()

option = st.selectbox(
    'Example Sentences From Clusters:',
    ('Cluster 0', 
     'Cluster 1',
     'Cluster 2',
     'Cluster 3',
     'Cluster 4',
     'Cluster 5',
     'Cluster 6',
     'Cluster 7',
     'Cluster 8',
     'Cluster 9',)
)

cluster_sentence_map = {
    'Cluster 0': ['Hydrogen properties, behaviour and potential hazards created (this is the biggest cluster and the most basic)'],
    'Cluster 1': ['Safety when working with or around hydrogen (this is second biggest cluster and also very basic)'],
    'Cluster 2': ['Appropriate selection, design and maintenance of hydrogen fuel tanks, piping systems and fitting, valves and seals to withstand hydrogen pressure (high/low) and temperatures (hot/cold)',
                  'Assess integrity of vessels, tanks, piping systems and fitting, valves and seals to withstand hydrogen pressure and temperatures',
                  'Design and selection of  pressure vessels, piping  systems and fitting, valves and  seals, coatings and insulation  to withstand hydrogen pressure and temperatures'],
    'Cluster 3': ['Knowledge of hydrogen related regulations, standards and codes'],
    'Cluster 4': ['Keep up-to-date with changes to hydrogen technology, regulations,standards and codes'],
    'Cluster 5': ['"specific skills/knowledge "'],
    'Cluster 6': ['Understanding of combined-cycle power generation using hydrogen blending'],
    'Cluster 7': ['Nothing that impacts this occupation’s ability to apply expertise to manufacturing for hydrogen supply chains'],
    'Cluster 8': ['Understanding of electrochemical reactions, processes and hydrogen production using PEM electrolyzers',
                  'Understanding of hydrogen production process using PEM electrolyzers'],
    'Cluster 9': ['Knowledge and selection of type of materials, coatings and inhibitors to use to protect from hydrogen corrosion',
                  'Materials, coatings and inhibitorsto use and correct application toprotect from hydrogen corrosion'],
}


display_sentences = cluster_sentence_map[option]
for sentence in display_sentences:
    st.write(f'- {sentence}')