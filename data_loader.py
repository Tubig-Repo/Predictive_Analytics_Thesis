import json
import streamlit as st
import pandas as pd
import re
import dask.dataframe as dd
from types import SimpleNamespace


def load_geodata():
    with open('GeoJSON/PHRegions.json', 'r') as f:
        geo_data = json.load(f)
        return geo_data
# Will handle the philippines geographic data structure
def load_geojson(option_level):
        if option_level == 'Region':
            # Load the GeoJSON file
            with open('GeoJSON/PHRegions.json', 'r') as f:
                geo_data = json.load(f)
            return geo_data
        elif option_level == 'Province/Districts':
            with open('GeoJSON/PH_MuniDist_Simplified.json', 'r') as f:
                geo_data = json.load(f)
            return geo_data
        elif option_level == 'Municipality':
            return 

def load_population(selected_year , option_level , option_island): 
    if option_level == 'Region':
        if option_island == 'All':
            # Read population data for all islands
            luzon_population = pd.read_csv('Population Dataset/Luzon-Region-Population_Cleaned.csv')
            visayas_population = pd.read_csv('Population Dataset/Visayas-Region-Population.csv')
            mindanao_population = pd.read_csv('Population Dataset/Mindanao-Region-Population.csv')
            
            # Clean and preprocess each dataframe
            # Luzon cleaning
            luzon_df = pd.DataFrame(luzon_population)
            luzon_df.loc[luzon_df['Name'] == 'MIMAROPA', 'Name'] = 'Mimaropa'
            luzon_df[selected_year] = luzon_df[selected_year].str.replace(',', '').astype(float)
            
            # Visayas cleaning
            visayas_population[selected_year] = visayas_population[selected_year].astype(str).str.replace(',', '').astype(float)
            
            # Mindanao cleaning (assuming no special cleaning needed)
            mindanao_df = pd.DataFrame(mindanao_population)
            
            # Combine all dataframes
            combined_df = pd.concat([luzon_df, visayas_population, mindanao_df], ignore_index=True)
            
            # Prepare the return data
            data = {
                'location': combined_df['Name'].tolist(), 
                "values": combined_df[selected_year].tolist()
            }
            return data 
        elif option_island == 'Luzon': 
            population = pd.read_csv('Population Dataset/Luzon-Region-Population_Cleaned.csv')
            df = pd.DataFrame(population)
            # change location name of MIMAROPA to Mimaropa only 
            df.loc[df['Name'] == 'MIMAROPA', 'Name'] = 'Mimaropa'
            ''' 
            Clean Data
            - Change  Selected Year or Population census from FLOAT to Object
            '''
            df[selected_year] = df[selected_year].str.replace(',', '').astype(float)
            # initializing the requested year of population and name of region 
            data = {'location': df['Name'].tolist(), "values": df[selected_year].tolist()}
            return data 
        elif option_island == 'Visayas':    
            # Read Data
            population = pd.read_csv('Population Dataset/Visayas-Region-Population.csv')
            # 
            population[selected_year] = population[selected_year].str.replace(',', '').astype(int)
            # 
            data = {'location': population['Name'].tolist(), "values": population[selected_year].tolist()}
            return data
        elif option_island == 'Mindanao':
            # Population Load
            population = pd.read_csv('Population Dataset/Mindanao-Region-Population.csv')
            df = pd.DataFrame(population)
            # Load Year and Turn in
            # Initialize the data needed
            data = {'location': df['Name'].tolist(), "values": df[selected_year].tolist()}
            # Return data
            return data
    elif option_level == 'Province/Districts':
        if option_island == 'Luzon':
            provinces = pd.read_csv('Population Dataset/Luzon-Province-Population_Cleaned.csv')
            # Convert Selected Year to Float
            provinces[selected_year] = provinces[selected_year].str.replace(',', '').astype(float)
            # Remove parentheses on names 
            provinces['Name'] = provinces['Name'].apply(lambda x: re.sub(r'\s*\(.*?\)\s*', '', x).strip())
            data = {'location': provinces['Name'].tolist(), "values": provinces[selected_year].tolist()}
            return data
        if option_island == 'Mindanao':
            
            return
        
        
