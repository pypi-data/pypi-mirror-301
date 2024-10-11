import logging
from typing import Dict

from statsmodels.tsa.stattools import adfuller

logger = logging.getLogger(__name__)


def adf_test(data, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False) -> Dict[str, float]:
    """
    Perform Augmented Dickey-Fuller test for stationarity.

    Parameters:
        data     : pd.Series
                   Time series data.
        maxlag   : int, optional, default=None
                     Maximum lag to consider.
        regression: str, optional, default='c'
                        Type of regression to include in the test ('c', 'ct', 'ctt', 'nc').
        autolag  : str, optional, default='AIC'
                        Method to use when automatically determining the lag length ('AIC', 'BIC', 't-stat', 'mle').
        store    : bool, optional, default=False
                        If True, store the regression results.
        regresults: bool, optional, default=False
                        If True, return full regression results.

    Returns:
        dict
            Dictionary containing the ADF statistic, p-value, used lag, number of observations, critical values,
            best information criterion, and regression results.
    """
    logger.info(f'Performing Augmented Dickey-Fuller test for stationarity')
    logger.info(f'Maximum lag: {maxlag}, Regression: {regression}, Autolag: {autolag}, Store: {store}, Regresults: {regresults}, ')
    result = adfuller(data, maxlag=maxlag, regression=regression, autolag=autolag, store=store, regresults=regresults)
    return {'adf_stat': result[0], 'p_value': result[1], 'used_lag': result[2], 'n_obs': result[3],
            'critical_values': result[4], 'ic_best': result[5], 'reg_results': result[6] if regresults else None}


def is_stationary(data, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False):
    """
    Check if the given time series data is stationary using Augmented Dickey-Fuller test.

    Parameters:
        data     : pd.Series
                   Time series data.
        maxlag   : int, optional, default=None
                     Maximum lag to consider.
        regression: str, optional, default='c'
                        Type of regression to include in the test ('c', 'ct', 'ctt', 'nc').
        autolag  : str, optional, default='AIC'
                        Method to use when automatically determining the lag length ('AIC', 'BIC', 't-stat', 'mle').
        store    : bool, optional, default=False
                        If True, store the regression results.
        regresults: bool, optional, default=False
                        If True, return full regression results.

    Returns:
        bool
            True if the data is stationary, False otherwise.
    """
    result = adf_test(data, maxlag=maxlag, regression=regression, autolag=autolag, store=store, regresults=regresults)
    return result['p_value'] <= 0.05


def diff_series_until_stationary(data, max_diffs=2, maxlag=None, regression='c', autolag='AIC', store=False,
                                 regresults=False):
    """
    Differencing the time series data until it becomes stationary.

    Parameters:
        data     : pd.Series
                   Time series data.
        max_diffs: int, optional, default=2
                   Maximum number of differences to try.
        filename : str
                   Name of the file to save the results.

    Returns:
        pd.Series
            Stationary time series data.
    """
    for i in range(max_diffs):
        if is_stationary(data, maxlag=maxlag, regression=regression, autolag=autolag, store=store,
                         regresults=regresults):
            return data
        data = data.diff().dropna()
    return data
