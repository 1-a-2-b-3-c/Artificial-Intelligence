import random 
import copy

class Node:
    def __init__(self, state=None, parent=None, direction=None, cost=None, x=None, y=None):
        self.parent = parent
        self.direction = direction
        self.cost = cost if cost is not None else 0
        if state is None:
            self.state, self.x, self.y = self.create() 
        else:
            self.state = state
            self.x = x
            self.y = y

    def create(self):
        while True:
            m = random.randint(4, 5)
            n = random.randint(4, 5)
            state = [[random.choice([-1, 0, 1]) for _ in range(n)] for _ in range(m)]

            has_dirt = any(state[i][j] == 1 for i in range(m) for j in range(n))
            if not has_dirt:
                continue
            
            return state, None, None

    def goal(self):
        g = copy.deepcopy(self.state)
        for i in range(len(g)):
            for j in range(len(g[0])):
                if self.state[i][j] == 1:
                    g[i][j] = 0
        return g

def move_possible(node):
    moves = []
    state = node.state
    m = len(state)
    n = len(state[0])
    x = node.x
    y = node.y
    if x > 0 and state[x-1][y] != -1:
        moves.append('up')
    if x < m - 1 and state[x+1][y] != -1:
        moves.append('down')
    if y > 0 and state[x][y-1] != -1:
        moves.append('left')
    if y < n - 1 and state[x][y+1] != -1:
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

def heuristic(node):
    # Số bụi còn lại + khoảng cách đến bụi gần nhất
    dirt_count = sum(row.count(1) for row in node.state)

    if dirt_count == 0:
        return 0

    distance_to_nearest_dirt = float('inf')
    for i in range(len(node.state)):
        for j in range(len(node.state[0])):
            if node.state[i][j] == 1:
                distance = abs(node.x - i) + abs(node.y - j)
                distance_to_nearest_dirt = min(distance_to_nearest_dirt, distance)
    return dirt_count + distance_to_nearest_dirt
