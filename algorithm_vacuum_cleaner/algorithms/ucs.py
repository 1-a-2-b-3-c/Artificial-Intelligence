from models.node import Node
from algorithms.utils import move_possible, action, solution


def UCS(node, goal):
    frontier = []
    # Là 1 dict để lưu trạng thái với chi phí, nếu trùng trạng thái sẽ ưu tiên chi phí thấp hon
    reached = {}

    frontier.append(node)

    while True:
        if not frontier:
            break

        frontier.sort(key = lambda x: x.cost)
        current_node = frontier.pop(0)

        if current_node.state == goal:
            return solution(current_node)
        
        dict_key = tuple(map(tuple, current_node.state)), current_node.x, current_node.y
        
        if dict_key in reached and reached[dict_key] <= current_node.cost:
            continue 
        else:
            reached[dict_key] = current_node.cost

        for move in move_possible(current_node):
            new_state, new_x, new_y = action(move, current_node)
            # Chi phí là số bụi còn tồn tại
            cost = sum(row.count(1) for row in new_state)
            
            new_node = Node(new_state, current_node, move, current_node.cost + cost, new_x, new_y)
            frontier.append(new_node)
