import json
import csv
import heapq
import argparse
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Any
from prettytable import PrettyTable
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

import networkx as nx
import matplotlib.pyplot as plt

import sys
import os

class AlgorithmError(Exception):
    pass

class InvalidInputError(AlgorithmError):
    pass

class AlgorithmNotFoundError(AlgorithmError):
    pass

class FileReadError(AlgorithmError):
    pass

class FileWriteError(AlgorithmError):
    pass

class InvalidFormatError(AlgorithmError):
    pass

class InvalidInputError(Exception):
    pass

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_edge(self, u: int, v: int, w: int, directed=False) -> None:
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, w))
        if not directed:
            self.graph[v].append((u, w))

    def to_dict(self) -> Dict[str, List[Tuple[int, int]]]:
        return {str(v): [(u, w) for u, w in self.graph[v]] for v in self.graph}

def create_graph_from_dict(graph_dict: Dict[int, List[Tuple[int, int]]]) -> Graph:
    g = Graph()
    for u, edges in graph_dict.items():
        for v, w in edges:
            g.add_edge(u, v, w)
    return g

def read_from_file(file_path: str) -> Graph:
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r') as file:
                data = json.load(file)
                return create_graph_from_dict({int(k): v for k, v in data['graph'].items()})
        elif file_path.endswith('.csv'):
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                g = Graph()
                for row in reader:
                    g.add_edge(int(row[0]), int(row[1]), int(row[2]))
                return g
        else:
            with open(file_path, 'r') as file:
                content = file.read().strip().split('\n')
                g = Graph()
                for line in content:
                    u, v, weight = map(int, line.split())
                    g.add_edge(u, v, weight)
                return g
    except Exception as e:
        raise FileReadError(f"Error reading file: {str(e)}")

def write_to_file(graph: Graph, file_path: str) -> None:
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'w') as file:
                json.dump({'graph': graph.to_dict()}, file)
        elif file_path.endswith('.csv'):
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for u in graph.graph:
                    for v, weight in graph.graph[u]:
                        writer.writerow([u, v, weight])
        else:
            with open(file_path, 'w') as file:
                for u in graph.graph:
                    for v, weight in graph.graph[u]:
                        file.write(f"{u} {v} {weight}\n")
    except Exception as e:
        raise FileWriteError(f"Error writing to file: {str(e)}")

def format_output(result, output_format):
    if output_format == 'bfs' or output_format == 'dfs':
        return f"Traversal order: {' -> '.join(map(str, result))}"
    elif output_format == 'dijkstra':
        return "\n".join([f"Distance to node {node}: {dist}" for node, dist in result.items()])
    elif output_format == 'prim' or output_format == 'kruskal':
        return f"Minimum Spanning Tree edges: {result}"
    elif output_format == 'topological_sort':
        return f"Topological order: {' -> '.join(map(str, result))}"
    elif output_format == 'floyd_warshall':
        return "\n".join([f"Shortest path from {i} to {j}: {dist}" for (i, j), dist in result.items()])
    elif output_format == 'is_cyclic':
        return f"Graph {'contains' if result else 'does not contain'} a cycle"
    elif output_format == 'strongly_connected_components':
        return f"Strongly Connected Components: {result}"
    else:
        raise InvalidFormatError(f"Unsupported output format: {output_format}")

def bfs(graph: Graph, start: int) -> List[int]:
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            queue.extend(v for v, _ in graph.graph[vertex] if v not in visited)

    return result

def dfs(graph: Graph, start: int) -> List[int]:
    visited = set()
    result = []

    def dfs_recursive(v):
        visited.add(v)
        result.append(v)
        for neighbor, _ in graph.graph[v]:
            if neighbor not in visited:
                dfs_recursive(neighbor)

    dfs_recursive(start)
    return result

