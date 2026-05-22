from collections import deque
from models.node import Node
from algorithms.utils import move_possible, action, solution

def BFS1(node, goal):
    frontier = deque()
    reached = set()

    frontier.append(node)

    while True:

        if not frontier:
            break

        current_node = frontier.popleft()

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


def BFS2(node, goal):
    frontier = deque()
    reached = set()

    frontier.append(node)

    while True:

        if not frontier:
            break

        current_node = frontier.popleft()

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