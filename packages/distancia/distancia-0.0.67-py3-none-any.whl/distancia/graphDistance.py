from .mainClass import Distance
from .vectorDistance import Euclidean,L1
from .tools     import Graph
        
        
class ShortestPath(Distance):
	
    def __init__(self)-> None:
        """
        Initialise la classe avec un graphe représenté sous forme de dictionnaire.
        :param graph: Un dictionnaire représentant le graphe, où les clés sont les nœuds et les valeurs sont des dictionnaires
                      de voisins avec les poids des arêtes.
        """
        super().__init__()
        self.type='graph'


    def compute(self,graph, start_node, end_node):
        """
        Obtient la distance du plus court chemin entre deux nœuds dans le graphe.
        :param start_node: Le nœud de départ.
        :param end_node: Le nœud d'arrivée.
        :return: La distance du plus court chemin.
        """

        return graph.dijkstra(start_node, end_node)
        
    def example(self):
        graph=Graph(Graph.nodes_1,Graph.edges_1)
        distance=self.compute(graph,'A','c')
        print(f"{self.__class__.__name__} distance between A and C in {graph} is {distance:.2f}")



class GraphEditDistance(Distance):
    def __init__(self)-> None:
        """
        Initializes the GraphEditDistance class with two graphs.
        
        :param graph1: The first graph as a dictionary where keys are nodes and values are sets of connected nodes.
        :param graph2: The second graph as a dictionary where keys are nodes and values are sets of connected nodes.
        """
        super().__init__()
        self.type='graph'

        

    def compute(self, graph1, graph2):
        """
        Computes the Graph Edit Distance (GED) between the two graphs.

        :return: The Graph Edit Distance between the two graphs.
        """
        self.g1 = graph1
        self.g2 = graph2
        
        # Compute node differences
        node_diff = self.node_diff()

        # Compute edge differences
        edge_diff = self.edge_diff()

        # Total cost is the sum of node and edge differences
        return node_diff + edge_diff

    def node_diff(self):
        """
        Computes the difference in nodes between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The node difference.
        """
        g1_nodes = set(self.g1.get_nodes())
        g2_nodes = set(self.g2.get_nodes())

        # Nodes to delete from g1 or add to g2
        node_intersection = g1_nodes & g2_nodes
        node_union = g2_nodes | g1_nodes

        # Node difference is the sum of deletions and additions
        return len(node_union) - len(node_intersection)

    def edge_diff(self, g1, g2):
        """
        Computes the difference in edges between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The edge difference.
        """
        g1_edges = set(self.g1.get_edges())
        g2_edges = set(self.g2.get_edges())

        # Edges to delete from g1 or add to g2
        edge_intersection = g1_edges & g2_edges
        edge_union = g2_edges | g1_edges

        # Edge difference is the sum of deletions and additions
        return len(edge_union) + len(edge_intersection)
        
    def example(self):
        graph=Graph(Graph.nodes_1,Graph.edges_1)
        distance=self.compute(graph,'A','c')
        print(f"{self.__class__.__name__} distance between A and C in {graph} is {distance:.2f}")
#claude
import networkx as nx

