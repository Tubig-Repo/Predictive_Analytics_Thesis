import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import numpy as np
import altair as alt
import json
sys.path.append(os.path.abspath(".."))

import data_loader
import visualization


st.set_page_config(
    page_title="Regional Meat Expenditure Dashboard",
    page_icon="🥩",
    layout="wide",
    initial_sidebar_state="expanded")


# # Select Boxes 
# color_theme = st.selectbox("Select a color theme", ['blues', 'greens', 'reds'])
# cluster_select = st.selectbox("Select cluster to visualize", ['Low Wealth', 'Moderate Wealth', 'High Wealth'])

# # Function to get selected region data
# cluster_columns = {
#     'Low Wealth': 'Low Wealth Score',
#     'Moderate Wealth': 'Moderate Wealth Score',
#     'High Wealth': 'High Wealth Score'
# }

# def get_selected_region_data(click_data):
#     if click_data is not None:
#         region_name = click_data['points'][0]['location']
#         region_data = df[df['Region Name'] == region_name]
        
#         # Dynamically extract the wealth score based on cluster_select
#         score_column = cluster_columns[cluster_select]
#         wealth_score = region_data[score_column].values[0]
#         # Extract total income
#         total_income = region_data['Total Household Income'].values[0]
        
#         return region_name, wealth_score, total_income
#     return None, None, None

# # Columns
# col1, col2 = st.columns([2, 1])

# df = data_loader.get_ml_output()
# geo_data = data_loader.load_geodata()
# with col1:
#     st.subheader("Cluster Map")
#     cluster_map = visualization.ml_map(data=df, geo_data=geo_data , cluster_select=cluster_select)
#     clicked_region = st.plotly_chart(cluster_map, use_container_width=True, on_click=True, key="map_click", on_select="rerun")
# # Handle region selection and display
# if 'clicked_point' not in st.session_state:
#     st.session_state.clicked_point = None

# if clicked_region:
#     # Extract the clicked region name from Plotly's click data
#     st.session_state.clicked_point = clicked_region['selection']['points'][0]['location']
# # Display selected region information
# if st.session_state.clicked_point:
#     # Find the selected region's data
#     region_data = df[df['Standardized Region Name'] == st.session_state.clicked_point]
#     st.write(region_data)
#     if not region_data.empty:
#         # Extract wealth score and total income
#         # Extract wealth score dynamically based on cluster_select
#         score_column = cluster_columns[cluster_select]
#         wealth_score = region_data[score_column].values[0]
#         total_income = region_data['Total Household Income'].values[0]
        
#         with col2:
#             st.write(f"**Selected Region: {st.session_state.clicked_point}**")
            
#             # Styled information boxes
#             st.markdown(f'''
#             <div style="background-color: #1a1a1a; padding: 1rem; margin-bottom: 1rem; border-radius: 0.5rem; color: white; font-size: 1rem; text-align: center;">
#             <strong style="font-size: 1.75rem;">{cluster_select} Score: <span style="font-size: 1.75rem;">{wealth_score}</span></strong>
#             </div>
#             <div style="background-color: #1a1a1a; padding: 1rem; margin-bottom: 1rem; border-radius: 0.5rem; color: white; font-size: 1rem; text-align: center;">
#             <strong style="font-size: 1.75rem;">Total Income: <span style="font-size: 1.75rem;">{total_income:,}</span></strong>
#             </div>
#             ''', unsafe_allow_html=True)

#     else:
#         # Display nothing if no valid data exists for the region
#         with col2:
#             st.write("No data found for the selected region.")
# else:
#     st.write("Click on a region to view details.")

#######################
# Page configuration


st.title("Socioeconomic Segmentation Analysis by Region in the Philippines")



alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)

#######################
# Load data

df = pd.read_csv('ModelOutput/Socioeconomic-Segementation.csv')

#######################
# Sidebar
with st.sidebar:
    factors = st.selectbox('Select Type of Factor', ())
    st.title('🏠 Socioeconomic Segmentation Analysis base on FIES')
    
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    # Select Specific Business Score Prediction 
    region_list = df['Standardized Region Name'].unique()
    # Add mapbox selection
    map_metric = st.selectbox(
        'Select Region',
        region_list
    )
    # Select a cluster to analyze
    unique_clusters = df['Clusters'].unique()
    selected_cluster = st.selectbox('Select Cluster', unique_clusters)
    clustered_data = df[df['Clusters'] == selected_cluster]
