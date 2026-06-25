# 🤖 AI Algorithm Visualization Suite

Bộ mô phỏng trực quan các thuật toán Trí tuệ nhân tạo (Artificial Intelligence) được xây dựng bằng Python nhằm hỗ trợ học tập, nghiên cứu và so sánh hiệu năng giữa các nhóm thuật toán AI khác nhau.

Dự án bao gồm ba mô-đun chính:

* 🧹 Robot Hút Bụi Thông Minh (Search Algorithms)
* 🎮 Tic-Tac-Toe AI (Adversarial Search)
* 🗺️ Hue Map Coloring (Constraint Satisfaction Problem)

---

## ✨ Tính năng

### 🧹 Robot Hút Bụi Thông Minh

Mô phỏng robot tự động tìm đường và dọn dẹp môi trường.

**16 thuật toán AI**

| Nhóm              | Thuật toán                    |
| ----------------- | ----------------------------- |
| Uninformed Search | BFS, DFS, IDS, UCS            |
| Informed Search   | Greedy, A*, IDA*              |
| Local Search      | HCS, HCT, HCR, HCR-R, LBS, SA |
| Planning          | AND-OR Search                 |

**Môi trường hỗ trợ**

* Full Observable
* Partial Observable
* Complex Environment

---

### 🎮 Tic-Tac-Toe AI

Mô phỏng trò chơi Tic-Tac-Toe giữa người và AI.

**Thuật toán**

* Minimax
* Alpha-Beta Pruning
* Expectimax

**Tính năng**

* Chọn thuật toán AI
* Chọn người đi trước
* Chơi lại nhiều lần
* Mô phỏng đối thủ ngẫu nhiên với Expectimax

---

### 🗺️ Hue CSP Map Coloring

Mô phỏng bài toán tô màu bản đồ dưới dạng Constraint Satisfaction Problem.

**Thuật toán**

* Backtracking
* Forward Checking
* AC-3
* Min-Conflicts

**Tính năng**

* Tô màu 9 khu vực hành chính Thừa Thiên Huế
* Hiển thị từng bước tìm nghiệm
* Điều chỉnh tốc độ mô phỏng
* Thống kê số nút duyệt và thời gian thực thi

---

## 📚 Kiến thức AI được áp dụng

| Lĩnh vực                        | Thuật toán                                          |
| ------------------------------- | --------------------------------------------------- |
| Uninformed Search               | BFS, DFS, IDS, UCS                                  |
| Informed Search                 | Greedy, A*, IDA*                                    |
| Local Search                    | Hill Climbing, Beam Search, Simulated Annealing     |
| Planning                        | AND-OR Search                                       |
| Adversarial Search              | Minimax, Alpha-Beta, Expectimax                     |
| Constraint Satisfaction Problem | Backtracking, Forward Checking, AC-3, Min-Conflicts |

Tổng cộng hơn **20 thuật toán AI** được triển khai và trực quan hóa.

---

## 🗂️ Cấu trúc dự án

```text
AI-Visualization-Suite/
│
├── RobotVacuum/
│   ├── main.py
│   ├── algorithms/
│   ├── core/
│   └── ui/
│
├── TicTacToe/
│   └── TicTacToe.py
│
├── HueMapColoring/
│   └── HueCSP.py
│
└── README.md
```

---

## ⚙️ Cài đặt

### Yêu cầu

* Python 3.8+
* Pygame
* Pillow
* Tkinter

### Cài đặt thư viện

```bash
pip install pygame pillow
```

---

## 🚀 Chạy chương trình

### Robot Hút Bụi

```bash
python RobotVacuum/main.py
```

### Tic-Tac-Toe AI

```bash
python TicTacToe/TicTacToe.py
```

### Hue CSP Map Coloring

```bash
python HueMapColoring/HueCSP.py
```

---

## 🛠️ Công nghệ sử dụng

* Python 3
* Pygame
* Tkinter
* Pillow

---

## 🎯 Mục tiêu học thuật

Dự án được xây dựng nhằm minh họa các chủ đề cốt lõi trong môn Trí tuệ nhân tạo:

* State Space Search
* Heuristic Search
* Local Search
* Planning
* Adversarial Search
* Constraint Satisfaction Problem

Thông qua giao diện trực quan, người học có thể quan sát quá trình hoạt động của từng thuật toán, hiểu rõ nguyên lý ra quyết định và so sánh hiệu năng giữa các phương pháp AI khác nhau.

---

## 📈 Kết quả đạt được

* Xây dựng thành công 3 hệ thống mô phỏng AI độc lập.
* Triển khai hơn 20 thuật toán AI phổ biến.
* Trực quan hóa quá trình tìm kiếm và ra quyết định.
* Hỗ trợ học tập các chủ đề quan trọng trong Trí tuệ nhân tạo.
* Tạo nền tảng cho các nghiên cứu nâng cao về Robotics, Planning, Game AI và Constraint Satisfaction.

