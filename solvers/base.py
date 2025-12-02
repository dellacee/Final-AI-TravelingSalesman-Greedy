import math
from typing import List, Tuple

import numpy as np


class TSPSolver:
    """Base class for TSP solvers"""

    def __init__(self, cities: List[Tuple[float, float]]):
        """
        Initialize with list of city coordinates
        cities: List of (x, y) tuples
        """
        self.cities = cities
        self.n = len(cities)
        self.distance_matrix = self._calculate_distance_matrix()

    def _calculate_distance_matrix(self) -> np.ndarray:
        """Calculate Euclidean distance matrix between all cities"""
        matrix = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    dx = self.cities[i][0] - self.cities[j][0]
                    dy = self.cities[i][1] - self.cities[j][1]
                    matrix[i][j] = math.sqrt(dx * dx + dy * dy)
        return matrix

    def calculate_tour_distance(self, tour: List[int]) -> float:
        """Calculate total distance of a tour"""
        total = 0
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            total += self.distance_matrix[from_city][to_city]
        return total

    def solve(self):
        """
        Solve TSP and return (tour, distance, time_taken)
        Must be implemented by subclasses
        """
        raise NotImplementedError

    def solve_with_steps(self):
        """
        Solve TSP and return (tour, distance, time_taken, steps)
        Must be implemented by subclasses
        """
        raise NotImplementedError

    def get_complexity(self):
        """
        Return (time_complexity, space_complexity) as Big O notation
        Must be implemented by subclasses
        """
        raise NotImplementedError

