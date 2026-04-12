from .game_timer import GameTimer


class GameStats:
    def __init__(self) -> None:
        """@brief Initialize all game statistics fields."""
        self.moves = 0
        self.hints_used = 0
        self.timer = GameTimer()
        self.time_elapsed = 0.0
        self.states_explored = 0
        self.max_memory = 0
        self.solution_depth = 0
        self.history = []

    def print(self) -> None:
        """@brief Print a formatted statistics summary to standard output."""
        print("=== Game Stats ===")
        print(f"Moves made: {self.moves}")
        print(f"Hints used: {self.hints_used}")
        print(f"Time elapsed: {self.timer.get_time():.2f} s")
        print(f"States explored: {self.states_explored}")
        print(f"Solution depth: {self.solution_depth}")
        print(f"Maximum memory used: {self.max_memory}")
        print(f"Move history: {self.history}")
        print("==================")

    def reset(self) -> None:
        """@brief Reset all statistics to default values."""
        self.moves = 0
        self.hints_used = 0
        self.timer.reset()
        self.time_elapsed = 0.0
        self.states_explored = 0
        self.max_memory = 0
        self.solution_depth = 0
        self.history = []