class SpectralDistance(Distance):
    """
    A class to compute the spectral distance between two graphs.

    The spectral distance is based on the difference between the eigenvalues
    of the Laplacian matrices of the graphs.

    Attributes:
        k (int): Number of eigenvalues to consider (default is None, which uses all eigenvalues)
        normalized (bool): Whether to use normalized Laplacian (default is False)
    """

    def __init__(self, k=None, normalized=False)-> None:
        """
        Initialize the SpectralDistance object.

        Args:
            k (int, optional): Number of eigenvalues to consider. If None, all eigenvalues are used.
            normalized (bool, optional): Whether to use the normalized Laplacian. Defaults to False.
        """
        super().__init__()
        self.type='graph'

        self.k = k
        self.normalized = normalized

    def laplacian_matrix(self, G):
        """
        Compute the Laplacian matrix of the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list of list: Laplacian matrix
        """
        n = G.number_of_nodes()
        L = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    L[i][j] = G.degree(i)
                elif G.has_edge(i, j):
                    L[i][j] = -1
        
        if self.normalized:
            for i in range(n):
                for j in range(n):
                    if G.degree(i) > 0 and G.degree(j) > 0:
                        L[i][j] /= (G.degree(i) * G.degree(j))**0.5
        
        return L

    def eigenvalues(self, matrix):
        """
        Compute eigenvalues using the power iteration method.

        Args:
            matrix (list of list): Input matrix

        Returns:
            list: Approximate eigenvalues
        """
        n = len(matrix)
        eigenvalues = []
        for _ in range(n):
            # Initialize random vector
            v = [1/(n)**0.5 for _ in range(n)]
            for _ in range(100):  # Number of iterations
                # Matrix-vector multiplication
                u = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
                # Normalize
                norm = (sum(x*x for x in u))**0.5
                if norm==0:norm=1
                v = [x/norm for x in u]
            # Compute Rayleigh quotient
            lambda_ = sum(v[i] * sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n))
            eigenvalues.append(lambda_)
            # Deflate the matrix
            for i in range(n):
                for j in range(n):
                    matrix[i][j] -= lambda_ * v[i] * v[j]
        return sorted(eigenvalues)

    def compute(self, G1, G2):
        """
        Calculate the spectral distance between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Spectral distance between G1 and G2

        Raises:
            ValueError: If the graphs have different numbers of nodes and k is None
        """
        L1 = self.laplacian_matrix(G1)
        L2 = self.laplacian_matrix(G2)
        
        eig1 = self.eigenvalues(L1)
        eig2 = self.eigenvalues(L2)

        if self.k is None:
            if len(eig1) != len(eig2):
                raise ValueError("Graphs must have the same number of nodes when k is None")
            k = len(eig1)
        else:
            k = min(self.k, len(eig1), len(eig2))

        # Pad or truncate eigenvalues to length k
        eig1 = eig1[:k] + [0] * max(0, k - len(eig1))
        eig2 = eig2[:k] + [0] * max(0, k - len(eig2))

        # Compute Euclidean distance between eigenvalues
        #distance = (sum((e1 - e2)**2 for e1, e2 in zip(eig1, eig2)))**0.5
        distance = Euclidean().calculate(eig1, eig2)

        return distance
    def example(self):
        def create_sample_graphs():
         # Create a path graph
         P10 = nx.path_graph(10)
         # Create a cycle graph
         C10 = nx.cycle_graph(10)
         # Create a complete graph
         K10 = nx.complete_graph(10)
         # Create two random graphs
         G1 = nx.gnm_random_graph(10, 20)
         G2 = nx.gnm_random_graph(10, 20)
         return P10, C10, K10, G1, G2
        def compare_graphs(graphs, names):
         # Initialize SpectralDistance object
         sd = SpectralDistance(k=5, normalized=True)
         print("Spectral distances between graphs:")
         for i, (G1, name1) in enumerate(zip(graphs, names)):
          for j, (G2, name2) in enumerate(zip(graphs[i+1:], names[i+1:])):
            distance = sd.calculate(G1, G2)
            print(f"{name1} vs {name2}: {distance:.4f}")
        # Create sample graphs
        P10, C10, K10, G1, G2 = create_sample_graphs()
        graph_names = ["Path", "Cycle", "Complete", "Random1", "Random2"]
        # Compare the graphs
        compare_graphs([P10, C10, K10, G1, G2], graph_names)
#claude
import networkx as nx
from collections import Counter

