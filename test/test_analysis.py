import pytest
import pandas as pd
from src.analysis import perform_hypothesis_test, perform_regression_analysis

def test_perform_hypothesis_test():
    group1 = pd.Series([1.2, 1.3, 1.5, 1.7])
    group2 = pd.Series([1.1, 1.2, 1.0, 1.4])
    t_stat, p_value = perform_hypothesis_test(group1, group2)
    assert isinstance(t_stat, float)
    assert isinstance(p_value, float)

def test_perform_regression_analysis():
    x = pd.Series([1.0, 2.0, 3.0, 4.0])
    y = pd.Series([2.0, 4.0, 6.0, 8.0])
    model = perform_regression_analysis(x, y)
    assert round(model.coef_[0], 2) == 2.00
