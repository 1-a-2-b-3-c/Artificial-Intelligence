import copy
from core.node import Node, solution, move_possible, action
from core.belief import belief_goal, belief_key, solution_partial 


def UCS_full(node, goal):
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
            index = next(
                (
                    i for i, n in enumerate(frontier)
                    if n.state == new_state and n.x == new_x and n.y == new_y
                ),
                -1
            )
            if index == -1:
                frontier.append(new_node)

            elif new_node.cost < frontier[index].cost:
                frontier[index] = new_node

def UCS_partial(belief_state):
    frontier = []
    reached = {}

    frontier.append(belief_state)

    while frontier:
        frontier.sort(key=lambda belief: max(node.cost for node in belief))
        current_belief = frontier.pop(0)

        key = belief_key(current_belief)

        if key in reached and reached[key] <= max(node.cost for node in current_belief):
            continue
        else:
            reached[key] = max(node.cost for node in current_belief)

        if belief_goal(current_belief):
            return solution_partial(current_belief)

        for move in ["up", "down", "left", "right"]:
            new_belief = []

            for node in current_belief:
                if belief_goal([node]):
                    new_node = Node(node.state, node, None, node.cost, node.x, node.y)
                    new_belief.append(new_node)
                    continue

                possible = move_possible(node)

                if move in possible:
                    new_state, new_x, new_y = action(move, node)
                else:
                    new_state = copy.deepcopy(node.state)
                    new_x = node.x
                    new_y = node.y

                cost = sum(row.count(1) for row in new_state)
                new_node = Node(new_state, node, move, node.cost + cost, new_x, new_y)
                new_belief.append(new_node)

            # Kiểm tra new_belief có trùng frontier không
            index = next(
                (
                    i for i, b in enumerate(frontier)
                    if belief_key(b) == belief_key(new_belief)
                ),
                -1
            )

            if index == -1:
                frontier.append(new_belief)
            elif max(node.cost for node in new_belief) < max(node.cost for node in frontier[index]):
                frontier[index] = new_belief

def UCS(node, goal):
    if isinstance(node, list):
        return UCS_partial(node)

    return UCS_full(node, goal)
