from typing import List, Tuple, TypeVar, Optional
import pygraphblas as grb

T = TypeVar("T")

__all__ = ["adjacency_matrix_from_edge_list", "label_matrix_from_edge_list"]

_GRAPHBLAS_ELEMENT_TYPES: List[type] = [
    grb.INT8,
    grb.INT16,
    grb.INT32,
    grb.INT64,
    grb.UINT8,
    grb.UINT16,
    grb.UINT32,
    grb.UINT64,
    grb.FC32,
    grb.FC64,
    grb.FP32,
    grb.FP64,
    grb.BOOL,
]


def undirected_adjacency_matrix_from_edge_list(
    node_count: int,
    adjacency_list: List[Tuple[int, int]],
    preferred_type: type = grb.UINT8,
) -> grb.Matrix:
    """

    Parameters
    ----------
    node_count: int
        Count of nodes in graph
    adjacency_list: List[Tuple[int, int]]
        List of edges with elements like (source, destination)
    preferred_type:
        GraphBLAS type of matrix elements

    Returns
    -------
    Matrix
        Undirected graph adjacency matrix
    """
    edge_list: List[Tuple[int, bool, int]] = [
        (source, True, destination) for (source, destination) in adjacency_list
    ] + [(destination, True, source) for (source, destination) in adjacency_list]
    return label_matrix_from_edge_list(node_count, edge_list, preferred_type)


def adjacency_matrix_from_edge_list(
    node_count: int,
    adjacency_list: List[Tuple[int, int]],
    preferred_type: type = grb.UINT8,
) -> grb.Matrix:
    """

    Parameters
    ----------
    node_count: int
        Count of nodes in graph
    adjacency_list: List[Tuple[int, int]]
        List of edges with elements like (source, destination)
    preferred_type:
        GraphBLAS type of matrix elements

    Returns
    -------
    Matrix
        Graph adjacency matrix
    """
    edge_list: List[Tuple[int, bool, int]] = [
        (source, True, destination) for (source, destination) in adjacency_list
    ]
    return label_matrix_from_edge_list(node_count, edge_list, preferred_type)


def label_matrix_from_edge_list(
    node_count: int,
    edge_list: List[Tuple[int, Optional[T], int]],
    label_type: type = grb.UINT8,
    default_label: T = 0,
) -> grb.Matrix:
    """

    Parameters
    ----------
    node_count: int
        Count of nodes in graph
    edge_list: List[Tuple[int, Optional[T], int]]
        List of edges with elements like (source, label, destination)
    label_type: type
        GraphBLAS type of labels
    default_label: T
        Label which used if label in edge_list is None

    Returns
    -------
    Matrix
        Graph label matrix
    """
    assert label_type in _GRAPHBLAS_ELEMENT_TYPES

    matrix = grb.Matrix.sparse(label_type, nrows=node_count, ncols=node_count)
    for source, label, destination in edge_list:
        if label is not None:
            matrix[source, destination] = label
        else:
            matrix[source, destination] = default_label
    return matrix
