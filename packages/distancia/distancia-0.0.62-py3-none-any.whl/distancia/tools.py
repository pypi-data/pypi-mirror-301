#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tools.py
#  

def check_bin(str_):
    if str(str_) in "01":
        return True
    return False
    
def check_probability(number):
    if number>=0 and number <=1.0:
        return True
    else: return False
    
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def exp(x, terms=20):
    """
    Calculate the exponential of x using Taylor series expansion.
    
    Parameters:
    x (float): The exponent
    terms (int): Number of terms to use in the Taylor series (default: 20)
    
    Returns:
    float: An approximation of e^x
    """
    result = 0
    for n in range(terms):
        result += x**n / factorial(n)
    return result
    
def sin(x, terms=10):
    x = x % (2 * 3.141592653589793)  # réduction de l'angle à une période
    result = 0
    for n in range(terms):
        numerator = ((-1) ** n) * (x ** (2 * n + 1))
        denominator = factorial(2 * n + 1)
        result += numerator / denominator
    return result
    
def cos(x, terms=10):
    x = x % (2 * 3.141592653589793)  # réduction de l'angle à une période
    result = 0
    for n in range(terms):
        numerator = ((-1) ** n) * (x ** (2 * n))
        denominator = factorial(2 * n)
        result += numerator / denominator
    return result
    
def degrees_to_radians(degrees):
    pi = 3.141592653589793
    radians = degrees * (pi / 180)
    return radians
    
def atan(x, terms=10):
    result = 0
    for n in range(terms):
        result += ((-1) ** n) * (x ** (2 * n + 1)) / (2 * n + 1)
    return result

def atan2(y, x, terms=10):
    if x > 0:
        return atan(y / x, terms)
    elif x < 0 and y >= 0:
        return atan(y / x, terms) + 3.141592653589793
    elif x < 0 and y < 0:
        return atan(y / x, terms) - 3.141592653589793
    elif x == 0 and y > 0:
        return 3.141592653589793 / 2
    elif x == 0 and y < 0:
        return -3.141592653589793 / 2
    else:
        return 0  # (0, 0) case
	
def log(x, iterations=1000):
    """
    Approximates the natural logarithm (log base e) of x using Newton's method.
    
    :param x: The value to compute the natural logarithm for.
    :param iterations: The number of iterations to improve the approximation.
    :return: Approximated natural logarithm of x.
    """
    if x <= 0:
        raise ValueError("Math domain error. Input must be greater than 0.")
    
    # Initial guess
    guess = x if x < 2 else x / 2
    
    # Newton's method to approximate log(x)
    for _ in range(iterations):
        guess -= (guess - x / (2.718281828459045 ** guess)) / (1 + x / (2.718281828459045 ** guess))
    
    return guess
    


    
def rank(data):
    """
    Spearman
    Calcule les rangs des valeurs dans la liste donnée.
    
    :param data: Liste des valeurs à classer.
    :return: Liste des rangs correspondant aux valeurs.
    """
    sorted_indices = sorted(range(len(data)), key=lambda i: data[i])
    ranks = [0] * len(data)
    rank_sum = 0
    last_value = None
    
    for index in sorted_indices:
        if last_value is None or data[index] != last_value:
            rank_sum = index + 1
        else:
            rank_sum += index + 1
        
        ranks[index] = rank_sum / (sorted_indices.index(index) + 1)
        last_value = data[index]
    
    return ranks

def spearman_correlation(x, y):
    """
    Spearman
    Calcule le coefficient de corrélation de Spearman entre deux listes de données.
    
    :param x: Liste des valeurs de la première variable.
    :param y: Liste des valeurs de la seconde variable.
    :return: Coefficient de corrélation de Spearman entre x et y.
    """
    if len(x) != len(y):
        raise ValueError("Les listes x et y doivent avoir la même longueur.")
    
    n = len(x)
    
    # Calcul des rangs
    rank_x = rank(x)
    rank_y = rank(y)
    
    # Calcul de la différence des rangs
    d_squared_sum = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
    
    # Calcul du coefficient de corrélation de Spearman
    spearman_corr = 1 - (6 * d_squared_sum) / (n * (n * n - 1))
    
    return spearman_corr
    
