Project-level main entry point for the MazeEscape+ project.

This file provides a minimal CLI to:
  1) Validate the AIMA search core using the Romania route-finding problem
  2) Run Offline A* (full knowledge) on a grid-based maze
  3) Run Online / Repeated A* (partial knowledge) on a grid-based maze

For domain-specific execution, see:
  mazeescape/main.py

For experiments, see:
  mazeescape/experiments/

Usage:
  python main.py
"""

from __future__ import annotations


def main() -> None:
    print("MazeEscape+ :: Online A* Search in Partially Known Grid Worlds")
    print("----------------------------------------------------------")
    print("1) Romania demo (compare Greedy/UCS/A*)")
    print("2) Offline A* on maze (full knowledge)")
    print("3) Online / Repeated A* on maze (partial knowledge)")
    print("q) Quit")

    choice = input("Select: ").strip().lower()

    if choice == "1":
        from demos.demo_romania_compare import run_demo
        run_demo()

    elif choice == "2":
        from mazeescape.experiments.run_offline import main as run
        run()

    elif choice == "3":
        from mazeescape.experiments.run_online import main as run
        run()

    else:
        print("Bye.")


if __name__ == "__main__":
    main()
