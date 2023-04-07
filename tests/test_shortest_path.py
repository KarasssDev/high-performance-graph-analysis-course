from typing import List, Tuple

import pygraphblas as grb
from project import graphblas_utils
from project import shortest_path


def _to_float_inf(lst: List[float]):
    def to_inf(x):
        if x == "inf":
            return float("inf")
        return x

    return list(map(to_inf, lst))


def assert_distance_equals(
    expected: List[Tuple[int, List[float]]], actual: List[Tuple[int, List[float]]]
):
    assert len(expected) == len(actual)
    for i in range(len(expected)):
        expected_v, expected_d = expected[i]
        actual_v, actual_d = actual[i]
        assert expected_v == actual_v
        assert len(expected_d) == len(actual_d)
        for j in range(len(expected_d)):
            if expected_d[j] == float("inf"):
                assert actual_d[j] == float("inf")
            else:
                assert abs(expected_d[j] - actual_d[j]) < 1e-7


def test_multi_source_shortest_path_bellman_ford(data):
    node_count: int = data["node_count"]
    starts: List[int] = data["starts"]
    edge_list: List[Tuple[int, float, int]] = data["edge_list"]
    expected: List[Tuple[int, List[float]]] = [
        (v, _to_float_inf(d)) for [v, d] in data["expected"]
    ]
    graph: grb.Matrix = graphblas_utils.label_matrix_from_edge_list(
        node_count, edge_list, grb.FP64
    )

    actual: List[
        Tuple[int, List[float]]
    ] = shortest_path.multi_source_shortest_path_bellman_ford(graph, starts)

    assert_distance_equals(expected, actual)


def test_shortest_path_floyd_warshall(data):
    node_count: int = data["node_count"]
    edge_list: List[Tuple[int, float, int]] = data["edge_list"]
    expected: List[Tuple[int, List[float]]] = [
        (v, _to_float_inf(d)) for [v, d] in data["expected"]
    ]
    graph: grb.Matrix = graphblas_utils.label_matrix_from_edge_list(
        node_count, edge_list, grb.FP64
    )

    actual: List[Tuple[int, List[float]]] = shortest_path.shortest_path_floyd_warshall(
        graph
    )

    assert_distance_equals(expected, actual)
