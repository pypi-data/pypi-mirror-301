from typing import Dict

from slade.query.prometheus_querier import PrometheusQuerier
from slade.utils import parse_base_query

SPAN_DURATION_QUERY = ('increase(duration_milliseconds_sum{{service_name=~\"{}\", span_name=~\".*\"}}[5m]) / increase('
                       'duration_milliseconds_count{{service_name=~\"{}\", span_name=~\".*\"}}[5m])')


class TracerQuerier(PrometheusQuerier):
    def __init__(self, endpoint):
        super().__init__(endpoint)

    def get_span_duration(
            self,
            match_exact_labels: Dict,
            match_regex_labels: Dict=None,
            exclude_exact_labels: Dict=None,
            interval='5m',
            _from=None, _to=None, step='1m'):
        num_base_query = parse_base_query(
            metric_name='duration_milliseconds_sum',
            match_exact_labels=match_exact_labels,
            match_regex_labels=match_regex_labels,
            exclude_regex_labels=exclude_exact_labels,
        )

        den_base_query = parse_base_query(
            metric_name='duration_milliseconds_count',
            match_exact_labels=match_exact_labels,
            match_regex_labels=match_regex_labels,
            exclude_regex_labels=exclude_exact_labels,
        )
        query = f'increase({num_base_query}[{interval}]) / increase({den_base_query}[{interval}])'
        print(query)
        return self.make_query_range(query, _from, _to, step)
