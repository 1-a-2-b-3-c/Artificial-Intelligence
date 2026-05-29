from models import random, copy

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
            m = random.randint(4, 6)
            n = random.randint(4, 6)
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
