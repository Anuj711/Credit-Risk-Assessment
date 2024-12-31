from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

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
            return render_template('index.html', plot_url=plot_url, table_html=table_html, ticker=ticker,
                                   start_date=start_date, end_date=end_date)
        else:
            return render_template('index.html', error="Invalid Ticker or Date Range")

    return render_template('index.html', plot_url=None, table_html=None, ticker=None)

@app.route('/regression', methods=['GET', 'POST'])
def regression():
    if request.method == 'POST':
        ticker = request.form.get('ticker', None)
        start_date = request.form.get('start_date', None)
        end_date = request.form.get('end_date', None)

        # Validate input
        if not ticker or not start_date or not end_date:
            return redirect(url_for('index', error="Missing required form fields"))

        # Fetch data
        data = fetch_stock_data(ticker, start_date, end_date)
        if data is not None:
            # Perform regression analysis
            regression_results = perform_regression_analysis(data)
            return render_template('regression.html', regression_results=regression_results, ticker=ticker,
                                   start_date=start_date, end_date=end_date)
        else:
            return redirect(url_for('index', error="Invalid data for regression analysis"))

    return render_template('regression.html', regression_results=None, ticker=request.args.get('ticker'),
                           start_date=request.args.get('start_date'), end_date=request.args.get('end_date'))



def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data.columns = [col[0] for col in stock_data.columns]  # Flatten MultiIndex
        stock_data.reset_index(inplace=True)
        return stock_data
    except Exception as e:
        print("Error fetching stock data:", e)
        return None

def perform_analysis(data):
    data['Daily Returns'] = data['Close'].pct_change()
    data['Cumulative Returns'] = (1 + data['Daily Returns']).cumprod()
    data['Cumulative Returns'].fillna(0, inplace=True)
    return data

def perform_regression_analysis(data):
    """
    Perform a simple linear regression on stock's closing price over time.

    Returns:
        A dictionary with regression details and a plot URL for visualization.
    """
    try:
        # Extract data for regression
        dates = (data['Date'] - data['Date'].min()).dt.days.values.reshape(-1, 1)  # Convert dates to ordinal
        closing_prices = data['Close'].values.reshape(-1, 1)

        # Perform regression
        model = LinearRegression()
        model.fit(dates, closing_prices)
        predictions = model.predict(dates)

        # Resample data for better visualization if the timeframe is large
        if len(data) > 365:  # More than a year's worth of data
            data = data.set_index('Date').resample('M').mean().reset_index()  # Resample to monthly averages
            dates = (data['Date'] - data['Date'].min()).dt.days.values.reshape(-1, 1)
            closing_prices = data['Close'].values.reshape(-1, 1)
            predictions = model.predict(dates)

        # Generate regression plot
        fig, ax = plt.subplots(figsize=(12, 6))  # Larger graph
        ax.scatter(data['Date'], closing_prices, label='Actual Prices', color='blue', alpha=0.6)  # Scatter plot
        ax.plot(data['Date'], predictions, label='Regression Line', color='red')  # Regression line
        ax.set(xlabel='Date', ylabel='Closing Price', title='Regression Analysis')
        ax.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()

        return {
            "slope": model.coef_[0][0],
            "intercept": model.intercept_[0],
            "r_squared": model.score(dates, closing_prices),
            "plot_url": f"data:image/png;base64,{plot_url}"
        }
    except Exception as e:
        return {"error": f"Regression analysis failed: {e}"}




def plot_results(analysis_results):
    fig, ax = plt.subplots()
    ax.plot(analysis_results['Date'], analysis_results['Cumulative Returns'], label='Cumulative Returns', color='b')
    ax.set(xlabel='Date', ylabel='Cumulative Returns', title='Stock Price Cumulative Returns')

    # TODO: When the timeframe between start and end dates is too small (within the same year for example), the x-axis formatting is messed up

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{plot_url}"

if __name__ == "__main__":
    app.run(debug=True)
