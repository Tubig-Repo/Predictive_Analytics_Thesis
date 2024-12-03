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

# Page configuration
st.set_page_config(
    page_title="Regional Expenditure Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")
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
            'Actual_Housing_Water_Expenditure', 
            'Business_Potential_Score'
        ],
        'Medical Care Expenditure': [
            'Actual_Medical_Care_Expenditure', 
            'Business_Potential_Score'
        ]
    }
    return metric_mappings.get(dataset, ['Business_Potential_Score'])

# Sidebar for dataset selection
with st.sidebar:
    dataset_options = [
        ('🥩', 'Meat Processing/Distribution'),
        ('🍽️', 'Restaurant Business'),
        ('🏠', 'Home Improvement/Construction'),
        ('🏥', 'Medical Care Expenditure'),
    ]

    # Unpack icons and names
    icons = [icon for icon, name in dataset_options]
    names = [name for icon, name in dataset_options]

    selected_dataset_index = st.selectbox(
        'Select Business/Expenditure Dataset', 
        range(len(names)),
        format_func=lambda x: f"{icons[x]} {names[x]}"
    )
    
    # Get selected dataset and icon
    selected_dataset = names[selected_dataset_index]
    selected_icon = icons[selected_dataset_index]

    # Dynamic title with icon
    st.title(f'{selected_icon} {selected_dataset} Dashboard')
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    
    # In sidebar section
    map_metric = st.selectbox(
        'Select Map Metric',
        get_map_metric_options(selected_dataset)
    )
    
# Data loading function with if-else
def load_dataset(dataset):
    try:
        if dataset == 'Meat Processing/Distribution':
            return pd.read_csv('ModelOutput/meat-scores-2018.csv')
        elif dataset == 'Restaurant Business':
            return pd.read_csv('ModelOutput/restaurant-scores-2018.csv')
        elif dataset == 'Home Improvement/Construction':
             return pd.read_csv('ModelOutput/construction-scores-2018.csv')
        elif dataset == 'Medical Care Expenditure':
            return pd.read_csv('ModelOutput/healthcare-scores-2018.csv')
        else:
            st.error("Dataset not found")
            return None
    except FileNotFoundError:
        st.error(f"File for {dataset} not found")
        return None

df = load_dataset(selected_dataset)

#######################
# Dashboard Main Panel
col = st.columns((1.5, 2, 1))


def get_expenditure_columns(dataset):
    """
    Map datasets to their specific expenditure column names
    """
    expenditure_mappings = {
        'Meat Processing/Distribution': {
            'actual_column': 'Actual_Meat_Expenditure',
            'predicted_column': 'Predicted_Meat_Expenditure',
            'label': 'Meat Expenditure'
        },
        'Restaurant Business': {
            'actual_column': 'Actual_Restaurant_Expenditure',
            'predicted_column': 'Predicted_Restaurant_Hotel_Expenditure',
            'label': 'Restaurant Business Expenditure'
        },
        'Home Improvement/Construction': {
            'actual_column': 'Actual_Housing_Water_Expenditure',
            'predicted_column': 'Actual_Housing_Water_Expenditure',
            'label': 'Construction Expenditure'
        },
        'Medical Care Expenditure': {
            'actual_column': 'Actual_Medical_Care_Expenditure',
            'predicted_column': 'Predicted_Medical_Care_Expenditure',
            'label': 'Medical Expenditure'
        }
    }
    return expenditure_mappings.get(dataset, {})

def create_expenditure_analysis(col, df, dataset, selected_color_theme):
    """
    Create expenditure analysis column for different datasets
    """
    # Get specific column names
    exp_columns = get_expenditure_columns(dataset)
    
    if not exp_columns:
        st.error("Unable to find expenditure columns")
        return
    
    with col[0]:
        st.markdown(f'#### {exp_columns["label"]} Analysis')
        
        # Highest and lowest expenditure regions
        max_exp_region = df.loc[df[exp_columns['actual_column']].idxmax()]
        min_exp_region = df.loc[df[exp_columns['actual_column']].idxmin()]
        
        st.metric(
            label="Highest Expenditure Region",
            value=f"₱{max_exp_region[exp_columns['actual_column']]:,.2f}",
            delta=f"{max_exp_region['Region']}"
        )
        
        st.metric(
            label="Lowest Expenditure Region",
            value=f"₱{min_exp_region[exp_columns['actual_column']]:,.2f}",
            delta=f"{min_exp_region['Region']}",
            delta_color="inverse"
        )
        
        st.markdown('#### Prediction Accuracy')
        
        # Calculate prediction accuracy
        df['Prediction_Accuracy'] = (1 - abs(
            df[exp_columns['predicted_column']] - 
            df[exp_columns['actual_column']]
        ) / df[exp_columns['actual_column']]) * 100
        
        accuracy_chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y('Region:N', sort='-x'),
            x=alt.X('Prediction_Accuracy:Q', title='Accuracy (%)'),
            color=alt.Color('Prediction_Accuracy:Q', scale=alt.Scale(scheme=selected_color_theme))
        ).properties(height=400)
        
        st.altair_chart(accuracy_chart, use_container_width=True)
        
