from typing import List, Tuple

import pygraphblas as grb
from project import graphblas_utils
from project import triangle


def _test_count_triangle(data, algorithm):
    node_count: int = data["node_count"]
    edge_list: List[Tuple[int, int]] = data["edge_list"]
    expected = data["expected"]
    graph: grb.Matrix = graphblas_utils.undirected_adjacency_matrix_from_edge_list(
        node_count, edge_list
    )
    actual: grb.Vector = algorithm(graph)

    assert expected == actual


def test_count_triangles_cohen(data):
    _test_count_triangle(data, triangle.count_triangles_cohen)


def test_count_triangles_sandia(data):
    _test_count_triangle(data, triangle.count_triangles_sandia)


def test_count_triangles_for_each_vertex(data):
    _test_count_triangle(data, triangle.count_triangles_for_each_vertex)
