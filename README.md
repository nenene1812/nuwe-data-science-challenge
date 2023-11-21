# SCHNEIDER ELECTRIC EUROPEAN HACKATHON 2023

# 📈 CHALLENGE 1: Data Science challenge

https://nuwe.io/dev/competitions/schneider-electric-european-2023


## Introduction

This repository contains a solution for the Schneider Electric Europe Green Energy Prediction Challenge. The goal of this competition is to build a model capable of predicting which European country will have the largest surplus of green energy in the next hour.

The solution ingests renewable energy generation and electricity load time series data from 9 countries via the ENTSO-E API. Data cleaning, feature engineering, and model training were performed using RandomForestClassifier to output predictions on which country will have the most surplus green energy.

The README describes the approach, documents key files. Please refer to the notebooks and scripts in [playground folder](https://github.com/nenene1812/nuwe-data-science-challenge/tree/main/playground) for implementation details.

### Authors

- [@nenene](https://github.com/nenene1812)

## Acknowledgements

- [Nuwe](https://nuwe.io/) : Organizer 
- [Schneider Electric](https://www.se.com/ww/en/) : Challenge Owner

## Repository Structure

### This repository is organized as follows:

- `data/`: This directory holds the CSV files used for project.
- `models/`: This directory is reserved for storing the trained models.

- `predictions/`: This directory contains the outputs of the model predictions.
  - `example_predictions.json`: An example file showing the structure of prediction outputs.
  - `predictions.json`: The actual prediction results from the trained models.

- `scripts/`: This directory contains shell scripts for automating the execution of the pipeline.
  - `run_pipeline.sh`: A shell script to run the entire data processing and prediction pipeline.

- `src/`: The source code directory with Python scripts for each step of the project pipeline.
  - `data_ingestion.py`: Script responsible for loading and ingesting data.
  - `data_processing.py`: Script for processing and cleaning data.
  - `model_training.py`: Script or Jupyter notebook for training forecasting models.
  - `model_prediction.py`: Script for making predictions with the trained models.
  - `utils.py`: Utility functions used across the project.

- `playground/`: A space for Jupyter notebooks used for exploratory data analysis and experimentation.
  - `discover.ipynb`: A Jupyter notebook used for initial data exploration.
  - `README.md`: Insight gained with dataset. 



The repository follows a modular approach, with separate scripts for each stage of the machine learning pipeline, ensuring ease of use and maintainability.

## Instructions
1. Install dependencies:
`pip install -r requirements.txt`
2. run_pipeline.sh

## Flow 
![Project flow](https://github.com/nenene1812/nuwe-data-science-challenge/blob/main/EcoForecast_Flow.png)

## Key in Approach:
1. **Data Processing**: Leveraging SQLite for data grouping by the hour to save processing time.
2. **Model Training**: Use of RandomForestClassifier due to time constraints and to bypass the need for extensive domain knowledge.
3. **Model Prediction**: Post-prediction processing involves removing hours without surplus and exporting the top 442 surplus predictions to a JSON file for result validation.

