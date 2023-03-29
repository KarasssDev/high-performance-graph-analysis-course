import json

import pygraphblas as grb
import pathlib


def load_from_file(file_name: str):
    test_resource_path = (
        pathlib.Path(__file__).parent.absolute() / "resource" / file_name
    ).with_suffix(".json")
    return json.loads(test_resource_path.read_text())


test_adjacency_matrix_from_edge_list_data = [
    {
        "name": "Empty graph",
        "node_count": 0,
        "edge_list": [],
        "label_type": grb.UINT8,
    },
    {
        "name": "One node graph",
        "node_count": 1,
        "edge_list": [],
        "label_type": grb.UINT8,
    },
    {
        "name": "Complete graph",
        "node_count": 2,
        "edge_list": [(0, 0), (0, 1), (1, 0), (1, 1)],
        "label_type": grb.UINT8,
    },
    {
        "name": "Huge graph",
        "node_count": 10000,
        "edge_list": [],
        "label_type": grb.UINT8,
    },
    {
        "name": "Different label type",
        "node_count": 10000,
        "edge_list": [],
        "label_type": grb.INT64,
    },
]

test_label_matrix_from_edge_list_data = [
    {
        "name": "Empty graph",
        "node_count": 0,
        "edge_list": [],
        "label_type": grb.UINT8,
        "default_label": 0,
    },
    {
        "name": "One node graph",
        "node_count": 1,
        "edge_list": [],
        "label_type": grb.UINT8,
        "default_label": 0,
    },
    {
        "name": "Complete graph",
        "node_count": 2,
        "edge_list": [(0, 1, 0), (0, 2, 1), (1, 3, 0), (1, 4, 1)],
        "label_type": grb.UINT8,
        "default_label": 0,
    },
    {
        "name": "No labels",
        "node_count": 2,
        "edge_list": [(0, None, 0), (0, None, 1), (1, None, 0), (1, None, 1)],
        "label_type": grb.UINT8,
        "default_label": 0,
    },
    {
        "name": "Mixed labels",
        "node_count": 2,
        "edge_list": [(0, None, 0), (0, 1, 1), (1, None, 0), (1, 2, 1)],
        "label_type": grb.UINT8,
        "default_label": 0,
    },
    {
        "name": "Huge graph",
        "node_count": 10000,
        "edge_list": [],
        "label_type": grb.UINT8,
        "default_label": 0,
    },
    {
        "name": "Different label type",
        "node_count": 10000,
        "edge_list": [],
        "label_type": grb.INT64,
        "default_label": 0,
    },
]

test_count_triangles_data = load_from_file("test_count_triangles_data")

resources = {
    "test_bfs_shortest_path_data": load_from_file("test_bfs_shortest_path_data"),
    "test_bfs_multiple_source_parents_data": load_from_file(
        "test_bfs_multiple_source_parents_data"
    ),
    "test_label_matrix_from_edge_list_data": test_label_matrix_from_edge_list_data,
    "test_adjacency_matrix_from_edge_list_data": test_adjacency_matrix_from_edge_list_data,
    "test_undirected_adjacency_matrix_from_edge_list_data": test_adjacency_matrix_from_edge_list_data,
    "test_count_triangles_cohen_data": test_count_triangles_data,
    "test_count_triangles_sandia_data": test_count_triangles_data,
    "test_count_triangles_for_each_vertex_data": load_from_file(
        "test_count_triangles_for_each_vertex_data"
    ),
}
