from typing import List, Tuple, TypeVar, Optional

import pytest
import pygraphblas as grb
from project import graphblas_utils

T = TypeVar("T")


def test_label_matrix_from_edge_list(data):
    node_count: int = data["node_count"]
    edge_list: List[Tuple[int, Optional[T], int]] = data["edge_list"]
    label_type: type = data["label_type"]
    default_label: T = data["default_label"]

    matrix: grb.Matrix = graphblas_utils.label_matrix_from_edge_list(
        node_count, edge_list, label_type, default_label
    )

    assert matrix.ncols == node_count and matrix.nrows == node_count
    assert matrix.gb_type == grb.Matrix.sparse(label_type).gb_type

    for source, label, destination in edge_list:
        if label is not None:
            assert matrix[source, destination] == label
        else:
            assert matrix[source, destination] == default_label


def test_adjacency_matrix_from_edge_list(data):
    node_count: int = data["node_count"]
    edge_list: List[Tuple[int, int]] = data["edge_list"]
    preferred_type: type = data["label_type"]

    matrix: grb.Matrix = graphblas_utils.adjacency_matrix_from_edge_list(
        node_count, edge_list, preferred_type
    )

    assert matrix.ncols == node_count and matrix.nrows == node_count
    assert matrix.gb_type == grb.Matrix.sparse(preferred_type).gb_type

    for source, destination in edge_list:
        assert matrix[source, destination] == 1
