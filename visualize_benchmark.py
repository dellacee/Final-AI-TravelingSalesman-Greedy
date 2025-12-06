"""
Visualization for TSP Benchmark Results
Vẽ biểu đồ so sánh kết quả benchmark
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import glob


def load_benchmark_results(pattern="benchmark_results_*.json"):
    """Load tất cả các file benchmark results"""
    files = sorted(glob.glob(pattern))
    results = {}
    
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            n_cities = data['metadata']['n_cities']
            results[n_cities] = data['results']
    
    return results


def plot_execution_time_comparison(results):
    """Biểu đồ so sánh thời gian thực thi"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    algorithms = ['nearest_neighbor', 'nearest_insertion', 'farthest_insertion', 'ant_colony']
    algo_names = {
        'nearest_neighbor': 'Nearest Neighbor',
        'nearest_insertion': 'Nearest Insertion',
        'farthest_insertion': 'Farthest Insertion',
        'ant_colony': 'Ant Colony'
    }
    colors = {
        'nearest_neighbor': '#2ecc71',
        'nearest_insertion': '#3498db',
        'farthest_insertion': '#e74c3c',
        'ant_colony': '#f39c12'
    }
    
    n_cities_list = sorted(results.keys())
    
    # Plot 1: Tất cả thuật toán
    for algo in algorithms:
        times = []
        stds = []
        for n_cities in n_cities_list:
            time_data = results[n_cities][algo]['time']
            times.append(time_data['mean'])
            stds.append(time_data['std'])
        
        ax1.errorbar(n_cities_list, times, yerr=stds, 
                    label=algo_names[algo], marker='o', linewidth=2,
                    color=colors[algo], capsize=5, markersize=8)
    
    ax1.set_xlabel('Số lượng thành phố', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Thời gian thực thi (giây)', fontsize=12, fontweight='bold')
    ax1.set_title('Thời gian thực thi theo số lượng thành phố\n(Tất cả thuật toán)', 
                  fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Plot 2: Không có Ant Colony (để nhìn rõ các thuật toán nhanh hơn)
    for algo in algorithms[:-1]:  # Bỏ ant_colony
        times = []
        stds = []
        for n_cities in n_cities_list:
            time_data = results[n_cities][algo]['time']
            times.append(time_data['mean'])
            stds.append(time_data['std'])
        
        ax2.errorbar(n_cities_list, times, yerr=stds, 
                    label=algo_names[algo], marker='o', linewidth=2,
                    color=colors[algo], capsize=5, markersize=8)
    
    ax2.set_xlabel('Số lượng thành phố', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Thời gian thực thi (giây)', fontsize=12, fontweight='bold')
    ax2.set_title('Thời gian thực thi theo số lượng thành phố\n(Không có Ant Colony)', 
                  fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmark_execution_time.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: benchmark_execution_time.png")
    plt.close()


def plot_distance_comparison(results):
    """Biểu đồ so sánh khoảng cách tour"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algorithms = ['nearest_neighbor', 'nearest_insertion', 'farthest_insertion', 'ant_colony']
    algo_names = {
        'nearest_neighbor': 'Nearest Neighbor',
        'nearest_insertion': 'Nearest Insertion',
        'farthest_insertion': 'Farthest Insertion',
        'ant_colony': 'Ant Colony'
    }
    colors = {
        'nearest_neighbor': '#2ecc71',
        'nearest_insertion': '#3498db',
        'farthest_insertion': '#e74c3c',
        'ant_colony': '#f39c12'
    }
    
    n_cities_list = sorted(results.keys())
    
    for algo in algorithms:
        distances = []
        stds = []
        for n_cities in n_cities_list:
            dist_data = results[n_cities][algo]['distance']
            distances.append(dist_data['mean'])
            stds.append(dist_data['std'])
        
        ax.errorbar(n_cities_list, distances, yerr=stds,
                   label=algo_names[algo], marker='o', linewidth=2,
                   color=colors[algo], capsize=5, markersize=8)
    
    ax.set_xlabel('Số lượng thành phố', fontsize=12, fontweight='bold')
    ax.set_ylabel('Khoảng cách tour', fontsize=12, fontweight='bold')
    ax.set_title('Chất lượng giải pháp (Khoảng cách tour)', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmark_distance.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: benchmark_distance.png")
    plt.close()


def plot_memory_usage(results):
    """Biểu đồ so sánh bộ nhớ sử dụng"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algorithms = ['nearest_neighbor', 'nearest_insertion', 'farthest_insertion', 'ant_colony']
    algo_names = {
        'nearest_neighbor': 'Nearest Neighbor',
        'nearest_insertion': 'Nearest Insertion',
        'farthest_insertion': 'Farthest Insertion',
        'ant_colony': 'Ant Colony'
    }
    colors = {
        'nearest_neighbor': '#2ecc71',
        'nearest_insertion': '#3498db',
        'farthest_insertion': '#e74c3c',
        'ant_colony': '#f39c12'
    }
    
    n_cities_list = sorted(results.keys())
    
    for algo in algorithms:
        memories = []
        for n_cities in n_cities_list:
            mem_data = results[n_cities][algo]['memory_mb']
            memories.append(mem_data['mean'])
        
        ax.plot(n_cities_list, memories, label=algo_names[algo], 
               marker='o', linewidth=2, color=colors[algo], markersize=8)
    
    ax.set_xlabel('Số lượng thành phố', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bộ nhớ sử dụng (MB)', fontsize=12, fontweight='bold')
    ax.set_title('Bộ nhớ sử dụng theo số lượng thành phố', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmark_memory.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: benchmark_memory.png")
    plt.close()


def plot_performance_heatmap(results):
    """Heatmap so sánh tổng hợp"""
    algorithms = ['nearest_neighbor', 'nearest_insertion', 'farthest_insertion', 'ant_colony']
    algo_names = {
        'nearest_neighbor': 'Nearest\nNeighbor',
        'nearest_insertion': 'Nearest\nInsertion',
        'farthest_insertion': 'Farthest\nInsertion',
        'ant_colony': 'Ant\nColony'
    }
    
    n_cities_list = sorted(results.keys())
    
    # Tạo 3 subplots cho 3 metrics
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    
    # Heatmap 1: Execution Time
    time_data = []
    for n_cities in n_cities_list:
        row = []
        for algo in algorithms:
            row.append(results[n_cities][algo]['time']['mean'])
        time_data.append(row)
    
    im1 = ax1.imshow(np.array(time_data).T, cmap='RdYlGn_r', aspect='auto')
    ax1.set_xticks(range(len(n_cities_list)))
    ax1.set_xticklabels(n_cities_list)
    ax1.set_yticks(range(len(algorithms)))
    ax1.set_yticklabels([algo_names[a] for a in algorithms])
    ax1.set_xlabel('Số lượng thành phố', fontweight='bold')
    ax1.set_title('Thời gian thực thi (s)', fontweight='bold', fontsize=12)
    
    # Thêm giá trị vào cells
    for i in range(len(algorithms)):
        for j in range(len(n_cities_list)):
            text = ax1.text(j, i, f'{time_data[j][i]:.4f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    plt.colorbar(im1, ax=ax1)
    
    # Heatmap 2: Distance
    dist_data = []
    for n_cities in n_cities_list:
        row = []
        for algo in algorithms:
            row.append(results[n_cities][algo]['distance']['mean'])
        dist_data.append(row)
    
    im2 = ax2.imshow(np.array(dist_data).T, cmap='RdYlGn_r', aspect='auto')
    ax2.set_xticks(range(len(n_cities_list)))
    ax2.set_xticklabels(n_cities_list)
    ax2.set_yticks(range(len(algorithms)))
    ax2.set_yticklabels([algo_names[a] for a in algorithms])
    ax2.set_xlabel('Số lượng thành phố', fontweight='bold')
    ax2.set_title('Khoảng cách tour', fontweight='bold', fontsize=12)
    
    for i in range(len(algorithms)):
        for j in range(len(n_cities_list)):
            text = ax2.text(j, i, f'{dist_data[j][i]:.1f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    plt.colorbar(im2, ax=ax2)
    
    # Heatmap 3: Memory
    mem_data = []
    for n_cities in n_cities_list:
        row = []
        for algo in algorithms:
            row.append(results[n_cities][algo]['memory_mb']['mean'])
        mem_data.append(row)
    
    im3 = ax3.imshow(np.array(mem_data).T, cmap='YlOrRd', aspect='auto')
    ax3.set_xticks(range(len(n_cities_list)))
    ax3.set_xticklabels(n_cities_list)
    ax3.set_yticks(range(len(algorithms)))
    ax3.set_yticklabels([algo_names[a] for a in algorithms])
    ax3.set_xlabel('Số lượng thành phố', fontweight='bold')
    ax3.set_title('Bộ nhớ (MB)', fontweight='bold', fontsize=12)
    
    for i in range(len(algorithms)):
        for j in range(len(n_cities_list)):
            text = ax3.text(j, i, f'{mem_data[j][i]:.2f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    plt.colorbar(im3, ax=ax3)
    
    plt.suptitle('Heatmap so sánh hiệu năng các thuật toán TSP', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('benchmark_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: benchmark_heatmap.png")
    plt.close()


def plot_bar_comparison(results):
    """Biểu đồ cột so sánh cho từng kích thước"""
    algorithms = ['nearest_neighbor', 'nearest_insertion', 'farthest_insertion', 'ant_colony']
    algo_names = {
        'nearest_neighbor': 'NN',
        'nearest_insertion': 'NI',
        'farthest_insertion': 'FI',
        'ant_colony': 'ACO'
    }
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    
    n_cities_list = sorted(results.keys())
    n_sizes = len(n_cities_list)
    
    fig, axes = plt.subplots(2, n_sizes, figsize=(5*n_sizes, 10))
    
    for idx, n_cities in enumerate(n_cities_list):
        # Subplot 1: Thời gian
        ax1 = axes[0, idx]
        times = [results[n_cities][algo]['time']['mean'] for algo in algorithms]
        stds = [results[n_cities][algo]['time']['std'] for algo in algorithms]
        
        bars = ax1.bar(range(len(algorithms)), times, yerr=stds, 
                      color=colors, capsize=5, alpha=0.8, edgecolor='black')
        ax1.set_xticks(range(len(algorithms)))
        ax1.set_xticklabels([algo_names[a] for a in algorithms], rotation=45)
        ax1.set_ylabel('Thời gian (s)', fontweight='bold')
        ax1.set_title(f'{n_cities} thành phố', fontweight='bold', fontsize=12)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Thêm giá trị lên cột
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{time_val:.4f}', ha='center', va='bottom', fontsize=9)
        
        # Subplot 2: Khoảng cách
        ax2 = axes[1, idx]
        distances = [results[n_cities][algo]['distance']['mean'] for algo in algorithms]
        stds = [results[n_cities][algo]['distance']['std'] for algo in algorithms]
        
        bars = ax2.bar(range(len(algorithms)), distances, yerr=stds,
                      color=colors, capsize=5, alpha=0.8, edgecolor='black')
        ax2.set_xticks(range(len(algorithms)))
        ax2.set_xticklabels([algo_names[a] for a in algorithms], rotation=45)
        ax2.set_ylabel('Khoảng cách', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Thêm giá trị lên cột
        for bar, dist_val in zip(bars, distances):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{dist_val:.1f}', ha='center', va='bottom', fontsize=9)
    
    axes[0, 0].set_ylabel('Thời gian thực thi (s)', fontweight='bold', fontsize=12)
    axes[1, 0].set_ylabel('Khoảng cách tour', fontweight='bold', fontsize=12)
    
    plt.suptitle('So sánh hiệu năng theo kích thước bài toán', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('benchmark_bars.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: benchmark_bars.png")
    plt.close()


def plot_speedup_analysis(results):
    """Phân tích speedup so với thuật toán chậm nhất"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algorithms = ['nearest_neighbor', 'nearest_insertion', 'farthest_insertion']
    algo_names = {
        'nearest_neighbor': 'Nearest Neighbor',
        'nearest_insertion': 'Nearest Insertion',
        'farthest_insertion': 'Farthest Insertion'
    }
    colors = {
        'nearest_neighbor': '#2ecc71',
        'nearest_insertion': '#3498db',
        'farthest_insertion': '#e74c3c'
    }
    
    n_cities_list = sorted(results.keys())
    
    for algo in algorithms:
        speedups = []
        for n_cities in n_cities_list:
            aco_time = results[n_cities]['ant_colony']['time']['mean']
            algo_time = results[n_cities][algo]['time']['mean']
            speedup = aco_time / algo_time
            speedups.append(speedup)
        
        ax.plot(n_cities_list, speedups, label=algo_names[algo],
               marker='o', linewidth=2, color=colors[algo], markersize=8)
    
    ax.set_xlabel('Số lượng thành phố', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speedup (lần)', fontsize=12, fontweight='bold')
    ax.set_title('Tốc độ nhanh hơn so với Ant Colony Optimization', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('benchmark_speedup.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: benchmark_speedup.png")
    plt.close()


def main():
    """Hàm chính"""
    print("="*70)
    print("TSP Benchmark Visualization")
    print("="*70)
    
    # Load results
    print("\nLoading benchmark results...")
    results = load_benchmark_results()
    
    if not results:
        print("❌ No benchmark results found!")
        print("Please run benchmark.py first to generate results.")
        return
    
    print(f"✓ Loaded results for {len(results)} different problem sizes")
    print(f"  Problem sizes: {sorted(results.keys())}")
    
    # Generate all plots
    print("\nGenerating visualizations...")
    print("-" * 70)
    
    plot_execution_time_comparison(results)
    plot_distance_comparison(results)
    plot_memory_usage(results)
    plot_performance_heatmap(results)
    plot_bar_comparison(results)
    plot_speedup_analysis(results)
    
    print("-" * 70)
    print("\n✅ All visualizations generated successfully!")
    print("\nGenerated files:")
    print("  1. benchmark_execution_time.png - Thời gian thực thi")
    print("  2. benchmark_distance.png - Chất lượng giải pháp")
    print("  3. benchmark_memory.png - Bộ nhớ sử dụng")
    print("  4. benchmark_heatmap.png - Heatmap tổng hợp")
    print("  5. benchmark_bars.png - Biểu đồ cột chi tiết")
    print("  6. benchmark_speedup.png - Phân tích speedup")
    print("="*70)


if __name__ == "__main__":
    main()
