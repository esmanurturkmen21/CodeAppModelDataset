"""
mazeescape/agents/maze_online_agent.py

An "intelligent agent" wrapper for the online / repeated A* procedure.

The project paper can refer to this as the agent layer
(perception -> planning -> action).
Implementation-wise, it delegates the heavy lifting to
mazeescape.algorithms.online_astar.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from ..environments.maze_grid_world import Coordinate, MazeWorld
from ..algorithms.online_astar import online_astar


@dataclass
class MazeEscapeOnlineAgent:
    """Agent that navigates a partially known maze using Repeated A*."""

    true_world: MazeWorld
    heuristic: Callable[[Coordinate, Coordinate], float]

    def run(self) -> Tuple[List[Coordinate], int, Dict[str, float]]:
        return online_astar(self.true_world, heuristic=self.heuristic)
