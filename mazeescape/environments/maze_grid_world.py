"""
<<<<<<< HEAD
maze_world.py
Grid-based maze world representation for the MazeEscape+ project.

Symbols:
    'S' : start position
    'G' : goal position
    '#' : wall
    '.' : free / walkable cell
=======
maze_grid_world.py

Grid-based maze world with PARTIAL OBSERVABILITY.
Produces PNG visualizations of the agent's belief map.
>>>>>>> 7be20c4 (Initial commit)
"""

from __future__ import annotations

<<<<<<< HEAD
from typing import List, Optional, Tuple

=======
import matplotlib
matplotlib.use("Agg")  # FORCE FILE OUTPUT (no GUI)

import numpy as np
import matplotlib.pyplot as plt
import os
from typing import List, Optional, Tuple
>>>>>>> 7be20c4 (Initial commit)

Coordinate = Tuple[int, int]


class MazeWorld:
<<<<<<< HEAD
    """A simple 2D grid world loaded from a text file."""

    def __init__(self, grid: List[List[str]]) -> None:
        self.grid: List[List[str]] = grid
        self.height: int = len(grid)
        self.width: int = len(grid[0]) if grid else 0

        self.start: Optional[Coordinate] = self._find_symbol("S")
        self.goal: Optional[Coordinate] = self._find_symbol("G")

    # ---------- construction / loading ----------

    @classmethod
    def from_file(cls, filepath: str) -> "MazeWorld":
        """Load a maze from a given text file."""
        with open(filepath, encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        grid = [list(row) for row in lines]
        return cls(grid)

    def _find_symbol(self, symbol: str) -> Optional[Coordinate]:
        """Return the (x, y) coordinate of the first occurrence of a symbol."""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == symbol:
                    return x, y
        return None

    # ---------- basic queries ----------

    def is_inside(self, x: int, y: int) -> bool:
        """Return True if (x, y) is inside the grid bounds."""
        return 0 <= y < self.height and 0 <= x < self.width

    def is_wall(self, x: int, y: int) -> bool:
        """Return True if the cell at (x, y) is a wall or outside the grid."""
=======
    def __init__(self, grid: List[List[str]]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0

        self.start = self._find_symbol("S")
        self.goal = self._find_symbol("G")

        # -1 unknown, 0 free, 1 wall
        self.known_map = np.full((self.height, self.width), -1, dtype=int)

        if self.start:
            x, y = self.start
            self.known_map[y, x] = 0

    @classmethod
    def from_file(cls, filepath: str) -> "MazeWorld":
        with open(filepath, encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]
        return cls([list(row) for row in lines])

    def _find_symbol(self, symbol: str) -> Optional[Coordinate]:
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == symbol:
                    return (x, y)
        return None

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_wall(self, x: int, y: int) -> bool:
>>>>>>> 7be20c4 (Initial commit)
        if not self.is_inside(x, y):
            return True
        return self.grid[y][x] == "#"

<<<<<<< HEAD
    def is_free(self, x: int, y: int) -> bool:
        """Return True if the cell at (x, y) is inside and not a wall."""
        return self.is_inside(x, y) and not self.is_wall(x, y)

    def neighbors4(self, state: Coordinate) -> List[Coordinate]:
        """Return valid 4-neighborhood (up, down, left, right) cells."""
        x, y = state
        candidates: List[Coordinate] = [
            (x, y - 1),  # up
            (x, y + 1),  # down
            (x - 1, y),  # left
            (x + 1, y),  # right
        ]
        return [(nx, ny) for nx, ny in candidates if self.is_free(nx, ny)]

    # ---------- simple visualization ----------

    def display(self, path: Optional[List[Coordinate]] = None) -> None:
        """Print the grid, optionally marking a path with '*'."""
        path_set = set(path) if path else set()

        for y, row in enumerate(self.grid):
            rendered_row = []
            for x, cell in enumerate(row):
                if (x, y) in path_set and cell not in ("S", "G"):
                    rendered_row.append("*")
                else:
                    rendered_row.append(cell)
            print("".join(rendered_row))
=======
    def neighbors4(self, state: Coordinate):
        x, y = state
        candidates = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        return [(nx, ny) for nx, ny in candidates if not self.is_wall(nx, ny)]

    # ---------------- PARTIAL OBSERVABILITY ----------------

    def sense(self, pos: Coordinate) -> None:
        x, y = pos
        for nx, ny in [(x,y), (x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
            if not self.is_inside(nx, ny):
                continue
            self.known_map[ny, nx] = 1 if self.is_wall(nx, ny) else 0

    # ---------------- VISUALIZATION ----------------

    def visualize_known_map(
        self,
        agent_pos: Coordinate,
        step_id: int,
        title_prefix: str,
        save_dir: str,
    ) -> None:
        os.makedirs(save_dir, exist_ok=True)

        img = np.zeros((self.height, self.width))
        img[self.known_map == -1] = 0.5
        img[self.known_map == 0] = 1.0
        img[self.known_map == 1] = 0.0

        ax, ay = agent_pos
        gx, gy = self.goal

        img[ay, ax] = 0.8
        img[gy, gx] = 0.3

        plt.figure(figsize=(5,5))
        plt.imshow(img, cmap="gray")
        plt.title(f"{title_prefix} {step_id}")
        plt.xticks([])
        plt.yticks([])

        path = os.path.join(save_dir, f"{title_prefix}_{step_id}.png")
        plt.savefig(path, bbox_inches="tight")
        plt.close()
>>>>>>> 7be20c4 (Initial commit)
