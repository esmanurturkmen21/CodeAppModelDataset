import os
import sys

# Allow running via: 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import os
import sys

# Allow running via: `python demos/<file>.py`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aima.search import GraphProblem, greedy_best_first_graph_search, romania_map


def main():
    print("=== Greedy Best-First Search Demo (Romania Map) ===")
    problem = GraphProblem("Arad", "Bucharest", romania_map)

    node = greedy_best_first_graph_search(problem)
    if node is None:
        print("No solution found.")
        return

    path_states = [n.state for n in node.path()]
    print("Path:", path_states)
    print("Cost:", node.path_cost)

    metrics = getattr(node, "metrics", {})
    if metrics:
        print("Expanded nodes:", metrics.get("expanded_nodes"))
        print("Frontier max:", metrics.get("frontier_max"))
        print("Explored set size:", metrics.get("explored"))


if __name__ == "__main__":
    main()
