import json
import streamlit as st
import pandas as pd
import re
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
        if option_island == 'Luzon': 
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

# Load Average Values
def load_average_values():
    
    df = load_FIES_Data()
    
    avg_household_age = df['Household Head Age'].mean()
    avg_household_inc = df['Total Household Income'].mean()
    avg_household_working = df['Total number of family members employed'].mean()
    
    return SimpleNamespace(
        avg_age=avg_household_age,
        avg_household_inc=avg_household_inc,
        avg_working_mem=avg_household_working
    )
    
# FIES Breakdown 

def load_expenditure_data(): 
    
    df = pd.read_csv('FIES/Family Income and Expenditure.csv')
    
    # expenditure = {
    #     'Total Food': df['Total Food Expenditure'].sum(),
    #     'Housing and water': df['Housing and water Expenditure'].sum(),
    #     'Total Rice': df['Total Rice Expenditure'].sum(),
    #     'Bread and Cereals': df['Bread and Cereals Expenditure'].sum(),
    #     'Restaurant and hotels': df['Restaurant and hotels Expenditure'].sum(),
    #     'Crop Farming and Gardening': df['Crop Farming and Gardening expenses'].sum(),
    #     'Miscellaneous Goods and Services': df['Miscellaneous Goods and Services Expenditure'].sum(),
    #     'Meat': df['Meat Expenditure'].sum(),
    #     'Total Fish and marine products': df['Total Fish and  marine products Expenditure'].sum(),
    #     'Transportation': df['Transportation Expenditure'].sum(),
    #     'Education': df['Education Expenditure'].sum(),
    #     'Medical Care': df['Medical Care Expenditure'].sum(),
    #     'Fruit Expenditure': df['Fruit Expenditure'].sum(),
    #     'Vegetables Expenditure': df['Vegetables Expenditure'].sum(),
    #     'Tobacco Expenditure': df['Tobacco Expenditure'].sum(),
    #     'Alcoholic Beverages Expenditure': df['Alcoholic Beverages Expenditure'].sum(),
    #     'Total Special Occasion Expenditure': df['Special Occasions Expenditure'].sum(),
    #     'Total Communication Expenditure': df['Communication Expenditure'].sum()
    #     }
    
    df_expenditure = df[['Total Food Expenditure','Total Rice Expenditure', 'Meat Expenditure' , 'Bread and Cereals Expenditure', 'Fruit Expenditure','Vegetables Expenditure',  'Restaurant and hotels Expenditure','Alcoholic Beverages Expenditure', 'Tobacco Expenditure',  'Clothing, Footwear and Other Wear Expenditure',  'Housing and water Expenditure',   'Medical Care Expenditure', 'Communication Expenditure', 'Education Expenditure',  'Miscellaneous Goods and Services Expenditure', 'Crop Farming and Gardening expenses', 'Total Fish and  marine products Expenditure','Transportation Expenditure', 'Special Occasions Expenditure']]

    # Melt the data: converting each expenditure category to a single row
    df_melted = df_expenditure.melt(var_name='Expenditure Category', value_name='Amount')

    return df_melted

