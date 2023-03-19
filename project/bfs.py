import pygraphblas as grb
from typing import List, Tuple

__all__ = ["bfs_shortest_path", "bfs_multiple_source_parents"]


def bfs_shortest_path(matrix: grb.Matrix, start_vertex: int) -> grb.Vector:
    """
    Parameters
    ----------
    matrix: Matrix
        Graph adjacency matrix
    start_vertex: int
        Starting position

    Returns
    -------
    Vector
        Vector of distance to all other nodes.
        If node unreachable distance will be equal to -1
    """
    vertices_count = matrix.nrows
    front = grb.Vector.sparse(grb.INT64, vertices_count)
    visited = grb.Vector.sparse(grb.BOOL, vertices_count)
    visited[start_vertex] = True
    current_depth = 1

    while visited.reduce_bool() and current_depth <= vertices_count:
        front.assign_scalar(current_depth, mask=visited)
        front.vxm(matrix, mask=front, out=visited, desc=grb.descriptor.RC)
        current_depth += 1

    minus_ones_vector = grb.Vector.sparse(grb.INT64, vertices_count)
    minus_ones_vector.assign_scalar(-1)
    front += minus_ones_vector

    return front


def bfs_multiple_source_parents(
    matrix: grb.Matrix, start_vertices: List[int]
) -> List[Tuple[int, List[int]]]:
    """
    Parameters
    ----------
    matrix: Matrix
        Graph adjacency matrix
    start_vertices: List[int]
        Starting positions

    Returns
    -------
    List[Tuple[int, List[int]]]
        List of pairs where
        first element described start vertex,
        second element is List of parents where each element correspond
        parent of vertex in the shortest path from start vertex.
        If vertex is start parent will be equal to -1.
        If vertex unreachable parent will be equal to -2.
    """
    start_vertices_count = len(start_vertices)
    graph_vertices_count = matrix.nrows
    front = grb.Matrix.sparse(grb.INT64, start_vertices_count, graph_vertices_count)
    result = grb.Matrix.sparse(grb.INT64, start_vertices_count, graph_vertices_count)
    for i, start in enumerate(start_vertices):
        front[i, start] = -1

    while front.nvals != 0:
        result.assign(front, mask=front, desc=grb.descriptor.S)
        front.apply(grb.INT64.POSITIONJ, out=front)
        front.mxm(
            matrix,
            semiring=grb.INT64.MIN_FIRST,
            out=front,
            mask=result,
            desc=grb.descriptor.RSC,
        )

    result.assign_scalar(-2, mask=result, desc=grb.descriptor.S & grb.descriptor.C)

    return [(start, list(result[i].vals)) for i, start in enumerate(start_vertices)]
