"""
mazeescape/experiments/run_online.py

Runs Online / Repeated A* experiments.
- Uses ASCII + academic logs from online_astar
- Saves step-by-step FIGURES
- Collects metrics for comparison plots
"""

from __future__ import annotations

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


if __name__ == "__main__":
    main()
