import argparse
import os 
import pandas as pd
from utils import *
from sqlalchemy import create_engine
import numpy as np

def load_data(file_path):
    """ELT: load data from ingestion data """
    # TODO: Load data from CSV file
    # Get gen green energy tag
    green_energy = [
        "B01", "B09", "B10", "B11", "B12",
        "B13", "B15", "B16", "B18", "B19"
    ]
    print(f'Fetching data from {file_path} ...')
    # Initialize an empty DataFrame to hold concatenated data
    concatenated_load_df = pd.DataFrame()
    concatenated_gen_df = pd.DataFrame()
    # Get file name by prefix 
    gen_all_files = list_files_containing_char(file_path, 'gen')
    load_all_files = list_files_containing_char(file_path, 'load')
    # Initialize an empty DataFrame to hold concatenated data
    # Loop through the gen files and concatenate only green energy file
    for file_name in gen_all_files:
        if file_name.endswith('.csv') and any(code in file_name for code in green_energy):
            # Read the csv file
            df = pd.read_csv(os.path.join(file_path, file_name))
            # Split the file name and create new columns
            split_name = file_name.replace('.csv', '').split('_')
            df['Country'] = split_name[1]
            # Concatenate the DataFrame to the main concatenated_df
            concatenated_gen_df = pd.concat([concatenated_gen_df, df])
    # Delete AreaID because already have country code
    concatenated_gen_df = concatenated_gen_df.drop(columns=['AreaID'])
    print(f'Load Generate green energy data from {file_path} completed...')

    # Loop through the load files and concatenate
    for file_name in load_all_files:
        if file_name.endswith('.csv'):
            # Read the csv file
            df = pd.read_csv(os.path.join(file_path, file_name))        
            # Split the file name and create new columns
            split_name = file_name.replace('.csv', '').split('_')
            df['Country'] = split_name[1]     
            # Concatenate the DataFrame to the main concatenated_df
            concatenated_load_df = pd.concat([concatenated_load_df, df])       
    # Delete AreaID because already have country code
    concatenated_load_df = concatenated_load_df.drop(columns=['AreaID'])
    # Save the concatenated DataFrame to a new csv file
    # output_file_path = os.path.join('../data/load_data', 'gen_green_energy.csv')
    # concatenated_load_df.to_csv(output_file_path, index=False)
    # print(f'load data ready in   {output_file_path}')
    print(f'Load consumption energy data from {file_path} completed...')

    # Using SQL Lite
    engine = create_engine('sqlite://', echo=False)
    concatenated_gen_df.to_sql('energy_data_gen', con=engine, index=False)
    concatenated_load_df.to_sql('energy_data_load', con=engine, index=False)

    #transform data using SQL 
    consolidated_data = pd.read_sql_query(load_query('Transform_join_load_gen'), con=engine)
    print('Load consolidate data completed...')
    print(consolidated_data.head(10))
    return consolidated_data

def clean_data(df):
    """Handle missing values, create index"""
    # TODO: Handle missing values, outliers, etc
    print('Start clean data...')
    # Create index
    df['index'] = (df['StartDate'] + '-' + df['dataHour']).str.replace('-', '').astype(int)
    # Replace 0 to NaN value 
    df.replace(0, np.nan, inplace=True)
    # handle NaN data using interpolate
    df.interpolate(method='linear', limit_direction='both', inplace=True)
    print('Completed clean data...')
    print(df.head(10))
    return df

def preprocess_data(df):
    """Generate new features, transform existing features, resampling"""
    # TODO: Generate new features, transform existing features, resampling, etc.
    print('Start preprocess data...')
    # The country IDs used to evaluate your model
    country_mapping = {
        'SP': 0,  # Spain
        'UK': 1,  # United Kingdom
        'DE': 2,  # Germany
        'DK': 3,  # Denmark
        'HU': 5,  # Hungary
        'SE': 4,  # Sweden
        'IT': 6,  # Italy
        'PO': 7,  # Poland
        'NE': 8   # Netherlands
    }
    print('Start calculate surplus...')
    # Calculate surplus
    for country in ['SP', 'UK', 'DE', 'DK', 'HU', 'SE', 'IT', 'PO', 'NE']:
        green_col = f'green_energy_{country}'
        load_col = f'load_{country}'
        diff_col = f'diff_{country}'
        df[diff_col] = df[green_col] - df[load_col]
    # Find the character with the highest difference for each row
    df['max_diff_char'] = df[['diff_HU', 'diff_IT', 'diff_PO', 'diff_SP', 
                            'diff_UK', 'diff_DE', 'diff_DK', 'diff_SE', 
                            'diff_NE']].idxmax(axis=1).str.extract(r'diff_(\w+)')

    # Create a new column 'max_diff_value' to store the maximum difference value for each row
    df['max_diff_value'] = df[['diff_HU', 'diff_IT', 'diff_PO', 'diff_SP', 
                                    'diff_UK', 'diff_DE', 'diff_DK', 'diff_SE', 
                                    'diff_NE']].max(axis=1)

    print('completed calculate surplus...')
    # mapping country code with country_id
    df['country_id'] = df['max_diff_char'].map(country_mapping)
    # If diff less than zero mean no surplus in any country that hour => assign value = 9 
    df.loc[df['max_diff_value'] < 0, 'country_id'] = 9

    print('Start Feature engineering ...')
    # extract predict data 
    surplus_predict = df[['index','country_id']]
    # Create feature 
    surplus_predict['index'] = pd.to_datetime(surplus_predict['index'], format='%Y%m%d%H')
    surplus_predict['hour'] = surplus_predict['index'].dt.hour
    surplus_predict['day_of_week'] = surplus_predict['index'].dt.dayofweek
    surplus_predict['month'] = surplus_predict['index'].dt.month

    print('Calculate lag feature ...')
    # Extract lag value for last 24 hours 
    for lag_hour in range(1, 25):
        lag_column_name = f'lag_{lag_hour}_hour'
        surplus_predict[lag_column_name] = surplus_predict['country_id'].shift(lag_hour)
    # Drop NaN value (No lag value)
    df_processed =  surplus_predict.dropna()
    print('Completed Feature engineering ...')
    return df_processed

def save_data(df, output_file):
    """Save processed data to a CSV file"""
    # TODO: Save processed data to a CSV file
    output_file_path = os.path.join(output_file, 'processed_data.csv')
    df.to_csv(output_file_path, index=False)
    print(f' Processed data ready in   {output_file_path}')


def parse_arguments():
    """assign argument"""
    parser = argparse.ArgumentParser(description='Data processing script for Forecasting')
    parser.add_argument(
        '--input_file',
        type=str,
        default='data/raw_data.csv',
        help='Path to the raw data file to process'
    )
    parser.add_argument(
        '--output_file', 
        type=str,
        default='data/processed_data.csv', 
        help='Path to save the processed data'
    )
    return parser.parse_args()

def main(input_file, output_file):
    """ Run function"""
    df = load_data(input_file)
    df_clean = clean_data(df)
    df_processed = preprocess_data(df_clean)
    save_data(df_processed, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)
    # End-of-file (EOF)