"""
mazeescape/algorithms/offline_astar.py

Offline A* baseline (single-shot planning with full map knowledge).

Returns a path and performance metrics.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Tuple

from aima.search import Node, astar_search
from environments.maze_grid_world import Coordinate, MazeWorld
from problems.maze_grid_problem import MazeGridProblem

def offline_astar(
    world: MazeWorld,
    heuristic: Callable[[Coordinate, Coordinate], float],
) -> Tuple[List[Coordinate], Dict[str, float]]:
    """Run classical A* assuming the agent knows the full maze.

    Metrics returned:
      - node_expansions
      - path_cost
      - path_length
    """

    if world.start is None or world.goal is None:
        raise ValueError("MazeWorld must define start (S) and goal (G).")

    problem = MazeGridProblem(world, world.start, world.goal)

    def h(node: Node) -> float:
        return heuristic(node.state, world.goal)  # type: ignore[arg-type]

    goal_node = astar_search(problem, h=h)
    if goal_node is None:
        raise RuntimeError("Offline A*: no solution found.")

    path = [n.state for n in goal_node.path()]
    metrics = getattr(goal_node, "metrics", {})
    node_expansions = float(metrics.get("expanded_nodes", 0))

    return path, {
        "node_expansions": node_expansions,
        "path_cost": float(goal_node.path_cost),
        "path_length": float(len(path)),
    }
