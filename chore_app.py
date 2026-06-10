import streamlit as st
import pandas as pd
import numpy as np
import gspread
import openpyxl
import datetime



#Configure the page
st.set_page_config(page_title='Chores Dashboard', layout='wide')
st.title('Golly Chores Dashboard')
today = datetime.date.today()


#Congifure the display for the main spreadsheet and allow for reloading the data.
st.session_state.df = pd.read_excel('chore_sheet.xlsx')

#variables for chore sums.
chore_sum_1 = st.session_state.df['chore1'].sum(axis=2, numeric_only=True)
chore_sum_2 = st.session_state.df['chore2'].sum(axis=2, numeric_only=True)
chore_sum_3 = st.session_state.df['chore3'].sum(axis=2, numeric_only=True)
#chore_sum_4 = df['chore4'].sum(axis=2, numeric_only=True)
#chore_sum_5 = df['chore5'].sum(axis=2, numeric_only=True)
#chore_sum_6 = df['chore6'].sum(axis=2, numeric_only=True)
#chore_sum_7 = df['chore7'].sum(axis=2, numeric_only=True)
#chore_sum_8 = df['chore8'].sum(axis=2, numeric_only=True)
#chore_sum_9 = df['chore9'].sum(axis=2, numeric_only=True)
#chore_sum_10 = df['chore10'].sum(axis=2, numeric_only=True)
chore_total_sum = chore_sum_1 + chore_sum_2 + chore_sum_3 #+ chore_sum_4 + chore_sum_5 + chore_sum_6 + chore_sum_7 + chore_sum_8 + chore_sum_9 + chore_sum_10


#Add a new button for a chore.
st.write(chore_total_sum)
chore1 = st.session_state.button(df['chore1'])
st.write(chore_sum_1)
chore2 = st.session_state.button(df['chore2'])
st.write(chore_sum_2)
chore3 = st.session_state.button(df['chore3'])
st.write(chore_sum_3)
#chore4 = st.session_state.button(df['chore4'])
#st.write(chore_sum_4)
#chore5 = st.session_state.button(df['chore5'])
#st.write(chore_sum_5)
#chore6 = st.session_state.button(df['chore6'])
#st.write(chore_sum_6)
#chore7 = st.session_state.button(df['chore7'])
#st.write(chore_sum_7)
#chore8 = st.session_state.button(df['chore8'])
#st.write(chore_sum_8)
#chore9 = st.session_state.button(df['chore9'])
#st.write(chore_sum_9)
#chore10 = st.session_state.button(df['chore10'])
#st.write(chore_sum_10)

#Set the action when the button is pressed.
