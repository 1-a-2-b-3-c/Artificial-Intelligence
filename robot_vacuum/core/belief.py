def belief_goal(belief_state):

    for node in belief_state:
        if node.state != node.goal():
            return False

    return True

def belief_key(belief_state):
    key = []

    for node in belief_state:
        key.append(
            (
                tuple(map(tuple, node.state)),
                node.x,
                node.y
            )
        )

    return tuple(key)

def solution_partial(goal_belief):
    path = []

    longest_node = max(goal_belief, key=lambda n: _count_steps(n))

    steps = []
    current = longest_node
    while current is not None:
        steps.append(current)
        current = current.parent
    steps.reverse()

    for step_idx in range(len(steps)):
        belief_at_step = []
        for node in goal_belief:
            node_at_step = _get_node_at_depth(node, step_idx)
            belief_at_step.append(node_at_step)
        path.append(belief_at_step)

    return path

def _count_steps(node):
    count = 0
    current = node
    while current.parent is not None:
        count += 1
        current = current.parent
    return count

def _get_node_at_depth(node, target_depth):
    total_depth = _count_steps(node)

    steps_back = total_depth - target_depth
    current = node
    for _ in range(steps_back):
        if current.parent is not None:
            current = current.parent
    return current
