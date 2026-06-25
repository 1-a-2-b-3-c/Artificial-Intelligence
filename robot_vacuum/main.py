import base64
import io
import tkinter as tk
from tkinter import ttk
from ui.buttons import Algorithm_button
from ui.log import update_scroll_region, _on_mousewheel
from ui.events import click_random, click_robot, click_start
from ui.matrix import Matrix
from ui.modes import switch_to_complex, switch_to_full, switch_to_partial
from ui.constants import FULL_PATH_ALGORITHMS, REALTIME_ALGORITHMS, LIST_ALGORITHM_BUTTON

root = tk.Tk()
root.geometry("1000x600")
root.title("Máy hút bụi")
root.configure(bg="#F5F7FA")

# ========================== Mode Frame (top)
mode_frame = tk.Frame(root, bg="#DDE6ED", height=50)
mode_frame.pack(side="top", fill="x")

btn_full_mode = tk.Button(
    mode_frame,
    text="Full Observable",
    font=("Segoe UI", 10, "bold")
)
btn_full_mode.pack(side="left", padx=10, pady=8)

btn_partial_mode = tk.Button(
    mode_frame,
    text="Partial Observable",
    font=("Segoe UI", 10, "bold")
)
btn_partial_mode.pack(side="left", padx=10, pady=8)

btn_complex_mode = tk.Button(
    mode_frame,
    text="Complex Environment",
    font=("Segoe UI", 10, "bold")
)
btn_complex_mode.pack(side="left", padx=10, pady=8)

# ========================== Main Frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# ========================== Left Frame (danh sách thuật toán)
left_frame = tk.Frame(main_frame, width=150)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

scrollbar = ttk.Scrollbar(left_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")
canvas = tk.Canvas(left_frame, bg="lightblue", highlightthickness=0,
                   yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.config(command=canvas.yview)

canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas)))
canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

algorithm_frame = tk.Frame(canvas, bg="lightblue")
canvas_frame = canvas.create_window((0, 0), window=algorithm_frame, anchor="nw")
algorithm_frame.bind("<Configure>", lambda e: update_scroll_region(e, canvas, canvas_frame))
canvas.bind('<Configure>', lambda event: canvas.itemconfig(canvas_frame, width=event.width))
canvas.after(100, lambda: update_scroll_region(None, canvas, canvas_frame))

# ========================== Algorithm Buttons
btn_BFS1 = Algorithm_button(algorithm_frame, "BFS1")
btn_BFS2 = Algorithm_button(algorithm_frame, "BFS2")
btn_DFS1 = Algorithm_button(algorithm_frame, "DFS1")
btn_DFS2 = Algorithm_button(algorithm_frame, "DFS2")
btn_IDS = Algorithm_button(algorithm_frame, "IDS")
btn_UCS = Algorithm_button(algorithm_frame, "UCS")
btn_Greedy = Algorithm_button(algorithm_frame, "Greedy")
btn_A = Algorithm_button(algorithm_frame, "A*")
btn_IDA = Algorithm_button(algorithm_frame, "IDA*")
btn_Hill_Climbing_Simple = Algorithm_button(algorithm_frame, "HCS")
btn_Hill_Climbing_Steepest = Algorithm_button(algorithm_frame, "HCT")
btn_Hill_Climbing_Random = Algorithm_button(algorithm_frame, "HCR")
btn_Hill_Climbing_Random_Restart = Algorithm_button(algorithm_frame, "HCR-R")
btn_Local_Beam_Search = Algorithm_button(algorithm_frame, "LBS")
btn_Simulated_Annealing = Algorithm_button(algorithm_frame, "SA")
btn_And_Or_Search = Algorithm_button(algorithm_frame, "AND-OR")

LIST_ALGORITHM_BUTTON.extend([
    btn_BFS1, btn_BFS2, btn_DFS1, btn_DFS2, btn_IDS,
    btn_UCS, btn_Greedy, btn_A, btn_IDA,
    btn_Hill_Climbing_Simple, btn_Hill_Climbing_Steepest,
    btn_Hill_Climbing_Random, btn_Hill_Climbing_Random_Restart,
    btn_Local_Beam_Search, btn_Simulated_Annealing, btn_And_Or_Search
])

