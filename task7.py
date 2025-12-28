import argparse
import collections
import random
from typing import Dict

import matplotlib.pyplot as plt

ANALYTIC_COUNTS: Dict[int, int] = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 5,
    9: 4,
    10: 3,
    11: 2,
    12: 1,
}
ANALYTIC_PROBS: Dict[int, float] = {s: c / 36 for s, c in ANALYTIC_COUNTS.items()}


def simulate_rolls(trials: int) -> Dict[int, int]:
    counts = collections.Counter()
    for _ in range(trials):
        roll_sum = random.randint(1, 6) + random.randint(1, 6)
        counts[roll_sum] += 1
    for s in range(2, 13):
        counts.setdefault(s, 0)
    return dict(counts)


def to_probabilities(counts: Dict[int, int], total: int) -> Dict[int, float]:
    return {s: counts[s] / total for s in sorted(counts)}


def print_table(sim_counts: Dict[int, int], sim_probs: Dict[int, float], total: int) -> None:
    print("Сума | Симуляція (імовірність) | Аналітична (імовірність) | Абс. похибка")
    print("-" * 74)
    for s in range(2, 13):
        sim_p = sim_probs[s]
        an_p = ANALYTIC_PROBS[s]
        diff = abs(sim_p - an_p)
        print(
            f"{s:>4} | {sim_counts[s]:>8} ({sim_p:6.2%}) | "
            f"{ANALYTIC_COUNTS[s]:>2}/36 ({an_p:6.2%}) | {diff:6.4f}"
        )
    print(f"\nКількість спроб: {total}")


def plot_probabilities(sim_probs: Dict[int, float]) -> None:
    sums = list(range(2, 13))
    sim = [sim_probs[s] for s in sums]
    analytic = [ANALYTIC_PROBS[s] for s in sums]

    width = 0.4
    x = range(len(sums))

    plt.figure(figsize=(9, 5))
    plt.bar([i - width / 2 for i in x], analytic, width=width, label="Аналітичні")
    plt.bar([i + width / 2 for i in x], sim, width=width, label="Монте-Карло")
    plt.xticks(list(x), sums)
    plt.ylabel("Імовірність")
    plt.xlabel("Сума на двох кубиках")
    plt.title("Порівняння аналітичних та емпіричних імовірностей")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Метод Монте-Карло для ймовірностей сум двох кубиків",
    )
    parser.add_argument(
        "-n",
        "--trials",
        type=int,
        default=100_000,
        help="кількість кидків",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="не показувати графік (лише таблиця в консолі)",
    )
    args = parser.parse_args()

    counts = simulate_rolls(args.trials)
    probs = to_probabilities(counts, args.trials)
    print_table(counts, probs, args.trials)

    if not args.no_plot:
        plot_probabilities(probs)


if __name__ == "__main__":
    main()
