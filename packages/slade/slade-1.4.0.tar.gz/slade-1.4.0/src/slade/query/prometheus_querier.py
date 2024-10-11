import requests

from slade.utils import set_logger, to_unix_timestamp
from slade.exceptions import QueryFailedException

logger = set_logger(__name__)


class PrometheusQuerier:
    """
    Base class for querying DataSource.
    :parameter endpoint: str, URL of the Prometheus server.
    """

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def prometheus_is_up(self):
        try:
            resp = requests.get(self.endpoint)
            return resp.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f'request failed with code {e.response.status_code}')
        except Exception as e:
            logger.error(f'generic error: {e}')

    def make_query_range(self, query, _from, _to, step='1m'):
        """
        Query Prometheus server with a range.
        :param query: is the query to be executed.
        :param _from: start time in Unix timestamp or date string.
        :param _to: end time in Unix timestamp or date string.
        :param step: step of the range.
        :return: list of results.
        """
        try:
            # Convert _from and _to to Unix timestamps if necessary
            start_time = to_unix_timestamp(_from)
            end_time = to_unix_timestamp(_to)

            resp = requests.get(
                url=f'{self.endpoint}/api/v1/query_range',
                params={
                    'query': query,
                    'start': start_time,
                    'end': end_time,
                    'step': step,
                }
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get('status') != 'success':
                raise QueryFailedException(f'Query "{query}" failed with status {data["status"]}')

            return data['data']['result']

        except QueryFailedException as qfe:
            logger.error(f"Prometheus query failed: {str(qfe)}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f'Request exception: {str(e)}')
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
        except Exception as e:
            logger.error(f'Generic error: {str(e)}')

    def make_query(self, query):
        """
        Query Prometheus server.
        :param query:
        :return:
        """
        try:
            resp = requests.get(
                url=f'{self.endpoint}/api/v1/query',
                params={'query': query}
            )
            resp.raise_for_status()
            data = resp.json()

            if data['status'] != 'success':
                raise QueryFailedException(f'query {query} failed')

            return data['data']['result']

        except requests.exceptions.RequestException as e:
            logger.error(f'request failed with code {e.response.status_code}')
        except Exception as e:
            logger.error(f'generic error: {e}')

    def get_all_metric(self):
        """
        Get all metrics from Prometheus server.
        :return: list of metrics.
        """
        try:
            resp = requests.get(
                url=f'{self.endpoint}/api/v1/label/__name__/values'
            )
            resp.raise_for_status()
            data = resp.json()

            if data['status'] != 'success':
                raise QueryFailedException(f'query failed')
            return data['data']
        except requests.exceptions.RequestException as e:
            logger.error(f'request failed with code {e.response.status_code}')
        except Exception as e:
            logger.error(f'generic error: {e}')