def load_luzon_province(selected_year): 
    # Get the data population
    provinces = pd.read_csv('Population Dataset/Luzon-Province-Population_Cleaned.csv')
    
    # Convert Selected Year to Float
    provinces[selected_year] = provinces[selected_year].str.replace(',', '').astype(float)
    # Remove parentheses on names 
    provinces['Name'] = provinces['Name'].apply(lambda x: re.sub(r'\s*\(.*?\)\s*', '', x).strip())
    
    return provinces
# def load_luzon_province(selected_province): 
#     # Acuqire the data
#     provinces = pd.read_csv('Population Dataset/Luzon-Province-Population_Cleaned.csv')
#     # Instantiate the Province Column and current province
#     df['Province'] = pd.NA
#     # Current province will be the value of the province in the iteration
#     current_province = None
#     for index,row  in df.iterrows(): 
#         if row['Status'] == 'Province': 
#             current_province = row['Name']
#         df.at[index, 'Province'] = current_province
#     df = pd.DataFrame(provinces)
#     return df

def load_grdp_plain(): 
    
    grdp = pd.read_csv('GRDP/GRDP-2000.csv')

    grdp.rename(columns={"Unnamed: 0": "Region Name"}, inplace=True)

    return grdp


def load_grdp(selected_year): 
    
    df = load_grdp_plain()

    data = {'location': df['Region Name'].tolist(), "values": df[selected_year].tolist()}
    
    return data

    
def load_GRDP_length():
    
    data = load_grdp_plain()
    
    return data.columns.drop('Region Name').tolist()


# Fies Function 

def load_FIES_Data(): 
    df = pd.read_csv('FIES/Final-Merge.csv')
    
    return df

def load_original_fies_data(): 
    
    df = dd.read_csv('FIES/FIES-breakdown-2018.csv')
    
    region_name_mapping = {
        "ARMM": "Autonomous Region in Muslim Mindanao",
        "Bicol Region": "Bicol",
        "CALABARZON": "Calabarzon",
        "Cagayan Valley": "Cagayan Valley",
        "CARAGA": "Caraga",
        "Central Luzon": "Central Luzon",
        "Central Visayas": "Central Visayas",
        "CAR": "Cordillera Administrative Region",
        "Davao Region": "Davao",
        "Eastern Visayas": "Eastern Visayas",
        "Ilocos Region": "Ilocos",
        "MIMAROPA": "Mimaropa",
        "NCR": "National Capital Region",
        "Northern Mindanao": "Northern Mindanao",
        "SOCCSKSARGEN": "Soccsksargen",
        "Western Visayas": "Western Visayas",
        "Zamboanga Peninsula": "Zamboanga Peninsula"
    }
    # Rename Total Income to Total Household Income 
    df = df.rename(columns={'Total Income': 'Total Household Income'})
    # Apply the mapping to the Region column
    df['Region Name'] = df['Region Name'].replace(region_name_mapping)


    return df
# def chosen_island(data , island):
#     if island == "Luzon":
#         luzon_df = data[data['Region Name'].isin([
#         'Ilocos', 
#         'Cagayan Valley', 
#         'Central Luzon', 
#         'Calabarzon', 
#         'Bicol', 
#         'National Capital Region', 
#         'Cordillera Administrative Region', 
#         'Mimaropa'
#         ])]
#         return luzon_df
#     elif island == "Visayas":
#         visayas_df = data[data['Region Name'].isin([
#             'Western Visayas', 
#             'Central Visayas', 
#             'Eastern Visayas'
#         ])]
#         return visayas_df

#     elif island == "Mindanao":
#         mindanao_df = data[data['Region Name'].isin([
#             'Zamboanga Peninsula', 
#             'Northern Mindanao', 
#             'Davao', 
#             'Soccsksargen', 
#             'Caraga', 
#             'Autonomous Region in Muslim Mindanao'
#         ])]
#         return mindanao_df
#     else:  # "All"
#         return data

