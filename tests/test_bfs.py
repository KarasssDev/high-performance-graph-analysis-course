from typing import List, Tuple

import pygraphblas as grb
from project import graphblas_utils
from project import bfs


def test_bfs_shortest_path(data):
    node_count: int = data["node_count"]
    edge_list: List[Tuple[int, int]] = data["edge_list"]
    expected: List[int] = data["expected"]
    graph: grb.Matrix = graphblas_utils.adjacency_matrix_from_edge_list(
        node_count, edge_list
    )
    expected_vector: grb.Vector = grb.Vector.from_list(expected)

    actual_vector: grb.Vector = bfs.bfs_shortest_path(graph, 0)

    assert expected_vector.iseq(actual_vector)


def test_bfs_multiple_source_parents(data):
    node_count: int = data["node_count"]
    edge_list: List[Tuple[int, int]] = data["edge_list"]
    start_vertices: List[int] = data["start_nodes"]
    expected_data: List[List[object]] = data["expected"]
    expected: List[Tuple[int, List[int]]] = [
        (start, parents) for [start, parents] in expected_data
    ]
    graph: grb.Matrix = graphblas_utils.adjacency_matrix_from_edge_list(
        node_count, edge_list
    )

    actual: List[Tuple[int, List[int]]] = bfs.bfs_multiple_source_parents(
        graph, start_vertices
    )

    assert actual == expected
