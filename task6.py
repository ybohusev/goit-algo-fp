from typing import Dict, List, Tuple


ItemInfo = Dict[str, int]
Items = Dict[str, ItemInfo]


def greedy_algorithm(items: Items, budget: int) -> List[str]:
    sorted_items = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )

    chosen: List[str] = []
    remaining = budget
    for name, info in sorted_items:
        if info["cost"] <= remaining:
            chosen.append(name)
            remaining -= info["cost"]
    return chosen


def dynamic_programming(items: Items, budget: int) -> List[str]:
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    calories = [items[n]["calories"] for n in names]
    n = len(names)

    dp: List[Tuple[int, int]] = [ (0, -1) for _ in range(budget + 1) ]

    parent = [[False] * (budget + 1) for _ in range(n)]

    for i in range(n):
        c, cal = costs[i], calories[i]
        for w in range(budget, c - 1, -1):
            if dp[w - c][0] + cal > dp[w][0]:
                dp[w] = (dp[w - c][0] + cal, w - c)
                parent[i][w] = True

    best_w = max(range(budget + 1), key=lambda w: dp[w][0])

    chosen: List[str] = []
    w = best_w
    for i in range(n - 1, -1, -1):
        if parent[i][w]:
            chosen.append(names[i])
            w = dp[w][1]

    return list(reversed(chosen))


def main():
    items: Items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350},
    }
    budget = 100

    greedy_choice = greedy_algorithm(items, budget)
    dp_choice = dynamic_programming(items, budget)

    print(f"Бюджет: {budget}")
    print("Жадібний вибір:", greedy_choice)
    print("ДП оптимальний вибір:", dp_choice)


if __name__ == "__main__":
    main()
