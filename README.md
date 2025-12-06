# Giải bài toán Traveling Salesman Problem (TSP)

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
