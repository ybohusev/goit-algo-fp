import heapq
from typing import Dict, List, Tuple

import networkx as nx


Edge = Tuple[str, str, float]


def dijkstra(graph: nx.Graph, start: str) -> tuple[Dict[str, float], Dict[str, str | None]]:
    distances: Dict[str, float] = {v: float("inf") for v in graph.nodes}
    previous: Dict[str, str | None] = {v: None for v in graph.nodes}

    if start not in graph:
        raise ValueError(f"Початкова вершина '{start}' відсутня у графі")

    distances[start] = 0
    heap: List[Tuple[float, str]] = [(0, start)]

    while heap:
        current_distance, u = heapq.heappop(heap)

        if current_distance > distances[u]:
            continue

        for neighbor, data in graph[u].items():
            weight = data.get("weight", 1.0)
            path_distance = current_distance + weight
            if path_distance < distances[neighbor]:
                distances[neighbor] = path_distance
                previous[neighbor] = u
                heapq.heappush(heap, (path_distance, neighbor))

    return distances, previous


def restore_path(previous: Dict[str, str | None], start: str, target: str) -> List[str]:
    path: List[str] = []
    current = target

    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous[current]

    if not path or path[-1] != start:
        return [] 

    return list(reversed(path))


def build_sample_graph() -> nx.Graph:
    graph = nx.Graph()
    edges: List[Edge] = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "Z", 6),
        ("E", "Z", 3),
        ("F", "F", 10),
        ("G", "E", 5),
        ("G", "A", 20),
        ("S", "E", 20),
        ("S", "A", 24),
    ]

    for u, v, w in edges:
        graph.add_edge(u, v, weight=w)

    return graph


def main() -> None:

    graph = build_sample_graph()
    distances, previous = dijkstra(graph, 'A')

    print(f"Найкоротші відстані від 'A':")
    for vertex in sorted(graph.nodes):
        distance = distances[vertex]
        if distance == float("inf"):
            print(f"{vertex}: недосяжно")
            continue

        path = restore_path(previous, 'A', vertex)
        path_str = " -> ".join(path) if path else "шляху немає"
        print(f"{vertex}: {distance} (шлях: {path_str})")


if __name__ == "__main__":
    main()