with open('GeoJSON/PHRegions.json', 'r') as f:
        geo_data = json.load(f)
            
#######################
# Dashboard Main Panel
col = st.columns((1.5, 2, 1.5))

# Cluster Profile Summary
with col[0]:
    st.markdown(f'### Cluster Profile for Region: {map_metric}')

    factored_columns = [
        'Total Household Income', 'Total Food Expenditure', 
        'Transportation Expenditure', 'Number of Personal Computer', 
        'Communication Expenditure', 'Miscellaneous Goods and Services Expenditure', 
        'Clothing, Footwear and Other Wear Expenditure', 'Number of Airconditioner'
    ]

    wealth_categories = ['Low Wealth Score', 'Moderate Wealth Score', 'High Wealth Score']


    # Create a dictionary to store the average values for each cluster
    cluster_averages = {}# Loop through each cluster to calculate the average for 'Total Household Income'
    # Create an empty dictionary to store average values for each wealth category
    wealth_averages = {}

    # Loop through each wealth category to calculate the average for each indicator
    for wealth_category in wealth_categories:
        # Filter the data for the current wealth category (where the wealth category score is 1)
        cluster_data = df[df[wealth_category] == 1]
        
        # Calculate the average for the socioeconomic indicators (factored_columns)
        average_values = cluster_data[factored_columns].mean()
        
        # Store the result in the dictionary with the wealth category as key
        wealth_averages[wealth_category] = average_values

    # Convert the dictionary into a DataFrame for display
    wealth_averages_df = pd.DataFrame(wealth_averages)

    # Reset the index so that the factored columns are rows
    wealth_averages_df.reset_index(inplace=True)

    # Rename the columns to reflect the correct names
    wealth_averages_df.columns = ['Indicator', 'Low Wealth', 'Moderate Wealth', 'High Wealth']

    # Display the DataFrame as a table
    st.table(wealth_averages_df)
    
    ## Display Cluster Distribution
    
    # Filter the data by the selected region
    region_data = df[df['Standardized Region Name'] == map_metric]

    # Count the number of regions in each cluster
    cluster_counts = region_data['Clusters'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Count']

    # Display the cluster counts in a table
    st.markdown(f"### Cluster Distribution for Region: {map_metric}")

    st.table(cluster_counts)
with col[1]: 

    choropleth_fig = visualization.socioeconomic_choropleth(
        df=df,
        geo_data=geo_data,
        selected_cluster=selected_cluster,
        selected_theme=selected_color_theme
    )
    st.plotly_chart(choropleth_fig, use_container_width=True)
with col[2]:
    # Filter the data by the selected region
    region_data = df[df['Standardized Region Name'] == map_metric]

    # Count the number of regions in each cluster
    cluster_counts = region_data['Clusters'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Count']


    # Plot the cluster distribution using Altair
    cluster_hist = alt.Chart(cluster_counts).mark_bar().encode(
        y=alt.Y('Cluster:N', title='Cluster'),
        x=alt.X('Count:Q', title='Number of Families/Regions'),
        color=alt.Color('Cluster:N', scale=alt.Scale(scheme=selected_color_theme), legend=alt.Legend(orient='bottom'))
    ).properties(
        height=500,
        width=900,
        title=f'Cluster Distribution in {map_metric}'
    )
    
    st.altair_chart(cluster_hist, use_container_width=True)

    with st.expander('About', expanded=True):
        st.write('''
        - 🔍 **Cluster Segmentation**: Divides regions into distinct clusters based on socioeconomic factors
        - 📊 **Cluster Distribution**: Visualizes the number of regions or families in each cluster
        - 🌍 **Wealth Score Mapping**: Displays how wealth scores (Low, Moderate, High) are distributed across regions in the Philippines using a choropleth map.
        - 📋 **Cluster Profiles**: Provides detailed profiles for each cluster, showcasing key socioeconomic factors, including income, expenditures, and household characteristics that define each cluster's unique profile.
         ''')


