from data_prep import transform_financials_to_date_column, preprocess_financial_data

# Define file paths
raw_financials_file = "data/raw/AAPL_financials.csv"  # Path to your raw financials file
transformed_financials_file = "data/processed/AAPL_transformed_financials.csv"  # Path to the transformed financials file
balance_sheet_file = "data/raw/AAPL_balance_sheet.csv"  # Path to your balance sheet file
output_file = "data/processed/AAPL_processed_ratios.csv"  # Path to save the processed ratios

# Step 1: Transform the financials file to include a Date column
transform_financials_to_date_column(
    raw_financials_file,  # Positional argument for input file
    transformed_financials_file  # Positional argument for output file
)

# Step 2: Preprocess the transformed financial data
preprocess_financial_data(
    financials_file=transformed_financials_file,
    balance_sheet_file=balance_sheet_file,
    output_file=output_file
)
