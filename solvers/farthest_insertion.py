import time
from typing import Dict, List, Tuple

from .base import TSPSolver


class FarthestInsertion(TSPSolver):
    """Greedy Farthest Insertion algorithm"""

    def get_complexity(self) -> Tuple[str, str]:
        """
        Time Complexity: O(n²) - For each city, find farthest and best insertion
        Space Complexity: O(n²) - Distance matrix
        """
        return ("O(n²)", "O(n²)")

    def solve(self) -> Tuple[List[int], float, float]:
        tour, distance, time_taken, _ = self.solve_with_steps()
        return tour, distance, time_taken

    def solve_with_steps(self) -> Tuple[List[int], float, float, List[Dict]]:
        start_time = time.time()
        steps = []

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

        # Start with two farthest cities, đảm bảo bắt đầu từ 0
        max_dist = 0
        start_city1, start_city2 = 0, 1
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.distance_matrix[i][j] > max_dist:
                    max_dist = self.distance_matrix[i][j]
                    start_city1, start_city2 = i, j

        if start_city1 == 0:
            tour = [0, start_city2]
        elif start_city2 == 0:
            tour = [0, start_city1]
        else:
            if self.distance_matrix[0][start_city1] < self.distance_matrix[0][start_city2]:
                tour = [0, start_city1]
            else:
                tour = [0, start_city2]

        unvisited = set(range(self.n)) - set(tour)

        steps.append({
            'step': 0,
            'description': f'Khởi tạo với thành phố 0 và thành phố {tour[1]} (xa nhất từ 0)',
            'tour': tour.copy(),
            'selected': None,
            'position': None
        })

        step_num = 1
        while unvisited:
            farthest_city = None
            max_min_dist = -1

            for city in unvisited:
                min_dist_to_tour = min(self.distance_matrix[city][t] for t in tour)
                if min_dist_to_tour > max_min_dist:
                    max_min_dist = min_dist_to_tour
                    farthest_city = city

            best_position = None
            best_increase = float('inf')

            for pos in range(len(tour)):
                prev_city = tour[pos]
                next_city = tour[(pos + 1) % len(tour)]
                cost = (self.distance_matrix[prev_city][farthest_city] +
                        self.distance_matrix[farthest_city][next_city] -
                        self.distance_matrix[prev_city][next_city])

                if cost < best_increase:
                    best_increase = cost
                    best_position = pos + 1

            tour.insert(best_position, farthest_city)
            unvisited.remove(farthest_city)

            steps.append({
                'step': step_num,
                'description': f'Chèn thành phố {farthest_city} (xa nhất) vào vị trí {best_position}',
                'tour': tour.copy(),
                'selected': farthest_city,
                'position': best_position,
                'distance': max_min_dist,
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

