import pytest
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Import function to test
from src.data_prep import preprocess_financial_data


def test_preprocess_financial_data():
    # Example paths for your data files
    financials_file = 'data/raw/AAPL_financials.csv'
    balance_sheet_file = 'data/raw/AAPL_balance_sheet.csv'
    
    # Call the function to test
    ratios = preprocess_financial_data(financials_file, balance_sheet_file)
    
    # Ensure the ratios are saved to CSV
    assert ratios is not None
    assert 'Net Profit Margin' in ratios.columns
    assert 'Current Ratio' in ratios.columns
    assert 'Debt-to-Equity' in ratios.columns

    # Check if the CSV was saved
    output_csv = 'data/processed/AAPL_processed_ratios.csv'
    assert os.path.exists(output_csv), f"CSV file {output_csv} does not exist"

    # Optionally, check if some rows are in the CSV (e.g., first row)
    saved_ratios = pd.read_csv(output_csv)
    assert not saved_ratios.empty, "The saved CSV is empty"
    print("CSV output test passed!")