for btn in LIST_ALGORITHM_BUTTON:
    others = [b for b in LIST_ALGORITHM_BUTTON if b != btn]
    btn.add_other_button(others)


# ========================== Center Frame (ma trận)
center_frame = tk.Frame(main_frame, bg='white')
center_frame.pack(side="left", fill="both", expand=True)

matrix_container = tk.Frame(center_frame, bg='white')
matrix_container.pack(side="top", fill="both", expand=True)

# Full mode frame
single_matrix_frame = tk.Frame(matrix_container)
single_matrix_frame.pack(expand=True)
matrix_frame = single_matrix_frame

# Partial mode frame
partial_container = tk.Frame(matrix_container, bg="white")

belief_frame_1 = tk.Frame(partial_container, bg="white")
separator = tk.Frame(partial_container, bg="black", width=2)
belief_frame_2 = tk.Frame(partial_container, bg="white")

belief_frame_1.pack(side="left", expand=True, fill="both")
separator.pack(side="left", fill="y", padx=5)
belief_frame_2.pack(side="left", expand=True, fill="both")

# ========================== Bottom Frame (các nút điều khiển)
bottom_frame = tk.Frame(center_frame, bg="gray", height=80)
bottom_frame.pack(side="bottom", fill="x")
bottom_frame.pack_propagate(False)

robot_button = tk.Button(bottom_frame, text="Robot", font=("Segoe UI", 12, "bold"))
robot_button.place(relx=0.25, rely=0.5, anchor='center')

random_button = tk.Button(bottom_frame, text="Random", font=("Segoe UI", 12, "bold"))
random_button.place(relx=0.5, rely=0.5, anchor='center')

start_button = tk.Button(bottom_frame, text="Bắt đầu", font=("Segoe UI", 12, "bold"))
start_button.place(relx=0.75, rely=0.5, anchor='center')

# ========================== Right Frame (log panel)
right_frame = tk.Frame(main_frame, bg="#2C3E50", width=250)
right_frame.pack(side="left", fill="y")
right_frame.pack_propagate(False)

log_panel = tk.Text(
    right_frame,
    bg="#1A252F",
    fg="lightgreen",
    font=("Segoe UI Emoji", 10),
    wrap="word",
    state="disabled",
    relief="flat",
    padx=8,
    pady=8
)
log_panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.96)

# ========================== Khởi tạo Matrix (sau khi đã có log_panel)
matrix = Matrix()
matrix_belief_1 = Matrix()
matrix_belief_2 = Matrix()

# ========================== Bind Events (sau khi đã có matrix và log_panel)
random_button.bind("<Button-1>", lambda event: click_random(
    event, matrix, matrix_belief_1, matrix_belief_2, log_panel,
    matrix_frame, current_mode_ref[0], belief_frame_1, belief_frame_2  
))

robot_button.bind("<Button-1>", lambda event: click_robot(
    event, matrix, matrix_belief_1, matrix_belief_2, root, log_panel, current_mode_ref[0]
))

start_button.config(command=lambda: click_start(
    matrix, LIST_ALGORITHM_BUTTON, log_panel, FULL_PATH_ALGORITHMS,
    REALTIME_ALGORITHMS, current_mode_ref[0], matrix_belief_1, matrix_belief_2
))
# ========================== Constants & Mode

# ========================== Switch Mode (sau cùng)
current_mode_ref = ["FULL"]
btn_full_mode.config(command=lambda: switch_to_full(
    single_matrix_frame, partial_container, current_mode_ref
))
btn_partial_mode.config(command=lambda: switch_to_partial(
    single_matrix_frame, partial_container, current_mode_ref
))
btn_complex_mode.config(command=lambda: switch_to_complex(
    single_matrix_frame, partial_container, current_mode_ref
))

root.mainloop()