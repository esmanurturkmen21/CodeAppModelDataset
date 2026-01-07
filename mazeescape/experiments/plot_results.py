"""
plot_results.py

Very simple bar charts for:
1) Offline vs Online A* comparison
2) Manhattan vs Euclidean comparison
"""

from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[2]
FIG_DIR = BASE_DIR / "figures" / "plots"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def plot_offline_vs_online():
    """
    Offline vs Online A* comparison
    Metric: node expansions
    """

    labels = ["Offline A*", "Online A*"]
    node_expansions = [
        14,   # Offline (from your output)
        40,   # Online (approx / average from your runs)
    ]

    plt.figure(figsize=(5, 4))
    plt.bar(labels, node_expansions)
    plt.ylabel("Node Expansions")
    plt.title("Offline vs Online A* Comparison")

    plt.tight_layout()
    plt.savefig(FIG_DIR / "offline_vs_online.png")
    plt.close()


def plot_manhattan_vs_euclidean():
    """
    Manhattan vs Euclidean comparison
    Metric: execution time (ms)
    """

    labels = ["Manhattan", "Euclidean"]
    times_ms = [
        2166,  # Online Manhattan time (ms)
        792,   # Online Euclidean time (ms)
    ]

    plt.figure(figsize=(5, 4))
    plt.bar(labels, times_ms)
    plt.ylabel("Time (ms)")
    plt.title("Manhattan vs Euclidean (Online A*)")

    plt.tight_layout()
    plt.savefig(FIG_DIR / "manhattan_vs_euclidean.png")
    plt.close()


def main():
    plot_offline_vs_online()
    plot_manhattan_vs_euclidean()
    print("Bar charts saved to:", FIG_DIR)


if __name__ == "__main__":
    main()