##############################
from typing import List,Tuple

class Vector:
	
	vec_int_1:list[int]=[1,2,3,4]
	vec_int_2:list[int]=[4,5,6,7]
	
	vec_bin_1:list[float]=[1, 0, 1, 1, 0]
	vec_bin_2:list[float]=[0, 1, 1, 0, 0]
	
	vec_float_1:list[float]=[1.1,2.2,3.3]
	vec_float_2:list[float]=[4.4,5.5,6.6]
	
	vec_prob_1:list[float]=[0.1, 0.2, 0.4, 0.3]
	vec_prob_2:list[float]=[0.2, 0.3, 0.1, 0.4]
	
	
	def norm(self,vec) -> float:
		"""
		Calculate the norm (magnitude) of a vector.
    
		:param vec: Input vector
		:return: Norm of the vector
		"""
		return (sum(x * x for x in vec))**0.5
		
	def dot_product(self,vec1, vec2) -> float:
		"""
		Calculate the dot product between two vectors.
    
		:param vec1: First vector
		:param vec2: Second vector
		:return: Dot product of vec1 and vec2
		"""
		return sum(x * y for x, y in zip(vec1, vec2))
	
class Matrix:
    
	def invert_matrix(matrix):
		"""
		Calcule l'inverse d'une matrice carrée.
    
		:param matrix: Matrice carrée à inverser.
		:return: Matrice inverse.
		"""
		from copy import deepcopy
		n = len(matrix)
		A = deepcopy(matrix)
		I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
		for i in range(n):
			if A[i][i] == 0:
				for k in range(i + 1, n):
					if A[k][i] != 0:
						A[i], A[k] = A[k], A[i]
						I[i], I[k] = I[k], I[i]
						break
        
				for j in range(n):
					if i != j:
						ratio = A[j][i] / A[i][i]
						for k in range(n):
							A[j][k] -= ratio * A[i][k]
							I[j][k] -= ratio * I[i][k]
    
		for i in range(n):
			divisor = A[i][i]
			for j in range(n):
				I[i][j] /= divisor
		return I
		
	def covariance_matrix(data):
		"""
		Calcule la matrice de covariance pour un ensemble de données.
    
		:param data: Liste de listes, où chaque sous-liste représente une observation.
		:return: Matrice de covariance.
		"""
		n = len(data)
		m = len(data[0])
		mean = [sum(col) / n for col in zip(*data)]
		cov_matrix = [[0] * m for _ in range(m)]
    
		for i in range(m):
			for j in range(m):
				cov_matrix[i][j] = sum((data[k][i] - mean[i]) * (data[k][j] - mean[j]) for k in range(n)) / (n - 1)
    
		return cov_matrix
		
	def eigenvalues_2x2(self, matrix):
		"""
		Compute the eigenvalues of a 2x2 matrix.
        
		Parameters:
		matrix (list of list of float): 2x2 matrix.
        
		Returns:
		list of complex: Eigenvalues of the matrix.
		"""
		coeffs = self.characteristic_polynomial(matrix)
		a, b, c = coeffs
		discriminant = b**2 - 4*a*c
		eigenvalue1 = (-b + discriminant**0.5) / (2*a)
		eigenvalue2 = (-b - discriminant**0.5) / (2*a)
		return [eigenvalue1, eigenvalue2]

	def matrix_subtraction(self, A, B):
		"""
		Subtract matrix B from matrix A element-wise.
        
		Parameters:
		A (list of list of float): First matrix.
		B (list of list of float): Second matrix.
        
		Returns:
		list of list of float: Resultant matrix of A - B.
		"""
		return [[A[i][j] - B[i][j] for j in range(self.num_states)] for i in range(self.num_states)]

	def matrix_trace(self, matrix):
		"""
		Compute the trace of a matrix (sum of diagonal elements).
        
		Parameters:
		matrix (list of list of float): Matrix.
        
		Returns:
		float: Trace of the matrix.
		"""
		return sum(matrix[i][i] for i in range(self.num_states))

	def characteristic_polynomial(self, matrix):
		"""
		Compute the characteristic polynomial of a matrix.
        
		Parameters:
		matrix (list of list of float): Matrix.
        
		Returns:
		list of float: Coefficients of the characteristic polynomial.
		"""
		# For a 2x2 matrix, the characteristic polynomial is given by:
		# det(A - λI) = λ^2 - (trace(A))λ + det(A)
		a = matrix
		if self.num_states == 2:
			trace = self.matrix_trace(a)
			det = a[0][0]*a[1][1] - a[0][1]*a[1][0]
			return [1, -trace, det]
		else:
			raise NotImplementedError("Characteristic polynomial calculation for matrices larger than 2x2 is not implemented.")
            
