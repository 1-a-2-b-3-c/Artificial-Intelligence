import copy
from core.node import Node, solution, move_possible, action
from core.belief import belief_goal, belief_key, solution_partial 

def IDS_full(node, goal):
    depth = 0
    while True:
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

            if current_node.cost >= depth:
                continue

            for move in move_possible(current_node):
                new_state, new_x, new_y = action(move, current_node)
                new_node = Node(new_state, current_node, move, current_node.cost + 1, new_x, new_y)
                frontier.append(new_node)
        depth += 1

def IDS_partial(belief_state):
    depth = 0
    while True:
        frontier = []
        reached = set()

        frontier.append(belief_state)

        while frontier:
            current_belief = frontier.pop()

            key = belief_key(current_belief)

            if key in reached:
                continue

            reached.add(key)

            if belief_goal(current_belief):
                return solution_partial(current_belief)

            if any(node.cost >= depth for node in current_belief):
                continue

            for move in ["up", "down", "left", "right"]:
                new_belief = []

                for node in current_belief:
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

                    new_node = Node(new_state, node, move, node.cost + 1, new_x, new_y)
                    new_belief.append(new_node)

                frontier.append(new_belief)

        depth += 1

def IDS(node, goal):
    if isinstance(node, list):
        return IDS_partial(node)

    return IDS_full(node, goal)
