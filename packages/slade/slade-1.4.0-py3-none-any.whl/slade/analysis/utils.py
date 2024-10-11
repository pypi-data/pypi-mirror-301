import pandas as pd


def raw_data_to_df(results):
    rows = []
    for result in results:
        metric = result.get('metric', {})
        values = result.get('values', [])

        for value in values:
            timestamp, val = value
            row = {
                'timestamp': pd.to_datetime(int(timestamp), unit='s'),  # Convert UNIX timestamp to datetime
                'value': float(val)
            }
            # Add metric labels to the row
            row.update(metric)
            rows.append(row)

        # Create a DataFrame from the rows
    df = pd.DataFrame(rows)
    return df


def raw_data_to_dfs(results):
    """
    Converts Prometheus raw results into a dictionary of DataFrames,
    with each DataFrame corresponding to a unique metric dimension.

    :param results: The list of raw Prometheus results containing metric labels and values.
    :return: A dictionary where keys are metric labels (tuple of label key-value pairs) and values are DataFrames.
    """
    dfs = {}  # Dictionary to store DataFrames for each unique metric dimension

    for result in results:
        metric = result.get('metric', {})
        values = result.get('values', [])

        # Convert the metric dictionary into a tuple of sorted key-value pairs to use as a dictionary key
        metric_key = tuple(sorted(metric.items()))

        # Prepare a list to store rows for this particular metric
        rows = []

        for value in values:
            timestamp, val = value
            row = {
                'timestamp': pd.to_datetime(int(timestamp), unit='s'),  # Convert UNIX timestamp to datetime
                'value': float(val)
            }
            # Add metric labels to the row
            row.update(metric)
            rows.append(row)

        # Create a DataFrame for this particular metric key
        df = pd.DataFrame(rows)

        # Store the DataFrame in the dictionary
        dfs[metric_key] = df

    return dfs