class Graph:
	
	edges_1 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
	nodes_1 = ["A", "B", "C", "D"]

	edges_2 = [("A", "B"), ("B", "C"), ("C", "D")]
	nodes_2 = ["A", "B", "C", "D"]
	
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.edges = edges
		self.adjacency_matrix = self.create_adjacency_matrix()
		self.adjacency_list = self.create_adjacency_list()

	def create_adjacency_matrix(self):
		matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
		node_index = {node: i for i, node in enumerate(self.nodes)}
        
		for edge in self.edges:
			i, j = node_index[edge[0]], node_index[edge[1]]
			matrix[i][j] = 1
			matrix[j][i] = 1  # Assuming the graph is undirected

		return matrix

	def create_adjacency_list(self):
		adj_list = {node: [] for node in self.nodes}
		for edge in self.edges:
			u, v = edge
			adj_list[u].append(v)
			adj_list[v].append(u)  # Assuming the graph is undirected
		return adj_list
    
	def adjacency_to_string(self, matrix):
		"""
		Convert the adjacency matrix to a string representation.

		:param matrix: Adjacency matrix of a graph
		:return: String representation of the adjacency matrix
		"""
		return ''.join([''.join(map(str, row)) for row in matrix])
		
	def compute_degree_distribution(self, graph):
		"""
		Computes the degree distribution of a graph.

		:param graph: The graph for which to compute the degree distribution.
		:return: A dictionary where the keys are node degrees and the values are the counts of nodes with that degree.
		"""
		degree_distribution = {}
		for node, neighbors in graph.items():
			degree = len(neighbors)
			if degree in degree_distribution:
				degree_distribution[degree] += 1
			else:
				degree_distribution[degree] = 1
		return degree_distribution
		
	def count_motifs(self, motif_size):
		motifs = {}
		for node in self.nodes:
			neighbors = self.adjacency_list[node]
			if len(neighbors) >= motif_size - 1:
				for sub_motif in self._find_sub_motifs(node, neighbors, motif_size - 1):
					sub_motif = tuple(sorted(sub_motif))
					if sub_motif in motifs:
						motifs[sub_motif] += 1
					else:
						motifs[sub_motif] = 1
		return motifs

	def _find_sub_motifs(self, node, neighbors, remaining):
		if remaining == 1:
			return [(node, neighbor) for neighbor in neighbors]
		sub_motifs = []
		for i, neighbor in enumerate(neighbors):
			new_neighbors = neighbors[i + 1:]
			for sub_motif in self._find_sub_motifs(neighbor, new_neighbors, remaining - 1):
				sub_motifs.append((node,) + sub_motif)
		return sub_motifs
        
	def get_nodes(self):
		nodes = set()
		for edge in self.edges:
			nodes.update(edge)
		return list(nodes)
        
	def get_edges(self, graph):
		"""
		Returns a set of edges from a graph, ensuring each edge is only counted once in an undirected graph.
        
		:param graph: The graph as a dictionary.
		:return: A set of edges.
		"""
		edges = set()
		for node, neighbors in graph.items():
			for neighbor in neighbors:
				if (node, neighbor) not in edges and (neighbor, node) not in edges:
					edges.add((node, neighbor))
		return edges
      
	def get_neighbors(self, graph, node):
			"""Get the neighbors of a node in a given graph."""
			neighbors = []
			for edge in graph.edges:
				if node == edge[0]:
					neighbors.append(edge[1])
				elif node == edge[1]:
					neighbors.append(edge[0])
			return neighbors
          
	def dijkstra(self, start_node, end_node):
		"""
		Implémente l'algorithme de Dijkstra pour trouver le plus court chemin entre deux nœuds.
		:param start_node: Le nœud de départ.
		:param end_node: Le nœud d'arrivée.
		:return: La distance du plus court chemin entre start_node et end_node.
		"""
		import heapq

		# Initialisation des distances de tous les nœuds à l'infini, sauf le nœud de départ à 0
		distances = {node: float('inf') for node in self.graph}
		distances[start_node] = 0

		# File de priorité pour gérer les nœuds à explorer
		priority_queue = [(0, start_node)]

		while priority_queue:
			current_distance, current_node = heapq.heappop(priority_queue)

			# Si nous avons atteint le nœud de destination, on peut arrêter
			if current_node == end_node:
				return current_distance

			# Si la distance actuelle est supérieure à la distance déjà trouvée, on saute
			if current_distance > distances[current_node]:
				continue

			# Explorer les voisins du nœud actuel
			for neighbor, weight in self.graph[current_node].items():
				distance = current_distance + weight

			# Si une distance plus courte est trouvée, mettre à jour et ajouter à la queue
			if distance < distances[neighbor]:
				distances[neighbor] = distance
				heapq.heappush(priority_queue, (distance, neighbor))

		# Si le nœud d'arrivée est injoignable, retourner l'infini
		return float('inf')

	def random_walk(self, graph, steps, start_node=None):
		"""
		Perform a random walk on the given graph.

		Parameters:
		graph (networkx.Graph): The graph to walk on
		steps (int): The number of steps to take
		start_node (int): The starting node for the walk. If None, a random node is chosen.

		Returns:
		list: The sequence of nodes visited during the walk
		"""
		if start_node is None:
			start_node = np.random.choice(list(graph.nodes()))

		walk = [start_node]
		current_node = start_node

		for _ in range(steps - 1):
			neighbors = list(graph.neighbors(current_node))
			if not neighbors:
				break
			current_node = np.random.choice(neighbors)
			walk.append(current_node)

		return walk
               
