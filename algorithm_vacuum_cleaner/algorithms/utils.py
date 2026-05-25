from algorithms import copy


def move_possible(node):
    moves = []

    state = node.state

    m = len(state)
    n = len(state[0])

    x = node.x
    y = node.y

    if x > 0 and state[x - 1][y] != -1:
        moves.append('up')

    if x < m - 1 and state[x + 1][y] != -1:
        moves.append('down')

    if y > 0 and state[x][y - 1] != -1:
        moves.append('left')

    if y < n - 1 and state[x][y + 1] != -1:
        moves.append('right')

    return moves


def action(move, node):
    new_state = copy.deepcopy(node.state)

    x = node.x
    y = node.y

    match move:
        case 'up':
            x -= 1

        case 'down':
            x += 1

        case 'left':
            y -= 1

        case 'right':
            y += 1

        case _:
            return -1, -1

    new_state[x][y] = 0

    return new_state, x, y


def solution(node):
    nodes = []

    current = node

    while current.parent is not None:
        nodes.append(current)
        current = current.parent

    nodes.append(current)
    nodes.reverse()

    return nodes