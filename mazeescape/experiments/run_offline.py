"""
mazeescape/experiments/run_offline.py

<<<<<<< HEAD
Offline A* experiment runner (full knowledge).

Runs both heuristics (Manhattan vs Euclidean) and prints metrics.

Usage:
  python -m mazeescape.experiments.run_offline
=======
Offline A* experiment runner (FULL KNOWLEDGE).

This version:
- Prints a SINGLE ASCII grid of the final solution
- Generates ONE visualization figure per heuristic
- Clearly contrasts with ONLINE behavior
>>>>>>> 7be20c4 (Initial commit)
"""

from __future__ import annotations

import time
from pathlib import Path
<<<<<<< HEAD

from ..algorithms.offline_astar import offline_astar
from ..environments.maze_grid_world import MazeWorld
from ..heuristics.heuristics import (
=======
import os

import numpy as np
import matplotlib.pyplot as plt

from mazeescape.algorithms.offline_astar import offline_astar
from mazeescape.environments.maze_grid_world import MazeWorld
from mazeescape.heuristics.heuristics import (
>>>>>>> 7be20c4 (Initial commit)
    euclidean_distance,
    manhattan_distance,
)

<<<<<<< HEAD

BASE_DIR = Path(__file__).resolve().parents[2]


=======
BASE_DIR = Path(__file__).resolve().parents[2]
FIG_DIR = BASE_DIR / "figures" / "offline"
os.makedirs(FIG_DIR, exist_ok=True)


# =========================================================
# ASCII GRID (FINAL SNAPSHOT)
# =========================================================

def print_ascii_final_grid(world: MazeWorld, path) -> None:
    print("\n[FINAL GRID – OFFLINE A*]")
    for y in range(world.height):
        row = []
        for x in range(world.width):
            if (x, y) == world.start:
                row.append("S")
            elif (x, y) == world.goal:
                row.append("G")
            elif (x, y) in path:
                row.append("*")
            elif world.is_wall(x, y):
                row.append("#")
            else:
                row.append(".")
        print(" ".join(row))


# =========================================================
# SINGLE FIGURE VISUALIZATION
# =========================================================

def visualize_offline_path(world: MazeWorld, path, title: str, filename: str) -> None:
    grid = np.zeros((world.height, world.width))

    for y in range(world.height):
        for x in range(world.width):
            if world.is_wall(x, y):
                grid[y, x] = 0.0       # wall
            else:
                grid[y, x] = 1.0       # free

    for (x, y) in path:
        grid[y, x] = 0.6               # path

    sx, sy = world.start
    gx, gy = world.goal
    grid[sy, sx] = 0.8                 # start
    grid[gy, gx] = 0.3                 # goal

    plt.figure(figsize=(5, 5))
    plt.imshow(grid, cmap="gray")
    plt.title(title)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(FIG_DIR / filename, bbox_inches="tight")
    plt.close()


# =========================================================
# MAIN
# =========================================================

>>>>>>> 7be20c4 (Initial commit)
def main() -> None:
    maze_path = BASE_DIR / "mazes" / "maze1.txt"
    world = MazeWorld.from_file(str(maze_path))

    print("=== MazeEscape+ Offline A* (Full Knowledge) ===")
    print(f"Maze: {maze_path.name}")

    for name, h in [
        ("Manhattan", manhattan_distance),
        ("Euclidean", euclidean_distance),
    ]:
<<<<<<< HEAD
=======
        print(f"\n[SEARCH] Offline A* (heuristic = {name})")

>>>>>>> 7be20c4 (Initial commit)
        t0 = time.perf_counter()
        path, metrics = offline_astar(world, heuristic=h)
        t1 = time.perf_counter()

<<<<<<< HEAD
        print(f"\nHeuristic: {name}")
=======
>>>>>>> 7be20c4 (Initial commit)
        print(f"Path cost       : {metrics['path_cost']:.0f}")
        print(f"Path length     : {metrics['path_length']:.0f}")
        print(f"Node expansions : {metrics['node_expansions']:.0f}")
        print(f"Time (ms)       : {(t1 - t0) * 1000:.2f}")
<<<<<<< HEAD
        print("\nMaze with path (*):")
        world.display(path)
=======

        # ASCII snapshot
        print_ascii_final_grid(world, path)

        # Single visualization
        visualize_offline_path(
            world,
            path,
            title=f"Offline A* ({name}) – Full Knowledge",
            filename=f"offline_{name.lower()}.png",
        )

        print(f"[FIGURE] Saved: figures/offline/offline_{name.lower()}.png")
>>>>>>> 7be20c4 (Initial commit)


if __name__ == "__main__":
    main()
