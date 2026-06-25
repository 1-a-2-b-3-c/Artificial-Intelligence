import copy
import tkinter as tk
from tkinter import messagebox
from core.node import Node
from ui.log import write_log
from algorithms.and_or import flatten_and_or_tree
from ui.animation import animate_full_path, animate_realtime, animate_full_path_partial

def click_random(event, matrix, matrix_belief_1, matrix_belief_2, log_panel, matrix_frame, current_mode, belief_frame_1=None, belief_frame_2=None):
    if current_mode == "FULL" or current_mode == "COMPLEX":
        for widget in matrix_frame.winfo_children():
            widget.destroy()

        matrix.node = Node()
        matrix.initial_node = None
        matrix.parent = matrix_frame
        matrix.x = 50
        matrix.y = 50

        matrix.img_vatcan = matrix.picture(-1, 50, 50)
        matrix.img_cleaned = matrix.picture(0, 50, 50)
        matrix.img_buiban = matrix.picture(1, 50, 50)

        matrix.show_state_no_robot()

        m = len(matrix.node.state)
        n = len(matrix.node.state[0])
        so_bui    = sum(matrix.node.state[i][j] == 1  for i in range(m) for j in range(n))
        so_vatcan = sum(matrix.node.state[i][j] == -1 for i in range(m) for j in range(n))
        write_log(log_panel, "=" * 23)
        write_log(log_panel, f"[KHỞI TẠO] Ma trận {m} x {n}")
        write_log(log_panel, f"  • Ô bụi   : {so_bui}")
        write_log(log_panel, f"  • Vật cản : {so_vatcan}")
        write_log(log_panel, "=" * 23)   
    
    else:
        for widget in belief_frame_1.winfo_children():
            widget.destroy()

        for widget in belief_frame_2.winfo_children():
            widget.destroy()

        matrix_belief_1.node = Node()
        matrix_belief_2.node = Node()

        matrix_belief_1.parent = belief_frame_1
        matrix_belief_2.parent = belief_frame_2

        matrix_belief_1.x = 50
        matrix_belief_1.y = 50

        matrix_belief_2.x = 50
        matrix_belief_2.y = 50

        matrix_belief_1.img_vatcan = matrix_belief_1.picture(-1, 50, 50)
        matrix_belief_1.img_cleaned = matrix_belief_1.picture(0, 50, 50)
        matrix_belief_1.img_buiban = matrix_belief_1.picture(1, 50, 50)

        matrix_belief_2.img_vatcan = matrix_belief_2.picture(-1, 50, 50)
        matrix_belief_2.img_cleaned = matrix_belief_2.picture(0, 50, 50)
        matrix_belief_2.img_buiban = matrix_belief_2.picture(1, 50, 50)

        matrix_belief_1.show_state_no_robot()
        matrix_belief_2.show_state_no_robot()

        write_log(log_panel, "=" * 23)
        write_log(log_panel, "[PARTIAL OBSERVABLE]")
        write_log(log_panel, "Belief State 1 được tạo")
        write_log(log_panel, "Belief State 2 được tạo")
        write_log(log_panel, "=" * 23)

