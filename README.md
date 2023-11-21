# SCHNEIDER ELECTRIC EUROPEAN HACKATHON 2023

# 📈 CHALLENGE 1: Data Science challenge

https://nuwe.io/dev/competitions/schneider-electric-european-2023


## Introduction

This repository contains a solution for the Schneider Electric Europe Green Energy Prediction Challenge. The goal of this competition is to build a model capable of predicting which European country will have the largest surplus of green energy in the next hour.

The solution ingests renewable energy generation and electricity load time series data from 9 countries via the ENTSO-E API. Data cleaning, feature engineering, and model training were performed using RandomForestClassifier to output predictions on which country will have the most surplus green energy.

The README describes the approach, documents key files, and discusses model performance. An F1 score of X was achieved on the test set. Please refer to the notebooks and scripts in [playground folder](https://github.com/nenene1812/nuwe-data-science-challenge/tree/main/playground) for implementation details.

### Authors

- [@nenene](https://github.com/nenene1812)

## Acknowledgements

- [Nuwe](https://nuwe.io/) : Organizer 
- [Schneider Electric](https://www.se.com/ww/en/) : Challenge Owner

## Flow 
![Project flow](https://github.com/nenene1812/nuwe-data-science-challenge/blob/main/EcoForecast_Flow.png)