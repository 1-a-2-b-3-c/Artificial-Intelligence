import copy
from core.node import Node, solution, move_possible, action
from core.belief import belief_goal, belief_key, solution_partial 

def DFS1_full(node, goal):
    frontier = []
    reached = set()

    frontier.append(node)

    while True:

        if not frontier:
            break

        current_node = frontier.pop()

        if current_node.state == goal:
            return solution(current_node)

        if (tuple(map(tuple, current_node.state)), current_node.x, current_node.y) in reached:
            continue 
        else:
            reached.add((tuple(map(tuple, current_node.state)), current_node.x, current_node.y))

        for move in move_possible(current_node):
            new_state, new_x, new_y = action(move, current_node)
            new_node = Node(new_state, current_node, move, 0, new_x, new_y)
            frontier.append(new_node)

def DFS1_partial(belief_state):
    frontier = []
    reached = set()

    frontier.append(belief_state)

    while frontier:
        current_belief = frontier.pop()

        if belief_goal(new_belief):
            return solution_partial(new_belief)

        key = belief_key(current_belief)

        if key in reached:
            continue

        reached.add(key)

        for move in ["up", "down", "left", "right"]:
            new_belief = []

            for node in current_belief:
                # Nếu node đã đạt đích thì giữ nguyên, không di chuyển nữa
                if belief_goal([node]):
                    new_node = Node(node.state, node, None, 0, node.x, node.y)
                    new_belief.append(new_node)
                    continue

                possible = move_possible(node)

                if move in possible:
                    new_state, new_x, new_y = action(move, node)
                else:
                    new_state = copy.deepcopy(node.state)
                    new_x = node.x
                    new_y = node.y

                new_node = Node(new_state, node, move, 0, new_x, new_y)
                new_belief.append(new_node)

            frontier.append(new_belief)

def DFS1(node, goal):
    if isinstance(node, list):
        return DFS1_partial(node)

    return DFS1_full(node, goal)

def DFS2_full(node, goal):
    frontier = []
    reached = set()

    frontier.append(node)

    while True:

        if not frontier:
            break

        current_node = frontier.pop()

        if (tuple(map(tuple, current_node.state)), current_node.x, current_node.y) in reached:
            continue 
        else:
            reached.add((tuple(map(tuple, current_node.state)), current_node.x, current_node.y))

        for move in move_possible(current_node):
            new_state, new_x, new_y = action(move, current_node)

            new_node = Node(new_state, current_node, move, 0, new_x, new_y)

            if new_state == goal:
                return solution(new_node)
            
            frontier.append(new_node)

def DFS2_partial(belief_state):
    frontier = []
    reached = set()

    frontier.append(belief_state)

    while frontier:
        current_belief = frontier.pop()

        key = belief_key(current_belief)

        if key in reached:
            continue

        reached.add(key)

        for move in ["up", "down", "left", "right"]:
            new_belief = []

            for node in current_belief:
                # Nếu node đã đạt đích thì giữ nguyên, không di chuyển nữa
                if belief_goal([node]):
                    new_node = Node(node.state, node, None, 0, node.x, node.y)
                    new_belief.append(new_node)
                    continue

                possible = move_possible(node)

                if move in possible:
                    new_state, new_x, new_y = action(move, node)
                else:
                    new_state = copy.deepcopy(node.state)
                    new_x = node.x
                    new_y = node.y

                new_node = Node(new_state, node, move, 0, new_x, new_y)
                new_belief.append(new_node)

            if belief_goal(new_belief):
                return solution_partial(new_belief)
            frontier.append(new_belief)

def DFS2(node, goal):
    if isinstance(node, list):
        return DFS1_partial(node)

    return DFS2_full(node, goal)
