import pandas as pd
import os

def transform_financials_to_date_column(filepath, output_filepath):
    """
    Transform financial data with dates in columns to a format with a Date column.
    """
    try:
        # Load the CSV
        df = pd.read_csv(filepath, index_col=0)

        # Transpose the DataFrame to move dates from columns to rows
        df_transposed = df.transpose()

        # Add a `Date` column based on the index (former column headers)
        df_transposed.reset_index(inplace=True)
        df_transposed.rename(columns={"index": "Date"}, inplace=True)

        # Save the transformed DataFrame
        df_transposed.to_csv(output_filepath, index=False)
        print(f"Transformed financials saved to {output_filepath}")
        return output_filepath

    except Exception as e:
        print(f"Error transforming financials: {e}")
        return None

def preprocess_historical_data(filepath):
    """
    Preprocess historical stock price data.
    """
    try:
        data = pd.read_csv(filepath, index_col=0, parse_dates=True)
        
        # Calculate daily returns
        data["Daily Return"] = data["Close"].pct_change()

        # Calculate rolling volatility (30-day standard deviation)
        data["30-Day Volatility"] = data["Daily Return"].rolling(window=30).std()

        # Calculate year-over-year (YoY) percentage change
        data["YoY Change"] = data["Close"].pct_change(periods=252)  # 252 trading days in a year

        return data

    except Exception as e:
        print(f"Error preprocessing historical data: {e}")
        return None

def preprocess_financial_data(financials_file, balance_sheet_file, output_file):
    try:
        # Load the transformed financial data
        financials = pd.read_csv(financials_file, index_col="Date", parse_dates=True)
        
        # Check if 'Date' column exists after transformation
        if 'Date' not in financials.columns:
            # If 'Date' is not found, make sure to set it explicitly
            financials = transform_financials_to_date_column(financials_file, financials_file)
            financials = pd.read_csv(financials_file, index_col="Date", parse_dates=True)

        # Load the balance sheet data
        balance_sheet = pd.read_csv(balance_sheet_file, index_col=0)

        # Print the available rows for debugging
        print("Available rows in balance sheet:", balance_sheet.index.tolist())

        # Cash label candidates
        cash_label_candidates = [
            'Cash and Cash Equivalents',
            'Cash Cash Equivalents And Short Term Investments',
            'Cash Financial',
            'Cash Equivalents'
        ]

        # Loop through possible variations for cash
        total_current_assets = None
        for label in cash_label_candidates:
            if label in balance_sheet.index:
                print(f"Found label for cash: {label}")
                total_current_assets = balance_sheet.loc[label, :]
                break
        
        # Short-term debt candidates
        short_term_debt_candidates = [
            'Short-Term Debt',
            'Current Debt',
            'Short-Term Liabilities',
            'Current Liabilities'
        ]

        # Loop through possible variations for short-term debt
        short_term_debt = None
        for label in short_term_debt_candidates:
            if label in balance_sheet.index:
                print(f"Found label for short-term debt: {label}")
                short_term_debt = balance_sheet.loc[label, :]
                break

        # If no match was found, raise an error
        if short_term_debt is None:
            raise ValueError("No matching 'Short-Term Debt' label found in balance sheet.")
        
        # Derive total current assets and liabilities
        total_current_assets += (
            balance_sheet.loc["Accounts Receivable", :] +
            balance_sheet.loc["Inventory", :]
        )

        total_current_liabilities = (
            balance_sheet.loc["Accounts Payable", :] +
            short_term_debt  # Use the found short-term debt
        )

        total_stockholder_equity = balance_sheet.loc["Stockholders Equity", :]

        # Example ratios
        ratios = pd.DataFrame(index=financials.columns)
        ratios["Net Profit Margin"] = financials.loc["Net Income"] / financials.loc["Total Revenue"]
        ratios["Current Ratio"] = total_current_assets / total_current_liabilities
        ratios["Debt-to-Equity"] = balance_sheet.loc["Total Liabilities Net Minority Interest"] / total_stockholder_equity

        # Ensure Date is properly aligned
        ratios["Date"] = financials.columns  # Dates will be aligned as they should be after transformation

        # Save the ratios to a CSV file
        save_preprocessed_data(ratios, output_file)

        return ratios

    except Exception as e:
        print(f"Error preprocessing financial data: {e}")
        return None


def save_preprocessed_data(data, filename, save_path="data/processed/"):
    """
    Save preprocessed data to a CSV file.
    """
    try:
        # Ensure the directory exists
        os.makedirs(save_path, exist_ok=True)
        
        # Check if the path includes the filename or if the filename needs to be appended
        file_path = os.path.join(save_path, filename) if not filename.startswith(save_path) else filename
        
        # Save the file to the specified path
        data.to_csv(file_path)
        print(f"Preprocessed data saved to {file_path}")
    except Exception as e:
        print(f"Error saving preprocessed data: {e}")



