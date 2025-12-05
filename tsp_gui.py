"""
GUI Application for TSP Solver Comparison
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
from solvers import (
    NearestNeighbor,
    NearestInsertion,
    FarthestInsertion,
    AntColonyOptimization,
)


class TSPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Solver - So sánh các thuật toán")
        self.root.geometry("1400x900")
        
        self.cities = []
        self.results = {}
        self.process_plot_frame = None
        self.current_step = 0
        self.auto_play_job = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # City generation section
        city_frame = ttk.LabelFrame(left_panel, text="Tạo dữ liệu thành phố", padding="10")
        city_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(city_frame, text="Số lượng thành phố:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.num_cities_var = tk.StringVar(value="20")
        ttk.Entry(city_frame, textvariable=self.num_cities_var, width=10).grid(row=0, column=1, pady=5)
        
        ttk.Button(city_frame, text="Tạo ngẫu nhiên", 
                  command=self.generate_random_cities).grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        
        # Algorithm parameters
        algo_frame = ttk.LabelFrame(left_panel, text="Tham số thuật toán", padding="10")
        algo_frame.pack(fill=tk.X, pady=(0, 10))
        
        # ACO parameters
        ttk.Label(algo_frame, text="Số lượng kiến (ACO):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.n_ants_var = tk.StringVar(value="50")
        ttk.Entry(algo_frame, textvariable=self.n_ants_var, width=10).grid(row=0, column=1, pady=2)
        
        ttk.Label(algo_frame, text="Số lần lặp (ACO):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.n_iterations_var = tk.StringVar(value="100")
        ttk.Entry(algo_frame, textvariable=self.n_iterations_var, width=10).grid(row=1, column=1, pady=2)
        
        # Solve button
        solve_frame = ttk.Frame(left_panel)
        solve_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(solve_frame, text="Giải bài toán", 
                  command=self.solve_all, style="Accent.TButton").pack(fill=tk.X, pady=5)
        
        ttk.Button(solve_frame, text="Xóa kết quả", 
                  command=self.clear_results).pack(fill=tk.X, pady=5)
        
        # Results table
        results_frame = ttk.LabelFrame(left_panel, text="Kết quả so sánh", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for results
        columns = ("Thuật toán", "Khoảng cách", "Thời gian (s)", "Cải thiện (%)", "Thời gian O()", "Không gian O()")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=5)
        
        column_widths = {
            "Thuật toán": 150,
            "Khoảng cách": 100,
            "Thời gian (s)": 100,
            "Cải thiện (%)": 100,
            "Thời gian O()": 120,
            "Không gian O()": 120
        }
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=column_widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Visualization
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab for city plot
        self.city_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.city_tab, text="Thành phố")
        
        # Tab for comparison
        self.comparison_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.comparison_tab, text="So sánh")
        
        # Tab for process visualization
        self.process_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.process_tab, text="Quá trình")
        
       
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def generate_random_cities(self):
        try:
            n = int(self.num_cities_var.get())
            if n < 3:
                messagebox.showerror("Lỗi", "Số lượng thành phố phải >= 3")
                return
           
            self.cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
            self.plot_cities()
            messagebox.showinfo("Thành công", f"Đã tạo {n} thành phố ngẫu nhiên")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
   
   
   
    def plot_cities(self):
        # Clear previous plot
        for widget in self.city_tab.winfo_children():
            widget.destroy()
       
        if not self.cities:
            return
       
        fig, ax = plt.subplots(figsize=(8, 6))
        x_coords = [city[0] for city in self.cities]
        y_coords = [city[1] for city in self.cities]
       
        ax.scatter(x_coords, y_coords, c='red', s=100, zorder=3)
        for i, (x, y) in enumerate(self.cities):
            ax.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points')
       
        ax.set_title(f"Bản đồ {len(self.cities)} thành phố", fontsize=14, fontweight='bold')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True, alpha=0.3)
       
        canvas = FigureCanvasTkAgg(fig, self.city_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
   
    def solve_all(self):
        if not self.cities or len(self.cities) < 3:
            messagebox.showerror("Lỗi", "Vui lòng tạo hoặc tải dữ liệu thành phố trước")
            return
       
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
       
        self.results = {}
       
        # Get ACO parameters
        try:
            n_ants = int(self.n_ants_var.get())
            n_iterations = int(self.n_iterations_var.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Tham số ACO không hợp lệ")
            return
       
        algorithms = [
            ("Nearest Neighbor", NearestNeighbor(self.cities)),
            ("Nearest Insertion", NearestInsertion(self.cities)),
            ("Farthest Insertion", FarthestInsertion(self.cities)),
            ("Ant Colony Optimization", AntColonyOptimization(
                self.cities, n_ants=n_ants, n_iterations=n_iterations
            ))
        ]
       
        # Solve with each algorithm
        for name, solver in algorithms:
            tour, distance, time_taken = solver.solve()
            time_complexity, space_complexity = solver.get_complexity()
           
            # Get steps for visualization
            try:
                _, _, _, steps = solver.solve_with_steps()
            except:
                steps = []
           
            self.results[name] = {
                'tour': tour,
                'distance': distance,
                'time': time_taken,
                'time_complexity': time_complexity,
                'space_complexity': space_complexity,
                'steps': steps
            }
       
        # Find best distance for comparison
        best_distance = min(r['distance'] for r in self.results.values())
       
        # Update results table
        for name in ["Nearest Neighbor", "Nearest Insertion", "Farthest Insertion", "Ant Colony Optimization"]:
            result = self.results[name]
            improvement = ((result['distance'] - best_distance) / best_distance) * 100 if best_distance > 0 else 0
           
            self.results_tree.insert("", tk.END, values=(
                name,
                f"{result['distance']:.2f}",
                f"{result['time']:.4f}",
                f"{improvement:.2f}%",
                result['time_complexity'],
                result['space_complexity']
            ))
       
        # Visualize results
        self.plot_comparison()
        self.setup_process_visualization()











































































































    def on_algorithm_change(self, event=None):
        """Handle algorithm change - reset step and stop auto play"""
        # Dừng auto play nếu đang chạy
        if self.auto_play_var.get():
            self.auto_play_var.set(False)
            if self.auto_play_job:
                self.root.after_cancel(self.auto_play_job)
                self.auto_play_job = None
       
        # Reset về bước đầu tiên
        self.current_step = 0
       
        # Cập nhật plot
        self.update_process_plot()
   
    def update_process_plot(self):
        """Update the process visualization plot"""
        algorithm = self.algorithm_var.get()
       
        # Nếu đổi thuật toán, reset về bước đầu
        if algorithm != self.current_algorithm:
            self.current_step = 0
            self.current_algorithm = algorithm
       
        if algorithm not in self.results or not self.results[algorithm].get('steps'):
            # Clear plot
            for widget in self.process_tab.winfo_children():
                if isinstance(widget, ttk.Frame) and widget.winfo_children():
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Frame):
                            for w in child.winfo_children():
                                w.destroy()
            return
       
        steps = self.results[algorithm]['steps']
        if not steps:
            return
       
        # Limit current step
        self.current_step = min(self.current_step, len(steps) - 1)
        self.current_step = max(0, self.current_step)
       
        step_data = steps[self.current_step]
       
        # Update step label if it exists
        if hasattr(self, 'step_label') and self.step_label:
            self.step_label.config(text=f"Bước: {self.current_step + 1}/{len(steps)}")
       
        # Clear previous plot
        if self.process_plot_frame:
            for widget in self.process_plot_frame.winfo_children():
                widget.destroy()
       
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))
       
        # Plot all cities
        x_coords = [city[0] for city in self.cities]
        y_coords = [city[1] for city in self.cities]
        ax.scatter(x_coords, y_coords, c='lightgray', s=100, zorder=1, alpha=0.5)
       
        # Plot cities with labels
        for i, (x, y) in enumerate(self.cities):
            ax.scatter(x, y, c='red', s=150, zorder=3)
            ax.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points',
                       fontsize=10, fontweight='bold')
       
        # Plot current tour if available
        if step_data.get('tour'):
            tour = step_data['tour']
            if len(tour) > 1:
                tour_x = [self.cities[city][0] for city in tour]
                tour_y = [self.cities[city][1] for city in tour]
               
                # Draw partial tour (các cạnh giữa các thành phố liên tiếp)
                for i in range(len(tour) - 1):
                    ax.plot([tour_x[i], tour_x[i+1]], [tour_y[i], tour_y[i+1]],
                           'b-', linewidth=2, alpha=0.6, zorder=2)
               
                # Nếu tour đã hoàn thành (bước cuối), vẽ cạnh khép kín từ điểm cuối về điểm đầu
                if self.current_step == len(steps) - 1 and len(tour) > 2:
                    # Vẽ cạnh khép kín
                    ax.plot([tour_x[-1], tour_x[0]], [tour_y[-1], tour_y[0]],
                           'b-', linewidth=2, alpha=0.6, zorder=2, linestyle='--', label='Khép kín')
               
                # Highlight selected city
                if step_data.get('selected') is not None:
                    selected = step_data['selected']
                    ax.scatter(self.cities[selected][0], self.cities[selected][1],
                             c='green', s=300, zorder=4, marker='*', edgecolors='darkgreen', linewidths=2)
               
                # Highlight current city
                if step_data.get('current') is not None:
                    current = step_data['current']
                    ax.scatter(self.cities[current][0], self.cities[current][1],
                             c='blue', s=250, zorder=4, marker='s', edgecolors='darkblue', linewidths=2)
               
                # Highlight thành phố 0 (điểm bắt đầu)
                ax.scatter(self.cities[0][0], self.cities[0][1],
                         c='orange', s=200, zorder=5, marker='o', edgecolors='darkorange', linewidths=2)
       
        # Title with description
        title = f"{algorithm}\n{step_data.get('description', '')}"
        ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True, alpha=0.3)
       
        if self.process_plot_frame:
            canvas = FigureCanvasTkAgg(fig, self.process_plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.process_canvas = canvas
   
    def change_step(self, delta):
        """Change current step"""
        algorithm = self.algorithm_var.get()
        if algorithm not in self.results or not self.results[algorithm].get('steps'):
            return
       
        steps = self.results[algorithm]['steps']
        self.current_step += delta
        self.current_step = max(0, min(self.current_step, len(steps) - 1))
        self.update_process_plot()
   
    def toggle_auto_play(self):
        """Toggle auto play"""
        if self.auto_play_var.get():
            self.auto_play()
        else:
            if self.auto_play_job:
                self.root.after_cancel(self.auto_play_job)
                self.auto_play_job = None
   
    def auto_play(self):
        """Auto play steps"""
        algorithm = self.algorithm_var.get()
        if algorithm not in self.results or not self.results[algorithm].get('steps'):
            self.auto_play_var.set(False)
            return
       
        steps = self.results[algorithm]['steps']
        if self.current_step < len(steps) - 1:
            self.current_step += 1
            self.update_process_plot()
            delay = int(self.speed_var.get())
            self.auto_play_job = self.root.after(delay, self.auto_play)
        else:
            self.auto_play_var.set(False)
   
    def clear_results(self):
        self.results = {}
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
       
        if self.auto_play_job:
            self.root.after_cancel(self.auto_play_job)
            self.auto_play_job = None
        self.auto_play_var.set(False)
       
        for widget in self.comparison_tab.winfo_children():
            widget.destroy()
       
        for widget in self.process_tab.winfo_children():
            widget.destroy()




def main():
    root = tk.Tk()
    app = TSPGUI(root)
    root.mainloop()




if __name__ == "__main__":
    main()







