import streamlit as st
st.set_page_config(page_title="Monkeypox Reporting", page_icon=":bar_chart:", layout= "wide")
from PIL import Image
import streamlit.components.v1 as components
from pathlib import Path
import pandas as pd
import plotly.express as px
import openpyxl
from streamlit_option_menu import option_menu
import json
import numpy as np
from streamlit_tags import st_tags
import plotly.graph_objects as go

# implement css into streamlit
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# page_bg = f"""
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-color: #353535;
# }}
# </style>
# """

# st.markdown(page_bg, unsafe_allow_html=True)

# Setting up collums for display website header-title
col1, col2, col3 = st.columns(3, gap = 'medium')

with col1:
    image = Image.open('csuf_logo.png')
    st.image(image, width= 150)

with col2:
    st.markdown("<h1>Mpox Surveillance Outbreak System</h1>", unsafe_allow_html = True)

with col3:
    image = Image.open('raise_logo.jpg')
    showimage = st.image(image, width= 200)

st.divider()


# sidebar for navigation
with st.sidebar:

    selected = option_menu('Menu Option',
                        
                        ['Overview',
                        'Demographic',
                        'Form',
                        'Prediction'],
                        icons=['activity','person','heart'],
                        default_index=0)
    
# Dashboard Page
if (selected == 'Overview'):
    main_col1, main_col2 = st.columns([6,3], gap = "large")
    with main_col1:

        col1, col2, col3, col4 = st.columns(4, gap = 'large')
        with col1:
            # st.write('Dashboard Updated at: \n<h4>8/3/2023. 1:30 PM</h4>', unsafe_allow_html= True)
            st.write('Dashboard Updated at:')
            st.subheader('8/3/2023. 1:30 PM')
        with col2:
            df = pd.read_csv("globalCaseDeath.csv")
            total_cases = df['Cases'].sum()
            st.write('Total Cases')
            st.subheader(total_cases)

        with col3:
            total_death = df['Deaths'].sum()
            st.write('Total Death')
            st.subheader(total_death)

        with col4:
            df_vaccine = pd.read_csv("vaccineAdmin.csv")
            total_vaccine = df_vaccine['Total'].sum()
            st.write('Total Vaccine')
            st.subheader(total_vaccine)
    

        # Setting up 2 tabs for map options
        tab1, tab2 = st.tabs(['States Map','Global Map'])

        # map_choices = option_menu('Map Options',
                        
        #                 ['States Map',
        #                 'Global Map'],
        #                 icons=[':statue_of_liberty:',':world_map:'],
        #                 default_index=0)
        
        with tab1:
            sub_col1, sub_col2 = st.columns([1,3])
            with sub_col1:
                df = pd.read_csv('caseCount.csv')  

                with st.expander('Cases by States'):
                    for index, row in df.iterrows():
                        st.divider()
                        st.write(f"{row['Location']} | {row['Cases']}")

                # add a scrollbar
                css='''
                <style>
                    [data-testid="stExpander"] div:has(>.streamlit-expanderContent) {
                        overflow: scroll;
                        height: 540px;
                    }
                </style>
                '''
                st.markdown(css, unsafe_allow_html=True)

            with sub_col2:
                f = open('usState.json')
                states_data = json.load(f)
                df_states = pd.read_csv("caseCount.csv")

                figure_1 = px.choropleth_mapbox(df_states, geojson = states_data, locations='Location', color='Cases',
                                        featureidkey = "properties.NAME",
                                        color_continuous_scale="blugrn",
                                        range_color=(0, 6000),
                                        mapbox_style = 'carto-positron',
                                        opacity = 0.5,
                                        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                                        #scope="usa",
                                        labels={'Cases':'Cases'}
                                        )

                figure_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo_bgcolor= '#0E1113')
                st.plotly_chart(figure_1)

        with tab2:
            sub_col1, sub_col2 = st.columns([1,3])
            with sub_col1:
                df = pd.read_csv('globalCaseDeath.csv')  

                with st.expander('Cases by Country'):
                    for index, row in df.iterrows():
                        st.divider()
                        st.write(f"{row['Country']} | {row['Cases']}")

                # add a scrollbar
                css='''
                <style>
                    [data-testid="stExpander"] div:has(>.streamlit-expanderContent) {
                        overflow: scroll;
                        height:540px;
                    }
                </style>
                '''
                st.markdown(css, unsafe_allow_html=True)

            with sub_col2:
                contries_geo = open('countries.geojson')
                countries_data = json.load(contries_geo)
                df_global = pd.read_csv('globalCaseDeath.csv')

                figure_2 = px.choropleth_mapbox(df_global, geojson = countries_data, locations='Country', color='Cases',
                                featureidkey = "properties.ADMIN",
                                color_continuous_scale="blugrn",
                                range_color=(1, 31000),
                                # scope="world",
                                mapbox_style = 'carto-positron',
                                zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                                labels={'Cases':'Cases'}
                                )
                figure_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo_bgcolor= '#0E1113')
                st.plotly_chart(figure_2)


    with main_col2:
        # with st.expander('Barcharts'):      
        cases = pd.read_csv("caseTrends.csv")
        cases['Timeline'] = pd.to_datetime(cases['Timeline']).dt.date

        st.bar_chart(cases, x = 'Timeline', y = 'Cases')

        st.bar_chart(cases,x = 'Timeline', y = 'Cumulative Cases')

            # Add custom CSS to change the background color of the chart
        st.markdown(
            """
            <style>
            .stDeckGlChart>div>div>div {
                background-color: #353535; /* Replace with your desired background color */
            }
            </style>
            """,
            unsafe_allow_html=True  )

    st.divider()
        # # add a scrollbar
        # css='''
        # <style>
        #     [data-testid="stExpander"] div:has(>.streamlit-expanderContent) {
        #         overflow: scroll;
        #         height: 400px;
        #     }
        # </style>
        # '''
        # st.markdown(css, unsafe_allow_html=True)

if (selected == 'Demographic'):
    gender_data = pd.read_csv("sexGender.csv")
    del gender_data[gender_data.columns[0]]
    gender_data_sum = gender_data.sum()
    input_col, pie_col = st.columns(2)
    gender_data_sum = gender_data_sum.reset_index()
    gender_data_sum.columns = ['Gender', 'Value']
    # st.dataframe(gender_data_sum)
    # st.dataframe(gender_data_sum)

    genderList = gender_data_sum['Gender']
    value = gender_data_sum['Value']
    fig = px.pie(gender_data_sum, names = genderList, values = value)    
    st.plotly_chart(fig)




if (selected == 'Form'):
     # page title
    st.title('Symptom Screening Form')

    col1, col2 = st.columns(2)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.selectbox('Gender', ('Male', 'Female', 'Transgender Male', 'Transgender Female', 'Other'))

    with col1:
        ethnic = st.selectbox('Ethnicity', ('American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latina', 'Native Hawaiian or Other Pacific Islander', 'White'))

    with col2:
        states = st.selectbox('State', ("Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"))        

    # symptoms = st.cg
    symptoms = st.multiselect(
    'Symptoms',
    ['None','Chills', 'Exhaustion', 'Fever', 'Headache'
     , 'Muscle aches', 'Backache', 'Swollen lymp nodes'])

    st.markdown('##')
    enter = st.button('Enter')

if (selected == 'Prediction'):
    st.write('Prediction')
