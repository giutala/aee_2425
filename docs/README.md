# The Importance of Utilizing Explainable Artificial Intelligence Models in Solar Photovoltaic Power Generation Forecasting

This repository contains a project focused on analyzing and modeling photovoltaic (PV) output data using various machine learning and deep learning techniques. The project includes data preprocessing, exploratory data analysis, model training, and evaluation.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results](#results)
- [Acknowledgments](#acknowledgments)

## Introduction

This project processes and analyzes a PV output dataset to predict energy output. The workflow includes:

- Data preparation and cleaning.
- Exploratory Data Analysis (EDA) for understanding the dataset.
- Splitting data and applying K-fold cross-validation.
- Training models including XGBoost and LSTM neural networks.
- Visualizing results and analyzing feature importance using SHAP (SHapley Additive exPlanations).

## Features

- **Data Manipulation and Processing**: Utilizes `pandas` and `numpy` for efficient data handling.
- **Machine Learning Models**: XGBoost for regression tasks.
- **Deep Learning**: LSTM models implemented with TensorFlow/Keras.
- **Performance Metrics**: Evaluates models with MAE, MSE, and R^2.
- **Feature Importance**: Uses SHAP for interpreting model outputs.

## Project Structure

- **Notebooks**: Contains Jupyter notebooks for data preparation, modeling, and analysis.
- **Dataset**: Placeholder or instructions for obtaining the PV dataset.
- **Scripts**: Includes reusable scripts for data processing and modeling.
- **Visualizations**: Stores generated plots and SHAP visualizations.

## Results

- XGBoost achieved an R^2 score of ... with a Mean Absolute Error (MAE) of ...
- LSTM provided temporal insights but required fine-tuning to achieve competitive performance.
- SHAP analysis highlighted key features influencing model predictions.

---

For questions or contributions, please contact [giuliatala32@gmail.com].

