import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# Create the choropleth map
def plot_map(data , geo_data):

    fig = px.choropleth_mapbox(data, 
                            geojson=geo_data, 
                            locations='location', 
                            featureidkey="properties.name",  # Adjust based on your GeoJSON structure
                            color='values', 
                            color_continuous_scale="Viridis",
                            mapbox_style="carto-positron",
                            zoom=5, 
                            center={"lat": 12.8797, "lon": 121.7740},  # Centered on the Philippines
                            opacity=0.5
                            )
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Population",  # Label for the color bar
            titlefont=dict(size=20),  # Title font size
            tickfont=dict(size=16),  # Size of the color bar values
            thickness=30,
            len=1
            
        )
    )

    fig.update_layout( height=600,margin={"r": 0, "t": 0, "l": 0, "b": 0})
    
    return fig

#Create the Bar Chart 
def plot_bar(data, selected_year): 
    
    fig = go.Figure()
    
     # Add a single bar for the selected year
    fig.add_trace(
        go.Bar(
            y=data['location'],
            x=data['values'],
            hovertemplate="%{x}",
            name=selected_year,
            orientation="h",
        )
    )
    
    fig.update_layout(
        title=f"{selected_year} Data by Region",
        xaxis_title="GRDP",
        yaxis_title="Region",
        # margin=dict(l=100, r=100, t=100, b=100),  # Adjust margins to center the plot
        yaxis=dict(
            tickfont=dict(size=18),  # Adjust font size of y-axis labels
            automargin=True,
        ),      
        width=1200,  # Adjust the width of the chart
        height=800  # Adjust the height of the chart
    )

    # Display the chart
    return fig

def plot_line_grdp(data): 
    
    data.rename(columns={"Unnamed: 0": "Region Name"}, inplace=True)
    
    grdp_long = data.melt(id_vars=['Region Name'], var_name='Year', value_name='GRDP')
    
    fig = px.line(grdp_long, x='Year', y='GRDP', color='Region Name',
              title='GRDP by Region Over the Years',
              labels={'Year': 'Year', 'GRDP': 'Gross Regional Domestic Product'},
              markers=True)
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Gross Regional Domestic Product',
        legend_title='Region',
    ) 
    
    return fig  

def plot_line_growth(data):
    
    data.set_index('Region Name', inplace=True)

    # Calculate growth rate for each year
    growth_rate_df = data.pct_change(axis=1) * 100  # Calculate percentage change
    growth_rate_df = growth_rate_df.fillna(0)  # Replace NaN with 0 for the first year

    # Reset index to plot easily
    growth_rate_df.reset_index(inplace=True)

    # Melt the DataFrame for plotting
    melted_df = growth_rate_df.melt(id_vars='Region Name', var_name='Year', value_name='Growth Rate')

    # Plot the growth rates using Plotly
    fig = px.line(melted_df, x='Year', y='Growth Rate', color='Region Name', 
                title='GRDP Growth Rate by Region Over Years',
                labels={'Growth Rate': 'Growth Rate (%)', 'Year': 'Year'})

    # Show the plot
    return fig    
    
    