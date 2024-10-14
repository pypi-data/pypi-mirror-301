from .mainClass import *
from .tools     import Vector,Matrix
		

class CosineInverse(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'
		
	def compute(self,vec1 :list, vec2 :list)-> float:
		return 1-Cosine().compute(vec1,vec2)


class Jaccard(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='set_float'

	def compute(self,set1 :set, set2 :set)-> float:
		"""
		Calculate the Jaccard distance between two sets.
    
		:param set1: First set
		:param set2: Second set
		:return: Jaccard distance between set1 and set2
		"""
		intersection = len(set1.intersection(set2))
		union = len(set1.union(set2))
		if union == 0:
			return 0.0  # Both sets are empty
		return 1 - (intersection / union)
		
	def exemple(self):
		self.obj1_exemple = {1, 2, 3, 4}
		self.obj2_exemple = {3, 4, 5, 6}
		super().exemple()

class Tanimoto(Jaccard):
	
	def __init__(self)-> None:
		super().__init__()
		
class GeneralizedJaccard(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,x :list, y :list)-> float:
		"""
		Calcule la distance de Jaccard généralisée entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:return: Distance de Jaccard généralisée entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		min_sum = sum(min(x_i, y_i) for x_i, y_i in zip(x, y))
		max_sum = sum(max(x_i, y_i) for x_i, y_i in zip(x, y))
    
		if max_sum == 0:
			return 0.0  # Pour éviter la division par zéro
        
		return 1 - (min_sum / max_sum)
		
	def exemple(self):
		self.obj1_exemple = {1, 2, 3, 4}
		self.obj2_exemple = {3, 4, 5, 6}
		super().exemple()

  
class Pearson(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,x :list[float], y :list[float])-> float:
		"""
		Calcule le coefficient de corrélation de Pearson entre deux listes de données.

		:param x: Liste des valeurs de la première variable.
		:param y: Liste des valeurs de la seconde variable.
		:return: Coefficient de corrélation de Pearson entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les listes x et y doivent avoir la même longueur.")
    
		n = len(x)
    
		# Calcul des moyennes
		mean_x = sum(x) / n
		mean_y = sum(y) / n
    
		# Calcul des covariances et des variances
		cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
		var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
		var_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
		# Calcul du coefficient de corrélation de Pearson
		if var_x == 0 or var_y == 0:
			raise ValueError("L'écart-type ne peut pas être nul.")
    
		pearson_corr = cov_xy / (var_x ** 0.5 * var_y ** 0.5)
    
		return 1 - pearson_corr
		
	def exemple(self):
		self.obj1_exemple = [1, 1, 3, 4, 5]
		self.obj2_exemple = [2, 3, 4, 5, 6]
		super().exemple()


class Spearman(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,x :list[float], y :list[float])-> float:
		"""
		Calcule la distance de Spearman entre deux listes de données.
    
		:param x: Liste des valeurs de la première variable.
		:param y: Liste des valeurs de la seconde variable.
		:return: Distance de Spearman entre x et y.
		"""
		spearman_corr = spearman_correlation(x, y)
		# La distance de Spearman est 1 moins le coefficient de corrélation de Spearman
		distance = 1 - spearman_corr
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4, 5]
		self.obj2_exemple = [5, 6, 7, 8, 7]
		super().exemple()

class Ochiai(Distance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,set1 :set, set2 :set)-> float:
		"""
		Calcule la distance d'Ochiai entre deux ensembles de données binaires.
    
		:param set1: Premier ensemble de données binaires (sous forme de liste de booléens).
		:param set2: Deuxième ensemble de données binaires (sous forme de liste de booléens).
		:return: Distance d'Ochiai entre set1 et set2.
		"""
		self.type='set_bin'

		if len(set1) != len(set2):
			raise ValueError("Les ensembles doivent avoir la même longueur.")
    
		# Convertir les listes en ensembles de indices où la valeur est True
		indices1 = {i for i, v in enumerate(set1) if v}
		indices2 = {i for i, v in enumerate(set2) if v}
    
		# Calculer les éléments communs
		intersection = indices1 & indices2
		intersection_size = len(intersection)
    
		# Calculer les tailles des ensembles
		size1 = len(indices1)
		size2 = len(indices2)
    
		# Calculer la distance d'Ochiai
		if size1 == 0 or size2 == 0:
			# Eviter la division par zéro
			return 0
        
		return intersection_size / (size1 * size2) ** 0.5
		
	def exemple(self):
		self.obj1_exemple = [True, False, True, True, False]
		self.obj2_exemple = [True, True, False, False, True]
		super().exemple()


class MotzkinStraus(Distance):
	
	def __init__(self)-> None:
		super().__init__(p=2)
		self.type='vec_float'

		self.p=p
		
	def compute(self,x :list[float], y :list[float])-> float:
		"""
		Calcule une distance hypothétique Motzkin-Straus généralisée entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:param p: Paramètre pour la norme de Minkowski (par défaut 2 pour la distance Euclidienne).
		:return: Distance Motzkin-Straus entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		# Calcul de la norme de Minkowski (généralement Euclidienne pour p=2)
		Minkowski_distance(self.p).compute(x,y)
    
		# Ajout d'une composante structurelle simple (hypothétique)
		structure_distance = sum((x_i - y_i)**2 for x_i, y_i in zip(x, y)) / len(x)
    
		# Combinaison des deux distances
		motzkin_straus_distance = minkowski_distance + structure_distance
    
		return motzkin_straus_distance
		
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4]
		self.obj2_exemple = [2, 2, 3, 5]
		super().exemple()




class EnhancedRogersTanimoto(Distance):
	
	def __init__(self, alpha=1)-> None:
		super().__init__()
		self.alpha=alpha
		self.type='vec_int'

	def compute(self,vector_a :list[int], vector_b :list[int])-> float:
		"""
		Calcule la distance Rogers-Tanimoto améliorée entre deux vecteurs binaires.
    
		:param vector_a: Premier vecteur (de type list).
		:param vector_b: Deuxième vecteur (de type list).
		:param alpha: Facteur de régularisation (par défaut: 1).
		:return: Distance Rogers-Tanimoto améliorée entre vector_a et vector_b.
		"""
		if len(vector_a) != len(vector_b):
			raise ValueError("Les deux vecteurs doivent avoir la même longueur")
    
		a = b = c = d = 0
    
		for i in range(len(vector_a)):
			if vector_a[i] == 1 and vector_b[i] == 1:
				a += 1
			elif vector_a[i] == 1 and vector_b[i] == 0:
				b += 1
			elif vector_a[i] == 0 and vector_b[i] == 1:
				c += 1
			elif vector_a[i] == 0 and vector_b[i] == 0:
				d += 1
    
		# Calcul de la distance Rogers-Tanimoto améliorée
		return (a + b + c) / (a + b + c + d + alpha)
		
	def exemple(self):
		self.obj1_exemple = [1, 1, 0, 0, 1]
		self.obj2_exemple = [1, 0, 1, 0, 1]
		self.obj3_exemple = 1# Facteur de régularisation
		super().exemple()

import numpy as np
from numpy import ones, pad, convolve,dot,linalg


class ContextualDynamicDistance(Distance):
    
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

		"""
		Initialize the CDD with a context weight function.
        
		:param context_weight_func: A function that takes in the contexts of two points
                                    and returns the weight for each feature.
		"""

	def compute(self, x :list, y :list, context_x :list, context_y :list)-> float:
		"""
		Calculate the Contextual Dynamic Distance (CDD) between two points.
        
		:param x: List or vector representing the first data point.
		:param y: List or vector representing the second data point.
		:param context_x: List or vector representing the context of the first data point.
		:param context_y: List or vector representing the context of the second data point.
        
		:return: The CDD value as a float.
		"""
		if len(x) != len(y) or len(context_x) != len(context_y):
			raise ValueError("Data points and contexts must be of the same length.")
        
		distance = 0.0
		for i in range(len(x)):
			weight = self.convolution_context_weight_func(context_x, context_y, i)
			distance += weight * (x[i] - y[i]) ** 2
        
		return distance ** 0.5

	def convolution_context_weight_func(self,context_x :list, context_y :list, index :int, kernel_size=3):
		"""
		A context weight function based on convolution.
    
		:param context_x: Context vector for the first point.
		:param context_y: Context vector for the second point.
		:param index: Current index for which the weight is calculated.
		:param kernel_size: Size of the convolution kernel.
    
		:return: The weight for the feature at the given index as a float.
		"""
		half_kernel = kernel_size // 2

		# Define convolution kernel (e.g., a simple averaging kernel)
		kernel = np.ones(kernel_size) / kernel_size

		# Extract the relevant sub-contexts around the current index
		sub_context_x = context_x[max(0, index - half_kernel):min(len(context_x), index + half_kernel + 1)]
		sub_context_y = context_y[max(0, index - half_kernel):min(len(context_y), index + half_kernel + 1)]

		# If sub-contexts are shorter than the kernel, pad them
		if len(sub_context_x) < kernel_size:
			sub_context_x = np.pad(sub_context_x, (0, kernel_size - len(sub_context_x)), 'constant')
		if len(sub_context_y) < kernel_size:
			sub_context_y = np.pad(sub_context_y, (0, kernel_size - len(sub_context_y)), 'constant')

		# Convolve the contexts with the kernel
		conv_x = np.convolve(sub_context_x, kernel, mode='valid')
		conv_y = np.convolve(sub_context_y, kernel, mode='valid')

		# Calculate the weight as the similarity of the convolved signals
		similarity = np.dot(conv_x, conv_y) / (np.linalg.norm(conv_x) * np.linalg.norm(conv_y) + 1e-10)
		return similarity
		
	def exemple(self):
		# Feature vectors
		self.obj1_exemple = [1.0, 2.0, 3.0]
		self.obj2_exemple = [4.0, 5.0, 6.0]
		# Context vectors
		self.obj3_exemple = [0.2, 0.3, 0.5]
		self.obj4_exemple = [0.1, 0.4, 0.6]
		super().exemple()



class MahalanobisTaguchi(Distance):
	
    def __init__(self, reference_group :list[list])-> None:
        """
        Initialize the MahalanobisTaguchi class with a reference group.

        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        super().__init__()
        self.type='vec_float'


        self.reference_group = reference_group
        self.mean_vector = self.calculate_mean_vector()
        self.covariance_matrix = Matrix.covariance_matrix()
        self.inverse_covariance_matrix = Matrix.invert_matrix(self.covariance_matrix)

    def calculate_mean_vector(self):
        """
        Calculate the mean vector of the reference group.

        :return: A list representing the mean vector.
        """
        num_points = len(self.reference_group)
        num_dimensions = len(self.reference_group[0])

        mean_vector = [0] * num_dimensions

        for point in self.reference_group:
            for i in range(num_dimensions):
                mean_vector[i] += point[i]

        mean_vector = [x / num_points for x in mean_vector]
        return mean_vector

    def compute(self, data_point)-> float:
        """
        Calculate the Mahalanobis-Taguchi distance for a given data point.

        :param data_point: A list representing the data point to be evaluated.
        :return: The Mahalanobis-Taguchi distance as a float.
        """
        diff_vector = [data_point[i] - self.mean_vector[i] for i in range(len(self.mean_vector))]
        
        # Matrix multiplication with the inverse covariance matrix
        temp_vector = [0] * len(diff_vector)
        for i in range(len(diff_vector)):
            for j in range(len(diff_vector)):
                temp_vector[i] += diff_vector[j] * self.inverse_covariance_matrix[j][i]

        # Final dot product to get the Mahalanobis-Taguchi distance
        distance_squared = sum(temp_vector[i] * diff_vector[i] for i in range(len(diff_vector)))
        return distance_squared ** 0.5

class Otsuka(Distance):
    def __init__(self)-> None:
        """
        Initialize the Otsuka class with two categorical vectors.

        :param vector1: First categorical vector (list of strings).
        :param vector2: Second categorical vector (list of strings).
        """
        super().__init__()
        self.type='vec_float'


    def compute(self, vector1 :list, vector2 :list)-> float:
        """
        Calculate the Otsuka distance between the two categorical vectors.

        :return: The Otsuka distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length.")

        a = b = c = d = 0

        for v1, v2 in zip(vector1, vector2):
            if v1 == v2:
                a += 1
            elif v1 != v2 and v1 != 'X' and v2 != 'X':
                b += 1
            elif v1 != v2 and v1 == 'X':
                c += 1
            elif v1 != v2 and v2 == 'X':
                d += 1

        total = a + b + c + d
        if total == 0:
            return 0.0

        return 0.5 * ( (a + d) / total + (b + c) / total )

class RogersTanimoto(Distance):
    def __init__(self)-> None:
        """
        Initialize the Rogers-Tanimoto class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()
        self.type='vec_int'

        

    def compute(self, vector1 :list[int], vector2 :list[int])-> float:
        """
        Calculate the Rogers-Tanimoto distance between the two binary vectors.

        :return: The Rogers-Tanimoto distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        self.vector1 = vector1
        self.vector2 = vector2
        # Calculate the components of the formula
        a = sum(v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))  # Both are 1
        b = sum(v1 and not v2 for v1, v2 in zip(self.vector1, self.vector2))  # Present in vector1 but not in vector2
        c = sum(not v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))  # Present in vector2 but not in vector1
        d = sum(not v1 and not v2 for v1, v2 in zip(self.vector1, self.vector2))  # Both are 0

        # Calculate the Rogers-Tanimoto distance
        distance = (a + b + c) / (a + b + c + d)

        return distance



class SokalMichener(Distance):
    def __init__(self)-> None:
        """
        Initialize the SokalMichener class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()
        self.type='vec_float'

        

    def compute(self, vector1 :list[int], vector2 :list[int])-> float:
        """
        Calculate the Sokal-Michener distance between the two binary vectors.

        :return: The Sokal-Michener distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        # Number of matches where both vectors have 1s (a)
        a = sum(v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Number of matches where both vectors have 0s (d)
        d = sum((not v1) and (not v2) for v1, v2 in zip(vector1, vector2))

        # Total number of features (n)
        n = len(vector1)

        # Calculate the Sokal-Michener distance
        similarity = (a + d) / n
        distance = 1 - similarity

        return distance

class SokalSneath(Distance):
    def __init__(self)-> None:
        """
        Initialize the SokalSneath class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()
        self.type='vec_int'

        

    def compute(self, vector1 :list[int], vector2 :list[int])-> float:
        """
        Calculate the Sokal-Sneath distance between the two binary vectors.

        :return: The Sokal-Sneath distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        # Number of matches where both vectors have 1s (a)
        a = sum(v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Number of mismatches where vector1 has 1 and vector2 has 0 (b)
        b = sum(v1 and not v2 for v1, v2 in zip(vector1, vector2))

        # Number of mismatches where vector1 has 0 and vector2 has 1 (c)
        c = sum(not v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Calculate the Sokal-Sneath distance
        distance = (c + 2 * b) / (a + b + c)

        return distance

		
class FagerMcGowan(Distance):
	
    def __init__(self)-> None:
        super().__init__()
        self.type='set'

    """
    FagerMcGowan similarity coefficient calculator.

    The FagerMcGowan similarity coefficient is used to measure the similarity 
    between two sets, particularly in ecological studies. It adjusts for the 
    expected overlap due to random chance, providing a more accurate reflection 
    of true similarity.

    Methods:
    --------
    calculate(set1, set2, N):
        Calculates the FagerMcGowan similarity coefficient between two sets.
    """

    def compute(self, set1 :set, set2 :set, N)-> float:
        """
        Calculate the Fager-McGowan similarity coefficient between two sets.

        Parameters:
        -----------
        set1 : set
            The first set of elements (e.g., species in a habitat).
        set2 : set
            The second set of elements.
        N : int
            The total number of unique elements in the universal set.

        Returns:
        --------
        float
            The Fager-McGowan similarity coefficient.
        """
        intersection_size = len(set1 & set2)  # Number of elements common to both sets
        set1_size = len(set1)  # Size of the first set
        set2_size = len(set2)  # Size of the second set

        # Calculate the Fager-McGowan similarity coefficient
        numerator = intersection_size - (set1_size * set2_size / N)
        denominator = min(set1_size, set2_size)

        if denominator == 0:
            return 0.0

        similarity = numerator / denominator
        return similarity

from typing import List
import math

class JensenShannonDivergence(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='vec_float'

    def compute(self, dist1: List[float], dist2: List[float]) -> float:
        """
        Calcule la Jensen-Shannon Divergence entre deux distributions de probabilités.

        :param dist1: Première distribution de probabilités (somme égale à 1).
        :param dist2: Deuxième distribution de probabilités (somme égale à 1).
        :return: La divergence Jensen-Shannon entre les deux distributions.
        """
        if len(dist1) != len(dist2):
            raise ValueError("Les distributions doivent avoir la même longueur")

        # Calcul de la distribution moyenne
        avg_dist: List[float] = [(p1 + p2) / 2 for p1, p2 in zip(dist1, dist2)]

        # Calcul de la divergence KL pour les deux distributions par rapport à la distribution moyenne
        kl_div1: float = self._kl_divergence(dist1, avg_dist)
        kl_div2: float = self._kl_divergence(dist2, avg_dist)

        # La Jensen-Shannon Divergence est la moyenne des deux divergences KL
        return (kl_div1 + kl_div2) / 2

    def _kl_divergence(self, dist_p: List[float], dist_q: List[float]) -> float:
        """
        Calcule la Kullback-Leibler Divergence entre deux distributions.

        :param dist_p: Distribution de probabilité p.
        :param dist_q: Distribution de probabilité q.
        :return: La divergence KL entre les distributions p et q.
        """
        divergence: float = 0.0
        for p, q in zip(dist_p, dist_q):
            if p > 0 and q > 0:
                divergence += p * math.log(p / q)
        return divergence
'''
# Exemple d'utilisation
dist1: List[float] = [0.4, 0.3, 0.2, 0.1]
dist2: List[float] = [0.3, 0.3, 0.2, 0.2]

# Créer une instance de la classe Jensen-Shannon Divergence
js_divergence = JensenShannonDivergence()

# Calculer la Jensen-Shannon Divergence
divergence: float = js_divergence.compute(dist1, dist2)
print(f"Jensen-Shannon Divergence: {divergence}")
'''