class WeisfeilerLehmanSimilarity(Distance):
    """
    A class to compute the Weisfeiler-Lehman similarity between two graphs.

    The Weisfeiler-Lehman algorithm is used to create a multi-set of labels
    for each graph, which are then compared to compute a similarity score.

    Attributes:
        num_iterations (int): Number of iterations for the WL algorithm
        node_label_attr (str): Attribute name for initial node labels
    """

    def __init__(self, num_iterations=3, node_label_attr=None)-> None:
        """
        Initialize the WeisfeilerLehmanSimilarity object.

        Args:
            num_iterations (int): Number of iterations for the WL algorithm. Default is 3.
            node_label_attr (str, optional): Attribute name for initial node labels.
                If None, all nodes are initially labeled with the same value.
        """
        super().__init__()
        self.type='graph'

        self.num_iterations = num_iterations
        self.node_label_attr = node_label_attr

    def wl_labeling(self, G):
        """
        Perform Weisfeiler-Lehman labeling on the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list: List of label multi-sets for each iteration
        """
        if self.node_label_attr:
            labels = nx.get_node_attributes(G, self.node_label_attr)
        else:
            labels = {node: '1' for node in G.nodes()}

        label_lists = [Counter(labels.values())]

        for _ in range(self.num_iterations):
            new_labels = {}
            for node in G.nodes():
                # Collect labels of neighbors
                neighbor_labels = sorted(labels[nbr] for nbr in G.neighbors(node))
                # Create a new label by combining current label and sorted neighbor labels
                new_labels[node] = f"{labels[node]}({''.join(neighbor_labels)})"
            
            # Update labels and add to label_lists
            labels = new_labels
            label_lists.append(Counter(labels.values()))

        return label_lists

    def compute(self, G1, G2):
        """
        Calculate the Weisfeiler-Lehman similarity between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Weisfeiler-Lehman similarity between G1 and G2
        """
        # Get label multi-sets for both graphs
        label_lists1 = self.wl_labeling(G1)
        label_lists2 = self.wl_labeling(G2)

        # Compute similarity for each iteration
        similarities = []
        for labels1, labels2 in zip(label_lists1, label_lists2):
            intersection = sum((labels1 & labels2).values())
            union = sum((labels1 | labels2).values())
            similarities.append(intersection / union if union > 0 else 0)

        # Return the average similarity across all iterations
        return sum(similarities) / len(similarities)

    def is_isomorphic(self, G1, G2, threshold=0.99):
        """
        Check if two graphs are potentially isomorphic using WL similarity.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph
            threshold (float): Similarity threshold for isomorphism. Default is 0.99.

        Returns:
            bool: True if the graphs are potentially isomorphic, False otherwise
        """
        if G1.number_of_nodes() != G2.number_of_nodes() or G1.number_of_edges() != G2.number_of_edges():
            return False
        
        similarity = self.calculate(G1, G2)
        return similarity > threshold
    def example(self):
     pass

import numpy as np
import networkx as nx

