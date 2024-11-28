import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import altair as alt

# Acccessing outside directory
import sys
import os
sys.path.append(os.path.abspath(".."))

import data_loader
import visualization

#######################
# Page configuration
st.set_page_config(
    page_title="Regional Expenditure Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("Business Score Prediction by Region in the Philippines")



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

df = pd.read_csv('ModelOutput/meat_scores.csv')

#######################
# Sidebar
def get_map_metric_options(dataset):
    """
    Dynamically generate map metric options based on dataset
    """
    metric_mappings = {
        'Meat Processing/Distribution': [
            'Actual_Meat_Expenditure', 
            'Business_Potential_Score'
        ],
        'Restaurant Business': [
            'Actual_Restaurant_Expenditure', 
            'Business_Potential_Score'
        ],
        'Home Improvement/Construction': [
            'Actual_Construction_Expenditure', 
            'Business_Potential_Score'
        ],
        'Bar/Clubs Business': [
            'Actual_Bar_Expenditure', 
            'Business_Potential_Score'
        ],
        'Medical Care Expenditure': [
            'Actual_Medical_Expenditure', 
            'Business_Potential_Score'
        ]
    }
    return metric_mappings.get(dataset, ['Business_Potential_Score'])

with st.sidebar:
    type_expenditure = st.selectbox('Select Type of Family Expenditure', ())
    st.title('🥩 Regional Meat Expenditure Dashboard')
    
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    # Select Specific Business Score Prediction 
    
    # Add mapbox selection
    map_metric = st.selectbox(
        'Select Map Metric',
        ['Actual_Meat_Expenditure', 'Business_Potential_Score']
    )
    
#######################
# Dashboard Main Panel
col = st.columns((1.5, 2, 1))

with col[0]:
    st.markdown('#### Expenditure Analysis')
    
    # Highest and lowest expenditure regions
    max_exp_region = df.loc[df['Actual_Meat_Expenditure'].idxmax()]
    min_exp_region = df.loc[df['Actual_Meat_Expenditure'].idxmin()]
    
    st.metric(
        label="Highest Expenditure Region",
        value=f"₱{max_exp_region['Actual_Meat_Expenditure']:,.2f}",
        delta=f"{max_exp_region['Region']}"
    )
    
    st.metric(
        label="Lowest Expenditure Region",
        value=f"₱{min_exp_region['Actual_Meat_Expenditure']:,.2f}",
        delta=f"{min_exp_region['Region']}",
        delta_color="inverse"
    )
    
    st.markdown('#### Prediction Accuracy')
    
    # Calculate prediction accuracy
    df['Prediction_Accuracy'] = (1 - abs(df['Predicted_Meat_Expenditure'] - df['Actual_Meat_Expenditure']) / df['Actual_Meat_Expenditure']) * 100
    
    accuracy_chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y('Region:N', sort='-x'),
        x=alt.X('Prediction_Accuracy:Q', title='Accuracy (%)'),
        color=alt.Color('Prediction_Accuracy:Q', scale=alt.Scale(scheme=selected_color_theme))
    ).properties(height=400)
    
    st.altair_chart(accuracy_chart, use_container_width=True)

with col[1]:
    st.markdown('#### Regional Overview')
    
    try:
        with open('GeoJSON/PHRegions.json', 'r') as f:
            geo_data = json.load(f)
            
        # Create and display choropleth map
        choropleth_fig = visualization.create_choropleth(df, map_metric, geo_data, selected_theme=selected_color_theme)
        st.plotly_chart(choropleth_fig, use_container_width=True)
    except FileNotFoundError:
        st.error("Please ensure you have the Philippines regions GeoJSON file in your directory")
with col[2]:
    st.markdown('#### Business Potential Ranking')

    # Create a sorted dataframe by Business Potential Score
    df_sorted = df.sort_values('Business_Potential_Score', ascending=False)

    st.dataframe(
        df_sorted[['Region', 'Business_Potential_Score']],
        hide_index=True,
        column_config={
            "Region": st.column_config.TextColumn("Region"),
            "Business_Potential_Score": st.column_config.ProgressColumn(
                "Business Potential",
                format="%.1f",
                min_value=0,
                max_value=100,
            )
        }
    )
    
    with st.expander('About', expanded=True):
        st.write('''
        - 🥩 **Expenditure Analysis**: Shows regions with highest and lowest meat expenditure
        - 📊 **Prediction Accuracy**: Displays how close the predicted values are to actual values
        - 💰 **Business Potential**: Ranks regions based on their business potential score
        - 📈 **Regional Overview**: Compares predicted vs actual expenditure and shows relationship with household income
        ''')
# Create a comparison chart between predicted and actual expenditure
# Melt the data for comparison
comparison_df = pd.melt(df, 
                        id_vars=['Region'], 
                        value_vars=['Predicted_Meat_Expenditure', 'Actual_Meat_Expenditure'],
                        var_name='Type', 
                        value_name='Expenditure')

# Chart for Predicted Meat Expenditure
predicted_chart = alt.Chart(comparison_df[comparison_df['Type'] == 'Predicted_Meat_Expenditure']).mark_bar().encode(
    x=alt.X('Region:N', title=None),
    y=alt.Y('Expenditure:Q', title='Meat Expenditure (₱)'),
    color=alt.Color('Type:N', scale=alt.Scale(scheme=selected_color_theme))
).properties(width=300, height=400)

# Chart for Actual Meat Expenditure
actual_chart = alt.Chart(comparison_df[comparison_df['Type'] == 'Actual_Meat_Expenditure']).mark_bar().encode(
    x=alt.X('Region:N', title=None),
    y=alt.Y('Expenditure:Q', title='Meat Expenditure (₱)'),
    color=alt.Color('Type:N', scale=alt.Scale(scheme=selected_color_theme))
).properties(width=300, height=400)
# Display both charts separately
st.altair_chart(predicted_chart, use_container_width=True)
st.altair_chart(actual_chart, use_container_width=True)



