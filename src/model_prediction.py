import pandas as pd
import argparse
import os 
import pickle
import numpy as np
import json

def load_data(file_path):
    """ Load test data from CSV file """
    # TODO: Load test data from CSV file
    print(f'Fetching data from {file_path} ...')
    df = pd.read_csv(os.path.join(file_path, 'test_data.csv'))
    return df

def load_model(model_path):
    # TODO: Load the trained model
    with open(os.path.join(model_path, 'model.pkl'), 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def make_predictions(df, model):
    # TODO: Use the model to make predictions on the test data
    lag_features = [f'lag_{i}_hour' for i in range(1, 25)]
    X_test = df[['hour', 'day_of_week', 'month'] + lag_features]
    y_pred = model.predict(X_test)
    predictions = y_pred
    print(predictions)
    return predictions

def save_predictions(predictions, predictions_file):
    # TODO: Save predictions to a JSON file
    predictions = predictions[predictions != 9]
    predictions_list = predictions.tolist()
    predictions_json = {
    "target": {str(i): predictions_list[i] for i in range(442)}
    }
    json_string = json.dumps(predictions_json)
    # Write to file
    output_file_path = os.path.join(predictions_file, 'predictions.json')
    with open(output_file_path, "w") as f:
        f.write(json_string)
        
    print(f"JSON data is written to `{output_file_path}`")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Prediction script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/test_data.csv', 
        help='Path to the test data file to make predictions'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/model.pkl',
        help='Path to the trained model file'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='predictions/predictions.json', 
        help='Path to save the predictions'
    )
    return parser.parse_args()

def main(input_file, model_file, output_file):
    df = load_data(input_file)
    model = load_model(model_file)
    predictions = make_predictions(df, model)
    save_predictions(predictions, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file, args.output_file)
