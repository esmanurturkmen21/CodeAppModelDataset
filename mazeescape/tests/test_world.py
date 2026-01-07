from mazeescape.environments.maze_grid_world import MazeWorld

def main():
    world = MazeWorld.from_file("mazes/maze1.txt")
    pos = world.start

    for step in range(5):
        world.sense(pos)
        world.visualize_known_map(
            agent_pos=pos,
            step_id=0,
            title_prefix="Test",
            save_dir="figures_test"
        )
        x, y = pos
        pos = (x + 1, y)

if __name__ == "__main__":
    main()
