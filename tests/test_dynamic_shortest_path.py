from typing import Tuple, List, Hashable, Dict

import utils
import networkx as nx

from project.dynamic_shortest_path import DynamicSSSP


def test_dynamic_shortest_path(data):
    init_edge_list: List[Tuple[int, int, float]] = data["init_edge_list"]
    init_expected: List[float] = utils._to_float_inf(data["init_expected"])
    graph: nx.DiGraph = nx.DiGraph()
    graph.add_weighted_edges_from(init_edge_list)
    dynamic_sssp = DynamicSSSP(graph, 0)

    actual: Dict[Hashable, float] = dynamic_sssp.query_dists()
    for v, expected_distance in enumerate(init_expected):
        assert expected_distance == actual[v]

    for update in data["updates"]:
        for change in update["changes"]:
            action, u, v = change
            if action == "+":
                dynamic_sssp.insert_edge(u, v)
            elif action == "-":
                dynamic_sssp.delete_edge(u, v)

        expected: List[float] = utils._to_float_inf(update["expected"])
        actual: Dict[Hashable, float] = dynamic_sssp.query_dists()
        for v, expected_distance in enumerate(expected):
            assert expected_distance == actual[v]
