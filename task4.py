import uuid

import networkx as nx
import matplotlib.pyplot as plt
import heapq
from typing import List, Optional


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def build_heap_tree(heap: List[int]) -> Optional[Node]:
    """Перетворює масив-купу у зв'язне бінарне дерево з вузлами Node."""
    if not heap:
        return None

    nodes: List[Node] = []
    for i, value in enumerate(heap):
        color = "gold" if i == 0 else "skyblue"
        nodes.append(Node(value, color=color))

    n = len(nodes)
    for i in range(n):
        left_i = 2 * i + 1
        right_i = 2 * i + 2
        if left_i < n:
            nodes[i].left = nodes[left_i]
        if right_i < n:
            nodes[i].right = nodes[right_i]

    return nodes[0]


def visualize_heap(values: List[int]) -> None:
    heap = list(values)
    heapq.heapify(heap)

    root = build_heap_tree(heap)
    draw_tree(root)


def main() -> None:
    values = [4, 10, 3, 5, 1, 2]

    visualize_heap(values)


if __name__ == "__main__":
    main()
