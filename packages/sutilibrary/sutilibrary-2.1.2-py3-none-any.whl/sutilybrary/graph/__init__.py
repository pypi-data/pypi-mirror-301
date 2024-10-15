from .graph_algorithms import (
    Graph,
    create_graph_from_dict,
    read_from_file,
    write_to_file,
    format_output,
    bfs,
    dfs,
    dijkstra,
    bellman_ford,
    prim,
    kruskal,
    topological_sort,
    floyd_warshall,
    is_cyclic,
    strongly_connected_components,
    visualize_graph,  # Add this line
    AlgorithmError,
    InvalidInputError,
    AlgorithmNotFoundError,
    FileReadError,
    FileWriteError,
    InvalidFormatError
)

__all__ = [
    'Graph',
    'create_graph_from_dict',
    'bfs',
    'dfs',
    'dijkstra',
    'bellman_ford',
    'prim',
    'kruskal',
    'topological_sort',
    'floyd_warshall',
    'is_cyclic',
    'strongly_connected_components',
    'read_from_file',
    'write_to_file',
    'format_output',
    'visualize_graph',  # Add this line
    'AlgorithmError',
    'InvalidInputError',
    'AlgorithmNotFoundError',
    'FileReadError',
    'FileWriteError',
    'InvalidFormatError',
    'run_algorithm'
]

def run_algorithm(graph: Graph, algorithm: str, start: int = None):
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

    result = algorithms[algorithm]()
    visualize_graph(graph, result, algorithm)  # Add this line
    return result

__version__ = '1.0.0'