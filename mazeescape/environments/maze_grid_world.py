"""
maze_grid_world.py

Grid-based maze world with PARTIAL OBSERVABILITY.
Produces PNG visualizations of the agent's belief map.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")  # FORCE FILE OUTPUT (no GUI)

import numpy as np
import matplotlib.pyplot as plt
import os
from typing import List, Optional, Tuple

Coordinate = Tuple[int, int]


class MazeWorld:
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
                    return x, y
        return None

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_wall(self, x: int, y: int) -> bool:
        if not self.is_inside(x, y):
            return True
        return self.grid[y][x] == "#"

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
