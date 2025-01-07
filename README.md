# README

## Stock Analysis and Prediction Tool

This web application allows users to analyze stock performance, test hypotheses about daily stock returns, and predict future stock prices. It is built using Python, Flask, and integrates data scraping, statistical analysis, and machine learning models for stock analysis.

### Features

1. **Stock Data Visualization**: 
   - Enter a stock ticker symbol and date range to generate a graph of historical stock prices.

2. **Hypothesis Testing**:
   - Tests the null hypothesis that the average daily returns of a stock are equal to zero.
   - Provides actionable insights based on statistical significance.

3. **Future Price Prediction**:
   - Uses regression analysis to predict the future price of a stock on a specific date.

### File Structure

- `app.py`: Main Flask application file that handles routing and backend logic.
- `templates/`: Contains HTML templates for the web interface.
  - `index.html`: Home page for stock ticker and date range input.
  - `hypothesis.html`: Displays results of hypothesis testing.
  - `future_prediction.html`: Displays future stock price predictions.
- `static/`: Folder for static files like CSS and JavaScript (if applicable).
- `requirements.txt`: Lists all dependencies required to run the application.

### Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/stock-analysis-tool.git
   cd stock-analysis-tool
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`.

### Usage

1. **Home Page**:
   - Enter a stock ticker (e.g., AAPL) and a date range to visualize historical stock prices.

2. **Hypothesis Testing**:
   - After entering the stock ticker and date range, click on `Test My Investment Claims` to navigate to the hypothesis testing page.
   - Review the statistical results and insights for your stock.

3. **Future Price Prediction**:
   - Click on `Future Projections` after entering the stock ticker and date range to predict the stock price for a future date.

### Technologies Used

- **Backend**: Python, Flask
- **Data Analysis**: Pandas, NumPy, SciPy
- **Visualization**: Matplotlib
- **Web Interface**: HTML, Bootstrap

### Requirements

All dependencies are listed in the `requirements.txt` file. Install them using `pip install -r requirements.txt`.

### Future Improvements

- Implement advanced machine learning models for more accurate predictions.
- Add options for comparing multiple stocks simultaneously.
- Enhance the user interface with more interactivity.
- Include a feature for users to download analysis reports.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

Anuj Shukla

---

## Acknowledgments

Special thanks to all contributors and the open-source community for libraries and tools used in this project.