class ComparingRandomWalkStationaryDistributions(Distance):
    """
    A class to compare stationary distributions of random walks on graphs.
    """

    def __init__(self,metric=L1())-> None:
        """
        Initialize the Distance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.metric = metric

    def compute_stationary_distribution(self, graph):
        """
        Compute the stationary distribution of a random walk on the given graph.

        Parameters:
        graph (networkx.Graph): The graph to compute the stationary distribution for

        Returns:
        numpy.ndarray: The stationary distribution vector
        """
        # Get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(graph).toarray()

        # Compute the transition matrix
        degree = np.sum(adj_matrix, axis=1)
        transition_matrix = adj_matrix / degree[:, np.newaxis]

        # Compute the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)

        # Find the eigenvector corresponding to eigenvalue 1
        stationary_index = np.argmin(np.abs(eigenvalues - 1))
        stationary_distribution = np.real(eigenvectors[:, stationary_index])

        # Normalize the distribution
        return stationary_distribution / np.sum(stationary_distribution)

    def compute(self, graph1, graph2):
        """
        Compare the stationary distributions of the two graphs.

        Parameters:
        metric (str): The distance metric to use. Options: 'l1', 'l2', 'kl'. Default is 'l1'.

        Returns:
        float: The distance between the two stationary distributions
        """
        dist1 = self.compute_stationary_distribution(graph1)
        dist2 = self.compute_stationary_distribution(graph2)

        if len(dist1) != len(dist2):
            raise ValueError("The graphs must have the same number of nodes")

        return self.metric.compute(dist1,dist2)
        
    def compare_random_walks(self, num_walks, walk_length):
        """
        Compare random walks on both graphs.

        Parameters:
        num_walks (int): The number of random walks to perform on each graph
        walk_length (int): The length of each random walk

        Returns:
        dict: A dictionary containing the average walk length and node visit frequencies for both graphs
        """
        results = {}

        for i, graph in enumerate([self.graph1, self.graph2]):
            total_length = 0
            node_visits = {node: 0 for node in graph.nodes()}

            for _ in range(num_walks):
                walk = self.random_walk(graph, walk_length)
                total_length += len(walk)
                for node in walk:
                    node_visits[node] += 1

            avg_length = total_length / num_walks
            visit_freq = {node: visits / (num_walks * walk_length) for node, visits in node_visits.items()}

            results[f'graph{i+1}'] = {
                'avg_walk_length': avg_length,
                'node_visit_frequencies': visit_freq
            }

        return results

#claude
import networkx as nx
from collections import deque

class DiffusionDistance(Distance):
    """
    A class to compare diffusion processes on two graphs.
    """

    def __init__(self, steps, metric='l1')-> None:
        """
        Initialize the DiffusionDistance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.steps = steps
        self.metric = metric


    def computeDiffusion(self, graph, source_node=None, steps=None):
        """
        Compute the diffusion process on the given graph starting from the source node.

        Parameters:
        graph (networkx.Graph): The graph to compute the diffusion process on
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process

        Returns:
        dict: A dictionary where the keys are the nodes and the values are the diffusion values
        """
        if source_node is None:
           source_node = np.random.choice(list(graph.nodes()))
           
        diffusion_values = {node: 0 for node in graph.nodes()}
        diffusion_values[source_node] = 1

        queue = deque([(source_node, 0)])

        while queue and queue[0][1] < steps:
            node, step = queue.popleft()
            neighbors = list(graph.neighbors(node))

            for neighbor in neighbors:
                diffusion_values[neighbor] += diffusion_values[node] / len(neighbors)

            for neighbor in neighbors:
                queue.append((neighbor, step + 1))

        return diffusion_values

    def compute(self, graph1, graph2, source_node):
        """
        Compare the diffusion processes on the two graphs.

        Parameters:
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process
        metric (str): The distance metric to use. Options: 'l1', 'l2'. Default is 'l1'.

        Returns:
        float: The distance between the two diffusion processes
        """
        diff1 = self.computeDiffusion(graph1, source_node, self.steps)
        diff2 = self.computeDiffusion(graph2, source_node, self.steps)

        if self.metric == 'l1':
            return sum(abs(diff1[node] - diff2[node]) for node in graph1.nodes())
        elif self.metric == 'l2':
            return sum((diff1[node] - diff2[node])**2 for node in graph1.nodes())**0.5
        else:
            raise ValueError("Invalid metric. Choose 'l1' or 'l2'.")
    def example(self):
      G1 = nx.erdos_renyi_graph(10, 0.3, seed=42)
      G2 = nx.erdos_renyi_graph(10, 0.35, seed=42)
      steps = 5
      diffusion_distance = DiffusionDistance(steps)
      source_node = 0
      l1_distance = diffusion_distance.compute(G1, G2,source_node)
      diffusion_distance = DiffusionDistance(steps,metric='l2')
      l2_distance = diffusion_distance.compute(G1, G2,source_node)
      print(f"L1 distance between diffusion processes: {l1_distance:.4f}")
      print(f"L2 distance between diffusion processes: {l2_distance:.4f}")
        
