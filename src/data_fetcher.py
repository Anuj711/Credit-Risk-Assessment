import yfinance as yf
import os




def fetch_yahoo_data(ticker, save_path="data/raw/"):
    """
    Fetches financial data for the specified ticker from Yahoo Finance
    and saves it locally as CSV files.
    """
    try:
        os.makedirs(save_path, exist_ok=True)
        stock = yf.Ticker(ticker)

        # Fetch data
        historical_data = stock.history(period="5y")
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow

        # Save data
        historical_data.to_csv(os.path.join(save_path, f"{ticker}_historical.csv"))
        financials.to_csv(os.path.join(save_path, f"{ticker}_financials.csv"))
        balance_sheet.to_csv(os.path.join(save_path, f"{ticker}_balance_sheet.csv"))
        cashflow.to_csv(os.path.join(save_path, f"{ticker}_cashflow.csv"))

        print(f"Data for {ticker} saved to {save_path}")
        return historical_data, financials, balance_sheet, cashflow

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None, None, None

def fetch_stock_prices(ticker, start_date, end_date, output_file="data/raw/stock_prices.csv"):
    """
    Fetch historical stock prices for a given ticker and save to a CSV file.

    Parameters:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        start_date (str): Start date for historical data (format: 'YYYY-MM-DD').
        end_date (str): End date for historical data (format: 'YYYY-MM-DD').
        output_file (str): Path to save the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing historical stock prices.
    """
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data[['Close']].reset_index().to_csv(output_file, index=False)
    print(f"Historical stock prices saved to '{output_file}'")
    return stock_data[['Close']].reset_index()

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    output_file = "data/raw/AAPL_stock_prices.csv"

    fetch_stock_prices(ticker, start_date, end_date, output_file)
