import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_fetcher import fetch_yahoo_data



# Test the function with a sample ticker
ticker = "AAPL"  # Apple Inc.
historical_data, financials, balance_sheet, cashflow = fetch_yahoo_data(ticker)

# Print results to verify
if historical_data is not None:
    print("Historical Data:")
    print(historical_data.head())

if financials is not None:
    print("\nFinancials:")
    print(financials.head())

if balance_sheet is not None:
    print("\nBalance Sheet:")
    print(balance_sheet.head())

if cashflow is not None:
    print("\nCash Flow:")
    print(cashflow.head())
