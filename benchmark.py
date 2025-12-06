"""
Benchmark System for TSP Algorithms
Đo và so sánh hiệu năng của các thuật toán TSP
"""

import time
import tracemalloc
import numpy as np
from typing import Dict, List, Tuple, Any
from statistics import mean, stdev, median
import json
from datetime import datetime

from solvers import (
    NearestNeighbor,
    NearestInsertion,
    FarthestInsertion,
    AntColonyOptimization,
)


class PerformanceMetrics:
    """Class để lưu trữ các metrics hiệu năng"""
    
    def __init__(self):
        self.execution_time = 0.0
        self.tour_distance = 0.0
        self.memory_usage = 0.0  # MB
        self.num_iterations = 0
        self.num_comparisons = 0
        self.tour = []
        
    def to_dict(self) -> Dict:
        return {
            'execution_time': round(self.execution_time, 6),
            'tour_distance': round(self.tour_distance, 2),
            'memory_usage_mb': round(self.memory_usage, 2),
            'num_iterations': self.num_iterations,
            'num_comparisons': self.num_comparisons,
            'tour_length': len(self.tour)
        }


class BenchmarkStats:
    """Class để lưu thống kê từ nhiều lần chạy"""
    
    def __init__(self, runs: List[PerformanceMetrics]):
        self.runs = runs
        self.n_runs = len(runs)
        
        # Thống kê thời gian
        times = [r.execution_time for r in runs]
        self.time_mean = mean(times)
        self.time_std = stdev(times) if len(times) > 1 else 0
        self.time_min = min(times)
        self.time_max = max(times)
        self.time_median = median(times)
        
        # Thống kê khoảng cách
        distances = [r.tour_distance for r in runs]
        self.distance_mean = mean(distances)
        self.distance_std = stdev(distances) if len(distances) > 1 else 0
        self.distance_min = min(distances)
        self.distance_max = max(distances)
        self.distance_median = median(distances)
        
        # Thống kê bộ nhớ
        memories = [r.memory_usage for r in runs]
        self.memory_mean = mean(memories)
        self.memory_std = stdev(memories) if len(memories) > 1 else 0
        self.memory_max = max(memories)
        
    def to_dict(self) -> Dict:
        return {
            'n_runs': self.n_runs,
            'time': {
                'mean': round(self.time_mean, 6),
                'std': round(self.time_std, 6),
                'min': round(self.time_min, 6),
                'max': round(self.time_max, 6),
                'median': round(self.time_median, 6)
            },
            'distance': {
                'mean': round(self.distance_mean, 2),
                'std': round(self.distance_std, 2),
                'min': round(self.distance_min, 2),
                'max': round(self.distance_max, 2),
                'median': round(self.distance_median, 2)
            },
            'memory_mb': {
                'mean': round(self.memory_mean, 2),
                'std': round(self.memory_std, 2),
                'max': round(self.memory_max, 2)
            }
        }


