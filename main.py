
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
        selected = st.sidebar.checkbox(f'Include {col}', value=False)
        if selected:
            min_val = st.sidebar.number_input(f'Minimum {col}', min_value=min(df[col]), max_value=max(df[col]), value=min(df[col]), key=f'min_{col}')
            max_val = st.sidebar.number_input(f'Maximum {col}', min_value=min(df[col]), max_value=max(df[col]), value=max(df[col]), key=f'max_{col}')
            filters[col] = (min_val, max_val)
    return filters

# Reset
def reset_dashboard():
    for col in columns:
        st.session_state[f'min_{col}'] = min(df[col])
        st.session_state[f'max_{col}'] = max(df[col])
        st.session_state[f'{col}_checkbox'] = False

# Setup
st.title(':blue[Mastercard Data Visualization]')
st.button('Reset Dashboard', on_click=reset_dashboard)

dataset_selection = st.selectbox('Select Dataset', ['MASTERCARD SINGAPORE', 'MASTERCARD MALAYSIA'])

if dataset_selection == 'MASTERCARD SINGAPORE':
    df = sgp_df
    columns = ['latitude', 'longitude', 'travel_agency_hs', 'hotels_online_hs', 'hotels_offline_hs', 'grocery_stores_fb', 'electronics_appliances_hs']
    color_map = {
        'travel_agency_hs': ('#78c9e3', 'Light Blue > Travel Agency'),  # Light blue
        'hotels_online_hs': ('#00FF00', 'Green > Hotels Online'),
        'hotels_offline_hs': ('#FFA500', 'Orange > Hotels Offline'),
        'grocery_stores_fb': ('#800080', 'Purple > Grocery Stores'),
        'electronics_appliances_hs': ('#FF0000', 'Red > Electronics & Appliances')
    }
    #     color_map = {
    #     'travel_agency_hs': ('#ADD8E6', 'Light Blue > Travel Agency'),  # Light blue
    #     'hotels_online_hs': ('#90EE90', 'Light Green > Hotels Online'),  # Light green
    #     'hotels_offline_hs': ('#FFDAB9', 'Peach Puff > Hotels Offline'),  # Peach puff
    #     'grocery_stores_fb': ('#E6E6FA', 'Lavender > Grocery Stores'),  # Lavender
    #     'electronics_appliances_hs': ('#FAD7A0', 'Light Coral > Electronics & Appliances')  # Light coral
    # }
else:
    df = mys_df
    columns = ['latitude', 'longitude', 'beauty_medical_hs', 'sporting_goods_fb', 'restaurants_hs', 'apparel_fb']
    color_map = {
        'beauty_medical_hs': ('#FFC0CB', 'Pink > Beauty & Medical'),
        'sporting_goods_fb': ('#FFFF00', 'Yellow > Sporting Goods'),
        'restaurants_hs': ('#A52A2A', 'Brown > Restaurants'),
        'apparel_fb': ('#00FFFF', 'Cyan > Apparel')
    }

# Legend
st.sidebar.header('Legend')
for category, (color, label) in color_map.items():
    st.sidebar.markdown(f"<span style='color:{color}'>&nbsp;&#9632;</span> {label}", unsafe_allow_html=True)
    
st.sidebar.header('Filters')
filters = create_sidebar_filters(df, columns)

filtered_df = df.copy()
for col, (min_val, max_val) in filters.items():
    filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]

# Create map data
map_data = filtered_df[['latitude', 'longitude']]
map_data['color'] = filtered_df.apply(lambda row: next((color_map.get(col)[0] for col in color_map if row[col] > 0), '#000000'), axis=1)

# Map
st.map(map_data, color='color')