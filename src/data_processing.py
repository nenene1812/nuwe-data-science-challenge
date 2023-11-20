import argparse
import os 
import pandas as pd
from utils import list_files_containing_char

def load_data(file_path):
    """ELT: load data from ingestion data """
    # TODO: Load data from CSV file
    # Get gen green energy tag 
    green_energy = [
        "B01", "B09", "B10", "B11", "B12",
        "B13", "B15", "B16", "B18", "B19"
    ]
    print(f'Fetching data from {file_path} ...')
    all_files = list_files_containing_char(file_path, 'gen')
    # Initialize an empty DataFrame to hold concatenated data
    concatenated_df = pd.DataFrame()
    # Loop through the files and concatenate the ones that meet the criteria
    for file_name in all_files:
        if file_name.endswith('.csv') and any(code in file_name for code in green_energy):
            print(f'loading data from {os.path.join(file_path, file_name)} ...')
            # Read the csv file
            df = pd.read_csv(os.path.join(file_path, file_name))
            
            # Split the file name and create new columns
            split_name = file_name.replace('.csv', '').split('_')
            df['Country'] = split_name[1]
            
            # Concatenate the DataFrame to the main concatenated_df
            concatenated_df = pd.concat([concatenated_df, df])
    #Delete AreaID because already have country code
    concatenated_df = concatenated_df.drop(columns=['AreaID'])
    # Save the concatenated DataFrame to a new csv file
    output_file_path = os.path.join('../data/load_data', 'gen_green_energy.csv')
    concatenated_df.to_csv(output_file_path, index=False)
    print(f'load data ready in   {output_file_path}')
    return concatenated_df

def clean_data(df):
    # TODO: Handle missing values, outliers, etc.
    df_clean = 'a'
    return df_clean

def preprocess_data(df):
    # TODO: Generate new features, transform existing features, resampling, etc.
    df_processed = 'a'
    return df_processed

def save_data(df, output_file):
    # TODO: Save processed data to a CSV file
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting Hackathon')
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
    # df_clean = clean_data(df)
    # df_processed = preprocess_data(df_clean)
    # save_data(df_processed, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)