import random
from typing import List, Dict, Tuple

class MarkovChain:
    def __init__(self, n: int = 2):
        self.n = n  # Ordre de la chaîne de Markov
        self.chain: Dict[Tuple[str, ...], Dict[str, int]] = {}
        self.start_tokens: List[Tuple[str, ...]] = []

    def add_text(self, text: str) -> None:
        """
        Ajoute un texte à la chaîne de Markov.
        """
        words = text.split()
        for i in range(len(words) - self.n):
            state = tuple(words[i:i+self.n])
            next_word = words[i+self.n]
            
            if i == 0:
                self.start_tokens.append(state)

            if state not in self.chain:
                self.chain[state] = {}
            if next_word not in self.chain[state]:
                self.chain[state][next_word] = 0
            self.chain[state][next_word] += 1

    def generate_text(self, length: int = 100) -> str:
        """
        Génère un nouveau texte basé sur la chaîne de Markov.
        """
        if not self.chain:
            return ""

        current = random.choice(self.start_tokens)
        result = list(current)

        for _ in range(length - self.n):
            if current not in self.chain:
                break
            
            possible_next = self.chain[current]
            next_word = self._weighted_choice(possible_next)
            result.append(next_word)
            current = tuple(result[-self.n:])

        return ' '.join(result)

    def _weighted_choice(self, choices: Dict[str, int]) -> str:
        """
        Choisit un élément en fonction de son poids.
        """
        total = sum(choices.values())
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in choices.items():
            if upto + weight >= r:
                return choice
            upto += weight
        assert False, "Shouldn't get here"

    def get_probability(self, state: Tuple[str, ...], next_word: str) -> float:
        """
        Retourne la probabilité d'un mot suivant un état donné.
        """
        if state not in self.chain or next_word not in self.chain[state]:
            return 0.0
        total = sum(self.chain[state].values())
        return self.chain[state][next_word] / total

    def get_most_likely_next(self, state: Tuple[str, ...]) -> str:
        """
        Retourne le mot le plus probable suivant un état donné.
        """
        if state not in self.chain:
            return ""
        return max(self.chain[state], key=self.chain[state].get)

    def exemple(self) -> None:
        """
        Exemple d'utilisation de la classe MarkovChain.
        """
        # Ajout de texte à la chaîne
        self.add_text("le chat mange la souris le chien mange le chat")
        self.add_text("le chat dort sur le tapis le chien dort dans sa niche")

        # Génération de texte
        print("Texte généré:")
        print(self.generate_text(20))

        # Probabilité d'un mot suivant un état
        print("\nProbabilité de 'mange' après 'le chat':")
        print(self.get_probability(("le", "chat"), "mange"))

        # Mot le plus probable suivant un état
        print("\nMot le plus probable après 'le chien':")
        print(self.get_most_likely_next(("le", "chien")))
        
