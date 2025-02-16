import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict



class RailwayNetwork:
    def __init__(self, stations):
        self.graph = defaultdict(list)
        self.capacity = {}
        self.stations = stations
    
    def add_track(self, u, v, weight, capacity):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))  # Undirected graph
        self.capacity[(u, v)] = capacity
        self.capacity[(v, u)] = capacity  # Capacity in both directions
    
    def dijkstra(self, start, end):
        pq = [(0, start)]  # (cost, node)
        distances = {station: float('inf') for station in self.stations}
        distances[start] = 0
        prev_nodes = {station: None for station in self.stations}
        
        while pq:
            current_distance, node = heapq.heappop(pq)
            if node == end:
                break
            
            for neighbor, weight in self.graph[node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    prev_nodes[neighbor] = node
                    heapq.heappush(pq, (distance, neighbor))
        
        path, node = [], end
        while node:
            path.append(node)
            node = prev_nodes[node]
        return path[::-1], distances[end]
    
    def kruskal_mst(self):
        edges = []
        for u in self.graph:
            for v, weight in self.graph[u]:
                edges.append((weight, u, v))
        
        edges = sorted(edges)
        parent = {station: station for station in self.stations}
        
        def find(station):
            if parent[station] != station:
                parent[station] = find(parent[station])
            return parent[station]
        
        def union(station1, station2):
            root1, root2 = find(station1), find(station2)
            if root1 != root2:
                parent[root2] = root1
        
        mst = []
        for weight, u, v in edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, weight))
        return mst
    
    def ford_fulkerson(self, source, sink):
        residual_capacity = self.capacity.copy()
        max_flow = 0
        
        def bfs():
            parent = {station: None for station in self.stations}
            visited = set()
            queue = [source]
            visited.add(source)
            while queue:
                u = queue.pop(0)
                for v, _ in self.graph[u]:
                    if v not in visited and residual_capacity.get((u, v), 0) > 0:
                        parent[v] = u
                        if v == sink:
                            return parent
                        queue.append(v)
                        visited.add(v)
            return None
        
        while True:
            parent = bfs()
            if not parent:
                break
            
            path_flow = float('inf')
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, residual_capacity[(u, v)])
                v = u
            
            v = sink
            while v != source:
                u = parent[v]
                residual_capacity[(u, v)] -= path_flow
                residual_capacity[(v, u)] += path_flow
                v = u
            
            max_flow += path_flow
        
        return max_flow
    
    def visualize_network(self):
        G = nx.Graph()
        for u in self.graph:
            for v, weight in self.graph[u]:
                G.add_edge(u, v, weight=weight)
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

# Example usage
stations = ['A', 'B', 'C', 'D', 'E']
network = RailwayNetwork(stations)
network.add_track('A', 'B', 4, 10)
network.add_track('A', 'C', 2, 15)
network.add_track('B', 'C', 1, 10)
network.add_track('B', 'D', 5, 10)
network.add_track('C', 'D', 8, 10)
network.add_track('C', 'E', 10, 15)
network.add_track('D', 'E', 2, 20)

# Shortest Path
print("Shortest Path from A to E:", network.dijkstra('A', 'E'))

# Minimum Spanning Tree
print("Minimum Spanning Tree:", network.kruskal_mst())

# Maximum Flow from A to E
print("Maximum Train Flow from A to E:", network.ford_fulkerson('A', 'E'))

# Visualization
network.visualize_network()

print(nx.__version__)
