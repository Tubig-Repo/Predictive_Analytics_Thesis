import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.path.abspath(".."))

import data_loader
import visualization


st.set_page_config(layout="wide")


# Select Boxes 
color_theme = st.selectbox("Select a color theme", ['blues', 'greens', 'reds'])
cluster_select = st.selectbox("Select cluster to visualize", ['Low Wealth', 'Moderate Wealth', 'High Wealth'])

# Function to get selected region data
cluster_columns = {
    'Low Wealth': 'Low Wealth Score',
    'Moderate Wealth': 'Moderate Wealth Score',
    'High Wealth': 'High Wealth Score'
}

def get_selected_region_data(click_data):
    if click_data is not None:
        region_name = click_data['points'][0]['location']
        region_data = df[df['Region Name'] == region_name]
        
        # Dynamically extract the wealth score based on cluster_select
        score_column = cluster_columns[cluster_select]
        wealth_score = region_data[score_column].values[0]
        # Extract total income
        total_income = region_data['Total Household Income'].values[0]
        
        return region_name, wealth_score, total_income
    return None, None, None

# Columns
col1, col2 = st.columns([2, 1])

df = data_loader.get_ml_output()
geo_data = data_loader.load_geodata()
with col1:
    st.subheader("Cluster Map")
    cluster_map = visualization.ml_map(data=df, geo_data=geo_data , cluster_select=cluster_select)
    clicked_region = st.plotly_chart(cluster_map, use_container_width=True, on_click=True, key="map_click", on_select="rerun")
# Handle region selection and display
if 'clicked_point' not in st.session_state:
    st.session_state.clicked_point = None

if clicked_region:
    # Extract the clicked region name from Plotly's click data
    st.session_state.clicked_point = clicked_region['selection']['points'][0]['location']
# Display selected region information
if st.session_state.clicked_point:
    # Find the selected region's data
    region_data = df[df['Standardized Region Name'] == st.session_state.clicked_point]
    st.write(region_data)
    if not region_data.empty:
        # Extract wealth score and total income
        # Extract wealth score dynamically based on cluster_select
        score_column = cluster_columns[cluster_select]
        wealth_score = region_data[score_column].values[0]
        total_income = region_data['Total Household Income'].values[0]
        
        with col2:
            st.write(f"**Selected Region: {st.session_state.clicked_point}**")
            
            # Styled information boxes
            st.markdown(f'''
            <div style="background-color: #1a1a1a; padding: 1rem; margin-bottom: 1rem; border-radius: 0.5rem; color: white; font-size: 1rem; text-align: center;">
            <strong style="font-size: 1.75rem;">{cluster_select} Score: <span style="font-size: 1.75rem;">{wealth_score}</span></strong>
            </div>
            <div style="background-color: #1a1a1a; padding: 1rem; margin-bottom: 1rem; border-radius: 0.5rem; color: white; font-size: 1rem; text-align: center;">
            <strong style="font-size: 1.75rem;">Total Income: <span style="font-size: 1.75rem;">{total_income:,}</span></strong>
            </div>
            ''', unsafe_allow_html=True)

    else:
        # Display nothing if no valid data exists for the region
        with col2:
            st.write("No data found for the selected region.")
else:
    st.write("Click on a region to view details.")