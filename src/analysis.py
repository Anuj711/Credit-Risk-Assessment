import pandas as pd
from scipy.stats import ttest_ind

def perform_hypothesis_test(group1, group2):
    """
    Perform a two-sample t-test for hypothesis testing.
    
    Parameters:
        group1 (pd.Series): First group of data.
        group2 (pd.Series): Second group of data.

    Returns:
        t_stat (float): T-statistic from the t-test.
        p_value (float): P-value from the t-test.
    """
    t_stat, p_value = ttest_ind(group1.dropna(), group2.dropna(), equal_var=False)
    return t_stat, p_value


if __name__ == "__main__":
    # Load the processed ratios from the CSV file
    df = pd.read_csv('data\processed\AAPL_processed_ratios.csv')
    

    # Select two ratio columns to compare
    group1 = df['Current Ratio']  # Replace with your column name
    group2 = df['Debt-to-Equity']  # Replace with your column name

    # Perform hypothesis test
    t_stat, p_value = perform_hypothesis_test(group1, group2)

    # Print results
    print(f"T-statistic: {t_stat:.2f}, P-value: {p_value:.5f}")

from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def perform_regression_analysis(x, y):
    """
    Perform linear regression analysis and plot the results.

    Parameters:
        x (pd.Series): Predictor variable (independent variable).
        y (pd.Series): Response variable (dependent variable).

    Returns:
        model (LinearRegression): Fitted regression model.
    """
    # Prepare data
    x = x.dropna().values.reshape(-1, 1)  # Reshape for sklearn
    y = y.dropna().values

    # Fit regression model
    model = LinearRegression()
    model.fit(x, y)

    # Predict for plotting
    y_pred = model.predict(x)

    # Plot the regression
    plt.scatter(x, y, color='blue', label='Data Points')
    plt.plot(x, y_pred, color='red', label='Regression Line')
    plt.xlabel("Independent Variable (e.g., Current Ratio)")
    plt.ylabel("Dependent Variable (e.g., Debt-to-Equity)")
    plt.title("Regression Analysis")
    plt.legend()
    plt.show()

    return model


if __name__ == "__main__":
    # Perform regression analysis on the same data
    x = df['Current Ratio']  # Replace with your independent variable
    y = df['Debt-to-Equity']  # Replace with your dependent variable

    model = perform_regression_analysis(x, y)

    # Print model coefficients
    print(f"Regression Coefficient: {model.coef_[0]:.4f}")
    print(f"Intercept: {model.intercept_:.4f}")