def click_robot(event, matrix, matrix_belief_1, matrix_belief_2, parent, log_panel, current_mode):
    def place_robot(matrix, row, col):
        try:
            rx = int(row)
            ry = int(col)

            if matrix.node.state[rx][ry] == -1:
                messagebox.showerror("Error", "Vị trí là vật cản!")
                return

            matrix.node.x = rx  
            matrix.node.y = ry

            write_log(log_panel, f"[ROBOT] Đặt tại ô ({rx}, {ry})")
            if matrix.node.state[rx][ry] == 1:
                messagebox.showinfo("Thông báo", f"Đã dọn sạch ô ({rx},{ry})")
                write_log(log_panel, f"  • Ô ({rx}, {ry}) có bụi → Đã dọn sạch!")
                matrix.node.state[rx][ry] = 0

            matrix.initial_node = copy.deepcopy(matrix.node)
            matrix.show_state_have_robot()
        except ValueError:
            messagebox.showerror("Error", "Phải nhập số!")
        except IndexError:
            messagebox.showerror("Error", "Tọa độ ngoài ma trận!")

    def click_get(m1, r1, c1, m2=None, r2=None, c2=None): 
        place_robot(m1, r1, c1)

        if m2 is not None:
            place_robot(m2, r2, c2)

        top.destroy()

    if current_mode == "FULL" or current_mode == "COMPLEX":
        if matrix.node is None:
            messagebox.showerror("Lỗi", "Chưa khởi tạo ma trận!")
            return 
        
        top = tk.Toplevel(parent)
        top.geometry('400x200')

        input_frame = tk.Frame(top, width=150, height=75)
        input_frame.place(relx=0.5, rely=0.5, anchor='center')
        input_frame.pack_propagate(False)

        tk.Label(input_frame, text='Nhập hàng:', font=("Arial", 14)).grid(row=0, column=0, sticky='nsew')
        entry_row = tk.Entry(input_frame, font=("Arial", 14))
        entry_row.grid(row=0, column=1, sticky='nsew')

        tk.Label(input_frame, text='Nhập cột:', font=("Arial", 14)).grid(row=1, column=0, sticky='nsew')
        entry_col = tk.Entry(input_frame, font=("Arial", 14))
        entry_col.grid(row=1, column=1, sticky='nsew')

        

        get_button = tk.Button(top, 
                            text='Lấy dữ liệu', 
                            font=("Segoe UI", 14, "bold"),
                            command=lambda: click_get(matrix, entry_row.get(), entry_col.get(), None, None, None)
                            )
        get_button.pack(side="bottom", pady=10)

    else:
        if matrix_belief_1.node is None or matrix_belief_2.node is None:
            messagebox.showerror("Lỗi", "Chưa khởi tạo ma trận!")
            return 
        
        top = tk.Toplevel(parent)
        top.geometry("450x250")
        top.title("Đặt robot cho Belief States")

        input_frame = tk.Frame(top)
        input_frame.place(relx=0.5, rely=0.5, anchor='center')

        # ===== Belief State 1 =====
        tk.Label(
            input_frame,
            text="Belief State 1",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(input_frame, text="Hàng:").grid(row=1, column=0)
        entry_row1 = tk.Entry(input_frame)
        entry_row1.grid(row=1, column=1)

        tk.Label(input_frame, text="Cột:").grid(row=2, column=0)
        entry_col1 = tk.Entry(input_frame)
        entry_col1.grid(row=2, column=1)

        # ===== Belief State 2 =====
        tk.Label(
            input_frame,
            text="Belief State 2",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, columnspan=2, padx=20, pady=5)

        tk.Label(input_frame, text="Hàng:").grid(row=1, column=2)
        entry_row2 = tk.Entry(input_frame)
        entry_row2.grid(row=1, column=3)

        tk.Label(input_frame, text="Cột:").grid(row=2, column=2)
        entry_col2 = tk.Entry(input_frame)
        entry_col2.grid(row=2, column=3)

        get_button = tk.Button(
            top,
            text="Lấy dữ liệu",
            font=("Segoe UI", 14, "bold"),
            command=lambda: click_get(matrix_belief_1, entry_row1.get(), entry_col1.get(), matrix_belief_2, entry_row2.get(), entry_col2.get())
        )

        get_button.pack(side="bottom", pady=10)

def click_start(matrix, list_algorithm_button, log_panel, FULL_PATH_ALGORITHMS, REALTIME_ALGORITHMS, current_mode, matrix_belief_1=None, matrix_belief_2=None):
    def start_full():
        matrix.reset_animation()

        if matrix.node is None:
            messagebox.showerror("Lỗi", "Chưa khởi tạo ma trận!")
            return

        if matrix.node.x is None or matrix.node.y is None:  
            messagebox.showerror("Lỗi", "Chưa đặt vị trí robot!")
            return
        
        selected = None 
        for btn in list_algorithm_button:
            if btn.selected:
                selected = btn
                break 

        if selected is None:
            messagebox.showerror("Lỗi", "Chưa chọn thuật toán!")
            return

        start_node = copy.deepcopy(matrix.initial_node)
        goal = start_node.goal()
        matrix.is_running = True

        if selected.name in FULL_PATH_ALGORITHMS:
            algorithm = FULL_PATH_ALGORITHMS[selected.name]

            # Hiện thời gian đang tính
            write_log(log_panel, f"[BẮT ĐẦU] Thuật toán: {selected.name}")
            write_log(log_panel, "⏳ Đang tính toán...")

            result_holder = [None]
            start_time = [0]

            def run_algorithm():
                import time
                start_time[0] = time.time()
                result_holder[0] = algorithm(start_node, goal)

            def check_done():
                import time
                if thread.is_alive():
                    elapsed = time.time() - start_time[0]
                    # Cập nhật dòng cuối log
                    log_panel.config(state="normal")
                    log_panel.delete("end-2l", "end-1l")
                    log_panel.insert("end-1l", f"⏳ Đang tính toán... {elapsed:.1f}s\n")
                    log_panel.config(state="disabled")
                    matrix.parent.after(500, check_done)
                else:
                    import time
                    elapsed = time.time() - start_time[0]
                    # Xóa dòng đếm, ghi kết quả
                    log_panel.config(state="normal")
                    log_panel.delete("end-2l", "end-1l")
                    log_panel.config(state="disabled")

                    result = result_holder[0]
                    if result is None or result == 'failure':
                        messagebox.showerror("Lỗi", "Không tìm được đường đi!")
                        return

                    write_log(log_panel, f"  • Thời gian: {elapsed:.2f}s")
                    if selected.name == "AND-OR":
                        paths = flatten_and_or_tree(result, start_node)
                        print("\n===== PATHS =====")

                        for i, path in enumerate(paths):
                            print(f"\nPATH {i+1}")

                            for n in path:
                                print(
                                    f"dir={n.direction}, pos=({n.x},{n.y})"
                                )
                        write_log(log_panel, f"  • Số đường đi: {len(paths)}")
                        write_log(log_panel, "-" * 41)

                        def run_next_path(index):
                            if index >= len(paths):
                                return
                            matrix.node = copy.deepcopy(matrix.initial_node)
                            matrix.show_state_have_robot()
                            write_log(log_panel, f"[ĐƯỜNG ĐI {index + 1}/{len(paths)}]")
                            animate_full_path(0, paths[index], matrix, log_panel,
                                            on_done=lambda: matrix.parent.after(800, run_next_path, index + 1))

                        run_next_path(0)
                    else:
                        write_log(log_panel, f"  • Số bước  : {len(result) - 1}")
                        write_log(log_panel, "-" * 41)
                        animate_full_path(0, result, matrix, log_panel)

            import threading
            thread = threading.Thread(target=run_algorithm, daemon=True)
            thread.start()
            start_time[0] = __import__('time').time()
            matrix.parent.after(500, check_done)

        elif selected.name in REALTIME_ALGORITHMS:
            algorithm = REALTIME_ALGORITHMS[selected.name]
            gen = algorithm(start_node, goal)

            write_log(log_panel, f"[BẮT ĐẦU] Thuật toán: {selected.name}")
            write_log(log_panel, "-" * 41)
            animate_realtime(gen, None, matrix, log_panel, step=0)
    
    def start_partial():
        if matrix_belief_1.node is None:
            messagebox.showerror("Lỗi", "Belief State 1 chưa được khởi tạo!")
            return

        if matrix_belief_2.node is None:
            messagebox.showerror("Lỗi", "Belief State 2 chưa được khởi tạo!")
            return

        if matrix_belief_1.node.x is None:
            messagebox.showerror("Lỗi", "Belief State 1 chưa đặt robot!")
            return

        if matrix_belief_2.node.x is None:
            messagebox.showerror("Lỗi", "Belief State 2 chưa đặt robot!")
            return

        selected = None
        for btn in list_algorithm_button:
            if btn.selected:
                selected = btn
                break

        if selected is None:
            messagebox.showerror("Lỗi", "Chưa chọn thuật toán!")
            return

        belief_state = [
            copy.deepcopy(matrix_belief_1.initial_node),
            copy.deepcopy(matrix_belief_2.initial_node)
        ]

        algorithm = FULL_PATH_ALGORITHMS[selected.name]

        write_log(log_panel, "=" * 23)
        write_log(log_panel, "[PARTIAL OBSERVABLE MODE]")
        write_log(log_panel, f"Thuật toán: {selected.name}")
        write_log(log_panel, f"Số belief states: {len(belief_state)}")
        write_log(log_panel, f"Belief 1 Robot: ({belief_state[0].x}, {belief_state[0].y})")
        write_log(log_panel, f"Belief 2 Robot: ({belief_state[1].x}, {belief_state[1].y})")
        write_log(log_panel, "=" * 23)

        # Hiện thời gian đang tính (giống start_full)
        write_log(log_panel, f"[BẮT ĐẦU] Thuật toán: {selected.name}")
        write_log(log_panel, "⏳ Đang tính toán...")

        result_holder = [None]
        start_time = [0]

        matrix_belief_1.is_running = True
        matrix_belief_2.is_running = True

        def run_algorithm():
            import time
            start_time[0] = time.time()
            result_holder[0] = algorithm(belief_state, None)

        def check_done():
            import time
            if thread.is_alive():
                elapsed = time.time() - start_time[0]
                log_panel.config(state="normal")
                log_panel.delete("end-2l", "end-1l")
                log_panel.insert("end-1l", f"⏳ Đang tính toán... {elapsed:.1f}s\n")
                log_panel.config(state="disabled")
                matrix_belief_1.parent.after(500, check_done)
            else:
                elapsed = time.time() - start_time[0]
                log_panel.config(state="normal")
                log_panel.delete("end-2l", "end-1l")
                log_panel.config(state="disabled")

                result = result_holder[0]
                if result is None:
                    messagebox.showerror("Lỗi", "Không tìm được đường đi!")
                    return

                write_log(log_panel, f"  • Thời gian: {elapsed:.2f}s")
                write_log(log_panel, f"  • Số bước  : {len(result) - 1}")
                write_log(log_panel, "-" * 41)

                # Animate 2 ma trận cùng lúc theo cùng 1 path
                animate_full_path_partial(0, result, matrix_belief_1, matrix_belief_2, log_panel)

        import threading
        thread = threading.Thread(target=run_algorithm, daemon=True)
        thread.start()
        start_time[0] = __import__('time').time()
        matrix_belief_1.parent.after(500, check_done)


    if current_mode == "FULL" or current_mode == "COMPLEX":
        start_full()
    else:
        start_partial()

