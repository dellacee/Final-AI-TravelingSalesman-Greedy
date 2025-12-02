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
    