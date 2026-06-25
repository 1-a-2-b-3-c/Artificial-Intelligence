from core.node import Node,  move_possible, action


def and_or_search(node, goal):
    return or_search(node, goal, [])

def or_search(node, goal, path):
    print(f"OR_SEARCH: state={node.state}, x={node.x}, y={node.y}")
    
    if node.state == goal:
        print("→ GOAL REACHED!")
        return []

    if any(node.state == p.state and node.x == p.x and node.y == p.y for p in path):
        print(f"→ CYCLE DETECTED tại x={node.x}, y={node.y}")
        return 'failure'
        
    list_move = move_possible(node)
    print(f"→ Các nước đi có thể: {list_move}")
    
    for move in list_move:
        new_state, new_x, new_y = action(move, node)
        new_node = Node(new_state, node, move, 0, new_x, new_y)
        plan = and_search(new_node, goal, path + [node])
        if plan != 'failure':
            return [move, plan]
    return 'failure'

def and_search(node, goal, path):
    plan = {}
    parent_node = node.parent
    opposite = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    reverse_move = opposite[node.direction]

    if reverse_move in move_possible(parent_node):
        rev_state, rev_x, rev_y = action(reverse_move, parent_node)
        node_2 = Node(rev_state, parent_node, reverse_move, 0, rev_x, rev_y)
    else:
        node_2 = Node(parent_node.state, parent_node, 
                      node.direction, 0, parent_node.x, parent_node.y)

    list_node = [node, node_2]
    for n in list_node:
        print(f"  Xét n: x={n.x}, y={n.y}, state={n.state}")
        print(f"  Path hiện tại: {[(p.x, p.y) for p in path]}")

        if any(n.state == p.state and n.x == p.x and n.y == p.y for p in path):
            return 'failure'

        plan_n = or_search(n, goal, path)
        if plan_n == 'failure':
            return 'failure'
        plan[n] = plan_n
    return plan

def flatten_and_or_tree(plan, start_node):

    paths = []

    def dfs(plan, path):

        if plan == []:
            paths.append(path.copy())
            return

        if plan == 'failure':
            return

        if isinstance(plan, list):

            move = plan[0]
            sub_plan = plan[1]

            if isinstance(sub_plan, dict):

                for outcome_node, outcome_plan in sub_plan.items():

                    dfs(
                        outcome_plan,
                        path + [outcome_node]
                    )

    dfs(plan, [start_node])

    return paths
