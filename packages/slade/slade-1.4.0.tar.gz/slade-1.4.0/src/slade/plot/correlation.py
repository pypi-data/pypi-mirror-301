from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from matplotlib import pyplot as plt


def plot_acf_pacf(data, filename, lags=40, alpha=0.05):
    """
    Plot ACF and PACF for the given time series data.

    Parameters:
        data     : pd.Series
                   Time series data.
        filename : str
                   Name of the file to save the plot.
        lags     : int, optional, default=40
                   Number of lags to consider.
        alpha    : float, optional, default=0.05
                   Significance level for the confidence intervals.

    Returns:
        None
    """
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    plot_acf(data, lags=lags, alpha=alpha, ax=ax[0])
    plot_pacf(data, lags=lags, alpha=alpha, ax=ax[1])
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


