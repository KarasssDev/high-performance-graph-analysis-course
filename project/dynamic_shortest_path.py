import heapq
from dataclasses import dataclass, field

from project.shortest_path import shortest_path_dijkstra
from typing import Hashable, Any, Dict, List
import networkx as nx

__all__ = ["DynamicSSSP"]


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    value: Any = field(compare=False)


class PriorityQueue:
    """
    OOP priority queue implementation based on heapq,
    support "remove_if_contains" operation and provide value unique
    """

    REMOVED = None

    def __init__(self) -> None:
        self._queue: List[PrioritizedItem] = []
        self._item_map = {}
        self._lazy_removed_count = 0

    def push(self, v: Hashable, priority: float) -> None:
        """
        Push the value onto the heap with provided priority

        Parameters
        ----------
        v: Hashable
            Value

        priority: float
            Priority
        """
        if v in self._item_map:
            self._lazy_remove(v)
        item = PrioritizedItem(priority, v)
        self._item_map[v] = item
        heapq.heappush(self._queue, item)

    def pop(self) -> Any:
        """
        Pop value from the heap

        Returns
        -------
        Any
            Popped value
        """
        self._force_removing()
        item = heapq.heappop(self._queue)
        self._item_map.pop(item.value)
        return item.value

    def is_empty(self) -> bool:
        """
        Returns
        -------
        bool
            True if queue is empty, False otherwise
        """
        return len(self._queue) - self._lazy_removed_count == 0

    def remove_if_contains(self, v: Hashable) -> None:
        """
        Remove item from queue

        Parameters
        ----------
        v: Hashable
            Value to remove
        """
        if v in self._item_map:
            self._lazy_remove(v)

    def _lazy_remove(self, v):
        item = self._item_map.pop(v)
        item.value = self.REMOVED
        self._lazy_removed_count += 1

    def _force_removing(self):
        while self._queue:
            item = self._queue[0]
            if item.value is self.REMOVED:
                self._lazy_removed_count -= 1
                heapq.heappop(self._queue)
                continue
            return


class DynamicSSSP:
    """
    Dynamic Dijkstra single-source shortest paths algorithm
    """

    def __init__(self, graph: nx.DiGraph, start: Hashable):
        self._graph: nx.DiGraph = graph
        self._start: Hashable = start
        self._dists: Dict[Hashable, float] = shortest_path_dijkstra(graph, start)
        self._modified_vertices: set[Hashable] = set()

    def insert_edge(self, u: Hashable, v: Hashable, weight: float = 1) -> None:
        """
        Insert edge (u ---> v) into graph with provided weight

        Parameters
        ----------
        u: Hashable
            Source vertex
        v: Hashable
            Destination vertex
        weight: float
            Weight (default = 1)
        """
        self._insert_vertices([u, v])
        self._graph.add_edge(u, v, weight=weight)
        self._modified_vertices.add(v)

    def delete_edge(self, u: Hashable, v: Hashable) -> None:
        """
        Delete edge (u ---> v) from graph

        Parameters
        ----------
        u: Hashable
            Source vertex
        v: Hashable
            Destination vertex
        """
        self._graph.remove_edge(u, v)
        self._modified_vertices.add(v)

    def query_dists(self) -> Dict[Hashable, float]:
        """
        Returns
        -------
        Dict[Hashable, float]
            Distances from start vertex to others.
            Distance will be float('inf') if vertex unreachable.
        """

        if len(self._modified_vertices) > 0:
            self._update_dists()
            self._modified_vertices = set()
        return self._dists

    def _insert_vertices(self, vertices) -> None:
        for v in vertices:
            self._graph.add_node(v)
            if v not in self._dists:
                self._dists[v] = float("inf")

    def _update_dists(self) -> None:
        """
        Applies the accumulated graph updates to the stored distances
        """
        rhs: Dict[Hashable, float] = {}
        queue = PriorityQueue()

        def push(vertex):
            if rhs[vertex] != self._dists[vertex]:
                queue.push(vertex, min(rhs[vertex], self._dists[vertex]))

        for u in self._modified_vertices:
            rhs[u] = self._calculate_rhs(u)
            push(u)

        while not queue.is_empty():
            u = queue.pop()

            if rhs[u] < self._dists[u]:
                self._dists[u] = rhs[u]
                to_update_rhs = self._graph.successors(u)
            else:
                self._dists[u] = float("inf")
                to_update_rhs = [*self._graph.successors(u), u]

            for v in to_update_rhs:
                rhs[v] = self._calculate_rhs(v)
                push(v)
                if rhs[v] == self._dists[v]:
                    queue.remove_if_contains(v)

    def _calculate_rhs(self, u: Hashable) -> float:
        """
        Parameters
        ----------
        u: Hashable
            Vertex

        Returns
        -------
        List[Tuple[int, List[float]]]
            rhs value for provided vertex
        """
        if u == self._start:
            return 0
        parent_distances = [
            self._dists[v] + self._graph[v][u]["weight"]
            for v in self._graph.predecessors(u)
        ]
        return min(
            parent_distances,
            default=float("inf"),
        )
