from slade.query.prometheus_querier import PrometheusQuerier


class LocustQuerier(PrometheusQuerier):
    def __init__(self, endpoint=None):
        super().__init__(endpoint)

    """
    Get the number of requests per second for a specific endpoint
    if endpoint_name is None, it will return the number of requests per second for all endpoints
    This function excludes the aggregated endpoint
    """

    def get_avg_response_time(self, namespace, endpoint_name, _from, _to, step='1m'):
        if endpoint_name is not None:
            query = 'locust_requests_avg_response_time{ namespace="' + namespace + '", name="' + endpoint_name + '"}'
        else:
            query = 'locust_requests_avg_response_time{ namespace="' + namespace + '", name!="Aggregated", name=~".*"}'

        result = self.make_query_range(query, _from, _to, step)
        return result

    def get_locust_requests_per_second(self, namespace, endpoint_name, _from, _to, step='1m'):
        if endpoint_name is not None:
            query = 'locust_requests_per_second{ namespace="' + namespace + '", name="' + endpoint_name + '"}'
        else:
            query = 'locust_requests_per_second{ namespace="' + namespace + '", name!="Aggregated", name=~".*"}'

        result = self.make_query_range(query, _from, _to, step)
        return result

    def get_locust_current_fail_per_sec(self, namespace, endpoint_name, _from, _to, step='1m'):
        if endpoint_name is not None:
            query = 'locust_fail_per_sec{ namespace="' + namespace + '", name="' + endpoint_name + '"}'
        else:
            query = 'locust_fail_per_sec{ namespace="' + namespace + '", name!="Aggregated", name=~".*"}'

        result = self.make_query_range(query, _from, _to, step)
        return result

        # result = self.make_query_range(query, _from, _to, step)
        # print(result)
        # if not result:
        #     return 0
        # return [[x[0], float(x[1])] for x in result[0]['values']]

    def format_metric_name(self, metric_info) -> str:
        path = metric_info.get('name', 'root').replace("/", "_").strip("_")
        if path == "":
            path = "root"
        metric_type = metric_info.get('__name__', '').split('_')[-1]
        method = metric_info.get('method', 'NO_METHOD').lower()  # Default 'NO_METHOD' if not present
        return f"locust_{metric_type}_{path}_{method}"
