

def write_log(log_panel, text, tag=None):
    log_panel.config(state="normal")
    log_panel.insert("end", text + "\n", tag)
    log_panel.see("end")
    log_panel.config(state="disabled")

def update_scroll_region(event, canvas, canvas_frame):
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(canvas_frame, width=canvas.winfo_width())

def _on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

