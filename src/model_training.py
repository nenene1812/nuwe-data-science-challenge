import pandas as pd
import argparse
import os 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pickle


def load_data(file_path):
    """ Load processed data from CSV file """
    # TODO: Load processed data from CSV file
    print(f'Fetching data from {file_path} ...')
    df = pd.read_csv(os.path.join(file_path, 'processed_data.csv'))
    return df

def split_data(df):
    """
    Split data into training and validation sets and save the validation set to a CSV file.

    Parameters:
    df (pandas.DataFrame): The dataset to split.
    csv_path (str): Path where the validation set CSV will be saved.

    Returns:
    X_train (pandas.DataFrame): Training features.
    X_val (pandas.DataFrame): Validation features.
    y_train (pandas.Series): Training target.
    y_val (pandas.Series): Validation target.
    """

    print('Start split data ...')
    # TODO: Split data into training and validation sets (the test set is already provided in data/test_data.csv)
    lag_features = [f'lag_{i}_hour' for i in range(1, 25)]
    X = df[['hour', 'day_of_week', 'month'] + lag_features]
    y = df['country_id']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    # Save the validation set to a CSV file
    val_set = pd.concat([X_val, y_val], axis=1)
    val_set.to_csv('../data/test_data.csv', index=False)
    print('Test data ready in `../data/test_data.csv`')
    print('Completed split data ...')
    return X_train, X_val, y_train, y_val

def train_model(X_train, y_train):
    """ Initialize your model and train it """
    print('Start training data ...')
    # TODO: Initialize your model and train it
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    print('Completed training data ...')
    return model

def save_model(model, model_path):
    """Save your trained model"""
    # TODO: Save your trained model
    output_file_path = os.path.join(model_path, 'model.pkl')
    # Save the model to a file as .pkl format
    with open(output_file_path, 'wb') as file:
        pickle.dump(model, file)
    print(f'Model ready in `{output_file_path}` ')

def parse_arguments():
    """assign argument"""
    parser = argparse.ArgumentParser(description='Model training script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/processed_data.csv', 
        help='Path to the processed data file to train the model'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/model.pkl', 
        help='Path to save the trained model'
    )
    return parser.parse_args()

def main(input_file, model_file):
    df = load_data(input_file)
    X_train, X_val, y_train, y_val = split_data(df)
    model = train_model(X_train, y_train)
    save_model(model, model_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file)