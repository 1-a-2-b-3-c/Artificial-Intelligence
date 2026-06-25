from algorithms.bfs import BFS1, BFS2
from algorithms.dfs import DFS1, DFS2
from algorithms.ids import IDS
from algorithms.ucs import UCS
from algorithms.informed import Greedy, A, IDA
from algorithms.and_or import and_or_search
from algorithms.local import hill_climbing_random, hill_climbing_random_restart, hill_climbing_simple, hill_climbing_steepest, local_beam_search, simulated_annealing

LIST_ALGORITHM_BUTTON = []

DIRECTION_LABEL = {
    'up'   : '⬆',
    'down' : '⬇',
    'left' : '⬅',
    'right': '➡',
}

FULL_PATH_ALGORITHMS = {
    "BFS1": BFS1, "BFS2": BFS2, "DFS1": DFS1, "DFS2": DFS2,
    "IDS": IDS, "UCS": UCS, "Greedy": Greedy, "A*": A, "IDA*": IDA,
    "AND-OR": and_or_search,
}

REALTIME_ALGORITHMS = {
    "HCS": hill_climbing_simple,
    "HCT": hill_climbing_steepest,
    "HCR": hill_climbing_random,
    "HCR-R": hill_climbing_random_restart,
    "LBS": local_beam_search,
    "SA": simulated_annealing,
}

DISABLED_BUTTONS_BY_MODE = {
    "FULL": ["AND-OR"],
    "PARTIAL": ["HCS", "HCT", "HCR", "HCR-R", "LBS", "SA","AND-OR"],  
    "COMPLEX": ["BFS1", "BFS2", "DFS1", "DFS2", "IDS", "UCS", "Greedy", "A*", "IDA*", "HCS", "HCT", "HCR", "HCR-R", "LBS", "SA"], 
}