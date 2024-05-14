
'''
requirements streamlit, pandas
'''
import pandas as pd
import streamlit as st
import os

# Load CSV files
sgp_df = pd.read_csv(f'{os.getcwd()}/data/sgp_mastercard.csv')
mys_df = pd.read_csv(f'{os.getcwd()}/data/mys_mastercard.csv')

def create_sidebar_filters(df, columns):
    filters = {}
    for col in columns:
        min_val = st.sidebar.number_input(f'Minimum {col}', min_value=min(df[col]), max_value=max(df[col]), value=min(df[col]), key=f'min_{col}')
        max_val = st.sidebar.number_input(f'Maximum {col}', min_value=min(df[col]), max_value=max(df[col]), value=max(df[col]), key=f'max_{col}')
        filters[col] = (min_val, max_val)
    return filters

# Reset
def reset_dashboard():
    for col in columns:
        st.session_state[f'min_{col}'] = min(df[col])
        st.session_state[f'max_{col}'] = max(df[col])

# Setup
st.title('"blue[Mastercard Data Visualization]')
st.button('Reset Dashboard', on_click=reset_dashboard)  # Add the reset button

dataset_selection = st.selectbox('Select Dataset', ['MASTERCARD SINGAPORE', 'MASTERCARD MALAYSIA'])

if dataset_selection == 'MASTERCARD SINGAPORE':
    df = sgp_df
    columns = ['latitude', 'longitude', 'travel_agency_hs', 'hotels_online_hs', 'hotels_offline_hs', 'grocery_stores_fb', 'electronics_appliances_hs']
else:
    df = mys_df
    columns = ['latitude', 'longitude', 'beauty_medical_hs', 'sporting_goods_fb', 'restaurants_hs', 'apparel_fb']

st.sidebar.header('Filters')

filters = create_sidebar_filters(df, columns)
filtered_df = df.copy()
for col, (min_val, max_val) in filters.items():
    filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]

# map
# st.write('Data', filtered_df)
st.map(filtered_df)