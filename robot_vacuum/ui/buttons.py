import tkinter as tk
from ui.constants import DISABLED_BUTTONS_BY_MODE, LIST_ALGORITHM_BUTTON

class Algorithm_button():
    def __init__(self, parent, name):
        self.name = name 
        self.selected = False
        self.disabled = False
        self.other_button = []
        self.btn = tk.Button(
            parent, 
            text=name,
            font=("Segoe UI", 10, "bold")
            )
        self.btn.pack(pady=15, padx=15, fill="x")
        self.btn.bind("<Button-1>", self.on_click)  
        self.btn.bind("<Enter>", self.on_enter)
        self.btn.bind("<Leave>", self.on_leave)    

    def disable(self):
        self.disabled = True
        self.btn.config(bg="#BDC3C7", fg="#7F8C8D", cursor="arrow")

    def enable(self):
        self.disabled = False
        self.btn.config(bg="SystemButtonFace", fg="black", cursor="")

    def add_other_button(self, list_button):
        self.other_button = list_button

    def on_click(self, event):
        if self.disabled:
            return 

        self.selected = True
        event.widget.config(bg="lightgreen", state="normal")
        for btn in self.other_button:
            btn.selected = False
            btn.btn.config(bg="#7F8C8D", state="normal")

    def on_enter(self, event):
        if self.disabled:  
            event.widget.config(cursor="arrow")
            return
    
        event.widget.config(relief="raised")

    def on_leave(self, event):
        if self.disabled:
            return
    
        event.widget.config(relief="flat")

def update_buttons_for_mode(mode):
    disabled = DISABLED_BUTTONS_BY_MODE.get(mode, [])
    for btn in LIST_ALGORITHM_BUTTON:
        if btn.name in disabled:
            btn.disable()
        else:
            btn.enable()
