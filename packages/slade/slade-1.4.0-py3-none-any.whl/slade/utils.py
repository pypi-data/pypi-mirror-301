import datetime
from datetime import datetime
import logging
from typing import Optional, Dict


def parse_base_query(
        metric_name: str,
        match_exact_labels: Optional[Dict[str, str]] = None,
        match_regex_labels: Optional[Dict[str, str]] = None,
        exclude_exact_labels: Optional[Dict[str, str]] = None,
        exclude_regex_labels: Optional[Dict[str, str]] = None
) -> str:
    """
    Parse the base query for a given metric, including exact matches, regex matches, and exclusions.

    Args:
        metric_name (str): The name of the metric to query.
        match_exact_labels (Optional[Dict[str, str]], optional): Labels to match exactly. Defaults to None.
        match_regex_labels (Optional[Dict[str, str]], optional): Labels to match with regex. Defaults to None.
        exclude_exact_labels (Optional[Dict[str, str]], optional): Labels to exclude exactly. Defaults to None.
        exclude_regex_labels (Optional[Dict[str, str]], optional): Labels to exclude with regex. Defaults to None.

    Returns:
        str: The constructed base query string.
    """
    label_clauses = []

    if match_exact_labels:
        for label, value in match_exact_labels.items():
            label_clauses.append(f'{label}="{value}"')

    if match_regex_labels:
        for label, value in match_regex_labels.items():
            label_clauses.append(f'{label}=~"{value}"')

    if exclude_exact_labels:
        for label, value in exclude_exact_labels.items():
            label_clauses.append(f'{label}!="{value}"')

    if exclude_regex_labels:
        for label, value in exclude_regex_labels.items():
            label_clauses.append(f'{label}!~"{value}"')

    label_clause_str = ', '.join(label_clauses)
    return f'{metric_name}{{{label_clause_str}}}'


def set_logger(name):
    logger = logging.Logger(name, level=logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def cpu_str_to_float(cpu_str):
    if cpu_str.endswith('m'):
        return float(cpu_str.rstrip('m')) / 1000
    elif cpu_str.endswith('Mi'):
        return float(cpu_str.rstrip('Mi')) / 1000
    else:
        return float(cpu_str)


def to_unix_timestamp(value):
    """
    Converts the input value (either a Unix timestamp or date string) to a Unix timestamp.
    :param value: Unix timestamp (int) or date string (str)
    :return: Unix timestamp (int)
    """
    if isinstance(value, (int, float)):  # Assume it's already a Unix timestamp
        return int(value)
    elif isinstance(value, str):  # Parse date string to Unix timestamp
        try:
            # Use strptime with the specific format
            dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')  # Adjust format if necessary
            return int(dt.timestamp())
        except ValueError:
            raise ValueError(f"Invalid date format: {value}")
    else:
        raise TypeError("Input must be a Unix timestamp (int) or ISO 8601 date string (str)")


def get_utc_now():
    """Return the current time in UTC."""
    return datetime.datetime.utcnow()


def get_time_delta(minutes):
    """Return a time delta object for the specified number of minutes."""
    return datetime.timedelta(minutes=minutes)


def format_rfc3339(dt):
    """Convert a datetime object into RFC3339 format."""
    return dt.isoformat() + "Z"


def get_past_time(minutes):
    """Return the time 'minutes' minutes ago, in RFC3339 format."""
    now = get_utc_now()
    past_time = now - get_time_delta(minutes)
    return format_rfc3339(past_time)
