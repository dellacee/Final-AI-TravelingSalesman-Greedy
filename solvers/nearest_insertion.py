import time
from typing import Dict, List, Tuple
from .base import TSPSolver
class NearestInsertion(TSPSolver):
    """Greedy Nearest Insertion algorithm"""


    def get_complexity(self) -> Tuple[str, str]:
        """
        Time Complexity: O(n²) - For each city, find best insertion position
        Space Complexity: O(n²) - Distance matrix
        """
        return ("O(n²)", "O(n²)")


    def solve(self) -> Tuple[List[int], float, float]:
        tour, distance, time_taken, _ = self.solve_with_steps()
        return tour, distance, time_taken


    def solve_with_steps(self) -> Tuple[List[int], float, float, List[Dict]]:
        start_time = time.time()
        steps = []


        # Start with a triangle (3 cities), luôn bắt đầu từ 0
        if self.n < 3:
            tour = list(range(self.n))
            distance = self.calculate_tour_distance(tour)
            steps.append({
                'step': 0,
                'description': f'Khởi tạo tour với {len(tour)} thành phố, bắt đầu từ thành phố 0',
                'tour': tour.copy(),
                'selected': None,
                'position': None
            })
            steps.append({
                'step': 1,
                'description': f'Hoàn thành tour với khoảng cách {distance:.2f}. Tour khép kín từ {tour[-1]} về {tour[0]}',
                'tour': tour.copy(),
                'selected': None,
                'position': None
            })
            return tour, distance, time.time() - start_time, steps


        # Initialize with first 3 cities, luôn bắt đầu từ 0
        tour = [0, 1, 2]
        unvisited = set(range(3, self.n))


        steps.append({
            'step': 0,
            'description': 'Khởi tạo tour với 3 thành phố đầu tiên',
            'tour': tour.copy(),
            'selected': None,
            'position': None
        })


        step_num = 1
        while unvisited:
            best_city = None
            best_position = None
            best_increase = float('inf')


            # Find city and position that minimizes insertion cost
            for city in unvisited:
                for pos in range(len(tour)):
                    prev_city = tour[pos]
                    next_city = tour[(pos + 1) % len(tour)]
                    cost = (self.distance_matrix[prev_city][city] +
                            self.distance_matrix[city][next_city] -
                            self.distance_matrix[prev_city][next_city])


                    if cost < best_increase:
                        best_increase = cost
                        best_city = city
                        best_position = pos + 1


            tour.insert(best_position, best_city)
            unvisited.remove(best_city)


            steps.append({
                'step': step_num,
                'description': f'Chèn thành phố {best_city} vào vị trí {best_position}',
                'tour': tour.copy(),
                'selected': best_city,
                'position': best_position,
                'cost': best_increase
            })
            step_num += 1


        distance = self.calculate_tour_distance(tour)
        time_taken = time.time() - start_time


        steps.append({
            'step': step_num,
            'description': f'Hoàn thành tour với khoảng cách {distance:.2f}. Tour khép kín từ {tour[-1]} về {tour[0]}',
            'tour': tour.copy(),
            'selected': None,
            'position': None
        })


        return tour, distance, time_taken, steps





