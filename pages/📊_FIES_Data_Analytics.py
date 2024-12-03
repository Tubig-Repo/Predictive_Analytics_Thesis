import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(".."))

import data_loader
import visualization



st.set_page_config(layout="wide")
st.title("FIES Data Analytics")


# Filter Options 
st.subheader("Filter Options")
col1, col2, col3 = st.columns(3)

# Major Island
with col1:
    major_island = st.radio("Major Island", options=["All", "Luzon", "Visayas", "Mindanao"])
# Type of Household  
with col2:
    type_of_household = st.radio("Type of Household", options=["All", "Single Family", "Two or More Nonrelated Persons/Members", "Extended Family"])
# Household Head Job or Business Indicator
with col3:
    household_head_indicator = st.radio("Household Head Job or Business", options=["All", "No Job/Business", "With Job/Business"])
    
get_avg_values = data_loader.load_average_values(major_island, type_of_household=type_of_household, household_head_indicator=household_head_indicator)
# FIES Average Values
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Household Head Age", round(get_avg_values.avg_age, 2))
col2.metric("Avg. Household Income", f"₱{round(get_avg_values.avg_household_inc, 2):,.0f}")
col3.metric("Avg. Number of Family Members Employed", round(get_avg_values.avg_working_mem, 2))
st.subheader('FIES Expenditure Breakdown')
expenditure = data_loader.load_expenditure_data(major_island, type_of_household=type_of_household,household_head_indicator=household_head_indicator)

# Handle no expenditure data
if expenditure is not None:
    fig1 = visualization.plot_expenditure_breakdown(expenditure)
    st.plotly_chart(fig1)
else:
    st.warning("No expenditure data available for the selected filters.")

# Mapbox and Pie Chart, Bar Chart (Top Regions)

st.subheader("Source of Income and Top Regions")
col1, col2 = st.columns(2)


# Map Plotting
with col1: 
    ph_regions_geojson = data_loader.load_geodata()
    total_inc = data_loader.get_totalinc()
    fig2 = visualization.plot_philippine_map(total_inc,ph_regions_geojson)
    st.plotly_chart(fig2)

with col2: 
    # Pie Chart
    fies_data = data_loader.load_original_fies_data().compute()
    fig3 = visualization.fies_piechart(fies_data)
    st.plotly_chart(fig3 , use_container_width=True)
    # Bar Chart
    fig4 = visualization.fies_barchart(fies_data)
    st.plotly_chart(fig4, use_container_width=True)

