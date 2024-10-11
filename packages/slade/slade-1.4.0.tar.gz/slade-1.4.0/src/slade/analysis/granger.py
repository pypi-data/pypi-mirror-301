import warnings

warnings.filterwarnings('ignore')

from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd
import numpy as np


def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False, maxlag=3):
    """
    Check Granger Causality for all combinations of time series variables.

    The resulting matrix has rows as response variables (Y) and columns as predictor variables (X).
    Values in the matrix are P-values from the Granger causality tests. A P-value < 0.05 indicates
    that the null hypothesis (that X does not Granger-cause Y) can be rejected.

    Parameters:
        data      : pd.DataFrame
                    Time series data with variables as columns.
        variables : list of str
                    Names of the time series variables.
        test      : str, optional, default='ssr_chi2test'
                    Type of Granger causality test ('ssr_chi2test', 'lrtest', etc.).
        verbose   : bool, optional, default=False
                    If True, print test details.
        maxlag    : int, optional, default=3
                    Maximum lag to consider.

    Returns:
        pd.DataFrame
            Matrix of P-values with rows as response variables (Y) and columns as predictors (X).
    """
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag)
            p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(maxlag)]
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            df.loc[r, c] = round(min_p_value, 2)
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    return df
