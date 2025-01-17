import pygraphblas as grb
import heapq
import networkx as nx
from typing import List, Tuple, Hashable, Dict

__all__ = [
    "multi_source_shortest_path_bellman_ford",
    "single_source_shortest_path_bellman_ford",
    "shortest_path_floyd_warshall",
    "shortest_path_dijkstra",
]


def multi_source_shortest_path_bellman_ford(
    matrix: grb.Matrix, starts: List[int]
) -> List[Tuple[int, List[float]]]:
    """
    Parameters
    ----------
    matrix: Matrix
        Weighted graph adjacency matrix

    starts: List[int]
        Indices of start vertices
    Returns
    -------
    List[Tuple[int, List[float]]]
        Distances from each start vertex to others.
        Distance will be float('inf') if vertex unreachable.
    """
    num_vertices = matrix.nrows
    num_starts = len(starts)

    matrix.assign_scalar(0.0, mask=grb.Matrix.identity(grb.FP64, num_vertices))
    distances = grb.Matrix.sparse(grb.FP64, num_starts, num_vertices)
    for i, start in enumerate(starts):
        distances[i, start] = 0.0

    for _ in range(num_vertices):
        current_distances = distances
        distances = distances.mxm(matrix, grb.FP64.MIN_PLUS)
        if current_distances.iseq(distances):
            distances.assign_scalar(
                float("inf"), mask=distances, desc=grb.descriptor.C & grb.descriptor.S
            )
            return [(start, list(distances[i].vals)) for i, start in enumerate(starts)]


def single_source_shortest_path_bellman_ford(
    matrix: grb.Matrix, start: int
) -> List[float]:
    """
    Parameters
    ----------
    matrix: Matrix
        Weighted graph adjacency matrix

    start: int
        Index of start vertex
    Returns
    -------
    List[float]
        Distances from start vertex to others.
        Distance will be float('inf') if vertex unreachable.
    """
    [(_, distances)] = multi_source_shortest_path_bellman_ford(matrix, [start])
    return distances


def shortest_path_floyd_warshall(matrix: grb.Matrix) -> List[Tuple[int, List[float]]]:
    """
    Parameters
    ----------
    matrix: Matrix
        Weighted graph adjacency matrix
    Returns
    -------
    List[Tuple[int, List[float]]]
        Distances from each vertex to others.
        Distance will be float('inf') if vertex unreachable.
    """
    distances = matrix
    num_vertices = matrix.nrows
    distances.assign_scalar(0.0, mask=grb.Matrix.identity(grb.FP64, num_vertices))

    for k in range(num_vertices):
        distances.extract_matrix(col_index=k).mxm(
            distances.extract_matrix(row_index=k),
            grb.FP64.MIN_PLUS,
            accum=grb.FP64.MIN,
            out=distances,
        )

    distances.assign_scalar(
        float("inf"), mask=distances, desc=grb.descriptor.C & grb.descriptor.S
    )
    return [(i, list(distances[i].vals)) for i in range(num_vertices)]


def shortest_path_dijkstra(graph: nx.Graph, start: Hashable) -> Dict[Hashable, float]:
    """
    Parameters
    ----------
    graph: Graph
        Weighted graph

    start: int
        Start vertex
    Returns
    -------
    Dict[Hashable, float]
        Distances from start vertex to others.
        Distance will be float('inf') if vertex unreachable.
    """
    distances = {node: float("inf") for node in graph.nodes}
    distances[start] = 0

    queue = [(0, start)]

    while len(queue) != 0:
        distance, node = heapq.heappop(queue)

        if distance > distances[node]:
            continue

        for neighbor in graph.neighbors(node):
            new_distance = distances[node] + graph[node][neighbor]["weight"]

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(queue, (new_distance, neighbor))

    return distances
