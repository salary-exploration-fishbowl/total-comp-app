#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

@st.cache
def load_data():
    df_salary_input = pd.read_csv("https://raw.githubusercontent.com/salary-exploration-fishbowl/total-comp-app/main/salary_info.csv")
    return df_salary_input

def main(): 
    df_salary_input = load_data()

    level = list(df_salary_input.LEVEL.sort_values().unique())
    sector = list(df_salary_input.SECTOR.sort_values().unique())
    business = list(df_salary_input.GLOBAL_BUSINESS.sort_values().unique())
    firm = list(df_salary_input.MEMBER_FIRM.sort_values().unique())
    gender = list(df_salary_input.GENDER.sort_values().unique())
    education = list(df_salary_input.EDUCATION.sort_values().unique())
    source = list(df_salary_input.HIRE_SOURCE.sort_values().unique())
    yoe = list(df_salary_input.TOTAL_YOE.sort_values().unique())
    
    st.header("Total Compensation: Aggregate Analysis from Fishbowl Survey")
    st.markdown('''##### Please DM the author of the original post linking to this website for feature requests or troubleshooting.  
    
This website reports average practitioner total compensation based on level, global business, sector, gender, member firm, educational attainment, and total years of experience. The data reported below were sourced from the total compensation survey posted to a *certain* Bowl on Fishbowl.   The raw data can be accessed [here](https://docs.google.com/spreadsheets/d/1b15fEbCLaTxN_SCiYn7RX9aglDpTEkNbBjJ-XL_68ZA/edit#gid=37692271).  The data were pre-processsed to calculate average salary and average AIP based on the data elements noted above. 

Practitioners can explore the data using the filters in the panel. **The metrics will not populate until you've selected a value for level, sector, global business, member firm, gender, education, hire source, and years of experience -- and then hit *Submit*.**  

If you submit data for which there is no reference the site will return an error in the space below, asking you to try again. ''')

    def get_data():
        place_holder = pd.DataFrame(columns = list(df_salary_input.columns))
        return place_holder

    form = st.sidebar.form(key = 'salary_analysis_form')
    st.sidebar.subheader("Data Elements for Analysis")
    select_level = st.sidebar.selectbox('Level', level)
    select_sector = st.sidebar.selectbox('Sector', sector)
    select_business = st.sidebar.selectbox('Global Business', business)
    select_firm = st.sidebar.selectbox('Member Firm', firm)
    select_gender = st.sidebar.selectbox('Gender', gender)
    select_education = st.sidebar.selectbox('Education', education)
    select_source = st.sidebar.selectbox('Hire Source', source)
    select_yoe = st.sidebar.slider('Years of Experience', min_value = 0, max_value = 35)
    if form.form_submit_button("Submit"): 
        try: 
            df_analysis = get_data().append({"LEVEL": select_level, "SECTOR": select_sector, "GLOBAL_BUSINESS": select_business, "MEMBER_FIRM": select_firm, "GENDER": select_gender, "EDUCATION": select_education, "HIRE_SOURCE": select_source, "TOTAL_YOE": select_yoe}, ignore_index = True)

            df_salary_input_copy = df_salary_input.copy()
            df_salary_input_analysis_helper = pd.concat([df_salary_input_copy, df_analysis], axis = 0, ignore_index=True)
            df_salary_input_analysis = df_salary_input_analysis_helper[df_salary_input_analysis_helper.duplicated(subset = ['LEVEL', 'SECTOR', 'GLOBAL_BUSINESS', 'MEMBER_FIRM', 'GENDER', 'EDUCATION', 'HIRE_SOURCE', 'TOTAL_YOE'], keep = False)]
            df_salary_input_analysis = df_salary_input_analysis.drop_duplicates(subset = ['LEVEL', 'SECTOR', 'GLOBAL_BUSINESS', 'MEMBER_FIRM', 'GENDER', 'EDUCATION', 'HIRE_SOURCE', 'TOTAL_YOE'])

            st.subheader('Total Compensation Metrics')
            average_salary_metric, median_salary_metric, average_aip_metric, median_aip_metric = st.columns(4)
            average_salary_metric.metric('Average Salary', value = df_salary_input_analysis.AVERAGE_SALARY)
            average_aip_metric.metric('Average AIP', value = df_salary_input_analysis.AVERAGE_AIP)

        except: 
            st.markdown('''### You input a combination of values for which the database does not have a reference. Please, try again.''')

        st.sidebar.title('About')
        st.sidebar.info('This website is meant for educational purposes only, as the Bowl has been filled with total compensation questions recently.')

if __name__ == '__main__':
    main()
