import os
import sys

# Allow running via: `python demos/<file>.py`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aima.search import (
    GraphProblem,
    astar_search,
    greedy_best_first_graph_search,
    uniform_cost_search,
    romania_map,
)


def _print_result(name: str, node):
    path_states = [n.state for n in node.path()]
    metrics = getattr(node, "metrics", {})
    print(f"\n{name}")
    print("Path:", path_states)
    print("Cost:", node.path_cost)
    if metrics:
        print("Expanded nodes:", metrics.get("expanded_nodes"))
        print("Frontier max:", metrics.get("frontier_max"))
        print("Explored set size:", metrics.get("explored"))


def run_demo():
    print("=== Romania Map Search Comparison ===")
    problem = GraphProblem("Arad", "Bucharest", romania_map)

    node_greedy = greedy_best_first_graph_search(problem)
    node_ucs = uniform_cost_search(problem)
    node_astar = astar_search(problem)

    _print_result("Greedy Best-First Search", node_greedy)
    _print_result("Uniform Cost Search (UCS)", node_ucs)
    _print_result("A* Search", node_astar)


if __name__ == "__main__":
    run_demo()
