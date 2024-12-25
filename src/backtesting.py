import pandas as pd
import os

def backtest_strategy(stock_prices_file, signal_ratios_file, output_file="data/processed/backtest_results.csv"):
    """
    Perform backtesting based on stock prices and signal ratios.

    Parameters:
        stock_prices_file (str): Path to CSV file containing historical stock prices.
        signal_ratios_file (str): Path to CSV file containing financial ratios.
        output_file (str): Path to save the backtesting results.

    Returns:
        pd.DataFrame: DataFrame containing backtesting results.
    """
    # Load historical stock prices
    if not os.path.exists(stock_prices_file):
        raise FileNotFoundError(f"Stock prices file '{stock_prices_file}' not found.")
    stock_prices = pd.read_csv(stock_prices_file, parse_dates=["Date"])
    stock_prices.set_index("Date", inplace=True)

    # Clean stock prices to ensure 'Close' is numeric
    stock_prices["Close"] = pd.to_numeric(stock_prices["Close"], errors="coerce")
    stock_prices = stock_prices.dropna(subset=["Close"])

    # Load financial ratios
    if not os.path.exists(signal_ratios_file):
        raise FileNotFoundError(f"Signal ratios file '{signal_ratios_file}' not found.")
    ratios = pd.read_csv(signal_ratios_file, parse_dates=["Date"])
    ratios.set_index("Date", inplace=True)

    # Remove unwanted columns like "Unnamed: 0"
    if "Unnamed: 0" in ratios.columns:
        ratios = ratios.drop(columns=["Unnamed: 0"])

    # Convert all ratio columns to numeric
    for col in ratios.columns:
        ratios[col] = pd.to_numeric(ratios[col], errors="coerce")

    # Prompt the user to select a ratio column
    available_columns = [col for col in ratios.columns if col != "Date"]
    print("Available ratios:")
    for idx, column in enumerate(available_columns, start=1):
        print(f"{idx}. {column}")

    ratio_column = None
    while not ratio_column:
        try:
            choice = int(input("Enter the number corresponding to the desired ratio: "))
            if 1 <= choice <= len(available_columns):
                ratio_column = available_columns[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"Selected ratio: {ratio_column}")

    # Ensure matching dates
    common_dates = stock_prices.index.intersection(ratios.index)
    if len(common_dates) == 0:
        raise ValueError("No matching dates found between stock prices and financial ratios.")

    stock_prices = stock_prices.loc[common_dates]
    ratios = ratios.loc[common_dates]

    # # Debug: Check the first few values of the ratio_column to ensure variability
    # print(f"First few values of {ratio_column}:")
    # print(ratios[ratio_column].head())

    # Example strategy: Buy if ratio_column < 0.05, Sell if ratio_column > 0.3
    signals = pd.DataFrame(index=ratios.index)
    signals["Signal"] = 0
    signals.loc[ratios[ratio_column] < 0.7, "Signal"] = 1  # Buy signal
    signals.loc[ratios[ratio_column] > 1, "Signal"] = -1  # Sell signal

    # # Debug: Check the distribution of signals
    # print("Signal distribution:")
    # print(signals["Signal"].value_counts())

    # Calculate portfolio returns
    signals["Stock Returns"] = stock_prices["Close"].pct_change()

    # # Debug: Check stock returns for a few days
    # print("Stock Returns for the first few days:")
    # print(signals["Stock Returns"].head())

    signals["Strategy Returns"] = signals["Signal"].shift(1) * signals["Stock Returns"]

    # Cumulative performance
    signals["Cumulative Stock Returns"] = (1 + signals["Stock Returns"]).cumprod()
    signals["Cumulative Strategy Returns"] = (1 + signals["Strategy Returns"]).cumprod()

    # # Debug: Check cumulative returns
    # print("Cumulative returns:")
    # print(signals[["Cumulative Stock Returns", "Cumulative Strategy Returns"]].tail())

    # Save results
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    signals.to_csv(output_file)
    print(f"Backtesting results saved to '{output_file}'")

    return signals

if __name__ == "__main__":
    stock_prices_file = "data/raw/AAPL_stock_prices.csv"  # Replace with your stock prices file path
    signal_ratios_file = "data/processed/AAPL_processed_ratios.csv"  # Replace with your ratios file path
    output_file = "data/processed/backtest_results.csv"

    try:
        results = backtest_strategy(stock_prices_file, signal_ratios_file, output_file)
        print("Backtesting complete. Sample results:")
        print(results.head())
    except ValueError as e:
        print(f"Error during backtesting: {e}")
