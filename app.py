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
        desired_date = request.form.get('desired_date', None)

        # Validate inputs
        if not ticker or not start_date or not end_date:
            return redirect(url_for('index', error="Missing required form fields"))

        try:
            # Convert dates
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            desired_date = datetime.strptime(desired_date, '%Y-%m-%d') if desired_date else None

            # Fetch data
            data = fetch_stock_data(ticker, start_date, end_date)
            if data is not None:
                # Perform regression analysis
                regression_results = perform_regression_analysis(data)

                # Handle future projection if desired_date is provided
                if desired_date:
                    if regression_results['r_squared'] > 0.7:
                        predicted_price = predict_closing_price_at_date(data, regression_results, desired_date)
                        regression_results['predicted_price'] = predicted_price
                        regression_results['desired_date'] = desired_date.strftime('%Y-%m-%d')
                    else:
                        regression_results['error'] = "Correlation is not strong enough to accurately project or interpolate data."

                return render_template('regression.html', regression_results=regression_results, ticker=ticker,
                                       start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
            else:
                return redirect(url_for('index', error="Invalid data for regression analysis"))

        except Exception as e:
            print(f"Error in regression: {e}")
            return redirect(url_for('index', error="An error occurred during regression analysis"))

    return render_template('regression.html', regression_results=None, ticker=request.args.get('ticker'),
                           start_date=request.args.get('start_date'), end_date=request.args.get('end_date'))

@app.route('/future-prediction', methods=['POST'])
def future_prediction():
    try:
        future_date = request.form['future_date']
        slope = float(request.form['slope'])
        intercept = float(request.form['intercept'])
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')

        # Convert future date to "days since start date"
        future_date_obj = datetime.strptime(future_date, '%Y-%m-%d')
        days_since_start = (future_date_obj - start_date).days

        # Calculate predicted price
        predicted_price = slope * days_since_start + intercept

        return render_template('future_prediction.html', future_date=future_date, predicted_price=predicted_price)
    except Exception as e:
        return f"Prediction failed: {e}"


def predict_closing_price_at_date(data, regression_results, desired_date):
    """
    Predict the closing price on a future date based on regression results.
    """
    min_date = data['Date'].min()
    days_since_start = (desired_date - min_date).days
    slope = regression_results["slope"]
    intercept = regression_results["intercept"]
    predicted_price = slope * days_since_start + intercept
    return round(predicted_price, 2)





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
    try:
        # Check the timeframe
        days_range = (data['Date'].max() - data['Date'].min()).days

        # If timeframe spans years, use monthly averages
        if days_range > 365:
            data = data.resample('M', on='Date').mean().reset_index()

        # Prepare data
        dates = (data['Date'] - data['Date'].min()).dt.days.values.reshape(-1, 1)
        closing_prices = data['Close'].values.reshape(-1, 1)

        # Perform regression
        model = LinearRegression()
        model.fit(dates, closing_prices)
        predictions = model.predict(dates)

        # Calculate regression details
        slope = model.coef_[0][0]
        intercept = model.intercept_[0]
        r_squared = model.score(dates, closing_prices)

        # Generate scatter plot
        fig, ax = plt.subplots(figsize=(12, 6))  # Adjust plot size
        ax.scatter(data['Date'], closing_prices, label='Actual Prices', color='blue', alpha=0.6)
        ax.plot(data['Date'], predictions, label='Regression Line', color='red')
        ax.set(xlabel='Date', ylabel='Closing Price', title='Time Series Analysis Using Linear Regression')
        ax.legend()

        # Save the plot
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()

        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "plot_url": f"data:image/png;base64,{plot_url}",
            "allow_future_prediction": r_squared > 0.7  # Add this
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
