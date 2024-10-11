from typing import Union, Any, List

from slade.query.prometheus_querier import PrometheusQuerier
from slade.utils import parse_base_query


class DeploymentQuerier(PrometheusQuerier):
    def __init__(self, endpoint: str):
        super().__init__(endpoint)

    def get_deployment_cpu_usage(
            self, namespace: str, deployment_name: str,
            _from: Union[int, str] = None, _to: Union[int, str] = None, step: str = '1m',
    ) -> Union[List[Any], List[List[float]]]:
        """
        Get the CPU usage range for a specific deployment within a namespace over a given time range.
        If _from and _to are not provided, the query will return the current (last) CPU usage for the deployment.
        Args:
            namespace (str): The Kubernetes namespace.
            deployment_name (str): The name of the deployment.
            _from (Union[int, str]): The start time for the query range.
            _to (Union[int, str]): The end time for the query range.
            step (str, optional): The step duration for the query. Defaults to '1m'.
        Returns:
            List[Tuple[float, float]]: A list of tuples containing the timestamp and CPU usage.
        """

        if _from is None or _to is None:
            base_query = parse_base_query('node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate',
                                          {'namespace': namespace},
                                          {'pod': f'{deployment_name}-.*'},
                                          {'container': 'istio-proxy'})
            cpu_query = f'sum({base_query})'
            result = self.make_query(cpu_query)
            if not result:
                return []
            return result[0]['value']

        else:
            base_query = parse_base_query('container_cpu_usage_second_total',
                                          {'namespace': namespace},
                                          {'pod': f'{deployment_name}-.*'},
                                          exclude_exact_labels={'container': 'istio-proxy'},
                                          exclude_regex_labels={'image': ''})

            cpu_query = f'sum(rate({base_query}[5m]))'
            result = self.make_query_range(cpu_query, _from, _to, step)
            if not result:
                return []
            return [[float(timestamp), float(value)] for timestamp, value in result[0]['values']]

    def get_deployment_mem_usage(
            self, namespace: str, deployment_name: str,
            _from: Union[int, str] = None, _to: Union[int, str] = None, step: str = '1m'
    ) -> Union[List[Any], List[List[float]]]:
        """
        Get the memory usage range for a specific deployment within a namespace over a given time range.
        If _from and _to are not provided, the query will return the current (last) memory usage for the deployment.

        Args:
            namespace (str): The Kubernetes namespace.
            deployment_name (str): The name of the deployment.
            _from (Union[int, str]): The start time for the query range.
            _to (Union[int, str]): The end time for the query range.
            step (str, optional): The step duration for the query. Defaults to '1m'.
            exclude_containers (List[str], optional): List of container names to exclude from the query. Defaults to [].

        Returns:
            List[Tuple[float, float]]: A list of tuples containing the timestamp and memory usage.
        """

        if _from is None or _to is None:
            base_query = parse_base_query('container_memory_working_set_bytes',
                                          {'namespace': namespace, 'cluster': ''},
                                          {'pod': f'{deployment_name}-.*'},
                                          exclude_exact_labels={'container': '', 'image': ''})
            mem_query = f'sum({base_query})'
            result = self.make_query(mem_query)
            if not result:
                return []
            return result[0]['value']

        base_query = parse_base_query('container_memory_usage_bytes',
                                      {'namespace': namespace},
                                      {'pod': f'{deployment_name}-.*'},
                                      exclude_exact_labels={'container': 'istio-proxy'},
                                      exclude_regex_labels={'image': ''})

        mem_query = f'sum(rate({base_query}[5m]))'
        result = self.make_query_range(mem_query, _from, _to, step)
        if not result:
            return []
        return [[float(timestamp), float(value)] for timestamp, value in result[0]['values']]

    def get_deployment_bw_tx_range(
            self, namespace: str, deployment_name: str,
            _from: Union[int, str], _to: Union[int, str], step: str = '1m'
    ) -> Union[List[Any], List[List[float]]]:
        """
        Get the transmit bandwidth range for a specific deployment within a namespace over a given time range.
        Results are returned in bytes per second.

        Args:
            namespace (str): The Kubernetes namespace.
            deployment_name (str): The name of the deployment.
            _from (Union[int, str]): The start time for the query range.
            _to (Union[int, str]): The end time for the query range.
            step (str, optional): The step duration for the query. Defaults to '1m'.
        Returns:
            List[Tuple[float, float]]: A list of tuples containing the timestamp and transmit bandwidth.
        """
        base_query = parse_base_query('container_network_transmit_bytes_total',
                                      {'namespace': namespace, 'cluster': ''},
                                      {'pod': f'{deployment_name}-.*'},
                                      exclude_exact_labels={'container': 'istio-proxy'},
                                      exclude_regex_labels={'image': ''})

        net_query = f'sum(irate({base_query}[5m]))'
        result = self.make_query_range(net_query, _from, _to, step)
        if not result:
            return []
        return [[float(timestamp), float(value)] for timestamp, value in result[0]['values']]

    def get_deployment_bw_rx_range(
            self, namespace: str, deployment_name: str,
            _from: Union[int, str], _to: Union[int, str], step: str = '1m'
    ) -> Union[List[Any], List[List[float]]]:
        """
        Get the receive bandwidth range for a specific deployment within a namespace over a given time range.
        Results are returned in bytes per second.

        Args:
            namespace (str): The Kubernetes namespace.
            deployment_name (str): The name of the deployment.
            _from (Union[int, str]): The start time for the query range.
            _to (Union[int, str]): The end time for the query range.
            step (str, optional): The step duration for the query. Defaults to '1m'.
        Returns:
            List[Tuple[float, float]]: A list of tuples containing the timestamp and transmit bandwidth.
        """
        base_query = parse_base_query('container_network_receive_bytes_total',
                                      {'namespace': namespace, 'cluster': ''},
                                      {'pod': f'{deployment_name}-.*'},
                                      exclude_exact_labels={'container': 'istio-proxy'},
                                      exclude_regex_labels={'image': ''})

        net_query = f'sum(irate({base_query}[5m]))'
        result = self.make_query_range(net_query, _from, _to, step)
        if not result:
            return []
        return [[float(timestamp), float(value)] for timestamp, value in result[0]['values']]

    def get_deployment_pkt_tx_range(
            self, namespace: str, deployment_name: str,
            _from: Union[int, str], _to: Union[int, str], step: str = '1m'
    ) -> Union[List[Any], List[List[float]]]:
        """
        Get the transmit packet range for a specific deployment within a namespace over a given time range.
        Results are returned in packets per second.

        Args:
            namespace (str): The Kubernetes namespace.
            deployment_name (str): The name of the deployment.
            _from (Union[int, str]): The start time for the query range.
            _to (Union[int, str]): The end time for the query range.
            step (str, optional): The step duration for the query. Defaults to '1m'.
        Returns:
            List[Tuple[float, float]]: A list of tuples containing the timestamp and transmit bandwidth.
        """
        base_query = parse_base_query('container_network_transmit_packets_total',
                                      {'namespace': namespace, 'cluster': ''},
                                      {'pod': f'{deployment_name}-.*'},
                                      exclude_exact_labels={'container': 'istio-proxy'},
                                      )

        net_query = f'sum(irate({base_query}[5m]))'
        result = self.make_query_range(net_query, _from, _to, step)
        if not result:
            return []
        return [[float(timestamp), float(value)] for timestamp, value in result[0]['values']]

    def get_deployment_pkt_rx_range(
            self, namespace: str, deployment_name: str,
            _from: Union[int, str], _to: Union[int, str], step: str = '1m'
    ) -> Union[List[Any], List[List[float]]]:
        """
        Get the receive packet range for a specific deployment within a namespace over a given time range.
        Results are returned in packets per second.

        Args:
            namespace (str): The Kubernetes namespace.
            deployment_name (str): The name of the deployment.
            _from (Union[int, str]): The start time for the query range.
            _to (Union[int, str]): The end time for the query range.
            step (str, optional): The step duration for the query. Defaults to '1m'.
        Returns:
            List[Tuple[float, float]]: A list of tuples containing the timestamp and transmit bandwidth.
        """
        base_query = parse_base_query('container_network_receive_packets_total',
                                      {'namespace': namespace, 'cluster': ''},
                                      {'pod': f'{deployment_name}-.*'},
                                      exclude_exact_labels={'container': 'istio-proxy'},
                                      )

        net_query = f'sum(irate({base_query}[5m]))'
        result = self.make_query_range(net_query, _from, _to, step)
        if not result:
            return []
        return [[float(timestamp), float(value)] for timestamp, value in result[0]['values']]

    def get_deployment_cpu_limit(self, namespace, deployment):
        base_query = parse_base_query('kube_pod_container_resource_limits',
                                      {'namespace': namespace},
                                      {'pod': f'{deployment}-.*'},
                                      exclude_exact_labels={'container': 'istio-proxy', 'resource': 'memory'})
        cpu_query = f'sum({base_query})'
        result = self.make_query(cpu_query)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_mem_limit(self, namespace, deployment):
        cpu = 'sum(kube_pod_container_resource_limits{container!="istio-proxy", namespace="' + namespace + '", pod=~"' + deployment + '-.*", resource="memory"})'
        result = self.make_query(cpu)
        if not result:
            return 0
        return float(result[0]['value'][1])
