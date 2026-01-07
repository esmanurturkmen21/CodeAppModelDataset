"""
mazeescape/experiments/execution_traces.py

Execution evidence script for classical search algorithms.

This script produces separate execution traces for:
  - Greedy Best-First Search
  - Uniform Cost Search (UCS)
  - A* Search

It is included as part of the project to provide reproducible
and verifiable execution evidence.
"""

from __future__ import annotations

from aima.search import (
    GraphProblem,
    astar_search,
    greedy_best_first_graph_search,
    romania_map,
    uniform_cost_search,
)


def _print_block(title: str, node) -> None:
    path_states = [n.state for n in node.path()]
    metrics = getattr(node, "metrics", {})
    print(f"\n=== {title} ===")
    print("Path:", path_states)
    print("Cost:", node.path_cost)
    if metrics:
        print("Expanded nodes:", metrics.get("expanded_nodes"))
        print("Frontier max:", metrics.get("frontier_max"))
        print("Explored set size:", metrics.get("explored"))


def run_ucs() -> None:
    """Uniform Cost Search (UCS) execution trace."""
    problem = GraphProblem("Arad", "Bucharest", romania_map)
    node = uniform_cost_search(problem)
    _print_block("Uniform Cost Search (UCS)", node)


def run_greedy() -> None:
    """Greedy Best-First Search execution trace."""
    problem = GraphProblem("Arad", "Bucharest", romania_map)
    node = greedy_best_first_graph_search(problem)
    _print_block("Greedy Best-First Search", node)


def run_astar() -> None:
    """A* Search execution trace."""
    problem = GraphProblem("Arad", "Bucharest", romania_map)
    node = astar_search(problem)
    _print_block("A* Search", node)


if __name__ == "__main__":
    run_greedy()
    run_ucs()
    run_astar()
