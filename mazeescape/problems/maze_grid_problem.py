"""
mazeescape/problems/maze_grid_problem.py

MazeEscape+ grid-world search problem.

This wraps our grid environment into the cleaned AIMA Problem interface so we can
reuse the AIMA-style search implementations (UCS / Greedy / A*).
"""

from __future__ import annotations

from typing import Iterable

from aima.search import Problem
from ..environments.maze_grid_world import Coordinate, MazeWorld


class MazeGridProblem(Problem):
    """AIMA-compatible search problem on a MazeWorld grid."""

    def __init__(self, world: MazeWorld, initial: Coordinate, goal: Coordinate):
        super().__init__(initial, goal)
        self.world = world

    def actions(self, state: Coordinate) -> Iterable[Coordinate]:
        # In this formulation, an "action" is simply choosing a neighbor cell.
        return self.world.neighbors4(state)

    def result(self, state: Coordinate, action: Coordinate) -> Coordinate:
        return action

    def path_cost(
        self,
        c: float,
        state1: Coordinate,
        action: Coordinate,
        state2: Coordinate,
    ) -> float:
        # Uniform step cost in the grid.
        return c + 1.0
