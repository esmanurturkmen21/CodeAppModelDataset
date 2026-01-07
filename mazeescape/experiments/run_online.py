"""
mazeescape/experiments/run_online.py

<<<<<<< HEAD
Online / Repeated A* experiment runner (partial knowledge).

Runs both heuristics (Manhattan vs Euclidean) and prints metrics.

Usage:
  python -m mazeescape.experiments.run_online
=======
Runs Online / Repeated A* experiments.
- Uses ASCII + academic logs from online_astar
- Saves step-by-step FIGURES
- Collects metrics for comparison plots
>>>>>>> 7be20c4 (Initial commit)
"""

from __future__ import annotations

<<<<<<< HEAD
import time
from pathlib import Path

from ..algorithms.online_astar import online_astar
from ..environments.maze_grid_world import MazeWorld
from ..heuristics.heuristics import (
    euclidean_distance,
    manhattan_distance,
)


BASE_DIR = Path(__file__).resolve().parents[2]


def main() -> None:
    maze_path = BASE_DIR / "mazes" / "maze1.txt"
    true_world = MazeWorld.from_file(str(maze_path))

    print("=== MazeEscape+ Online / Repeated A* (Partial Knowledge) ===")
    print(f"Maze: {maze_path.name}")

    for name, h in [
        ("Manhattan", manhattan_distance),
        ("Euclidean", euclidean_distance),
    ]:
        t0 = time.perf_counter()
        path, replans, metrics = online_astar(true_world, heuristic=h)
        t1 = time.perf_counter()

        print(f"\nHeuristic: {name}")
        print(f"Path cost       : {metrics['path_cost']:.0f}")
        print(f"Path length     : {metrics['path_length']:.0f}")
        print(f"Replans         : {replans}")
        print(f"Node expansions : {metrics['node_expansions']:.0f}")
        print(f"Time (ms)       : {(t1 - t0) * 1000:.2f}")
        print("\nMaze with path (*):")
        true_world.display(path)
=======
import shutil
import time
from pathlib import Path

from mazeescape.algorithms.online_astar import online_astar
from mazeescape.environments.maze_grid_world import MazeWorld
from mazeescape.heuristics.heuristics import (
    manhattan_distance,
    euclidean_distance,
)

BASE_DIR = Path(__file__).resolve().parents[2]
MAZE_PATH = BASE_DIR / "mazes" / "maze1.txt"
FIG_DIR = BASE_DIR / "figures" / "online"


def main():
    # temiz başla
    if FIG_DIR.exists():
        shutil.rmtree(FIG_DIR)
    FIG_DIR.mkdir(parents=True)

    print("FIGURES DIR:", FIG_DIR.resolve())

    results = {}

    for heuristic_name, heuristic_fn in [
        ("Manhattan", manhattan_distance),
        ("Euclidean", euclidean_distance),
    ]:
        print(f"\nRunning: {heuristic_name}")

        world = MazeWorld.from_file(str(MAZE_PATH))
        step_counter = {"i": 0}

        # ---- CALLBACKS ----
        def step_cb(pos):
            world.visualize_known_map(
                agent_pos=pos,
                step_id=step_counter["i"],
                title_prefix=heuristic_name,
                save_dir=str(FIG_DIR),
            )
            step_counter["i"] += 1

        def replan_cb(_pos):
            pass  # log online_astar içinde zaten var

        # ---- RUN ----
        t0 = time.perf_counter()
        path, replans, metrics = online_astar(
            world,
            heuristic_fn,
            step_callback=step_cb,
            replan_callback=replan_cb,
        )
        t1 = time.perf_counter()

        metrics["time_ms"] = (t1 - t0) * 1000
        results[heuristic_name] = metrics

        print(f"{heuristic_name} finished in {metrics['time_ms']:.2f} ms")

    # ---- FINAL SUMMARY (for plots) ----
    print("\n=== ONLINE A* METRICS SUMMARY ===")
    for name, m in results.items():
        print(
            f"{name:10s} | "
            f"path_cost={m['path_cost']:.0f}, "
            f"node_exp={m['node_expansions']:.0f}, "
            f"replans={m['replans']:.0f}, "
            f"time_ms={m['time_ms']:.2f}"
        )
>>>>>>> 7be20c4 (Initial commit)


if __name__ == "__main__":
    main()
