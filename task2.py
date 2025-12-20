import argparse
from typing import List, Tuple

import matplotlib.pyplot as plt

Point = complex
Square = Tuple[Point, Point, Point, Point]


def build_tree(base: Point, vec: Point, level: int, store: List[Square]) -> None:
    v_perp = vec * 1j
    square = (base, base + vec, base + vec + v_perp, base + v_perp)
    store.append(square)

    if level == 0:
        return

    peak = base + v_perp + vec / 2 + (vec / 2) * 1j

    left_vec = peak - (base + v_perp)
    right_vec = (base + vec + v_perp) - peak

    build_tree(base + v_perp, left_vec, level - 1, store)
    build_tree(peak, right_vec, level - 1, store)


def plot_tree(squares: List[Square]) -> None:
    _, ax = plt.subplots()
    color = "red"

    for sq in squares:
        xs = [pt.real for pt in sq] + [sq[0].real]
        ys = [pt.imag for pt in sq] + [sq[0].imag]
        ax.plot(xs, ys, color=color, linewidth=2)

    all_x = [p.real for sq in squares for p in sq]
    all_y = [p.imag for sq in squares for p in sq]
    ax.set_aspect("equal")
    ax.set_xlim(min(all_x) - 0.3, max(all_x) + 0.3)
    ax.set_ylim(min(all_y) - 0.3, max(all_y) + 0.6)
    ax.axis("off")

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--level", type=int, default=8, help="рівень рекурсії"
    )
    args = parser.parse_args()

    squares: List[Square] = []
    base_point = 0 + 0j
    base_vec = 1 + 0j

    build_tree(base_point, base_vec, args.level, squares)
    plot_tree(squares)


if __name__ == "__main__":
    main()
