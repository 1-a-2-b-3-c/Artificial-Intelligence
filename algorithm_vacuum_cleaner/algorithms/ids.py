from algorithms import Node, move_possible, action, solution

def IDS(node, goal):
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
