"""
mazeescape/algorithms/online_astar.py

Online / Repeated A* in a PARTIALLY KNOWN grid world.

This version:
- Keeps matplotlib FIGURE generation (via callbacks)
- Prints ASCII GRID snapshots at each step
- Produces clear ACADEMIC LOG OUTPUT
- Explicitly proves ONLINE / REPLANNING behavior
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Set, Tuple

from aima.search import Node, astar_search
from mazeescape.environments.maze_grid_world import Coordinate, MazeWorld
from mazeescape.problems.maze_grid_problem import MazeGridProblem


# =========================================================
# FINAL ASCII (classic output – old style, hocaya tanıdık)
# =========================================================

def print_final_ascii(world: MazeWorld, path: List[Coordinate]) -> None:
    path_set = set(path)
    for y in range(world.height):
        row = ""
        for x in range(world.width):
            if (x, y) == world.start:
                row += "S"
            elif (x, y) == world.goal:
                row += "G"
            elif (x, y) in path_set:
                row += "*"
            elif world.is_wall(x, y):
                row += "#"
            else:
                row += "."
        print(row)


# =========================================================
# BELIEF WORLD (agent’s internal map)
# =========================================================

@dataclass
class _BeliefWorld:
    true_world: MazeWorld
    known_walls: Set[Coordinate]

    @property
    def start(self):
        return self.true_world.start

    @property
    def goal(self):
        return self.true_world.goal

    def is_inside(self, x: int, y: int) -> bool:
        return self.true_world.is_inside(x, y)

    def is_wall(self, x: int, y: int) -> bool:
        if not self.is_inside(x, y):
            return True
        return (x, y) in self.known_walls

    def is_free(self, x: int, y: int) -> bool:
        return self.is_inside(x, y) and not self.is_wall(x, y)

    def neighbors4(self, state: Coordinate) -> List[Coordinate]:
        x, y = state
        return [
            (nx, ny)
            for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
            if self.is_free(nx, ny)
        ]


# =========================================================
# PERCEPTION
# =========================================================

def _sense_walls(true_world: MazeWorld, pos: Coordinate) -> Set[Coordinate]:
    x, y = pos
    sensed: Set[Coordinate] = set()

    for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
        if true_world.is_inside(nx, ny) and true_world.is_wall(nx, ny):
            sensed.add((nx, ny))

    return sensed


# =========================================================
# ASCII GRID SNAPSHOT (partial observability proof)
# =========================================================

def _print_ascii_known_map(world: MazeWorld, agent_pos: Coordinate, step: int) -> None:
    print(f"\n[GRID] Step {step}")
    for y in range(world.height):
        row = []
        for x in range(world.width):
            if (x, y) == agent_pos:
                row.append("A")
            elif world.goal and (x, y) == world.goal:
                row.append("G")
            else:
                v = world.known_map[y, x]
                if v == -1:
                    row.append("?")
                elif v == 0:
                    row.append(".")
                else:
                    row.append("#")
        print(" ".join(row))


# =========================================================
# ONLINE / REPEATED A*
# =========================================================

def online_astar(
    true_world: MazeWorld,
    heuristic: Callable[[Coordinate, Coordinate], float],
    step_callback: Optional[Callable[[Coordinate], None]] = None,
    replan_callback: Optional[Callable[[Coordinate], None]] = None,
) -> Tuple[List[Coordinate], int, Dict[str, float]]:

    if true_world.start is None or true_world.goal is None:
        raise ValueError("MazeWorld must define start (S) and goal (G).")

    current: Coordinate = true_world.start
    goal: Coordinate = true_world.goal

    known_walls: Set[Coordinate] = set()
    path_taken: List[Coordinate] = [current]

    astar_calls = 0
    replans = 0
    total_expansions = 0.0
    step_id = 0

    # Initial sensing
    true_world.sense(current)

    print(f"\n[STATE] Agent at {current}")
    print(f"[GOAL] Goal at {goal}")
    _print_ascii_known_map(true_world, current, step_id)

    if step_callback:
        step_callback(current)

    # ================= MAIN LOOP =================
    while current != goal:

        print(f"\n[SEARCH] A* planning (heuristic = {heuristic.__name__})")
        astar_calls += 1
        print(f"[SEARCH] A* called (call #{astar_calls})")

        if replan_callback:
            replan_callback(current)

        belief_world = _BeliefWorld(true_world, known_walls)
        problem = MazeGridProblem(belief_world, current, goal)  # type: ignore

        def h(node: Node) -> float:
            return heuristic(node.state, goal)

        goal_node = astar_search(problem, h=h)
        replans += 1

        if goal_node is None:
            raise RuntimeError("Online A*: no plan found")

        metrics = getattr(goal_node, "metrics", {})
        total_expansions += float(metrics.get("expanded_nodes", 0))

        planned_path = [n.state for n in goal_node.path()]
        progressed = False

        # =============== EXECUTION =================
        for next_cell in planned_path[1:]:

            newly_sensed = _sense_walls(true_world, current)
            for w in newly_sensed - known_walls:
                print(f"[PERCEPT] Obstacle discovered at {w}")
            known_walls |= newly_sensed

            if next_cell in known_walls:
                print("[SEARCH] Current plan invalid")
                print("[SEARCH] Replanning with A*")
                break

            print(f"[ACTION] Moving to {next_cell}")
            current = next_cell
            path_taken.append(current)
            progressed = True
            step_id += 1

            true_world.sense(current)
            _print_ascii_known_map(true_world, current, step_id)

            if step_callback:
                step_callback(current)

            if current == goal:
                break

        if not progressed and current != goal:
            raise RuntimeError("Online A*: stuck (no progress possible)")

    # ================= SUMMARY =================
    print("\n[SUMMARY]")
    print(f"A* calls : {astar_calls}")
    print(f"Replans  : {replans}")

    print("\n[FINAL PATH – ASCII]")
    print_final_ascii(true_world, path_taken)

    return path_taken, replans, {
        "node_expansions": float(total_expansions),
        "path_cost": float(len(path_taken) - 1),
        "path_length": float(len(path_taken)),
        "replans": float(replans),
    }