#chatgpt
class GraphKernelDistance(Distance):
    def __init__(self)-> None:
         super().__init__()
         self.type='graph'

    def random_walk_kernel(self, depth=3):
        """Compute a simple random walk kernel similarity."""
        kernel_value = 0
        
        for node1 in self.graph1.nodes:
            for node2 in self.graph2.nodes:
                kernel_value += self.random_walk(node1, node2, depth)
        
        return kernel_value
    
    def random_walk(self, node1, node2, depth):
        """Recursive helper function to compute random walk similarity."""
        if depth == 0:
            return 1
        
        similarity = 0
        
        neighbors1 = graph1.neighbors(node1)
        neighbors2 = graph1.neighbors(nodeé)
        
        for neighbor1 in neighbors1:
            for neighbor2 in neighbors2:
                similarity += self.random_walk(neighbor1, neighbor2, depth - 1)
        
        return similarity
    
    def compute(self, graph1,graph2, method="random_walk"):
        """Compute the graph kernel distance using the specified method."""
        if method == "random_walk":
            similarity = self.random_walk_kernel()
            return 1 / (1 + similarity)  # Convert similarity to distance
        else:
            raise ValueError(f"Unknown method: {method}")

class FrobeniusDistance(Distance):
    def __init__(self)-> None:
        super().__init__()
        self.type='graph'

    def compute(self, graph1, graph2):
        if len(graph1.nodes) != len(graph2.nodes):
            raise ValueError("Graphs must have the same number of nodes")

        distance = 0
        matrix1 = graph1.adjacency_matrix
        matrix2 = graph2.adjacency_matrix
        
        for i in range(len(matrix1)):
            for j in range(len(matrix1[i])):
                diff = matrix1[i][j] - matrix2[i][j]
                distance += diff * diff
        
        return distance ** 0.5
    def example(self):
      nodes1 = ["A", "B", "C"]
      edges1 = [("A", "B"), ("B", "C")]

      nodes2 = ["A", "B", "C"]
      edges2 = [("A", "B"), ("A", "C")]

      graph1 = Graph(nodes1, edges1)
      graph2 = Graph(nodes2, edges2)
      print(graph1.adjacency_matrix)
      frobenius_distance = FrobeniusDistance().compute(graph1, graph2)
      print(f"La distance de Frobenius entre les deux graphes est: {frobenius_distance}")

