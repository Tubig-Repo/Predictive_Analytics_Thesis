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


#######################
# Sidebar

def select_year(factor , year):
    # Load the dataset based on the selected year and factor
    if factor == 'Household Amenities':
        if year == "2012":
            df = pd.read_csv('ModelOutput/Household-Size-Basic-Needs-2012.csv')
        elif year == "2015":
            df = pd.read_csv('ModelOutput/Household-Size-Basic-Needs-2015.csv')
        elif year == "2018":
            df = pd.read_csv('ModelOutput/Household-Size-Basic-Needs-2018.csv')
        else:
            st.error("Invalid data year selected.")
            df = None
    elif factor == 'Socioeconomic Status and Wealth':
        if year == "2012":
            df = pd.read_csv('ModelOutput/Socioeconomic-Segmentation-2012.csv')
        elif year == "2015":
            df = pd.read_csv('ModelOutput/Socioeconomic-Segmentation-2015.csv')
        elif year == "2018":
            df = pd.read_csv('ModelOutput/Socioeconomic-Segmentation-2018.csv')
        else:
            st.error("Invalid data year selected.")
            df = None
    else:
        st.error("Invalid factor selected.")
        df = None
    return df
        
        
with st.sidebar:
    factors = st.selectbox('Select Type of Factor', ('Socioeconomic Status and Wealth', 'Household Amenities'))
    data_year = st.selectbox('Select Data Year', ("2012", "2015", "2018"))
    df = select_year(factor=factors , year=data_year)
    st.title('💸 Socioeconomic Segmentation Analysis base on FIES')
    
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
    print(selected_cluster)
    clustered_data = df[df['Clusters'] == selected_cluster]
    
with open('GeoJSON/PHRegions.json', 'r') as f:
        geo_data = json.load(f)
            
#######################
# Dashboard Main Panel
col = st.columns((1.5, 2, 1.5))

# Cluster Profile Summary
with col[0]:
    # Factor 1: Socioeconomic Status and Wealth
    if factors == 'Socioeconomic Status and Wealth': 
        st.markdown(f'### Cluster Profile for Region: {map_metric}')

        factored_columns = [
            'Total Household Income', 'Total Food Expenditure', 
            'Transportation Expenditure', 'Number of Personal Computer', 
            'Communication Expenditure', 'Miscellaneous Goods and Services Expenditure', 
            'Clothing, Footwear and Other Wear Expenditure', 'Number of Airconditioner'
        ]

        cluster_categories = ['Low Wealth', 'Moderate Wealth', 'High Wealth']
        category_column_mapping = {
            'Low Wealth': 'Low Wealth',
            'Moderate Wealth': 'Moderate Wealth',
            'High Wealth': 'High Wealth'
        }
    # Factor 2: Household Amenities and Needs
    elif factors == 'Household Amenities':
        st.markdown(f'### Household Needs & Amenities Cluster Profile: {map_metric}')
        
        # Columns for Household Amenities
        factored_columns = ['Total Number of Family members',
                            'Total Rice Expenditure',
                            'Total number of family members employed',
                            'Bread and Cereals Expenditure',
                            'Members with age 5 - 17 years old']

        # Cluster categories for Household Amenities
        cluster_categories = ['Small Essential Households', 'Average-sized Households', 'Large Extended Households']
        category_column_mapping = {
            'Small Essential Households': 'Small Living Standard',
            'Average-sized Households': 'Average Living Standard',
            'Large Extended Households': 'Premium Living Standard'
        }
    else:
        st.error("Invalid factor selected")
        # Provide default values to prevent errors
        factored_columns = []
        cluster_categories = []
        category_column_mapping = {}
        cluster_key = 'Clusters'
        
    region_data = df[df['Standardized Region Name'] == map_metric]

    # Create a dictionary to store the average values for each cluster
    cluster_averages = {}# Loop through each cluster to calculate the average for 'Total Household Income'

    # Loop through each cluster category to calculate the average for indicators
    for cluster_category in cluster_categories:
        # Filter the data for the current cluster category
        # For amenities, filter by cluster name
        cluster_data = region_data[region_data['Clusters'] == cluster_category]
        # Calculate the average for the indicators
        average_values = cluster_data[factored_columns].mean()

        # Store the result in the dictionary with the category as key
        cluster_averages[cluster_category] = average_values


    # Convert the dictionary into a DataFrame for display
    cluster_averages_df = pd.DataFrame(cluster_averages)

    # Reset the index so that the factored columns are rows
    cluster_averages_df.reset_index(inplace=True)

    # Rename the columns to reflect the correct names
    cluster_column_names = ['Indicator'] + [category_column_mapping[col] for col in cluster_categories]
    cluster_averages_df.columns = cluster_column_names

    # Display the DataFrame as a table
    st.table(cluster_averages_df)
    
    ## Display Cluster Distribution
    
    # Filter the data by the selected region

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
        selected_theme=selected_color_theme,
        factors=factors
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
        if factors == 'Socioeconomic Status and Wealth':
            st.write('''
            - 🔍 **Cluster Segmentation**: Divides regions into distinct clusters based on socioeconomic and wealth-related factors.
            - 📊 **Cluster Distribution**: Visualizes the number of regions or families in each wealth cluster.
            - 🌍 **Wealth Score Mapping**: Displays how wealth scores (Low, Moderate, High) are distributed across regions in the Philippines using a choropleth map.
            - 📋 **Cluster Profiles**: Provides detailed profiles for each wealth cluster, showcasing key socioeconomic factors such as income, expenditures, and possessions.
            ''')
        elif factors == 'Household Amenities':
            st.write('''
            - 🔍 **Cluster Segmentation**: Categorizes regions into clusters based on household amenities and needs.
            - 📊 **Cluster Distribution**: Visualizes the number of regions or families in each household amenity cluster.
            - 🌍 **Amenities Score Mapping**: Displays the distribution of basic, moderate, and advanced household amenities across regions in the Philippines using a choropleth map.
            - 📋 **Cluster Profiles**: Highlights key household characteristics such as family size, employment, and expenditures that define each cluster's profile.
            ''')