def filter_data(data, island='All', household_type='All', household_head_job='All'):
    """
    Filter the data based on the provided parameters.
    
    Parameters:
    data (pandas.DataFrame): The original DataFrame.
    island (str, optional): The major island to filter for. Can be "Luzon", "Visayas", "Mindanao", or None for all islands.
    household_type (str, optional): The type of household to filter for. Can be "Single Family", "Two or More Unrelated Persons/Members", "Extended Family", or None for all types.
    tenure_status (str, optional): The tenure status to filter for. Can be any value from the "Tenure Status" column, or None for all statuses.
    building_type (str, optional): The type of building/house to filter for. Can be any value from the "Type of Building/House" column, or None for all types.
    household_head_job (str, optional): The job/business indicator of the household head to filter for. Can be "With Job/Business" or "No Job/Business", or None for all.
    
    Return,household_head_indicators:
    pandas.DataFrame: The filtered DataFrame.
    """
    # Filter by island
    if island != "All":
        if island == "Luzon":
            data = data[data['Region Name'].isin([
                'Ilocos', 'Cagayan Valley', 'Central Luzon', 'Calabarzon', 'Bicol',
                'National Capital Region', 'Cordillera Administrative Region', 'Mimaropa'
            ])]
        elif island == "Visayas":
            data = data[data['Region Name'].isin(['Western Visayas', 'Central Visayas', 'Eastern Visayas'])]
        elif island == "Mindanao":
            data = data[data['Region Name'].isin([
                'Zamboanga Peninsula', 'Northern Mindanao', 'Davao', 'Soccsksargen',
                'Caraga', 'Autonomous Region in Muslim Mindanao'
            ])]

    # Filter by household type
    if household_type != "All":
        data = data[data['Type of Household'] == household_type]

    # Filter by household head job/business
    if household_head_job != "All":
        data = data[data['Household Head Job or Business Indicator'] == household_head_job]
     # Check if any data remains after filtering
    if len(data) == 0:
        # Return a DataFrame with the same columns but no rows
        return data.head(0)
    return data
# Load Average Values
def load_average_values(island,type_of_household,household_head_indicator):
    
    df = load_original_fies_data()
    filtered_data = filter_data(df, island=island, household_type=type_of_household,household_head_job=household_head_indicator)
    avg_household_age = filtered_data['Household Head Age'].mean().compute()
    avg_household_inc = filtered_data['Total Household Income'].mean().compute()
    avg_household_working = filtered_data['Total number of family members employed for pay'].mean().compute()
    
    return SimpleNamespace(
        avg_age=avg_household_age,
        avg_household_inc=avg_household_inc,
        avg_working_mem=avg_household_working
    )

# FIES Breakdown 
def load_expenditure_data(island, type_of_household,household_head_indicator): 
    
    df = load_original_fies_data()
    filtered_data = filter_data(df, island=island, household_type=type_of_household,household_head_job=household_head_indicator)

    df_expenditure = filtered_data[['Total Food Expenditure','Total Rice Expenditure', 'Meat Expenditure' , 'Bread and Cereals Expenditure', 'Fruit Expenditure','Vegetables Expenditure',  'Restaurant and hotels Expenditure','Alcoholic Beverages Expenditure', 'Tobacco Expenditure',  'Clothing, Footwear and Other Wear Expenditure',  'Housing and water Expenditure',   'Medical Care Expenditure', 'Communication Expenditure', 'Education Expenditure',  'Miscellaneous Goods and Services Expenditure', 'Crop Farming and Gardening expenses', 'Total Fish and  marine products Expenditure','Transportation Expenditure', 'Special Occasions Expenditure']]

    # Melt the data: converting each expenditure category to a single row
    df_melted = df_expenditure.melt(var_name='Expenditure Category', value_name='Amount').compute()

    return df_melted

def get_totalinc(): 
    df = load_original_fies_data()
    df_summary = df.groupby('Region Name')['Total Household Income'].sum().compute().reset_index()
    return df_summary


def get_ml_output(): 
    
    df = pd.read_csv('ModelOutput/Standardized FIES Dataset.csv')
    
    return df

def testFunction():
    return ""