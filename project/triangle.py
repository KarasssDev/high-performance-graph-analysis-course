import pygraphblas as grb
from typing import List, Tuple


def count_triangles_for_each_vertex(matrix: grb.Matrix) -> List[int]:
    """
    Parameters
    ----------
    matrix: Matrix
        Undirected graph adjacency matrix

    Returns
    -------
    List[int]
        Count of triangles which contains corresponding node
    """
    matrix.assign_scalar(
        False, mask=grb.Matrix.identity(grb.BOOL, matrix.nrows) & matrix
    )
    result = matrix.mxm(matrix, grb.UINT64.PLUS_TIMES, mask=matrix).reduce_vector()
    result.assign_scalar(0, mask=result, desc=grb.descriptor.C)
    return [i // 2 for i in result.vals]


def count_triangles_cohen(matrix: grb.Matrix) -> int:
    """
    Parameters
    ----------
    matrix: Matrix
        Undirected graph adjacency matrix

    Returns
    -------
    int
        Count of triangles in the graph
    """
    matrix_lower_triangle = matrix.tril(-1)
    matrix_upper_triangle = matrix.triu(1)
    result = (
        matrix_lower_triangle.mxm(
            matrix_upper_triangle,
            grb.UINT64.PLUS_TIMES,
            mask=matrix_lower_triangle | matrix_upper_triangle,
        ).reduce_int()
        // 2
    )
    return result


def count_triangles_sandia(matrix: grb.Matrix) -> int:
    """
    Parameters
    ----------
    matrix: Matrix
        Undirected graph adjacency matrix

    Returns
    -------
    int
        Count of triangles in the graph
    """
    matrix_lower_triangle = matrix.tril(-1)
    result = matrix_lower_triangle.mxm(
        matrix_lower_triangle.transpose(),
        grb.UINT64.PLUS_TIMES,
        mask=matrix_lower_triangle,
    ).reduce_int()
    return result
