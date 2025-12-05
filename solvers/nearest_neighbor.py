import random
import time
from typing import Dict, List, Tuple


from .base import TSPSolver




class NearestNeighbor(TSPSolver):
    """Greedy Nearest Neighbor algorithm"""


    def get_complexity(self) -> Tuple[str, str]:
        """
        Time Complexity: O(n²) - For each city, find nearest unvisited city
        Space Complexity: O(n²) - Distance matrix
        """
        return ("O(n²)", "O(n²)")


    def solve(self) -> Tuple[List[int], float, float]:
        tour, distance, time_taken, _ = self.solve_with_steps()
        return tour, distance, time_taken


    def solve_with_steps(self) -> Tuple[List[int], float, float, List[Dict]]:
        start_time = time.time()
        steps = []


        unvisited = set(range(self.n))
        tour = []
        current = 0  # luôn bắt đầu từ thành phố 0
        tour.append(current)
        unvisited.remove(current)


        steps.append({
            'step': 0,
            'description': f'Bắt đầu từ thành phố {current}',
            'tour': tour.copy(),
            'current': current,
            'selected': None
        })


        step_num = 1
        while unvisited:
            nearest = min(unvisited, key=lambda city: self.distance_matrix[current][city])
            tour.append(nearest)
            unvisited.remove(nearest)


            steps.append({
                'step': step_num,
                'description': f'Chọn thành phố {nearest} (gần nhất từ {current})',
                'tour': tour.copy(),
                'current': current,
                'selected': nearest,
                'distance': self.distance_matrix[current][nearest]
            })


            current = nearest
            step_num += 1


        distance = self.calculate_tour_distance(tour)
        time_taken = time.time() - start_time


        steps.append({
            'step': step_num,
            'description': f'Hoàn thành tour với khoảng cách {distance:.2f}. Tour khép kín từ {tour[-1]} về {tour[0]}',
            'tour': tour.copy(),
            'current': None,
            'selected': None
        })


        return tour, distance, time_taken, steps





