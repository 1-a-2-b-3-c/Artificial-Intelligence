import copy 
import base64
import io
import tkinter as tk
from PIL import Image, ImageTk
from core.node import move_possible
from ui.assets import load_image_from_b64, B64_CLEAN, B64_DIRT, B64_OBSTACLE, B64_ROBOT

class Matrix():
    # x, y kích thước từng ô trong ma trận
    def __init__(self, node=None, parent=None, x=None, y=None):
        self.node = None 
        self.parent = parent
        self.x = x
        self.y = y

        self.initial_node = None
        self.after_id = None
        self.is_running = False

        if node is not None:
            self.node = node 

            self.initial_node = copy.deepcopy(node)

            self.img_vatcan = self.picture(-1, 50, 50)
            self.img_cleaned = self.picture(0, 50, 50)
            self.img_buiban = self.picture(1, 50, 50)

    def picture(self, value, x, y):
        b64_map = {
            -1: B64_OBSTACLE,
            1: B64_DIRT,
            0: B64_CLEAN,
        }
        return load_image_from_b64(b64_map[value], (x, y))
        
    def show_state_no_robot(self):
        state = self.node.state
        m = len(state)
        n = len(state[0])
        
        for i in range(m):
            self.parent.rowconfigure(i, weight=1)
        for i in range(n):
            self.parent.columnconfigure(i, weight=1)


        for i in range(m):
            for j in range(n):
                if state[i][j] == -1:
                    img = self.img_vatcan
                elif state[i][j] == 0:
                    img = self.img_cleaned
                else:
                    img = self.img_buiban
                cell = tk.Label(
                    self.parent,
                    image=img,
                    borderwidth=1,
                    relief='solid'
                )
                cell.image = img 
                cell.grid(row=i, column=j, sticky='nsew')

    def reset_animation(self):

        if self.after_id is not None:
            self.parent.after_cancel(self.after_id)
            self.after_id = None

        self.is_running = False

        if self.initial_node is None:
            return

        self.node = copy.deepcopy(self.initial_node)

        self.show_state_have_robot()

    def show_state_have_robot(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        state = self.node.state
        m = len(state)
        n = len(state[0])
        x = self.node.x
        y = self.node.y

        for i in range(m):
            self.parent.rowconfigure(i, weight=1)
        for i in range(n):
            self.parent.columnconfigure(i, weight=1)

        # ✅ Load robot image đúng cách, 1 lần duy nhất trước vòng lặp
        data = base64.b64decode(B64_ROBOT)
        img_robot = Image.open(io.BytesIO(data)).resize((self.x, self.y))
        img_robot = ImageTk.PhotoImage(img_robot)

        reachable = set()
        for move in move_possible(self.node):
            if move == 'up':    reachable.add((x-1, y))
            if move == 'down':  reachable.add((x+1, y))
            if move == 'left':  reachable.add((x, y-1))
            if move == 'right': reachable.add((x, y+1))

        for i in range(m):
            for j in range(n):
                if x == i and y == j:
                    img = img_robot
                elif state[i][j] == -1:
                    img = self.img_vatcan
                elif state[i][j] == 0:
                    img = self.img_cleaned
                else:
                    img = self.img_buiban

                if (i, j) in reachable:
                    cell = tk.Label(
                        self.parent, image=img,
                        borderwidth=0, relief='flat',
                        highlightthickness=3,
                        highlightbackground="#00CC44",
                        highlightcolor="#00CC44"
                    )
                else:
                    cell = tk.Label(self.parent, image=img, borderwidth=1, relief='solid')
                cell.image = img 
                cell.grid(row=i, column=j, sticky='nsew')
