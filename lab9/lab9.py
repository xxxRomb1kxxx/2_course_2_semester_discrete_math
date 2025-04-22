import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite

# Список рёбер
edges = [
    (4, 13), (3, 10), (10, 13), (8, 12), (10, 16), (9, 13),
    (2, 13), (10, 15), (8, 14), (5, 6), (4, 6), (4, 12), (2, 7),
    (7, 9), (10, 14), (10, 12), (8, 16), (4, 15), (9, 15),
    (3, 5), (4, 7), (5, 15), (3, 9), (10, 11), (5, 11), (2, 11),
    (7, 10), (2, 15), (2, 14), (4, 14), (7, 8), (3, 8), (5, 16),
    (2, 12), (5, 7)
]

# Построение графа
G = nx.Graph()
G.add_edges_from(edges)

# Проверка на двудольность
if nx.is_bipartite(G):
    print("✅ Граф уже двудольный.")
    G_bipartite = G.copy()
else:
    print("⚠️ Граф не двудольный. Будем исправлять.")

    def make_bipartite(graph):
        g = graph.copy()
        while not nx.is_bipartite(g):
            try:
                cycle = nx.find_cycle(g)
                g.remove_edge(*cycle[0])
            except nx.NetworkXNoCycle:
                break
        return g

    G_bipartite = make_bipartite(G)

# Разделяем на доли
left_nodes, right_nodes = bipartite.sets(G_bipartite)

# Поиск максимального паросочетания
def ford_fulkerson(graph):
    matching = {}
    def dfs(v, visited):
        for u in graph[v]:
            if u in visited:
                continue
            visited.add(u)
            if u not in matching or dfs(matching[u], visited):
                matching[u] = v
                matching[v] = u
                return True
        return False

    for v in left_nodes:
        dfs(v, set())

    return matching



def max_matching_kun(graph):
    matching = {}
    def dfs(v, visited):
        for u in graph[v]:
            if u in visited:
                continue
            visited.add(u)
            if u not in matching or dfs(matching[u], visited):
                matching[u] = v
                matching[v] = u
                return True
        return False

    for v in left_nodes:
        dfs(v, set())

    return matching


matching_ff = ford_fulkerson(G_bipartite)
matching_kun = max_matching_kun(G_bipartite)


# Визуализация
pos = nx.spring_layout(G_bipartite, seed=42)
plt.figure(figsize=(10, 8))
nx.draw_networkx_nodes(G_bipartite, pos, nodelist=left_nodes, node_color='skyblue', node_size=500, label='Левая доля')
nx.draw_networkx_nodes(G_bipartite, pos, nodelist=right_nodes, node_color='lightgreen', node_size=500, label='Правая доля')
nx.draw_networkx_edges(G_bipartite, pos, edge_color='gray', width=1.2, alpha=0.8)
nx.draw_networkx_labels(G_bipartite, pos, font_size=12)
plt.legend()
plt.title("Двудольный граф и паросочетание")
plt.axis('off')
plt.tight_layout()
plt.show()
plt.figure(figsize=(12, 5))
plt.subplot(121)
pos = nx.bipartite_layout(G_bipartite, left_nodes)
nx.draw_networkx_nodes(G_bipartite, pos, nodelist=left_nodes, node_color='skyblue', node_size=500, label='Левая доля')
nx.draw_networkx_nodes(G_bipartite, pos, nodelist=right_nodes, node_color='lightgreen', node_size=500, label='Правая доля')
nx.draw_networkx_edges(G_bipartite, pos, edge_color='gray', width=1.2, alpha=0.5)
# Выделяем рёбра паросочетания
matching_edges_ff = [(u, v) for u, v in matching_ff.items() if u < v]
nx.draw_networkx_edges(G_bipartite, pos, edgelist=matching_edges_ff, edge_color='red', width=2)
nx.draw_networkx_labels(G_bipartite, pos, font_size=12)
plt.title(f"Паросочетание Форда-Фалкерсона\n(размер = {len(matching_ff)//2})")
plt.legend()
plt.axis('off')

# Визуализация паросочетания Куна
plt.subplot(122)
pos = nx.bipartite_layout(G_bipartite, left_nodes)
nx.draw_networkx_nodes(G_bipartite, pos, nodelist=left_nodes, node_color='skyblue', node_size=500, label='Левая доля')
nx.draw_networkx_nodes(G_bipartite, pos, nodelist=right_nodes, node_color='lightgreen', node_size=500, label='Правая доля')
nx.draw_networkx_edges(G_bipartite, pos, edge_color='gray', width=1.2, alpha=0.5)
# Выделяем рёбра паросочетания
matching_edges_kun = [(u, v) for u, v in matching_kun.items() if u < v]
nx.draw_networkx_edges(G_bipartite, pos, edgelist=matching_edges_kun, edge_color='blue', width=2)
nx.draw_networkx_labels(G_bipartite, pos, font_size=12)
plt.title(f"Паросочетание Куна\n(размер = {len(matching_kun)//2})")
plt.legend()
plt.axis('off')

plt.tight_layout()
plt.show()


# Вывод
if G_bipartite != G:
    removed_edges = set(G.edges()) - set(G_bipartite.edges())
    print("\nУдалённые рёбра для превращения графа в двудольный:")
    for edge in removed_edges:
        print(edge)
else:
    print("\nНикакие рёбра не были удалены — граф уже двудольный.")

print("Максимальное паросочетание (Форд-Фалкерсон):", matching_ff)
print("Размер паросочетания (Форд-Фалкерсон):", len(matching_ff) // 2)
print("\nМаксимальное паросочетание (Куна):", matching_kun)
print("Размер паросочетания (Куна):", len(matching_kun) // 2)

