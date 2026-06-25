import random
import copy
import math 
from core.node import Node,  move_possible, action, heuristic

def hill_climbing_simple(node, goal):
    # Theo hướng trái -> phải -> lên -> xuống 
    # h(n) là số bụi còn tồn tại + khoảng cách đến bụi gần nhất

    current_node = node 

    while True:
        yield current_node

        if current_node.state == goal:
            return 
        
        check = False
        list_move = move_possible(current_node)

        for move in ['left', 'right', 'up', 'down']:
            if move not in list_move:
                continue

            new_state, new_x, new_y = action(move, current_node)
            new_node = Node(new_state, current_node, move, 0, new_x, new_y)
            if heuristic(new_node) < heuristic(current_node):
                check = True
                current_node = new_node
                break

        if not check:
            return

def hill_climbing_steepest(node, goal):
    # h(n) là số bụi còn tồn tại + khoảng cách đến bụi gần nhất

    current_node = node 

    while True:
        yield current_node

        if current_node.state == goal:
            return 
        
        check = False
        best_node = None
        for move in move_possible(current_node):
            new_state, new_x, new_y = action(move, current_node)
            new_node = Node(new_state, current_node, move, 0, new_x, new_y)
            if heuristic(new_node) < heuristic(current_node):
                check = True
                if best_node is None or heuristic(new_node) < heuristic(best_node):
                    best_node = new_node
        if not check:
            return
        current_node = best_node

def hill_climbing_random(node, goal):
        # h(n) là số bụi còn tồn tại + khoảng cách đến bụi gần nhất

    current_node = node 

    while True:
        yield current_node

        if current_node.state == goal:
            return 
        
        list_node = []
        for move in move_possible(current_node):
            new_state, new_x, new_y = action(move, current_node)
            new_node = Node(new_state, current_node, move, 0, new_x, new_y)
            if heuristic(new_node) < heuristic(current_node):
                list_node.append(new_node)
        if not list_node:
            return
        current_node = random.choice(list_node)

def hill_climbing_random_restart(node, goal):
    count = 10

    for _ in range(count):
        current_node = copy.deepcopy(node)
        
        while True:
            yield current_node

            if current_node.state == goal:
                return

            better_nodes = []

            for move in move_possible(current_node):
                new_state, new_x, new_y = action(move, current_node)
                new_node = Node(new_state, current_node, move, 0, new_x, new_y)

                if heuristic(new_node) < heuristic(current_node):
                    better_nodes.append(new_node)

            if not better_nodes:
                break

            current_node = random.choice(better_nodes)

def local_beam_search(node, goal):
    k = 3
    current_nodes = [node]

    while True:
        yield current_nodes[0]

        if any(current_node.state == goal for current_node in current_nodes):
            return 
        
        next_nodes = []
        for current_node in current_nodes:
            for move in move_possible(current_node):
                new_state, new_x, new_y = action(move, current_node)
                new_node = Node(new_state, current_node, move, 0, new_x, new_y)
                next_nodes.append(new_node)

        next_nodes.sort(key=heuristic)
        current_nodes = next_nodes[:k]

def simulated_annealing(node, goal):
    T = 1000
    alpha = 0.95
    T_min = 0.001

    while T > T_min:
        yield node

        if node.state == goal:
            return 
        
        moves = move_possible(node)
        if not moves:
            return
        
        move = random.choice(moves)
        new_state, new_x, new_y = action(move, node)
        new_node = Node(new_state, node, move, 0, new_x, new_y)

        delta_e = heuristic(new_node) - heuristic(node)

        if delta_e < 0 or random.random() < math.exp(-delta_e / T):
            node = new_node

        T *= alpha
