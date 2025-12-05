import random
import time
from typing import Dict, List, Tuple


import numpy as np


from .base import TSPSolver




class AntColonyOptimization(TSPSolver):
    """Ant Colony Optimization algorithm for TSP"""


    def __init__(self, cities: List[Tuple[float, float]],
                 n_ants: int = 50,
                 n_iterations: int = 100,
                 alpha: float = 1.0,
                 beta: float = 2.0,
                 evaporation: float = 0.5,
                 q: float = 100.0):
        """
        Initialize ACO solver
        n_ants: Number of ants
        n_iterations: Number of iterations
        alpha: Importance of pheromone
        beta: Importance of heuristic (distance)
        evaporation: Pheromone evaporation rate
        q: Pheromone deposit constant
        """
        super().__init__(cities)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.q = q


        initial_pheromone = 1.0 / (self.n * np.mean(self.distance_matrix))
        self.pheromone = np.ones((self.n, self.n)) * initial_pheromone
        np.fill_diagonal(self.pheromone, 0)


        self.heuristic = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    self.heuristic[i][j] = 1.0 / self.distance_matrix[i][j]


    def get_complexity(self) -> Tuple[str, str]:
        """
        Time Complexity: O(iterations * n_ants * n²)
        Space Complexity: O(n²)
        """
        return ("O(iterations × n_ants × n²)", "O(n²)")


    def solve(self) -> Tuple[List[int], float, float]:
        tour, distance, time_taken, _ = self.solve_with_steps()
        return tour, distance, time_taken


    def _construct_solution(self) -> Tuple[List[int], float]:
        """Construct a solution using ant colony"""
        # Mỗi kiến bắt đầu từ thành phố ngẫu nhiên (chiến lược đúng của ACO)
        start = random.randint(0, self.n - 1)
        tour = [start]
        unvisited = set(range(self.n)) - {start}


        current = start
        while unvisited:
            probabilities = []
            for city in unvisited:
                pheromone = self.pheromone[current][city] ** self.alpha
                heuristic = self.heuristic[current][city] ** self.beta
                probabilities.append(pheromone * heuristic)


            total = sum(probabilities)
            if total == 0:
                next_city = random.choice(list(unvisited))
            else:
                probabilities = [p / total for p in probabilities]
                next_city = np.random.choice(list(unvisited), p=probabilities)


            tour.append(next_city)
            unvisited.remove(next_city)
            current = next_city


        distance = self.calculate_tour_distance(tour)
        return tour, distance


    def _update_pheromone(self, tours: List[Tuple[List[int], float]]):
        """Update pheromone matrix"""
        self.pheromone *= (1 - self.evaporation)


        for tour, distance in tours:
            if distance > 0:
                deposit = self.q / distance
                for i in range(len(tour)):
                    from_city = tour[i]
                    to_city = tour[(i + 1) % len(tour)]
                    self.pheromone[from_city][to_city] += deposit
                    self.pheromone[to_city][from_city] += deposit


    def solve_with_steps(self) -> Tuple[List[int], float, float, List[Dict]]:
        start_time = time.time()
        steps = []


        best_tour = None
        best_distance = float('inf')


        steps.append({
            'step': 0,
            'description': f'Khởi tạo ACO với {self.n_ants} kiến, {self.n_iterations} lần lặp',
            'tour': None,
            'iteration': 0,
            'best_distance': None
        })


        for iteration in range(self.n_iterations):
            tours = []


            for _ in range(self.n_ants):
                tour, distance = self._construct_solution()
                tours.append((tour, distance))


                if distance < best_distance:
                    best_distance = distance
                    best_tour = tour.copy()


            self._update_pheromone(tours)


            if (iteration + 1) % max(1, self.n_iterations // 10) == 0 or iteration == 0:
                steps.append({
                    'step': iteration + 1,
                    'description': f'Lần lặp {iteration + 1}: Khoảng cách tốt nhất = {best_distance:.2f}',
                    'tour': best_tour.copy() if best_tour else None,
                    'iteration': iteration + 1,
                    'best_distance': best_distance
                })


        time_taken = time.time() - start_time


        # Chuẩn bị thông tin đầu/cuối để tránh biểu thức phức tạp trong f-string
        if best_tour:
            start_city = best_tour[0]
            end_city = best_tour[-1]
        else:
            start_city = "N/A"
            end_city = "N/A"


        steps.append({
            'step': self.n_iterations,
            'description': f'Hoàn thành! Tour tốt nhất có khoảng cách {best_distance:.2f}. Tour khép kín từ {end_city} về {start_city}',
            'tour': best_tour.copy() if best_tour else None,
            'iteration': self.n_iterations,
            'best_distance': best_distance
        })


        return best_tour, best_distance, time_taken, steps





