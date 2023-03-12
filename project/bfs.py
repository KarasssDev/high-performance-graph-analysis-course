import pygraphblas as grb

__all__ = ["bfs_shortest_path"]


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
    front = grb.Vector.sparse(grb.INT64, matrix.nrows)
    visited = grb.Vector.sparse(grb.BOOL, matrix.nrows)

    visited[start_vertex] = True
    current_depth = 1

    while visited.reduce_bool() and current_depth <= matrix.nrows:
        front.assign_scalar(current_depth, mask=visited)
        front.vxm(matrix, mask=front, out=visited, desc=grb.descriptor.RC)
        current_depth += 1

    minus_ones_vector = grb.Vector.sparse(grb.INT64, matrix.nrows)
    minus_ones_vector.assign_scalar(-1)
    front += minus_ones_vector

    return front
