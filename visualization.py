import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import altair as alt
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
def ml_map(data, geo_data, cluster_select):
    color_column = f"{cluster_select} Score"  # Example: "Low Wealth Score", "Moderate Wealth Score", "High Wealth Score"

    # Moderate Wealth Score
    fig = px.choropleth_mapbox(
        data,
        geojson=geo_data,
        locations="Standardized Region Name",
        featureidkey="properties.name",  # Adjust this to match the property name in the GeoJSON file
        color=color_column,
        color_continuous_scale="Reds",
        range_color=(0, 1),
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 12.8797, "lon": 121.7740},
        opacity=0.6,
        labels={'Moderate Wealth Score': 'Moderate Wealth Score'},
        title=f"{cluster_select} Cluster Visualization",
    )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
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
    

# FIES Visualization

def plot_expenditure_breakdown(data):
    
    # Create the treemap using the melted DataFrame
    fig = px.treemap(data, path=['Expenditure Category'], values='Amount')

    fig.update_traces(textfont=dict(color='black', size=20))
         
    return fig

#  FIES
def plot_philippine_map(data, geojson_data):
    def format_number(num):
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"
        else:
            return f"{num:.2f}"
    data['Formatted Income'] = data['Total Household Income'].apply(format_number)
  
    fig = px.choropleth_mapbox(data,
                              geojson=geojson_data,
                              locations='Region Name',
                              featureidkey="properties.name",
                              color='Total Household Income',
                              color_continuous_scale="Reds",                              
                              mapbox_style="carto-positron",
                              zoom=4.5,
                              center={"lat": 12.8797, "lon": 121.7740},
                              opacity=0.5)
    
    # Update hover template to show the formatted values
    fig.update_traces(hovertemplate="<b>%{location}</b><br>Total Household Income: %{customdata[0]}<extra></extra>")

    # Pass the formatted column as customdata to the hovertemplate
    fig.update_traces(customdata=data[['Formatted Income']])
    
    fig.update_layout(height=700, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def fies_barchart(data):
    
    fig = px.bar(
        data,
        x='Total Household Income',
        y='Region Name',
        orientation='h',
        title='Top Regions',
        color_discrete_sequence=['#FF8080']    
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        height=400,  # Adjust the height as needed
        xaxis_title="Total Household Income ₱",
        yaxis_title="",
        yaxis={'categoryorder': 'total ascending'}

    )
    
    return fig

def fies_piechart(data):
    income_sources = data['Major Grouping of Main Source of Income'].value_counts().to_dict()

    fig = px.pie(
        values=list(income_sources.values()),
        names=list(income_sources.keys()),
        title="Source of Income",
        color_discrete_sequence=['#FFD0D0', '#FFC0C0', '#FFAFAF']
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        showlegend=False,
        margin=dict(t=40, b=0, l=0, r=0),
        height=300  # Adjust the height as needed
    )
    return fig
# Business Scoring
def create_choropleth(df, color_column, geo_data, selected_theme):
    fig = px.choropleth_mapbox(
        df,
        geojson=geo_data,
        locations="Region",
        featureidkey="properties.name",
        color=color_column,
        color_continuous_scale=selected_theme,
        mapbox_style="carto-positron",
        zoom=4.5,
        center={"lat": 12.8797, "lon": 121.7740},
        opacity=0.6,
        labels={'Actual_Meat_Expenditure': 'Actual Meat Expenditure (₱)',
                'Business_Potential_Score': 'Business Potential Score'},
        title=f"Regional {color_column.replace('_', ' ')}",
    )
    
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},width=460, height=700)
    
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="gray"
    )

    # Layout adjustments
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        width=460, 
        height=700
    )
    
    return fig
# Socioeconomic and Household Mapping
def socioeconomic_choropleth(df, geo_data, selected_cluster, selected_theme,factors): 
    print("Selected Cluster:", selected_cluster)
    print("Available Columns:", list(df.columns))
    
    # Determine the wealth score column based on the selected cluster
    if factors == 'Socioeconomic Status and Wealth':
        score_column = f"{selected_cluster} Score"
    elif factors == 'Household Amenities':
        cluster_mapping = {
            'Average-sized Households': 'Average-sized Score',
            'Small Essential Households': 'Small Essential Score',
            'Large Extended Households': 'Large Extended Score'
        }
        
        score_column = cluster_mapping[selected_cluster]

    
    # Verify the column exists
    if score_column not in df.columns:
        raise ValueError(f"Column '{score_column}' not found in DataFrame. Available columns are: {list(df.columns)}")
    # Create the choropleth map
    fig = px.choropleth_mapbox(
        df,
        geojson=geo_data,
        locations="Standardized Region Name",
        featureidkey="properties.name",  # Matches GeoJSON property for regions
        color=score_column,  # Use the selected wealth score
        color_continuous_scale=selected_theme,
        range_color=(0, 1),  # Assuming wealth scores are normalized between 0 and 1
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 12.8797, "lon": 121.7740},
        opacity=0.6,
        labels={score_column: f"{selected_cluster} Score"},
        title=f"{selected_cluster} Score by Region"
    )

    # Add hover labels with region and wealth score
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="white"
    )

    # Layout adjustments
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        width=460, 
        height=700
    )
    
    return fig