class MarkovChain:

	def stationary_distribution(self, matrix, tolerance=1e-10, max_iterations=1000):
		"""
		Compute the stationary distribution of a Markov chain from its transition matrix.
        
		Parameters:
		matrix (list of list of float): Transition matrix of the Markov chain.
		tolerance (float): Tolerance level for convergence.
		max_iterations (int): Maximum number of iterations for convergence.
        
		Returns:
		list of float: The stationary distribution of the Markov chain.
		"""
		dist = [1.0 / self.num_states] * self.num_states  # Initial uniform distribution
		for _ in range(max_iterations):
			next_dist = [0] * self.num_states
			for i in range(self.num_states):
				for j in range(self.num_states):
					next_dist[i] += dist[j] * matrix[j][i]
				if all(abs(next_dist[i] - dist[i]) < tolerance for i in range(self.num_states)):
					break
				dist = next_dist
		return dist

import cmath

class Image:
	pass
	
class text:
	pass
	
class Sound:

	def exemple(self):
		signal1 = [0.5, 0.1, 0.2, 0.4, 0.3, 0.2, 0.1, 0.0]
		signal2 = [0.4, 0.2, 0.2, 0.5, 0.3, 0.1, 0.2, 0.0]
		return[signal1,signal2]
		
	def generate_test_signals(duration: float = 1.0, sample_rate: int = 16000) -> tuple[list[float], list[float]]:
		"""
		Génère deux signaux audio de test.

		Args:
		duration (float): Durée du signal en secondes. Par défaut 1.0 seconde.
		sample_rate (int): Taux d'échantillonnage en Hz. Par défaut 16000 Hz.

		Returns:
		tuple[list[float], list[float]]: Deux signaux audio de test.
		"""
		num_samples = int(duration * sample_rate)

		# Signal 1: Combinaison de deux sinusoïdes (440 Hz et 880 Hz)
		signal1 = [
			0.5 * math.sin(2 * math.pi * 440 * t / sample_rate) +
			0.3 * math.sin(2 * math.pi * 880 * t / sample_rate)
			for t in range(num_samples)
		]

		# Signal 2: Combinaison de trois sinusoïdes (330 Hz, 660 Hz et 990 Hz)
		signal2 = [
			0.4 * math.sin(2 * math.pi * 330 * t / sample_rate) +
			0.3 * math.sin(2 * math.pi * 660 * t / sample_rate) +
			0.2 * math.sin(2 * math.pi * 990 * t / sample_rate)
			for t in range(num_samples)
		]

		return signal1, signal2
    
	def fft( signal: List[float]) -> List[complex]:
		"""
		Compute the Fast Fourier Transform (FFT) of the input signal.

		:param signal: The input signal as a list of floats.
		:return: The FFT of the signal as a list of complex numbers.
		"""
		n: int = len(signal)
		if n == 1:
			return signal
		else:
			even: List[complex] = fft(signal[0::2])
			odd: List[complex] = fft(signal[1::2])
			combined: List[complex] = [0] * n
			for k in range(n // 2):
				t: complex = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
				combined[k] = even[k] + t
				combined[k + n // 2] = even[k] - t
			return combined
