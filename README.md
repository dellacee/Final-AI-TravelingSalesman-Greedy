# Giải bài toán Traveling Salesman Problem (TSP)

Chương trình Python giải bài toán TSP sử dụng 4 thuật toán và so sánh hiệu năng của chúng.

## Các thuật toán được triển khai

1. **Nearest Neighbor (Tham lam - Láng giềng gần nhất)**
   - Bắt đầu từ một thành phố ngẫu nhiên
   - Luôn chọn thành phố chưa thăm gần nhất tiếp theo

2. **Nearest Insertion (Tham lam - Chèn gần nhất)**
   - Bắt đầu với 3 thành phố đầu tiên
   - Mỗi bước chèn thành phố chưa thăm vào vị trí tối ưu trong tour hiện tại

3. **Farthest Insertion (Tham lam - Chèn xa nhất)**
   - Bắt đầu với 2 thành phố xa nhất
   - Mỗi bước chọn thành phố xa nhất khỏi tour hiện tại và chèn vào vị trí tối ưu

4. **Ant Colony Optimization (ACO)**
   - Thuật toán metaheuristic dựa trên hành vi của kiến
   - Sử dụng pheromone và heuristic để tìm giải pháp tốt hơn

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

Chạy chương trình:
```bash
python tsp_gui.py
```

### Giao diện

1. **Tạo dữ liệu thành phố:**
   - Nhập số lượng thành phố và nhấn "Tạo ngẫu nhiên"
   - Hoặc tải từ file (mỗi dòng chứa 2 số: x y)
   - Có thể lưu dữ liệu thành phố để sử dụng sau

2. **Thiết lập tham số:**
   - Số lượng kiến (ACO): Mặc định 50
   - Số lần lặp (ACO): Mặc định 100

3. **Giải bài toán:**
   - Nhấn "Giải bài toán" để chạy cả 4 thuật toán
   - Kết quả sẽ hiển thị trong bảng so sánh và biểu đồ

4. **Xem kết quả:**
   - Tab "Thành phố": Hiển thị bản đồ các thành phố
   - Tab "So sánh": Hiển thị tour của từng thuật toán và kết quả so sánh
   - Bảng kết quả: Khoảng cách, thời gian chạy, và % chênh lệch so với kết quả tốt nhất

## Cấu trúc file

- `solvers/`: Thư mục chứa các thuật toán TSP
  - `base.py`: Lớp nền `TSPSolver`
  - `nearest_neighbor.py`: Thuật toán Nearest Neighbor
  - `nearest_insertion.py`: Thuật toán Nearest Insertion
  - `farthest_insertion.py`: Thuật toán Farthest Insertion
  - `ant_colony.py`: Thuật toán Ant Colony Optimization
- `tsp_solver.py`: File aggregator, re-export các solver trong `solvers/` (giữ tương thích nếu muốn import kiểu cũ)
- `tsp_gui.py`: Giao diện đồ họa sử dụng tkinter và matplotlib
- `requirements.txt`: Danh sách các thư viện cần thiết
- `README.md`: Hướng dẫn sử dụng

## Lưu ý

- Số lượng thành phố tối thiểu: 3
- Với số lượng thành phố lớn (>50), ACO có thể mất nhiều thời gian
- Có thể điều chỉnh tham số ACO để cân bằng giữa chất lượng giải pháp và thời gian chạy