class TSPBenchmark:
    """Hệ thống benchmark cho TSP"""
    
    def __init__(self, cities: List[Tuple[float, float]]):
        self.cities = cities
        self.n_cities = len(cities)
        
    def _measure_algorithm(self, solver_class, **kwargs) -> PerformanceMetrics:
        """Đo hiệu năng của một thuật toán"""
        metrics = PerformanceMetrics()
        
        # Bắt đầu đo bộ nhớ
        tracemalloc.start()
        
        # Khởi tạo solver
        if solver_class == AntColonyOptimization:
            solver = solver_class(self.cities, **kwargs)
        else:
            solver = solver_class(self.cities)
        
        # Đo thời gian thực thi
        start_time = time.perf_counter()
        tour, distance, _ = solver.solve()
        end_time = time.perf_counter()
        
        # Lấy thông tin bộ nhớ
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Lưu metrics
        metrics.execution_time = end_time - start_time
        metrics.tour_distance = distance
        metrics.memory_usage = peak / (1024 * 1024)  # Convert to MB
        metrics.tour = tour
        
        # Đếm số iterations (chỉ có ý nghĩa với ACO)
        if hasattr(solver, 'n_iterations'):
            metrics.num_iterations = solver.n_iterations
            
        return metrics
    
    def run_single(self, algorithm_name: str, **kwargs) -> PerformanceMetrics:
        """Chạy benchmark cho một thuật toán một lần"""
        algorithms = {
            'nearest_neighbor': NearestNeighbor,
            'nearest_insertion': NearestInsertion,
            'farthest_insertion': FarthestInsertion,
            'ant_colony': AntColonyOptimization
        }
        
        if algorithm_name not in algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        
        return self._measure_algorithm(algorithms[algorithm_name], **kwargs)
    
    def run_multiple(self, algorithm_name: str, n_runs: int = 10, **kwargs) -> BenchmarkStats:
        """Chạy benchmark nhiều lần và tính thống kê"""
        print(f"Running {algorithm_name} for {n_runs} times...")
        
        runs = []
        for i in range(n_runs):
            metrics = self.run_single(algorithm_name, **kwargs)
            runs.append(metrics)
            print(f"  Run {i+1}/{n_runs}: Time={metrics.execution_time:.4f}s, Distance={metrics.tour_distance:.2f}")
        
        return BenchmarkStats(runs)
    
    def compare_all(self, n_runs: int = 10, aco_params: Dict = None) -> Dict[str, BenchmarkStats]:
        """So sánh tất cả thuật toán"""
        print(f"\n{'='*70}")
        print(f"BENCHMARK: {self.n_cities} cities, {n_runs} runs each")
        print(f"{'='*70}\n")
        
        results = {}
        
        # Thuật toán đơn giản
        for algo in ['nearest_neighbor', 'nearest_insertion', 'farthest_insertion']:
            results[algo] = self.run_multiple(algo, n_runs)
            print()
        
        # Ant Colony với parameters tùy chỉnh
        if aco_params is None:
            aco_params = {
                'n_ants': min(50, self.n_cities),
                'n_iterations': 100,
                'alpha': 1.0,
                'beta': 2.0,
                'evaporation': 0.5,
                'q': 100.0
            }
        
        results['ant_colony'] = self.run_multiple('ant_colony', n_runs, **aco_params)
        
        return results
    
    def print_comparison(self, results: Dict[str, BenchmarkStats]):
        """In bảng so sánh các thuật toán"""
        print(f"\n{'='*100}")
        print(f"COMPARISON SUMMARY ({self.n_cities} cities)")
        print(f"{'='*100}")
        
        # Header
        print(f"\n{'Algorithm':<20} {'Time (s)':<25} {'Distance':<30} {'Memory (MB)':<15}")
        print(f"{'':<20} {'Mean±Std [Min-Max]':<25} {'Mean±Std [Min-Max]':<30} {'Mean±Std':<15}")
        print('-' * 100)
        
        algo_names = {
            'nearest_neighbor': 'Nearest Neighbor',
            'nearest_insertion': 'Nearest Insertion',
            'farthest_insertion': 'Farthest Insertion',
            'ant_colony': 'Ant Colony'
        }
        
        for algo_key, stats in results.items():
            name = algo_names.get(algo_key, algo_key)
            
            time_str = f"{stats.time_mean:.4f}±{stats.time_std:.4f} [{stats.time_min:.4f}-{stats.time_max:.4f}]"
            dist_str = f"{stats.distance_mean:.2f}±{stats.distance_std:.2f} [{stats.distance_min:.2f}-{stats.distance_max:.2f}]"
            mem_str = f"{stats.memory_mean:.2f}±{stats.memory_std:.2f}"
            
            print(f"{name:<20} {time_str:<25} {dist_str:<30} {mem_str:<15}")
        
        print('-' * 100)
        
        # Tìm best performer
        best_time = min(results.items(), key=lambda x: x[1].time_mean)
        best_distance = min(results.items(), key=lambda x: x[1].distance_mean)
        most_stable = min(results.items(), key=lambda x: x[1].distance_std)
        
        print(f"\n🏆 WINNERS:")
        print(f"   Fastest: {algo_names[best_time[0]]} ({best_time[1].time_mean:.4f}s)")
        print(f"   Best Distance: {algo_names[best_distance[0]]} ({best_distance[1].distance_mean:.2f})")
        print(f"   Most Stable: {algo_names[most_stable[0]]} (std={most_stable[1].distance_std:.2f})")
        print(f"{'='*100}\n")
    
    def save_results(self, results: Dict[str, BenchmarkStats], filename: str = None):
        """Lưu kết quả benchmark ra file JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{self.n_cities}cities_{timestamp}.json"
        
        output = {
            'metadata': {
                'n_cities': self.n_cities,
                'timestamp': datetime.now().isoformat(),
            },
            'results': {algo: stats.to_dict() for algo, stats in results.items()}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Results saved to: {filename}")
        return filename


def generate_random_cities(n: int, seed: int = None) -> List[Tuple[float, float]]:
    """Tạo danh sách thành phố ngẫu nhiên"""
    if seed is not None:
        np.random.seed(seed)
    
    cities = [(np.random.uniform(0, 100), np.random.uniform(0, 100)) for _ in range(n)]
    return cities


def main():
    """Chương trình chính để chạy benchmark"""
    print("TSP Algorithm Benchmark System")
    print("=" * 70)
    
    # Cấu hình
    n_cities_list = [10, 20, 30, 50]  # Test với các kích thước khác nhau
    n_runs = 5  # Số lần chạy mỗi thuật toán
    
    all_results = {}
    
    for n_cities in n_cities_list:
        print(f"\n\n{'#'*70}")
        print(f"# Testing with {n_cities} cities")
        print(f"{'#'*70}")
        
        # Tạo cities với seed cố định để reproducible
        cities = generate_random_cities(n_cities, seed=42)
        
        # Tạo benchmark
        benchmark = TSPBenchmark(cities)
        
        # Chạy benchmark
        results = benchmark.compare_all(n_runs=n_runs)
        
        # In kết quả
        benchmark.print_comparison(results)
        
        # Lưu kết quả
        benchmark.save_results(results)
        
        all_results[n_cities] = results
    
    print("\n" + "="*70)
    print("BENCHMARK COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    main()
