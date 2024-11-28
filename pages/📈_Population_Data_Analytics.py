import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
# Acccessing outside directory
import sys
import os
sys.path.append(os.path.abspath(".."))

import data_loader
import visualization



st.set_page_config(layout="wide")

###  Start of Mapping 

# Title for the Visualization
st.title("Population Density in the Philippines")
# Choose base on island
option_island = st.selectbox(
      "Select By Island",
      ("All","Luzon" , "Visayas", "Mindanao")
)
# Choose on wether to choose from Province/District, Regions or Municipalities
# option_level = st.selectbox(
#         "Select Base on Region or Province",
#         ("Region", "Province/Districts", "Municipality")
# )
# Choose base on cencsus year 
option_census_year = st.selectbox(
    "Select Population Census",
    ("Population Census 1990" , "Population Census 2000" , "Population Census 2010", "Population Census 2015", "Population Census 2020")
)
# Load Data
option_level = "Region"
geo_data = data_loader.load_geojson(option_level=option_level)

population_data = data_loader.load_population(option_census_year, option_level=option_level, option_island=option_island)
# Create the choropleth map
fig = visualization.plot_map(data=population_data,geo_data=geo_data)

st.plotly_chart(fig)


#### End of Mapping Population

####  Start of Bar Charts 

st.title("GRDP by Region")

grdp_data_length = data_loader.load_GRDP_length()

option_grdp_year = st.selectbox(
    "Select GRDP Year",
    grdp_data_length
)

# Get Data  
grdp_data = data_loader.load_grdp(selected_year=option_grdp_year) 

# Visualize data

fig1 = visualization.plot_bar(grdp_data, option_grdp_year)
# Display the map in Streamlit
 
st.plotly_chart(fig1, use_container_width=True)
####  End of Bar Charts 


####  Start of Line Plots for GRDP

st.title("GRDP by Region Line Plot")

grpd_plain = data_loader.load_grdp_plain()

fig2 = visualization.plot_line_grdp(grpd_plain)
fig3 = visualization.plot_line_growth(grpd_plain)
st.plotly_chart(fig2)
st.plotly_chart(fig3)

####  End of Line Plots for GRDP


