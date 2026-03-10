class GameStats:
    def __init__(self):
        self.score = 0
        self.moves = 0
        self.time_elapsed = 0.0
        self.states_explored = 0
        self.max_memory = 0
        self.solution_depth = 0
        self.history = []

    def print(self):
        print("=== Game Stats ===")
        print(f"Score: {self.score}")
        print(f"Moves made: {self.moves}")
        print(f"Time elapsed: {self.time_elapsed:.2f} s")
        print(f"States explored: {self.states_explored}")
        print(f"Solution depth: {self.solution_depth}")
        print(f"Maximum memory used: {self.max_memory}")
        print(f"Move history: {self.history}")
        print("==================")
