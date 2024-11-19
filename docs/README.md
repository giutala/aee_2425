# The Importance of Solar Photovoltaic Power Generation Forecasting Utilizing Explainable Artificial Intelligence Models- AEE Report 2425
This university project forecasts solar photovoltaic (PV) power generation using solar irradiance and temperature data from the NSRDB. It employs machine learning models to predict energy output based on GHI, DNI, DHI, and temperature, while integrating explainable AI techniques for transparency and understanding key influencing factors.

# Predictive Modeling for Solar Irradiance

This repository contains a predictive model built to estimate solar irradiance using various meteorological and environmental features. The dataset was collected from the **National Solar Radiation Data Base (NSRDB)**, and an **XGBRegressor** model was used for the prediction task. This README explains the data collection process, model construction, and the analysis performed on the data.

## Data Collection

### **Source of Data**
The data used in this study is sourced from the **National Solar Radiation Data Base (NSRDB)**. The NSRDB provides solar radiation and meteorological data for locations across the United States and worldwide. The data includes key features such as **Global Horizontal Irradiance (GHI)**, **Direct Normal Irradiance (DNI)**, **Diffuse Horizontal Irradiance (DHI)**, **Temperature**, and other relevant environmental variables.

For this project, we focused on the following variables:

- **GHI (Global Horizontal Irradiance)**: The total amount of shortwave radiation received from above by a horizontal surface.
- **DNI (Direct Normal Irradiance)**: The amount of solar radiation received by a surface normal to the sunbeam.
- **DHI (Diffuse Horizontal Irradiance)**: The amount of solar radiation received from the sky, excluding the direct beam.
- **Temperature**: Ambient temperature of the location, which affects the solar power output.
- **Tilted Irradiance (Adjusted)**: Irradiance adjusted for a surface with a specific tilt, often relevant for solar panel orientation.

These features were used as input variables to train the predictive model, with **Tilted Irradiance (Adjusted)** being the target variable we aimed to predict.

### **Data Preprocessing**
Before using the data for training, the following preprocessing steps were carried out:
- **Handling missing values**: Any missing or null values were imputed or removed.
- **Feature scaling**: Numerical features were scaled to a standard range to help the model converge more efficiently during training.
- **Data splitting**: The dataset was split into a **training set** and a **test set** (typically 80% for training and 20% for testing).

## Model Construction

### **Model Choice**
For this predictive task, we chose the **XGBRegressor**, a gradient boosting model known for its efficiency and high performance in regression tasks. XGBRegressor is an ensemble learning method that builds strong models by combining the predictions of many weaker models (decision trees), focusing on minimizing the error in each successive iteration.

### **Model Architecture**
The **XGBRegressor** was configured with the following hyperparameters:
- **Learning Rate**: Controls the contribution of each tree to the final prediction.
- **Max Depth**: Limits the depth of each decision tree to avoid overfitting.
- **Number of Estimators**: Specifies the number of trees to build during training.

A **GridSearchCV** approach was used for hyperparameter tuning, where we tested multiple combinations of the hyperparameters to identify the best-performing model configuration.

### **Model Training**
The model was trained using the training dataset, where the features (GHI, DNI, DHI, Temperature) were used as input, and **Tilted Irradiance (Adjusted)** was the target variable. After training, the model was evaluated using the test dataset to assess its generalization performance.

### **Performance Metrics**
The model’s performance was evaluated using the following metrics:
- **Mean Squared Error (MSE)**: Measures the average squared difference between predicted and actual values. A lower MSE indicates better model performance.
- **R² Score**: Represents the proportion of variance explained by the model. A score closer to 1 indicates that the model fits the data well.
- **Root Mean Squared Error (RMSE)**: The square root of MSE, providing a more interpretable measure of error in the same units as the target variable.

## Data Analysis

### **Exploratory Data Analysis (EDA)**
Prior to building the model, an **Exploratory Data Analysis (EDA)** was conducted to understand the relationships between different features and the target variable. This included:
- **Visualizations**: Scatter plots, correlation heatmaps, and distribution plots to identify patterns, trends, and potential outliers.
- **Feature Importance**: We analyzed the importance of each feature in predicting the target variable by using the built-in feature importance of the XGBRegressor.

### **Model Evaluation**
After training the model, we evaluated its performance on both the training and test datasets:
- **Training Results**: The model achieved a **R² score of 0.9994** on the training data, indicating that it explains 99.94% of the variance in the target variable.
- **Test Results**: The model achieved a **R² score of 0.9981** on the test data, indicating strong generalization capability, though there was a slight decrease in performance compared to the training data.
- **Residuals Analysis**: The residuals (the difference between predicted and actual values) were analyzed to ensure there were no patterns indicating model bias.

### **Visualization of Results**
To assess the model's accuracy, the following visualizations were generated:
1. **Actual vs Predicted Plot**: Scatter plots were used to compare the actual vs. predicted values, with a red line indicating perfect predictions.
2. **Residual Plot**: Plots of the residuals to check for any systematic errors or trends in the model’s predictions.

### **Conclusions**
The model demonstrated high predictive accuracy with strong performance on both the training and test sets. The **XGBRegressor** was able to predict solar irradiance with an **R² score of 0.9981** on the test data, showcasing its potential for real-world applications in solar energy prediction. The slight difference between the training and test performances indicates the model’s strong generalization ability, while the low **Mean Squared Error (MSE)** reflects its accuracy in predicting solar irradiance values.

---

### **Future Work**
Future improvements could include:
- **Hyperparameter Tuning**: Further tuning the model's hyperparameters to further reduce error and improve predictions.
- **Incorporating Additional Features**: Including more environmental variables (e.g., humidity, cloud cover) to improve prediction accuracy.
- **Cross-validation**: Implementing cross-validation techniques to evaluate model robustness across multiple data splits.
