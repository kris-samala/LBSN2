import networkx as nx
import pickle
import numpy as np

class LocationGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, name):
        self.graph.add_node(name)

    def add_edge(self, node1, node2, w=1):
        if node1 != None:
            if self.graph.has_edge(node1, node2):
                self.graph[node1][node2]['weight'] += w
            else:
                self.graph.add_edge(node1, node2, weight = w)

    def make_connected(self, w):
        for node1 in self.graph.nodes():
            for node2 in self.graph.nodes():
                self.add_edge(node1, node2, w)

    def set_coord(self, node, latd, longd):
        self.graph.add_node(node, latitude = latd, longitude = longd)

    def set_weight(self, name, weight):
        self.graph.node[name]['weight'] = weight

    def get_weight(self, name):
        return self.graph.node[name]['weight']

    def contains(self, name):
        return name in self.graph

    def neighbors(self, node):
        return self.graph.neighbors(node)

    def nodes(self):
        return self.graph.nodes()

    def get_nodes_size(self):
        return len(self.graph)

    def get_edges_size(self):
        return self.graph.size()

    def edge_weight(self, node1, node2):
        return self.graph[node1][node2]['weight']

    def total_edge_weights(self, node):
        total = 0
        for nb in self.graph.neighbors(node):
            total += self.graph[node][nb]['weight']

        return total

    def transition_matrix(self, nodes):
        size = len(nodes)
        T = np.zeros(shape=(size,size))

        for i in range(size):
            n1 = nodes[i]
            sum_w = self.total_edge_weights(n1)
            for j in range(size):
                n2 = nodes[j]
                w = self.edge_weight(n1, n2)
                T[i,j] = w / float(sum_w)

        return T


    def save(self, filename):
        pickle.dump(self.graph.nodes(), open(filename+"_nodes.pickle", "wb"))
        pickle.dump(self.graph.edges(data=True), open(filename+"_edges.pickle", "wb"))
        nx.write_gpickle(self.graph, filename + ".gpickle")

    def load(self, filename):
        self.graph = nx.read_gpickle(filename + ".gpickle")

    def write(self, filename):
        out = open(filename, 'w')
        for node1,node2,data in self.graph.edges_iter(data=True):
            out.write(str(node1) + "\t" + str(node2) + "\t" + str(data) + "\n")
        out.close()
        nx.write_gexf(self.graph, filename+".gexf")