def get_choropleth_metric(dataset, map_metric):
    """
    Validate and potentially modify the map metric based on dataset
    """
    metric_mappings = {
        'Meat Processing/Distribution': {
            'Actual_Meat_Expenditure': 'Meat Expenditure',
            'Business_Potential_Score': 'Business Potential'
        },
        'Restaurant Business': {
            'Actual_Restaurant_Expenditure': 'Restaurant Expenditure',
            'Business_Potential_Score': 'Business Potential'
        },
        'Medical Care Expenditure': {
            'Actual_Medical_Care_Expenditure': 'Medical Expenditure',
            'Business_Potential_Score': 'Business Potential'
        },
        'Home Improvement/Construction': {
            'Actual_Housing_Water_Expenditure': 'Housing and Water Expenditure',
            'Business_Potential_Score': 'Business Potential'
        }
    }
    
    return map_metric
def create_third_column_and_charts(col, df, selected_dataset, selected_color_theme):
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
        
        # Get expenditure columns for the selected dataset
        exp_columns = get_expenditure_columns(selected_dataset)
        
        with st.expander('About', expanded=True):
            st.write(f'''
            - 💰 **{exp_columns['label']} Analysis**: Shows regions with highest and lowest {exp_columns['label'].lower()}
            - 📊 **Prediction Accuracy**: Displays how close the predicted values are to actual values
            - 💼 **Business Potential**: Ranks regions based on their business potential score
            - 📈 **Regional Overview**: Compares predicted vs actual {exp_columns['label'].lower()} and shows business potential
            ''')
        
# In main dashboard code
col = st.columns((1.8, 2.5, 1.5))
create_expenditure_analysis(col, df, selected_dataset, selected_color_theme)
with col[1]:
    st.markdown('#### Regional Overview')
    
    try:
        with open('GeoJSON/PHRegions.json', 'r') as f:
            geo_data = json.load(f)
        
        # Validate and potentially modify map metric
        validated_map_metric = get_choropleth_metric(selected_dataset, map_metric)
        
        # Create and display choropleth map
        choropleth_fig = visualization.create_choropleth(
            df, 
            validated_map_metric, 
            geo_data, 
            selected_theme=selected_color_theme
        )
        st.plotly_chart(choropleth_fig, use_container_width=True)
    
    except FileNotFoundError:
        st.error("Please ensure you have the Philippines regions GeoJSON file in your directory")
    except Exception as e:
        st.error(f"An error occurred while creating the choropleth map: {e}")
create_third_column_and_charts(col, df, selected_dataset, selected_color_theme)
# Create a comparison chart between predicted and actual expenditure
# Melt the data for comparison
exp_columns = get_expenditure_columns(selected_dataset)

comparison_df = pd.melt(df, 
                        id_vars=['Region'], 
                        value_vars=[exp_columns['predicted_column'], exp_columns['actual_column']],
                        var_name='Type', 
                        value_name='Expenditure')

# Chart for Predicted Expenditure
predicted_chart = alt.Chart(comparison_df[comparison_df['Type'] == exp_columns['predicted_column']]).mark_bar().encode(
    x=alt.X('Region:N', title=None),
    y=alt.Y('Expenditure:Q', title=f'{exp_columns["label"]} (₱)'),
    color=alt.Color('Type:N', scale=alt.Scale(scheme=selected_color_theme))
).properties(width=300, height=400)

# Chart for Actual Expenditure
actual_chart = alt.Chart(comparison_df[comparison_df['Type'] == exp_columns['actual_column']]).mark_bar().encode(
    x=alt.X('Region:N', title=None),
    y=alt.Y('Expenditure:Q', title=f'{exp_columns["label"]} (₱)'),
    color=alt.Color('Type:N', scale=alt.Scale(scheme=selected_color_theme))
).properties(width=300, height=400)

# Display both charts
st.altair_chart(predicted_chart, use_container_width=True)
st.altair_chart(actual_chart, use_container_width=True)