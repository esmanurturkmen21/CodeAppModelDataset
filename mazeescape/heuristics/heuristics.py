"""
heuristics.py
Heuristic functions to be used with A* search in MazeEscape+.
"""

from __future__ import annotations

from typing import Tuple
import math


Coordinate = Tuple[int, int]


def manhattan_distance(a: Coordinate, b: Coordinate) -> float:
    """Return the Manhattan distance between two grid coordinates."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_distance(a: Coordinate, b: Coordinate) -> float:
    """Return the Euclidean distance between two grid coordinates."""
    return math.hypot(a[0] - b[0], a[1] - b[1])
