"""aima/search.py

Cleaned, minimal AIMA-style search codebase for HW4.

Goal (HW4): understand and document the architecture of the core search components
and run standard examples (e.g., Romania route finding) on a simplified codebase.

This file intentionally focuses on:
  - Problem / Node abstractions
  - Best-first graph search engine (shared by Greedy / UCS / A*)
  - Graph + GraphProblem (Romania map)
  - A small, measurable execution surface (metrics)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from .utils import PriorityQueue, distance, is_in, memoize


# -----------------------------------------------------------------------------
# Abstract Problem and Node


class Problem:
    """The abstract class for a formal problem."""

    def __init__(self, initial: Any, goal: Optional[Any] = None):
        self.initial = initial
        self.goal = goal

    def actions(self, state: Any) -> Iterable[Any]:
        raise NotImplementedError

    def result(self, state: Any, action: Any) -> Any:
        raise NotImplementedError

    def goal_test(self, state: Any) -> bool:
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        return state == self.goal

    def path_cost(self, c: float, state1: Any, action: Any, state2: Any) -> float:
        return c + 1

    def h(self, node: "Node") -> float:
        return 0.0


@dataclass
class Node:
    """A node in a search tree."""

    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0
    depth: int = 0

    def __post_init__(self) -> None:
        if self.parent is not None:
            self.depth = self.parent.depth + 1

    # IMPORTANT: frontier update relies on equality-by-state
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self) -> int:
        return hash(self.state)

    def expand(self, problem: Problem) -> List["Node"]:
        return [self.child_node(problem, a) for a in problem.actions(self.state)]

    def child_node(self, problem: Problem, action: Any) -> "Node":
        next_state = problem.result(self.state, action)
        new_cost = problem.path_cost(self.path_cost, self.state, action, next_state)
        return Node(next_state, self, action, new_cost)

    def solution(self) -> List[Any]:
        return [n.action for n in self.path()[1:]]

    def path(self) -> List["Node"]:
        node, path_back = self, []
        while node is not None:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


# -----------------------------------------------------------------------------
# Heuristic Search (Best-first engine + specializations)


def best_first_graph_search(
    problem: Problem,
    f: Callable[[Node], float],
    *,
    collect_metrics: bool = True,
) -> Optional[Node]:
    """Best-first graph search.

    Shared engine used by:
      - Greedy Best-First Search (f = h)
      - Uniform Cost Search (f = g)
      - A* Search (f = g + h)

    If collect_metrics=True, attaches a dict to the returned Node:
      node.metrics = {"expanded_nodes": ..., "frontier_max": ..., "explored": ...}
    """

    f = memoize(f, "f")
    node = Node(problem.initial)
    frontier = PriorityQueue(order="min", f=f)
    frontier.append(node)
    explored = set()

    expanded_nodes = 0
    frontier_max = len(frontier)

    while frontier:
        frontier_max = max(frontier_max, len(frontier))

        node = frontier.pop()
        if problem.goal_test(node.state):
            if collect_metrics:
                node.metrics = {
                    "expanded_nodes": expanded_nodes,
                    "frontier_max": frontier_max,
                    "explored": len(explored),
                }
            return node

        explored.add(node.state)
        expanded_nodes += 1

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier and f(child) < frontier[child]:
                del frontier[child]
                frontier.append(child)

    return None


def greedy_best_first_graph_search(problem: Problem) -> Optional[Node]:
    return best_first_graph_search(problem, lambda n: problem.h(n))


def uniform_cost_search(problem: Problem) -> Optional[Node]:
    return best_first_graph_search(problem, lambda n: n.path_cost)


def astar_search(problem: Problem, h: Optional[Callable[[Node], float]] = None) -> Optional[Node]:
    h = memoize(h or problem.h, "h")
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# -----------------------------------------------------------------------------
# Graph and GraphProblem (Romania map)


class Graph:
    def __init__(self, graph_dict: Optional[Dict[Any, Dict[Any, float]]] = None, directed: bool = False):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        self.locations: Dict[Any, Tuple[float, float]] = {}
        if not directed:
            self.make_undirected()

    def make_undirected(self) -> None:
        for a in list(self.graph_dict.keys()):
            for b, d in self.graph_dict[a].items():
                self.connect1(b, a, d)

    def connect(self, A: Any, B: Any, distance_cost: float = 1.0) -> None:
        self.connect1(A, B, distance_cost)
        if not self.directed:
            self.connect1(B, A, distance_cost)

    def connect1(self, A: Any, B: Any, distance_cost: float) -> None:
        self.graph_dict.setdefault(A, {})[B] = distance_cost

    def get(self, a: Any, b: Optional[Any] = None):
        links = self.graph_dict.setdefault(a, {})
        return links if b is None else links.get(b)


class GraphProblem(Problem):
    def __init__(self, initial: Any, goal: Any, graph: Graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, A: Any) -> Iterable[Any]:
        return list(self.graph.get(A).keys())

    def result(self, state: Any, action: Any) -> Any:
        # Action is “go to neighbor”
        return action

    def path_cost(self, c: float, A: Any, action: Any, B: Any) -> float:
        return c + (self.graph.get(A, B) or float("inf"))

    def h(self, node: Node) -> float:
        if self.graph.locations and node.state in self.graph.locations and self.goal in self.graph.locations:
            return distance(self.graph.locations[node.state], self.graph.locations[self.goal])
        return float("inf")


def _make_romania_map() -> Graph:
    g = Graph(directed=False)

    roads = [
        ("Arad", "Zerind", 75),
        ("Arad", "Sibiu", 140),
        ("Arad", "Timisoara", 118),
        ("Zerind", "Oradea", 71),
        ("Oradea", "Sibiu", 151),
        ("Timisoara", "Lugoj", 111),
        ("Lugoj", "Mehadia", 70),
        ("Mehadia", "Drobeta", 75),
        ("Drobeta", "Craiova", 120),
        ("Craiova", "Rimnicu Vilcea", 146),
        ("Craiova", "Pitesti", 138),
        ("Sibiu", "Fagaras", 99),
        ("Sibiu", "Rimnicu Vilcea", 80),
        ("Rimnicu Vilcea", "Pitesti", 97),
        ("Fagaras", "Bucharest", 211),
        ("Pitesti", "Bucharest", 101),
        ("Bucharest", "Giurgiu", 90),
        ("Bucharest", "Urziceni", 85),
        ("Urziceni", "Hirsova", 98),
        ("Hirsova", "Eforie", 86),
        ("Urziceni", "Vaslui", 142),
        ("Vaslui", "Iasi", 92),
        ("Iasi", "Neamt", 87),
    ]
    for a, b, d in roads:
        g.connect(a, b, d)

    # Coordinates for straight-line distance heuristic
    g.locations = {
        "Arad": (91, 492),
        "Bucharest": (400, 327),
        "Craiova": (253, 288),
        "Drobeta": (165, 299),
        "Eforie": (562, 293),
        "Fagaras": (305, 449),
        "Giurgiu": (375, 270),
        "Hirsova": (534, 350),
        "Iasi": (473, 506),
        "Lugoj": (165, 379),
        "Mehadia": (168, 339),
        "Neamt": (406, 537),
        "Oradea": (131, 571),
        "Pitesti": (320, 368),
        "Rimnicu Vilcea": (233, 410),
        "Sibiu": (207, 457),
        "Timisoara": (94, 410),
        "Urziceni": (456, 350),
        "Vaslui": (509, 444),
        "Zerind": (108, 531),
    }
    return g


romania_map = _make_romania_map()
