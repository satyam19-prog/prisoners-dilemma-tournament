import random
import numpy as np
import matplotlib.pyplot as plt
from strategies import ALL_STRATEGIES
from engine import run_tournament

# Fix random seed for reproducible results
random.seed(42)


def experiment_1_standard():
    print("\n=== EXPERIMENT 1: Standard Round-Robin (200 rounds, 0% noise) ===")
    scores, coop_rates, matrix = run_tournament(ALL_STRATEGIES, rounds=200, noise=0.0, trials=10)

    # Sort strategies by score descending
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for rank, (name, score) in enumerate(sorted_items, start=1):
        avg_per_round = score / (200 * len(ALL_STRATEGIES))
        print(f"{rank}. {name:<18} | Total: {score:7.1f} | Avg/Round: {avg_per_round:.2f} | Coop: {coop_rates[name]:5.1f}%")

    # --- Chart 1: Leaderboard Bar Chart ---
    names = [item[0] for item in sorted_items][::-1]
    vals = [item[1] for item in sorted_items][::-1]

    plt.figure(figsize=(9, 5))
    bars = plt.barh(names, vals, color="#2b6cb0")
    plt.xlabel("Total Tournament Score (200 rounds per match)")
    plt.title("Experiment 1: Standard Round-Robin Leaderboard (0% Noise)")
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    for bar in bars:
        width = bar.get_width()
        plt.text(width + 40, bar.get_y() + bar.get_height() / 2, f"{width:.0f}", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig("outputs/1_standard_leaderboard.png", dpi=200)
    plt.close()

    # --- Chart 2: Pairwise Score Heatmap ---
    ordered_names = [item[0] for item in sorted_items]
    grid = np.zeros((len(ordered_names), len(ordered_names)))
    for i, n1 in enumerate(ordered_names):
        for j, n2 in enumerate(ordered_names):
            grid[i, j] = matrix[n1][n2]

    plt.figure(figsize=(8, 6.5))
    plt.imshow(grid, cmap="YlGnBu", aspect="auto")
    plt.colorbar(label="Row Strategy Score (out of 1000 max)")
    plt.xticks(range(len(ordered_names)), ordered_names, rotation=35, ha="right")
    plt.yticks(range(len(ordered_names)), ordered_names)
    plt.title("Experiment 1: Pairwise Matchup Scores (Row vs. Column)")

    for i in range(len(ordered_names)):
        for j in range(len(ordered_names)):
            val = grid[i, j]
            text_color = "white" if val > 500 else "black"
            plt.text(j, i, f"{val:.0f}", ha="center", va="center", color=text_color, fontsize=8)

    plt.tight_layout()
    plt.savefig("outputs/2_pairwise_heatmap.png", dpi=200)
    plt.close()


def experiment_2_noise():
    print("\n=== EXPERIMENT 2: Noise Sensitivity (0% to 20% error rate) ===")
    noise_levels = [0.0, 0.02, 0.05, 0.10, 0.15, 0.20]
    results = {name: [] for name in ALL_STRATEGIES.keys()}

    for noise in noise_levels:
        scores, _, _ = run_tournament(ALL_STRATEGIES, rounds=200, noise=noise, trials=15)
        for name in ALL_STRATEGIES.keys():
            avg_per_round = scores[name] / (200 * len(ALL_STRATEGIES))
            results[name].append(avg_per_round)

    # Print summary at 10% noise
    print("Average score per round at 10% noise:")
    idx_10 = noise_levels.index(0.10)
    ranked_10 = sorted(results.items(), key=lambda x: x[1][idx_10], reverse=True)
    for rank, (name, vals) in enumerate(ranked_10, start=1):
        print(f"{rank}. {name:<18} | Avg/Round: {vals[idx_10]:.2f}")

    # --- Chart 3: Noise Sensitivity Line Chart ---
    plt.figure(figsize=(9, 5.5))
    noise_pct = [n * 100 for n in noise_levels]

    for name, vals in results.items():
        plt.plot(noise_pct, vals, marker="o", linewidth=2, label=name)

    plt.xlabel("Noise Level (% chance of accidental move flip)")
    plt.ylabel("Average Score per Round")
    plt.title("Experiment 2: Effect of Noise on Strategy Performance")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="best", fontsize=8.5)
    plt.tight_layout()
    plt.savefig("outputs/3_noise_sensitivity.png", dpi=200)
    plt.close()


def experiment_3_horizon():
    print("\n=== EXPERIMENT 3: Short Horizon (10 rounds) vs. Long Horizon (200 rounds) ===")
    short_scores, _, _ = run_tournament(ALL_STRATEGIES, rounds=10, noise=0.0, trials=10)
    long_scores, _, _ = run_tournament(ALL_STRATEGIES, rounds=200, noise=0.0, trials=10)

    names = list(ALL_STRATEGIES.keys())
    short_avg = [short_scores[n] / (10 * len(names)) for n in names]
    long_avg = [long_scores[n] / (200 * len(names)) for n in names]

    for i, name in enumerate(names):
        print(f"{name:<18} | 10-Round Avg: {short_avg[i]:.2f} | 200-Round Avg: {long_avg[i]:.2f}")

    # --- Chart 4: Horizon Comparison Grouped Bar Chart ---
    x = np.arange(len(names))
    width = 0.35

    plt.figure(figsize=(9.5, 5))
    plt.bar(x - width / 2, short_avg, width, label="Short Horizon (10 rounds)", color="#dd6b20")
    plt.bar(x + width / 2, long_avg, width, label="Long Horizon (200 rounds)", color="#2f855a")

    plt.ylabel("Average Score per Round")
    plt.title("Experiment 3: Shadow of the Future (Short vs. Long Horizon)")
    plt.xticks(x, names, rotation=25, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/4_horizon_comparison.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    experiment_1_standard()
    experiment_2_noise()
    experiment_3_horizon()
    print("\nAll 4 charts saved successfully in the 'outputs/' folder!")