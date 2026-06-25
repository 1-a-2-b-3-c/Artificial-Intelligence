import copy
from core.node import Node, solution, move_possible, action, heuristic
from core.belief import belief_goal, belief_key, solution_partial 


def Greedy_full(node, goal):
    frontier = []
    reached = set()

    frontier.append(node)

    while True:
        if not frontier:
            break

        frontier.sort(key = lambda x: x.cost)

        current_node = frontier.pop()

        if current_node.state == goal:
            return solution(current_node)

        if (tuple(map(tuple, current_node.state)), current_node.x, current_node.y) in reached:
            continue 
        else:
            reached.add((tuple(map(tuple, current_node.state)), current_node.x, current_node.y))

        for move in move_possible(current_node):
            new_state, new_x, new_y = action(move, current_node)

            h = heuristic(Node(new_state, None, None, 0, new_x, new_y))
            
            new_node = Node(new_state, current_node, move, h, new_x, new_y)
            frontier.append(new_node)

def Greedy_partial(belief_state):
    frontier = []
    reached = set()

    frontier.append(belief_state)

    while frontier:
        frontier.sort(key=lambda belief: max(node.cost for node in belief))
        current_belief = frontier.pop()

        key = belief_key(current_belief)

        if key in reached:
            continue

        reached.add(key)

        if belief_goal(current_belief):
            return solution_partial(current_belief)

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

                h = heuristic(Node(new_state, None, None, 0, new_x, new_y))
                new_node = Node(new_state, node, move, h, new_x, new_y)
                new_belief.append(new_node)

            frontier.append(new_belief)

def Greedy(node, goal):
    if isinstance(node, list):
        return Greedy_partial(node)

    return Greedy_full(node, goal)

def A_full(node, goal):
    # Node.cost là f(n)
    # g(n) là số bước đã đi
    # h(n) là số bụi còn tồn tại

    frontier = []
    # Là 1 dict để lưu trạng thái với chi phí, nếu trùng trạng thái sẽ ưu tiên chi phí thấp hon
    reached = {}
    node.cost = sum(row.count(1) for row in node.state)
    frontier.append(node)

    while True:
        if not frontier:
            break

        frontier.sort(key = lambda x: x.cost)
        current_node = frontier.pop(0)
        g_n = current_node.cost - sum(row.count(1) for row in current_node.state)

        if current_node.state == goal:
            return solution(current_node)
        
        dict_key = tuple(map(tuple, current_node.state)), current_node.x, current_node.y
        
        if dict_key in reached and reached[dict_key] <= current_node.cost:
            continue 
        else:
            reached[dict_key] = current_node.cost

        for move in move_possible(current_node):
            new_state, new_x, new_y = action(move, current_node)
            f_n = g_n + 1 + sum(row.count(1) for row in new_state)
            
            new_node = Node(new_state, current_node, move, f_n, new_x, new_y)
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

def A_partial(belief_state):
    frontier = []
    reached = {}

    # Khởi tạo cost ban đầu cho từng node
    for node in belief_state:
        node.cost = sum(row.count(1) for row in node.state)

    frontier.append(belief_state)

    while frontier:
        frontier.sort(key=lambda belief: max(node.cost for node in belief))
        current_belief = frontier.pop(0)

        key = belief_key(current_belief)
        max_cost = max(node.cost for node in current_belief)

        if key in reached and reached[key] <= max_cost:
            continue
        else:
            reached[key] = max_cost

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

                # g(n) = f(n) - h(n) của node hiện tại
                g_n = node.cost - sum(row.count(1) for row in node.state)
                f_n = g_n + 1 + sum(row.count(1) for row in new_state)

                new_node = Node(new_state, node, move, f_n, new_x, new_y)
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

def A(node, goal):
    if isinstance(node, list):
        return A_partial(node)

    return A_full(node, goal)

def IDA_full(node, goal):
    # Node.cost là f(n)
    # g(n) là số bước đã đi
    # h(n) là số bụi còn tồn tại

    threshold = sum(row.count(1) for row in node.state)
    
    while True:
        min_threshold = float('inf')

        frontier = []
        # Là 1 dict để lưu trạng thái với chi phí, nếu trùng trạng thái sẽ ưu tiên chi phí thấp hon
        reached = {}
        node.cost = sum(row.count(1) for row in node.state)
        frontier.append(node)

        while True:
            if not frontier:
                break

            frontier.sort(key = lambda x: x.cost)
            current_node = frontier.pop(0)
            g_n = current_node.cost - sum(row.count(1) for row in current_node.state)

            if current_node.state == goal:
                return solution(current_node)
            
            dict_key = tuple(map(tuple, current_node.state)), current_node.x, current_node.y
            
            if dict_key in reached and reached[dict_key] <= current_node.cost:
                continue 
            else:
                reached[dict_key] = current_node.cost

            for move in move_possible(current_node):
                new_state, new_x, new_y = action(move, current_node)
                f_n = g_n + 1 + sum(row.count(1) for row in new_state)

                if f_n > threshold:
                    if f_n < min_threshold:
                        min_threshold = f_n
                    continue
                
                new_node = Node(new_state, current_node, move, f_n, new_x, new_y)
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
        threshold = min_threshold

def IDA_partial(belief_state):
    threshold = max(sum(row.count(1) for row in node.state) for node in belief_state)

    while True:
        min_threshold = float('inf')

        frontier = []
        reached = {}

        for node in belief_state:
            node.cost = sum(row.count(1) for row in node.state)

        frontier.append(belief_state)

        while frontier:
            frontier.sort(key=lambda belief: max(node.cost for node in belief))
            current_belief = frontier.pop(0)

            key = belief_key(current_belief)
            max_cost = max(node.cost for node in current_belief)

            if key in reached and reached[key] <= max_cost:
                continue
            else:
                reached[key] = max_cost

            if belief_goal(current_belief):
                return solution_partial(current_belief)

            for move in ["up", "down", "left", "right"]:
                new_belief = []
                max_f_n = 0

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

                    g_n = node.cost - sum(row.count(1) for row in node.state)
                    f_n = g_n + 1 + sum(row.count(1) for row in new_state)

                    if f_n > max_f_n:
                        max_f_n = f_n

                    new_node = Node(new_state, node, move, f_n, new_x, new_y)
                    new_belief.append(new_node)

                # Kiểm tra threshold theo max f_n của belief
                if max_f_n > threshold:
                    if max_f_n < min_threshold:
                        min_threshold = max_f_n
                    continue

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

        threshold = min_threshold

def IDA(node, goal):
    if isinstance(node, list):
        return IDA_partial(node)

    return IDA_full(node, goal)
