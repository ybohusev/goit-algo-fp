import heapq
import uuid
from collections import deque
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key: int, color: str = "#1296F0"):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph: nx.DiGraph, node: Optional[Node], pos, x=0.0, y=0.0, layer: int = 1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2**layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2**layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def build_heap_tree(values: List[int]) -> Optional[Node]:
    if not values:
        return None

    heap = list(values)
    heapq.heapify(heap)

    nodes: List[Node] = []
    for i, value in enumerate(heap):
        color = "#ffbf00" if i == 0 else "#1296F0"
        nodes.append(Node(value, color=color))

    n = len(nodes)
    for i in range(n):
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n:
            nodes[i].left = nodes[l]
        if r < n:
            nodes[i].right = nodes[r]

    return nodes[0]


def dfs(root: Optional[Node]) -> List[Node]:
    if root is None:
        return []
    stack = [root]
    order: List[Node] = []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs(root: Optional[Node]) -> List[Node]:
    if root is None:
        return []
    q: deque[Node] = deque([root])
    order: List[Node] = []
    while q:
        node = q.popleft()
        order.append(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return order

def hex_gradient(n: int, base_color: str = "#1296F0") -> List[str]:
    import matplotlib.colors as mcolors
    base = mcolors.to_rgb(base_color)
    dark = tuple(c * 0.4 for c in base)
    light = tuple(c + (1 - c) * 0.7 for c in base)

    def lerp(a: Tuple[float, float, float], b: Tuple[float, float, float], t: float):
        return tuple(a_i * (1 - t) + b_i * t for a_i, b_i in zip(a, b))

    return [mcolors.to_hex(lerp(dark, light, i / max(1, n - 1))) for i in range(n)]


def snapshot_colors(order: List[Node], step: int, palette: List[str], default_color: str) -> Dict[str, str]:
    colors = {}
    for i, node in enumerate(order):
        if i <= step:
            colors[node.id] = palette[i]
        else:
            colors[node.id] = default_color
    return colors


def draw_combined(root: Optional[Node]):
    if root is None:
        print("Дерево порожнє — немає що візуалізувати.")
        return

    graph = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    add_edges(graph, root, pos)
    labels = {node_id: data["label"] for node_id, data in graph.nodes(data=True)}
    ordered_nodes = list(graph.nodes)

    traversals = {
        "DFS": dfs(root),
        "BFS": bfs(root),
    }
    palettes = {name: hex_gradient(len(order)) for name, order in traversals.items()}

    for name, order in traversals.items():
        print(f"{name}: порядок відвідування =", [n.val for n in order])

    steps = [len(ordered_nodes) - 1]
    default_color = "#D3D3D3"

    for step in steps:
        _, axes = plt.subplots(1, 2, figsize=(12, 5))
        for ax, (name, order) in zip(axes, traversals.items()):
            colors_map = snapshot_colors(order, step, palettes[name], default_color)
            node_colors = [colors_map[node_id] for node_id in ordered_nodes]
            nx.draw(
                graph,
                pos=pos,
                labels=labels,
                arrows=False,
                node_size=2500,
                node_color=node_colors,
                ax=ax,
            )
            ax.set_title(f"{name}")
        plt.tight_layout()
        plt.show()
        return


def visualize_traversals(root: Optional[Node]):
    draw_combined(root)

def main():
    root = build_heap_tree([7, 3, 9, 1, 5, 8, 10])
    visualize_traversals(root)


if __name__ == "__main__":
    main()
