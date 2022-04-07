#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

def load_data():
    df_salary_input = pd.read_csv("https://raw.githubusercontent.com/koryhayward/deloitte-salary-analysis/main/salary_info.csv")
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
    st.markdown('''This notebook reports average practitioner salaries based on level, global business, sector, gender, member firm, educational attainment, and total years of experience. The data reported below were sourced from the total compensation survey posted to a *certain* Bowl on Fishbowl.   
    
The raw data can be accessed [here](https://docs.google.com/spreadsheets/d/1b15fEbCLaTxN_SCiYn7RX9aglDpTEkNbBjJ-XL_68ZA/edit#gid=37692271).  The data were pre-processsed to calculate average salary, median salary, average AIP, and median AIP based on the data elements noted above. 

As this is an MVP, it does not report unaggregated data. Please refer to the link above to explore in greater detail. Additionally, certain values from the survey were updated to match field options, given the ability for individuals to input freeform text (e.g., gender was collapsed into four options — female, male, non-confirming/non-binary, and prefer not to say).  

Practitioners can explore the data using the filters below. **The metrics will not populate until you've selected a value for level, global business, sector, gender, member firm, educational attainment, and years of experience -- and hit Submit.**  ''')

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
        df_analysis = get_data().append({"LEVEL": select_level, "SECTOR": select_sector, "GLOBAL_BUSINESS": select_business, "MEMBER_FIRM": select_firm, "GENDER": select_gender, "EDUCATION": select_education, "HIRE_SOURCE": select_source, "TOTAL_YOE": select_yoe}, ignore_index = True)

        df_salary_input_copy = df_salary_input.copy()
        df_salary_input_analysis_helper = pd.concat([df_salary_input_copy, df_analysis], axis = 0, ignore_index=True)
        df_salary_input_analysis = df_salary_input_analysis_helper[df_salary_input_analysis_helper.duplicated(subset = ['LEVEL', 'SECTOR', 'GLOBAL_BUSINESS', 'MEMBER_FIRM', 'GENDER', 'EDUCATION', 'HIRE_SOURCE', 'TOTAL_YOE'], keep = False)]
        df_salary_input_analysis = df_salary_input_analysis.drop_duplicates(subset = ['LEVEL', 'SECTOR', 'GLOBAL_BUSINESS', 'MEMBER_FIRM', 'GENDER', 'EDUCATION', 'HIRE_SOURCE', 'TOTAL_YOE'])

        st.subheader('Total Compensation Metrics')
        average_salary_metric, median_salary_metric, average_aip_metric, median_aip_metric = st.columns(4)
        average_salary_metric.metric('Average Salary', value = df_salary_input_analysis.AVERAGE_SALARY)
        median_salary_metric.metric('Median Salary', value = df_salary_input_analysis.MEDIAN_SALARY)
        average_aip_metric.metric('Average AIP', value = df_salary_input_analysis.AVERAGE_AIP)
        median_aip_metric.metric('Median AIP', value = df_salary_input_analysis.MEDIAN_AIP)

        st.sidebar.title('About')
        st.sidebar.info('This app is meant for educational purposes only.')

if __name__ == '__main__':
    main()