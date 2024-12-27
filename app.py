from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import yfinance as yf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Fetch data using yfinance
        data = fetch_stock_data(ticker, start_date, end_date)

        if data is not None:
            analysis_results = perform_analysis(data)
            plot_url = plot_results(analysis_results)
            table_html = analysis_results.to_html(classes='table table-striped', index=False)
            return render_template('index.html', plot_url=plot_url, table_html=table_html, ticker=ticker)
        else:
            return render_template('index.html', error="Invalid Ticker or Date Range")

    return render_template('index.html', plot_url=None, table_html=None, ticker=None)

def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        
        # Flatten the MultiIndex by resetting columns
        stock_data.columns = [col[0] for col in stock_data.columns]
        
        stock_data.reset_index(inplace=True)
        return stock_data
    except Exception as e:
        print("Error fetching stock data:", e)
        return None



def perform_analysis(data):
    # Calculate Daily Returns and Cumulative Returns
    data['Daily Returns'] = data['Close'].pct_change()
    data['Cumulative Returns'] = (1 + data['Daily Returns']).cumprod()

    # Fill NaN values in 'Cumulative Returns' with 0
    data['Cumulative Returns'].fillna(0, inplace=True)

    return data



def plot_results(analysis_results):
    fig, ax = plt.subplots()
    ax.plot(analysis_results['Date'], analysis_results['Cumulative Returns'], label='Cumulative Returns', color='b')
    ax.set(xlabel='Date', ylabel='Cumulative Returns', title='Stock Price Cumulative Returns')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    #TODO: When the timeframe between start and end dates is too small (within the same year for example), the x axis formatting is messed up
    # Convert the plot to a base64-encoded string for embedding in the HTML
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{plot_url}"

if __name__ == "__main__":
    app.run(debug=True)
