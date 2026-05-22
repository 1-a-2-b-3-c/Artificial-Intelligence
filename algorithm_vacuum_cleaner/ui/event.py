import tkinter as tk
from tkinter import messagebox
from logger import write_log

def click_random(event, matrix, log_panel):
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    matrix.node = Node()
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

def click_robot(event, matrix, parent, log_panel):
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

    def click_get():
        try:
            rx = int(entry_row.get())
            ry = int(entry_col.get())

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

            matrix.show_state_have_robot()
            top.destroy()
        except ValueError:
            messagebox.showerror("Error", "Phải nhập số!")
        except IndexError:
            messagebox.showerror("Error", "Tọa độ ngoài ma trận!")

    get_button = tk.Button(top, 
                           text='Lấy dữ liệu', 
                           font=("Segoe UI", 14, "bold"),
                           command=click_get
                           )
    get_button.pack(side="bottom", pady=10)

def write_log(log_panel, text, tag=None):
    log_panel.config(state="normal")
    log_panel.insert("end", text + "\n", tag)
    log_panel.see("end")
    log_panel.config(state="disabled")
