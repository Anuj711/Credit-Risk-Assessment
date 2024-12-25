import os
import pandas as pd
import sys
from src.data_prep import preprocess_financial_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Define paths for financial and balance sheet data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FINANCIALS_FILE = os.path.join(BASE_DIR, "../data/raw/AAPL_financials.csv")
BALANCE_SHEET_FILE = os.path.join(BASE_DIR, "../data/raw/AAPL_balance_sheet.csv")
PROCESSED_FILE = os.path.join(BASE_DIR, "../data/processed/AAPL_processed_ratios.csv")

def test_preprocess_financial_data():
    """
    Test the preprocess_financial_data function.
    """
    try:
        print("Testing preprocess_financial_data...")
        
        # Call the preprocessing function
        ratios = preprocess_financial_data(FINANCIALS_FILE, BALANCE_SHEET_FILE)
        
        # Check if ratios are generated successfully
        if ratios is not None:
            print("Financial ratios successfully calculated:")
            print(ratios)

            # Save the processed ratios to a CSV file
            ratios.to_csv(PROCESSED_FILE)
            print(f"Processed ratios saved to: {PROCESSED_FILE}")
        else:
            print("No ratios were generated. Check your input data and labels.")

    except Exception as e:
        print(f"Error during testing: {e}")

# Run the test
if __name__ == "__main__":
    test_preprocess_financial_data()
