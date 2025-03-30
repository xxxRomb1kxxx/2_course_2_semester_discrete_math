import numpy as np
import networkx as nx


def generate_sparse_graph(n):
    avg_degree = int(n ** 0.5)
    p = avg_degree / n
    G = nx.gnp_random_graph(n, p)
    while not nx.is_connected(G):
        G = nx.gnp_random_graph(n, p)

    return G


def insert_clique(G, nodes):
    """Вставляет клику (полносвязный подграф) в граф."""
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            G.add_edge(nodes[i], nodes[j])


def insert_bipartite_clique(G, part1, part2):
    """Вставляет двудольный полный подграф K3,5."""
    for u in part1:
        for v in part2:
            G.add_edge(u, v)


def generate_graph_with_cliques(n):
    G = generate_sparse_graph(n)

    # Вставляем K6
    k6_nodes = np.random.choice(list(G.nodes), 6, replace=False)
    insert_clique(G, k6_nodes)

    # Вставляем K3,5, если хватает вершин
    remaining_nodes = list(set(G.nodes) - set(k6_nodes))
    if len(remaining_nodes) >= 8:
        k3_nodes = np.random.choice(remaining_nodes, 3, replace=False)
        remaining_nodes = list(set(remaining_nodes) - set(k3_nodes))
        k5_nodes = np.random.choice(remaining_nodes, 5, replace=False)
        insert_bipartite_clique(G, k3_nodes, k5_nodes)

    return G


def floyd_warshall_distances(G):
    n = G.number_of_nodes()
    dist_matrix = np.full((n, n), np.inf)
    np.fill_diagonal(dist_matrix, 0)

    node_list = list(G.nodes)
    index_map = {node: i for i, node in enumerate(node_list)}

    for u, v in G.edges():
        i, j = index_map[u], index_map[v]
        dist_matrix[i][j] = dist_matrix[j][i] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = min(dist_matrix[i][j], dist_matrix[i][k] + dist_matrix[k][j])

    return dist_matrix


sizes = [15, 33, 77, 220, 350]
for size in sizes:
    G = generate_graph_with_cliques(size)
    distances = floyd_warshall_distances(G)
    print(f"Матрица расстояний для графа с {size} вершинами вычислена.")
    print(distances[:15, :15])