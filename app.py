#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(layout = 'wide')

@st.cache
def load_data():
    df_salary_input = pd.read_csv("https://raw.githubusercontent.com/salary-exploration-fishbowl/total-comp-app/main/salary_cleaned.csv")
    return df_salary_input

def main(): 
    df_salary_input = load_data()

    st.header("Total Compensation: Aggregate Analysis from Fishbowl Survey")
    st.markdown('''##### Please DM the author of the original post linking to this website for feature requests or troubleshooting.  
    
This website reports total compensation based on level, global business, sector, gender, member firm, educational attainment, and total years of experience. The data reported below were sourced from the total compensation survey posted to a *certain* Bowl on Fishbowl.   The raw data can be accessed [here](https://docs.google.com/spreadsheets/d/1HfsaGWobDNaqua6wlQfqB0SOQYrJA5s0xMz7eZDSIrE/edit#gid=1369497600). The data presented in the charts below report the distribution of salary, AIP, and % AIP based on user inputs. Practitioners can explore the data using the filters in the panel. Additionally, summary statistics are presented in the Data Table below. ''')

    column_one, column_two, column_three = st.columns(3)

    container = st.sidebar.container()
    container.title('About')
    container.info('This website is meant for educational purposes only, as the Bowl has been filled with total compensation questions recently.')
    st.subheader('Data Table')

    select_some_years = container.checkbox("Would you like to select a YOE range for the plots?")

    level = list(df_salary_input.LEVEL.sort_values().unique())
    sector = list(df_salary_input.SECTOR.sort_values().unique())
    business = list(df_salary_input.GLOBAL_BUSINESS.sort_values().unique())
    firm = list(df_salary_input.MEMBER_FIRM.sort_values().unique())
    gender = list(df_salary_input.GENDER.sort_values().unique())
    education = list(df_salary_input.EDUCATION.sort_values().unique())
    source = list(df_salary_input.HIRE_SOURCE.sort_values().unique())

    level.insert(0, 'All')
    sector.insert(0, 'All')
    business.insert(0, 'All')
    firm.insert(0, 'All')
    gender.insert(0, 'All')
    education.insert(0, 'All')
    source.insert(0, 'All')

    st.sidebar.subheader("Data Elements for Analysis")
    select_level = st.sidebar.selectbox('Level:', level)
    if select_level == 'All': 
        df_salary_input = df_salary_input
    else: 
        df_salary_input = df_salary_input.loc[df_salary_input.LEVEL.apply(lambda x: x in select_level)]

    select_sector = st.sidebar.selectbox('Sector', sector)
    if select_sector == 'All': 
        df_salary_input = df_salary_input
    else: 
        df_salary_input = df_salary_input.loc[df_salary_input.SECTOR.apply(lambda x: x in select_sector)]

    select_business = st.sidebar.selectbox('Global Business', business)
    if select_business == 'All': 
        df_salary_input = df_salary_input
    else: 
        df_salary_input = df_salary_input.loc[df_salary_input.GLOBAL_BUSINESS.apply(lambda x: x in select_business)]

    select_firm = st.sidebar.selectbox('Member Firm', firm)
    if select_firm == 'All': 
        df_salary_input = df_salary_input
    else: 
        df_salary_input = df_salary_input.loc[df_salary_input.MEMBER_FIRM.apply(lambda x: x in select_firm)]

    select_gender = st.sidebar.selectbox('Gender', gender)
    if select_gender == 'All': 
        df_salary_input = df_salary_input
    else: 
        df_salary_input = df_salary_input.loc[df_salary_input.GENDER.apply(lambda x: x in select_gender)]

    select_education = st.sidebar.selectbox('Education', education)
    if select_education == 'All': 
        df_salary_input = df_salary_input
    else: 
        df_salary_input = df_salary_input.loc[df_salary_input.EDUCATION.apply(lambda x: x in select_education)]

    select_source = st.sidebar.selectbox('Hire Source', source)
    if select_source == 'All': 
        df_salary_input = df_salary_input
    else: 
        df_salary_input = df_salary_input.loc[df_salary_input.HIRE_SOURCE.apply(lambda x: x in select_source)]

    if select_some_years:
        start_yoe, end_yoe = container.select_slider('Select range of YOE:', options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], value = [0, 35])
        start_yoe = int(start_yoe)
        end_yoe = int(end_yoe)

        df_salary_input = df_salary_input.loc[df_salary_input.TOTAL_YOE.between(start_yoe, end_yoe)]

        try: 
            salary_distribution = px.histogram(df_salary_input, x = 'SALARY').update_yaxes(visible = False)
            aip_distribution = px.histogram(df_salary_input, x = 'AIP').update_yaxes(visible = False)
            aip_percent_distribution = px.histogram(df_salary_input, x = 'AIP_PERCENT').update_yaxes(visible = False)

            column_one.plotly_chart(salary_distribution, use_container_width = True)
            column_two.plotly_chart(aip_distribution, use_container_width = True)
            column_three.plotly_chart(aip_percent_distribution, use_container_width = True)
            
            st.table(df_salary_input.describe())

        except: 
            st.markdown('''### You caught an error! Please ensure you only selected one checkbox option for total years of experience.''')

    else: 
        #df_salary_input = df_salary_input
        try: 
            salary_distribution = px.histogram(df_salary_input, x = 'SALARY').update_yaxes(visible = False)
            aip_distribution = px.histogram(df_salary_input, x = 'AIP').update_yaxes(visible = False)
            aip_percent_distribution = px.histogram(df_salary_input, x = 'AIP_PERCENT').update_yaxes(visible = False)

            column_one.plotly_chart(salary_distribution, use_container_width = True)
            column_two.plotly_chart(aip_distribution, use_container_width = True)
            column_three.plotly_chart(aip_percent_distribution, use_container_width = True)
            
            st.table(df_salary_input.describe())

        except: 
            st.markdown('''### You caught an error!''')

if __name__ == '__main__':
    main()