class PatternBasedDistance(Distance):
    def __init__(self,motif_size)-> None:
        super().__init__()
        self.type='graph'

        self.motif_size = motif_size

    def compute(self, graph1, graph2):
        motifs1 = graph1.count_motifs(self.motif_size)
        motifs2 = graph2.count_motifs(self.motif_size)
        return self._calculate_distance(motifs1, motifs2)

    def _calculate_distance(self, motifs1, motifs2):
        all_motifs = set(motifs1.keys()).union(set(motifs2.keys()))
        distance = 0
        for motif in all_motifs:
            freq1 = motifs1.get(motif, 0)
            freq2 = motifs2.get(motif, 0)
            distance += abs(freq1 - freq2)
        return distance
        
    def example(self):
      nodes1 = ["A", "B", "C", "D"]
      edges1 = [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")]

      nodes2 = ["A", "B", "C", "D"]
      edges2 = [("A", "B"), ("B", "D"), ("D", "A"), ("A", "C")]

      graph1 = Graph(nodes1, edges1)
      graph2 = Graph(nodes2, edges2)

      pattern_distance = PatternBasedDistance(motif_size=3).compute(graph1, graph2)

      print(f"La distance basée sur les motifs entre les deux graphes est: {pattern_distance}")
 
import zlib

class GraphCompressionDistance(Distance):
    def __init__(self)-> None:
        """
        Initialize the GraphCompressionDistance class with two graphs.
        Each graph is represented as an adjacency matrix, which is a list of lists.

        :param graph1: Adjacency matrix of the first graph
        :param graph2: Adjacency matrix of the second graph
        """
        super().__init__()
        self.type='graph'
        
    def compress(self, data):
        """
        Compress the data using zlib compression and return the compressed size.

        :param data: String representation of the graph
        :return: Length of the compressed data
        """
        compressed_data = zlib.compress(data.encode('utf-8'))
        return len(compressed_data)

    def combined_compression(self):
        """
        Compress the combined adjacency matrices of both graphs.

        :return: Length of the compressed combined adjacency matrix
        """
        combined_matrix = self.adjacency_to_string(self.graph1) + self.adjacency_to_string(self.graph2)
        return self.compress(combined_matrix)

    def compute(self, graph1, graph2):
        """
        Compute the Graph Compression Distance between the two graphs.

        :return: Compression distance between the two graphs
        """
        graph1_compressed_size = self.compress(graph1.adjacency_to_string())
        graph2_compressed_size = self.compress(graph2.adjacency_to_string())
        combined_compressed_size = self.combined_compression()

        distance = combined_compressed_size - min(graph1_compressed_size, graph2_compressed_size)
        return distance
    def example(self):
      graph1=Graph(Graph.nodes_1,Graph.edges_1)
      graph2=Graph(Graph.nodes_2,Graph.edges_2)
      distance_calculator = GraphCompressionDistance().compute(graph1, graph2)
      print(f"Graph Compression Distance: {distance_calculator}")
       
class DegreeDistributionDistance(Distance):
    def __init__(self)-> None:
        """
        Initializes the DegreeDistributionDistance class with two graphs.

        :param graph1: First graph, represented as an adjacency list or edge list.
        :param graph2: Second graph, represented as an adjacency list or edge list.
        """
        super().__init__()
        self.type='graph'


    def compare_distributions(self, dist1, dist2):
        """
        Compares two degree distributions using a simple difference metric.

        :param dist1: Degree distribution of the first graph.
        :param dist2: Degree distribution of the second graph.
        :return: A floating-point value representing the difference between the distributions.
        """
        all_degrees = set(dist1.keys()).union(set(dist2.keys()))
        difference = 0.0
        for degree in all_degrees:
            count1 = dist1.get(degree, 0)
            count2 = dist2.get(degree, 0)
            difference += abs(count1 - count2)
        return difference

    def compute(self, graph1, graph2):
        """
        Computes the degree distribution distance between the two graphs.

        :return: A floating-point value representing the distance between the degree distributions of the two graphs.
        """
        dist1 = Graph.compute_degree_distribution(graph1)
        dist2 = Graph.compute_degree_distribution(graph2)
        return self.compare_distributions(dist1, dist2)


class CommunityStructureDistance(Distance):
    def __init__(self, community_detection_algorithm)-> None:
        """
        Initialize the CommunityStructureDistance class with a specific community detection algorithm.
        
        :param community_detection_algorithm: A function that takes a graph as input and returns a list of sets, 
                                              where each set represents a community (i.e., nodes that belong together).
        """
        
        super().__init__()
        self.type='graph'

        self.community_detection_algorithm = community_detection_algorithm

    def jaccard_index(self, set1, set2):
        """
        Compute the Jaccard Index between two sets.
        
        :param set1: A set of nodes.
        :param set2: Another set of nodes.
        :return: The Jaccard Index, a measure of similarity between two sets.
        """
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0

    def compare_communities(self, communities1, communities2):
        """
        Compare two sets of communities and return a similarity score based on Jaccard Index.
        
        :param communities1: List of sets, where each set represents a community in the first graph.
        :param communities2: List of sets, where each set represents a community in the second graph.
        :return: The average Jaccard Index over all community pairs.
        """
        total_similarity = 0
        count = 0
        
        for community1 in communities1:
            best_similarity = 0
            for community2 in communities2:
                similarity = self.jaccard_index(community1, community2)
                best_similarity = max(best_similarity, similarity)
            total_similarity += best_similarity
            count += 1
            
        return total_similarity / count if count > 0 else 0

    def compute(self, graph1, graph2):
        """
        Compute the community structure distance between two graphs.
        
        :param graph1: The first graph (networkx.Graph object).
        :param graph2: The second graph (networkx.Graph object).
        :return: The distance between the community structures of the two graphs.
        """
        # Detect communities in both graphs
        communities1 = self.community_detection_algorithm(graph1)
        communities2 = self.community_detection_algorithm(graph2)

        # Compute similarity score
        similarity = self.compare_communities(communities1, communities2)
        
        # Convert similarity to distance (1 - similarity)
        distance = 1 - similarity
        
        return distance