def dijkstra(graph: Graph, start: int) -> Dict[int, int]:
    distances = {vertex: float('infinity') for vertex in graph.graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph.graph[current_vertex]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def bellman_ford(graph: Graph, start: int) -> Dict[int, int]:
    distances = {vertex: float('infinity') for vertex in graph.graph}
    distances[start] = 0

    for _ in range(len(graph.graph) - 1):
        for u in graph.graph:
            for v, weight in graph.graph[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    for u in graph.graph:
        for v, weight in graph.graph[u]:
            if distances[u] + weight < distances[v]:
                raise ValueError("Graph contains a negative weight cycle")

    return distances

def prim(graph: Graph) -> List[Tuple[int, int, int]]:
    start_vertex = next(iter(graph.graph))
    mst = []
    visited = set([start_vertex])
    edges = [(weight, start_vertex, to) for to, weight in graph.graph[start_vertex]]
    heapq.heapify(edges)

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.append((frm, to, weight))
            for next_to, next_weight in graph.graph[to]:
                if next_to not in visited:
                    heapq.heappush(edges, (next_weight, to, next_to))

    return mst

def kruskal(graph: Graph) -> List[Tuple[int, int, int]]:
    def find(parent, i):
        if parent[i] == i:
            return i
        return find(parent, parent[i])

    def union(parent, rank, x, y):
        xroot = find(parent, x)
        yroot = find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    edges = []
    for u in graph.graph:
        for v, weight in graph.graph[u]:
            edges.append((u, v, weight))
    edges.sort(key=lambda x: x[2])

    vertices = set(graph.graph.keys()).union({v for u in graph.graph for v, _ in graph.graph[u]})
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}

    mst = []
    for u, v, weight in edges:
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            mst.append((u, v, weight))
            union(parent, rank, x, y)

    return mst

def topological_sort(graph: Graph) -> List[int]:
    def dfs(v):
        if v in visited:
            return
        visited.add(v)
        for neighbor, _ in graph.graph[v]:
            if neighbor in path:
                raise ValueError("Graph contains a cycle, topological sort is not possible")
            if neighbor not in visited:
                path.add(neighbor)
                dfs(neighbor)
                path.remove(neighbor)
        stack.append(v)

    visited = set()
    stack = []
    path = set()
    for vertex in graph.graph:
        if vertex not in visited:
            path.add(vertex)
            dfs(vertex)
            path.remove(vertex)
    
    return stack[::-1]

def test_topological_sort(self):
    # Создаем направленный ациклический граф для тестирования топологической сортировки
    dag = Graph()
    dag_dict = {
        0: [(1, 1), (2, 1)],
        1: [(3, 1)],
        2: [(3, 1)],
        3: [(4, 1)],
        4: []
    }
    for u, edges in dag_dict.items():
        for v, w in edges:
            dag.add_edge(u, v, w, directed=True)
    
    result = run_algorithm(dag, 'topological_sort')
    self.assertEqual(result, [0, 2, 1, 3, 4])

def floyd_warshall(graph: Graph) -> Dict[Tuple[int, int], int]:
    dist = {(u, v): float('infinity') for u in graph.graph for v in graph.graph}
    for u in graph.graph:
        dist[(u, u)] = 0
        for v, weight in graph.graph[u]:
            dist[(u, v)] = weight
    
    for k in graph.graph:
        for i in graph.graph:
            for j in graph.graph:
                dist[(i, j)] = min(dist[(i, j)], dist[(i, k)] + dist[(k, j)])
    
    return dist

def is_cyclic(graph: Graph) -> bool:
    def dfs(v):
        visited.add(v)
        rec_stack.add(v)
        for neighbor, _ in graph.graph[v]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(v)
        return False

    visited = set()
    rec_stack = set()
    for vertex in graph.graph:
        if vertex not in visited:
            if dfs(vertex):
                return True
    return False

def strongly_connected_components(graph: Graph) -> List[List[int]]:
    def dfs(v, stack):
        visited.add(v)
        for neighbor, _ in graph.graph[v]:
            if neighbor not in visited:
                dfs(neighbor, stack)
        stack.append(v)

    def transpose():
        g = Graph()
        for u in graph.graph:
            for v, weight in graph.graph[u]:
                g.add_edge(v, u, weight)
        return g

    def dfs_scc(v, component):
        visited.add(v)
        component.append(v)
        for neighbor, _ in transposed.graph[v]:
            if neighbor not in visited:
                dfs_scc(neighbor, component)

    visited = set()
    stack = []
    for vertex in graph.graph:
        if vertex not in visited:
            dfs(vertex, stack)

    transposed = transpose()
    visited.clear()
    components = []
    while stack:
        v = stack.pop()
        if v not in visited:
            component = []
            dfs_scc(v, component)
            components.append(component)

    return components

def visualize_graph(graph: Graph, algorithm_result=None, algorithm_name=None):
    G = nx.Graph()
    for u in graph.graph:
        for v, weight in graph.graph[u]:
            G.add_edge(u, v, weight=weight)

    fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    if algorithm_result and algorithm_name:
        if algorithm_name in ['bfs', 'dfs']:
            path_edges = list(zip(algorithm_result, algorithm_result[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, ax=ax)
        elif algorithm_name in ['prim', 'kruskal']:
            nx.draw_networkx_edges(G, pos, edgelist=algorithm_result, edge_color='r', width=2, ax=ax)

    ax.set_title(f"Graph Visualization{' - ' + algorithm_name if algorithm_name else ''}")
    ax.axis('off')
    plt.show()

def run_algorithm(graph: Graph, algorithm: str, start: int = None) -> Any:
    if not graph.graph:
        raise InvalidInputError("Graph is empty")

    algorithms = {
        'bfs': lambda: bfs(graph, start),
        'dfs': lambda: dfs(graph, start),
        'dijkstra': lambda: dijkstra(graph, start),
        'bellman_ford': lambda: bellman_ford(graph, start),
        'prim': lambda: prim(graph),
        'kruskal': lambda: kruskal(graph),
        'topological_sort': lambda: topological_sort(graph),
        'floyd_warshall': lambda: floyd_warshall(graph),
        'is_cyclic': lambda: is_cyclic(graph),
        'strongly_connected_components': lambda: strongly_connected_components(graph)
    }

    if algorithm not in algorithms:
        raise AlgorithmNotFoundError(f"Algorithm '{algorithm}' not found")

    if algorithm in ['bfs', 'dfs', 'dijkstra', 'bellman_ford'] and start is None:
        raise InvalidInputError(f"Start vertex is required for {algorithm} algorithm")

    result = algorithms[algorithm]()

    # Визуализация графа и результата
    plt.figure(figsize=(12, 8))
    G = nx.Graph(graph.graph)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if algorithm in ['bfs', 'dfs'] and isinstance(result, list):
        path_edges = list(zip(result, result[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
    elif algorithm in ['prim', 'kruskal'] and isinstance(result, list):
        nx.draw_networkx_edges(G, pos, edgelist=result, edge_color='r', width=2)

    plt.title(f"Graph Visualization - {algorithm}")
    plt.axis('off')
    plt.tight_layout()
    
    # Создаем директорию для сохранения изображений, если она не существует
    os.makedirs('graph_visualizations', exist_ok=True)
    
    # Сохраняем изображение
    filename = f"graph_visualizations/graph_{algorithm}.png"
    plt.savefig(filename)
    plt.close()
    print(f"Graph visualization saved as {filename}")

    return result

def main():
    parser = argparse.ArgumentParser(description="Graph Algorithms")
    parser.add_argument("--input_file", help="Path to the input file")
    parser.add_argument("--algorithm", choices=[
        'bfs', 'dfs', 'dijkstra', 'bellman_ford', 'prim', 'kruskal',
        'topological_sort', 'floyd_warshall', 'is_cyclic', 'strongly_connected_components'
    ], help="Algorithm to run")
    parser.add_argument("--start", type=int, help="Starting vertex for algorithms that require it")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", choices=['json', 'pretty_json', 'csv', 'table', 'text'], 
                        default='text', help="Output format")
    parser.add_argument("--visualize", action="store_true", help="Visualize the graph")

    args = parser.parse_args()

    try:
        if args.input_file:
            graph = read_from_file(args.input_file)
        else:
            # Если файл не указан, используем граф по умолчанию
            default_graph = {
                0: [(1, 4), (2, 3)],
                1: [(2, 1), (3, 2)],
                2: [(3, 5)],
                3: []
            }
            graph = create_graph_from_dict(default_graph)

        if args.visualize:
            visualize_graph(graph)

        if args.algorithm:
            result = run_algorithm(graph, args.algorithm, args.start)
            formatted_result = format_output(result, args.algorithm)

            if args.output:
                with open(args.output, 'w') as f:
                    if args.format == 'json':
                        json.dump(result, f)
                    elif args.format == 'pretty_json':
                        json.dump(result, f, indent=2)
                    elif args.format == 'csv':
                        writer = csv.writer(f)
                        if isinstance(result, dict):
                            for key, value in result.items():
                                writer.writerow([key, value])
                        elif isinstance(result, list):
                            for item in result:
                                writer.writerow(item)
                    elif args.format == 'table':
                        table = PrettyTable()
                        if isinstance(result, dict):
                            table.field_names = ["Key", "Value"]
                            for key, value in result.items():
                                table.add_row([key, value])
                        elif isinstance(result, list):
                            if all(isinstance(item, tuple) for item in result):
                                table.field_names = ["From", "To", "Weight"]
                                for item in result:
                                    table.add_row(item)
                            else:
                                table.field_names = ["Value"]
                                for item in result:
                                    table.add_row([item])
                        f.write(str(table))
                    else:
                        f.write(formatted_result)
                print(f"Result written to {args.output}")
            else:
                if args.format == 'json':
                    print(json.dumps(result))
                elif args.format == 'pretty_json':
                    print(highlight(json.dumps(result, indent=2), JsonLexer(), TerminalFormatter()))
                elif args.format == 'csv':
                    writer = csv.writer(sys.stdout)
                    if isinstance(result, dict):
                        for key, value in result.items():
                            writer.writerow([key, value])
                    elif isinstance(result, list):
                        for item in result:
                            writer.writerow(item)
                elif args.format == 'table':
                    table = PrettyTable()
                    if isinstance(result, dict):
                        table.field_names = ["Key", "Value"]
                        for key, value in result.items():
                            table.add_row([key, value])
                    elif isinstance(result, list):
                        if all(isinstance(item, tuple) for item in result):
                            table.field_names = ["From", "To", "Weight"]
                            for item in result:
                                table.add_row(item)
                        else:
                            table.field_names = ["Value"]
                            for item in result:
                                table.add_row([item])
                    print(table)
                else:
                    print(formatted_result)

    except (AlgorithmError, FileReadError, FileWriteError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()