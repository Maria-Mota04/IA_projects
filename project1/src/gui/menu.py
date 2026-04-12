import pygame
import random
from src.game.solver import Solver
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState
from src.utils.leaderboard import Leaderboard
from src.utils.file_manager import FileManager
import time
import copy


class Menu:
    def __init__(self, screen):
        """
        @brief Initialize the main menu UI state and shared resources.

        @param screen Pygame display surface used to render menu screens.
        """
        self.screen = screen
        self.leaderboard = Leaderboard()

        self.WHITE = (255, 255, 255)
        self.LIGHT = (170, 170, 170)
        self.DARK = (100, 100, 100)
        self.BG = (60, 25, 60)
        self.SELECTED = (180, 80, 180)

        self.difficulty = "medium"
        self.difficulty_moves = {
            "easy": (4, 6),
            "medium": (7, 10),
            "hard": (11, 14),
        }

    def _shuffle_board_for_difficulty(self, board: Board):
        """
        @brief Shuffle the board according to the selected difficulty range.

        @param board Board instance to shuffle in-place.
        """
        min_moves, max_moves = self.difficulty_moves[self.difficulty]
        n_moves = random.randint(min_moves, max_moves)
        board.shuffle_board(n_moves=n_moves)

    def run(self):
        """
        @brief Run the main menu loop and dispatch selected game modes.
        """
        game_running = True
        font = pygame.font.SysFont("arial", 40)

        board = Board(list(range(1, 21)))
        self._shuffle_board_for_difficulty(board)
        game = Game(GameState(board))

        solver = Solver()
        try_again = False

        play_button = pygame.Rect(250, 120, 300, 50)
        ia_button = pygame.Rect(250, 185, 300, 50)
        difficulty_button = pygame.Rect(250, 250, 300, 50)
        leaderboard_button = pygame.Rect(250, 315, 300, 50)
        read_file_button = pygame.Rect(250, 380, 300, 50)
        quit_button = pygame.Rect(250, 445, 300, 50)

        play_text = font.render("Play", True, self.WHITE)
        ia_text = font.render("Algorithms", True, self.WHITE)
        difficulty_text = font.render("Difficulty", True, self.WHITE)
        leaderboard_text = font.render("Leaderboard", True, self.WHITE)
        read_file_text = font.render("Read from File", True, self.WHITE)
        quit_text = font.render("Quit", True, self.WHITE)

        loading_text = font.render("Loading...", True, self.WHITE)

        while game_running:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            for button in [
                play_button,
                ia_button,
                difficulty_button,
                leaderboard_button,
                read_file_button,
                quit_button,
            ]:
                pygame.draw.rect(
                    self.screen,
                    self.LIGHT if button.collidepoint(mouse) else self.DARK,
                    button,
                )

            self.screen.blit(play_text, (355, 125))
            self.screen.blit(ia_text, (290, 190))
            self.screen.blit(difficulty_text, (290, 255))
            self.screen.blit(leaderboard_text, (275, 320))
            self.screen.blit(read_file_text, (255, 385))
            self.screen.blit(quit_text, (355, 450))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                if event.type == pygame.MOUSEBUTTONUP or try_again:
                    click_pos = (
                        event.pos if event.type == pygame.MOUSEBUTTONUP else mouse
                    )

                    if play_button.collidepoint(click_pos) or try_again:
                        try_again = False
                        game.start_game()
                        self.screen.fill(self.BG)
                        ret = solver.solve(game=game, screen=self.screen, mode=2)

                        if ret == 0:
                            game._game_stats.solution_depth = game._game_stats.moves
                            game.finalize_game_time()
                            time.sleep(0.5)
                            self.leaderboard.add_entry(
                                game._game_stats.moves,
                                game.get_game_time(),
                            )

                            if self.display_win(game) == -1:
                                game_running = False
                                break

                        elif ret == -1:
                            game_running = False
                            break

                        else:
                            ret1 = self.display_lose()

                            if ret1 == 0:
                                board.reset_board()
                                game.set_board_state(GameState(board))
                                try_again = True
                                pygame.event.post(pygame.event.Event(pygame.USEREVENT))
                                continue

                            if ret1 == -1:
                                game_running = False
                                break

                        self._shuffle_board_for_difficulty(board)
                        state = GameState(board)
                        game = Game(state)

                    elif ia_button.collidepoint(click_pos):
                        config = self.display_algorithm_choice()

                        if config == -1:
                            game_running = False
                            break
                        elif config == -2:
                            continue
                        else:
                            self.screen.fill(self.BG)
                            self.screen.blit(loading_text, (300, 280))
                            pygame.display.update()

                            path, stats = solver.solve(
                                game=game,
                                screen=self.screen,
                                mode=1,
                                strategy=config["strategy"],
                                depth_limit=config["depth_limit"],
                                max_cost=config["max_cost"],
                                weight=config["weight"],
                                heuristic_func=config["heuristic_func"],
                            )

                            game._game_stats.states_explored = stats["nodes"]
                            game._game_stats.solution_depth = stats["depth"]
                            game._game_stats.max_memory = stats["nodes"]

                            if (
                                self.display_algo_result(game, path, stats, solver)
                                == -1
                            ):
                                game_running = False
                                break

                            self._shuffle_board_for_difficulty(board)
                            state = GameState(board)
                            game = Game(state)

                    elif difficulty_button.collidepoint(click_pos):
                        ret = self.display_difficulty_choice()

                        if ret == -1:
                            game_running = False
                            break
                        elif ret is not None:
                            self.difficulty = ret
                            self._shuffle_board_for_difficulty(board)
                            game = Game(GameState(board))

                    elif leaderboard_button.collidepoint(click_pos):
                        if self.display_leaderboard() == -1:
                            game_running = False
                            break

                    elif read_file_button.collidepoint(click_pos):
                        if self.display_choose_file_menu(game) == -1:
                            game_running = False
                            break

                    elif quit_button.collidepoint(click_pos):
                        game_running = False

            pygame.display.update()

    def display_difficulty_choice(self):
        """
        @brief Show the difficulty selection screen.

        @return Selected difficulty string, None for back, or -1 when quitting.
        """
        font = pygame.font.SysFont("arial", 40)

        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        title_text = font.render("DIFFICULTY", True, self.WHITE)

        easy_button = pygame.Rect(250, 180, 300, 60)
        medium_button = pygame.Rect(250, 270, 300, 60)
        hard_button = pygame.Rect(250, 360, 300, 60)

        easy_text = font.render("Easy", True, self.WHITE)
        medium_text = font.render("Medium", True, self.WHITE)
        hard_text = font.render("Hard", True, self.WHITE)

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 32))

            self.screen.blit(title_text, (260, 90))

            easy_color = (
                self.SELECTED
                if self.difficulty == "easy"
                else (self.LIGHT if easy_button.collidepoint(mouse) else self.DARK)
            )
            medium_color = (
                self.SELECTED
                if self.difficulty == "medium"
                else (self.LIGHT if medium_button.collidepoint(mouse) else self.DARK)
            )
            hard_color = (
                self.SELECTED
                if self.difficulty == "hard"
                else (self.LIGHT if hard_button.collidepoint(mouse) else self.DARK)
            )

            pygame.draw.rect(self.screen, easy_color, easy_button)
            pygame.draw.rect(self.screen, medium_color, medium_button)
            pygame.draw.rect(self.screen, hard_color, hard_button)

            self.screen.blit(easy_text, (360, 190))
            self.screen.blit(medium_text, (330, 280))
            self.screen.blit(hard_text, (365, 370))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos

                    if back_button.collidepoint(click_pos):
                        return None
                    if easy_button.collidepoint(click_pos):
                        return "easy"
                    if medium_button.collidepoint(click_pos):
                        return "medium"
                    if hard_button.collidepoint(click_pos):
                        return "hard"

            pygame.display.update()

    def display_algorithm_choice(self):
        """
        @brief Show available search algorithms and open the configuration screen.

        @return Configuration dictionary, -2 for back, or -1 when quitting.
        """
        game_running = True

        font = pygame.font.SysFont("arial", 32)
        title_font = pygame.font.SysFont("arial", 40)

        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        title_text = title_font.render("ALGORITHMS", True, self.WHITE)

        bfs_button = pygame.Rect(60, 170, 300, 58)
        dfs_button = pygame.Rect(440, 170, 300, 58)
        dfs_limited_button = pygame.Rect(60, 250, 300, 58)
        id_button = pygame.Rect(440, 250, 300, 58)
        greedy_button = pygame.Rect(60, 330, 300, 58)
        a_star_button = pygame.Rect(440, 330, 300, 58)
        weighted_a_star_button = pygame.Rect(60, 410, 300, 58)
        uniform_button = pygame.Rect(440, 410, 300, 58)

        bfs_text = font.render("BFS", True, self.WHITE)
        dfs_text = font.render("DFS", True, self.WHITE)
        dfs_limited_text = font.render("Limited DFS", True, self.WHITE)
        id_text = font.render("Iterative Deepening", True, self.WHITE)
        greedy_text = font.render("Greedy", True, self.WHITE)
        a_star_text = font.render("A*", True, self.WHITE)
        weighted_a_star_text = font.render("Weighted A*", True, self.WHITE)
        uniform_text = font.render("Uniform Cost", True, self.WHITE)

        while game_running:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 38))

            self.screen.blit(title_text, (285, 90))

            for button in [
                bfs_button,
                dfs_button,
                dfs_limited_button,
                id_button,
                greedy_button,
                a_star_button,
                weighted_a_star_button,
                uniform_button,
            ]:
                pygame.draw.rect(
                    self.screen,
                    self.LIGHT if button.collidepoint(mouse) else self.DARK,
                    button,
                )

            self.screen.blit(bfs_text, (175, 182))
            self.screen.blit(dfs_text, (560, 182))
            self.screen.blit(dfs_limited_text, (120, 262))
            self.screen.blit(id_text, (470, 262))
            self.screen.blit(greedy_text, (155, 342))
            self.screen.blit(a_star_text, (575, 342))
            self.screen.blit(weighted_a_star_text, (110, 422))
            self.screen.blit(uniform_text, (500, 422))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos

                    if back_button.collidepoint(click_pos):
                        return -2

                    if bfs_button.collidepoint(click_pos):
                        return self.display_algorithm_config(0)
                    if dfs_button.collidepoint(click_pos):
                        return self.display_algorithm_config(1)
                    if dfs_limited_button.collidepoint(click_pos):
                        return self.display_algorithm_config(2)
                    if id_button.collidepoint(click_pos):
                        return self.display_algorithm_config(3)
                    if greedy_button.collidepoint(click_pos):
                        return self.display_algorithm_config(4)
                    if a_star_button.collidepoint(click_pos):
                        return self.display_algorithm_config(5)
                    if weighted_a_star_button.collidepoint(click_pos):
                        return self.display_algorithm_config(6)
                    if uniform_button.collidepoint(click_pos):
                        return self.display_algorithm_config(7)

            pygame.display.update()

    def display_algorithm_config(self, strategy):
        """
        @brief Configure parameters for the selected search strategy.

        @param strategy Numeric identifier of the selected algorithm.
        @return Configuration dictionary, -2 for back, or -1 when quitting.
        """
        font = pygame.font.SysFont("arial", 28)
        title_font = pygame.font.SysFont("arial", 36)
        small_font = pygame.font.SysFont("arial", 20)

        back_button = pygame.Rect(30, 30, 85, 50)
        confirm_button = pygame.Rect(275, 520, 250, 50)

        back_text = font.render("Back", True, self.WHITE)
        confirm_text = font.render("Run", True, self.WHITE)

        strategy_names = {
            0: "BFS",
            1: "DFS",
            2: "Limited DFS",
            3: "Iterative Deepening",
            4: "Greedy",
            5: "A*",
            6: "Weighted A*",
            7: "Uniform Cost",
        }

        heuristic_names = ["misplaced", "breakpoints", "distance", "pdb"]
        heuristic_index = 0

        depth_limit = 20
        weight = 1.5
        max_cost = 50

        uses_heuristic = strategy in [4, 5, 6]
        uses_depth = strategy in [1, 2, 3]
        uses_weight = strategy == 6

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            title = title_font.render("Algorithm Config", True, self.WHITE)
            algo_text = font.render(
                f"Algorithm: {strategy_names[strategy]}", True, self.WHITE
            )

            self.screen.blit(title, (240, 70))
            self.screen.blit(algo_text, (170, 145))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 38))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if confirm_button.collidepoint(mouse) else self.DARK,
                confirm_button,
            )
            self.screen.blit(confirm_text, (360, 528))

            y = 220

            heuristic_minus = heuristic_plus = None
            depth_minus = depth_plus = None
            weight_minus = weight_plus = None
            cost_minus = cost_plus = None

            if uses_heuristic:
                h_label = font.render(
                    f"Heuristic: {heuristic_names[heuristic_index]}",
                    True,
                    self.WHITE,
                )
                self.screen.blit(h_label, (160, y))

                heuristic_minus = pygame.Rect(600, y, 40, 35)
                heuristic_plus = pygame.Rect(650, y, 40, 35)

                pygame.draw.rect(self.screen, self.DARK, heuristic_minus)
                pygame.draw.rect(self.screen, self.DARK, heuristic_plus)
                self.screen.blit(font.render("-", True, self.WHITE), (613, y - 2))
                self.screen.blit(font.render("+", True, self.WHITE), (661, y - 2))
                y += 70

            if uses_depth:
                d_label = font.render(f"Depth limit: {depth_limit}", True, self.WHITE)
                self.screen.blit(d_label, (160, y))

                depth_minus = pygame.Rect(600, y, 40, 35)
                depth_plus = pygame.Rect(650, y, 40, 35)

                pygame.draw.rect(self.screen, self.DARK, depth_minus)
                pygame.draw.rect(self.screen, self.DARK, depth_plus)
                self.screen.blit(font.render("-", True, self.WHITE), (613, y - 2))
                self.screen.blit(font.render("+", True, self.WHITE), (661, y - 2))
                y += 70

            if uses_weight:
                w_label = font.render(f"Weight: {weight:.1f}", True, self.WHITE)
                self.screen.blit(w_label, (160, y))

                weight_minus = pygame.Rect(600, y, 40, 35)
                weight_plus = pygame.Rect(650, y, 40, 35)

                pygame.draw.rect(self.screen, self.DARK, weight_minus)
                pygame.draw.rect(self.screen, self.DARK, weight_plus)
                self.screen.blit(font.render("-", True, self.WHITE), (613, y - 2))
                self.screen.blit(font.render("+", True, self.WHITE), (661, y - 2))
                y += 70

            c_label = font.render(f"Max cost: {max_cost}", True, self.WHITE)
            self.screen.blit(c_label, (160, y))

            cost_minus = pygame.Rect(600, y, 40, 35)
            cost_plus = pygame.Rect(650, y, 40, 35)

            pygame.draw.rect(self.screen, self.DARK, cost_minus)
            pygame.draw.rect(self.screen, self.DARK, cost_plus)
            self.screen.blit(font.render("-", True, self.WHITE), (613, y - 2))
            self.screen.blit(font.render("+", True, self.WHITE), (661, y - 2))

            help_text = small_font.render(
                "Choose parameters, then click Run.",
                True,
                self.WHITE,
            )
            self.screen.blit(help_text, (240, 485))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos

                    if back_button.collidepoint(click_pos):
                        return -2

                    if confirm_button.collidepoint(click_pos):
                        solver = Solver()
                        heuristic_func = None
                        if uses_heuristic:
                            heuristic_func = solver.get_heuristic_by_name(
                                heuristic_names[heuristic_index]
                            )

                        return {
                            "strategy": strategy,
                            "depth_limit": depth_limit,
                            "max_cost": max_cost,
                            "weight": weight,
                            "heuristic_func": heuristic_func,
                        }

                    if heuristic_minus and heuristic_minus.collidepoint(click_pos):
                        heuristic_index = (heuristic_index - 1) % len(heuristic_names)
                    if heuristic_plus and heuristic_plus.collidepoint(click_pos):
                        heuristic_index = (heuristic_index + 1) % len(heuristic_names)

                    if depth_minus and depth_minus.collidepoint(click_pos):
                        depth_limit = max(1, depth_limit - 1)
                    if depth_plus and depth_plus.collidepoint(click_pos):
                        depth_limit += 1

                    if weight_minus and weight_minus.collidepoint(click_pos):
                        weight = max(1.0, round(weight - 0.1, 1))
                    if weight_plus and weight_plus.collidepoint(click_pos):
                        weight = round(weight + 0.1, 1)

                    if cost_minus and cost_minus.collidepoint(click_pos):
                        max_cost = max(1, max_cost - 1)
                    if cost_plus and cost_plus.collidepoint(click_pos):
                        max_cost += 1

            pygame.display.update()

    def display_algo_result(self, game: Game, path, stats, solver):
        """
        @brief Display algorithm execution metrics and optional step-by-step animation.

        @param game Game instance used to render the replay.
        @param path Sequence of states/moves returned by the solver.
        @param stats Dictionary with execution metrics.
        @param solver Solver instance used to animate the path.
        @return -1 when quitting; otherwise returns to the previous menu.
        """
        og_game = copy.deepcopy(game)

        font = pygame.font.SysFont("arial", 28)
        title_font = pygame.font.SysFont("arial", 40)
        small_font = pygame.font.SysFont("arial", 22)

        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        step_button = pygame.Rect(240, 500, 320, 50)
        step_text = font.render("Show Step by Step", True, self.WHITE)

        speed_options = [("Slow", 2.0), ("Normal", 1.0), ("Fast", 0.3)]
        speed_buttons = [
            pygame.Rect(220 + i * 120, 440, 100, 38) for i in range(len(speed_options))
        ]
        speed_texts = [
            small_font.render(label, True, self.WHITE) for label, _ in speed_options
        ]
        selected_speed = 1

        if stats["found"]:
            labels = [
                "Solution found!",
                f"Nodes explored: {stats['nodes']}",
                f"Solution depth: {stats['depth']}",
                f"Time: {stats['time']:.3f}s",
            ]
        else:
            labels = [
                "No solution found.",
                f"Nodes explored: {stats['nodes']}",
                f"Time: {stats['time']:.3f}s",
            ]

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            title = title_font.render("Algorithm Result", True, self.WHITE)
            self.screen.blit(title, (230, 90))

            for i, label in enumerate(labels):
                text = font.render(label, True, self.WHITE)
                self.screen.blit(text, (210, 180 + i * 50))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 38))

            if stats["found"] and path:
                speed_label = small_font.render("Speed:", True, self.WHITE)
                self.screen.blit(speed_label, (150, 448))
                for i, (btn, txt) in enumerate(zip(speed_buttons, speed_texts)):
                    color = (
                        self.SELECTED
                        if i == selected_speed
                        else (self.LIGHT if btn.collidepoint(mouse) else self.DARK)
                    )
                    pygame.draw.rect(self.screen, color, btn)
                    self.screen.blit(txt, (btn.x + 14, btn.y + 8))

                pygame.draw.rect(
                    self.screen,
                    self.LIGHT if step_button.collidepoint(mouse) else self.DARK,
                    step_button,
                )
                self.screen.blit(step_text, (275, 508))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos
                    if back_button.collidepoint(click_pos):
                        return
                    if stats["found"] and path:
                        for i, btn in enumerate(speed_buttons):
                            if btn.collidepoint(click_pos):
                                selected_speed = i
                        if step_button.collidepoint(click_pos):
                            _, delay = speed_options[selected_speed]
                            self.screen.fill(self.BG)
                            solver.animate_path(game, self.screen, path, delay=delay)
                            game = copy.deepcopy(og_game)

            pygame.display.update()

    def display_win(self, game=None):
        """
        @brief Show the win screen with shortcuts to stats and leaderboard.

        @param game Optional game instance used to show final stats.
        @return -1 when quitting; otherwise returns after continue.
        """
        font = pygame.font.SysFont("arial", 40)
        win_text = font.render("YOU WIN!", True, self.WHITE)

        stats_button = pygame.Rect(250, 240, 300, 50)
        stats_text = font.render("Stats", True, self.WHITE)
        leaderboard_button = pygame.Rect(250, 320, 300, 50)
        leaderboard_text = font.render("Leaderboard", True, self.WHITE)
        continue_button = pygame.Rect(250, 400, 300, 50)
        continue_text = font.render("Continue", True, self.WHITE)

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            self.screen.blit(win_text, (285, 140))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if stats_button.collidepoint(mouse) else self.DARK,
                stats_button,
            )
            self.screen.blit(stats_text, (360, 247))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if leaderboard_button.collidepoint(mouse) else self.DARK,
                leaderboard_button,
            )
            self.screen.blit(leaderboard_text, (285, 327))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if continue_button.collidepoint(mouse) else self.DARK,
                continue_button,
            )
            self.screen.blit(continue_text, (310, 407))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos
                    if stats_button.collidepoint(click_pos) and game is not None:
                        if self.display_stats(game) == -1:
                            return -1
                    elif leaderboard_button.collidepoint(click_pos):
                        if self.display_leaderboard() == -1:
                            return -1
                    elif continue_button.collidepoint(click_pos):
                        return

            pygame.display.update()

    def display_leaderboard(self):
        """
        @brief Render the leaderboard screen with best results.

        @return -1 when quitting; otherwise returns to the previous menu.
        """
        font = pygame.font.SysFont("arial", 28)
        title_font = pygame.font.SysFont("arial", 40)
        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            title = title_font.render("Leaderboard", True, self.WHITE)
            self.screen.blit(title, (255, 60))

            entries = self.leaderboard.get_entries()

            header = font.render("#    Moves    Time (s)", True, (200, 200, 200))
            self.screen.blit(header, (225, 130))
            pygame.draw.line(self.screen, (200, 200, 200), (220, 165), (580, 165), 1)

            if entries:
                for i, entry in enumerate(entries):
                    gold = i == 0
                    color = (255, 215, 0) if gold else self.WHITE
                    row = font.render(
                        f"{i + 1:<5}{entry['moves']:<10}{entry['time']:.2f}",
                        True,
                        color,
                    )
                    self.screen.blit(row, (225, 180 + i * 35))
            else:
                empty = font.render(
                    "No scores yet — play a game!", True, (170, 170, 170)
                )
                self.screen.blit(empty, (190, 230))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 38))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.MOUSEBUTTONUP:
                    if back_button.collidepoint(event.pos):
                        return

            pygame.display.update()

    def display_stats(self, game):
        """
        @brief Show current game statistics and timing information.

        @param game Game instance that owns the statistics object.
        @return -1 when quitting; otherwise returns to the previous menu.
        """
        font = pygame.font.SysFont("arial", 28)
        title_font = pygame.font.SysFont("arial", 36)
        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        stats = game._game_stats

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            labels = [
                f"Moves: {stats.moves}",
                f"Hints used: {stats.hints_used}",
                f"Time: {game.get_game_time():.2f}s",
                f"States explored: {stats.states_explored}",
                f"Solution depth: {stats.solution_depth}",
                f"Max memory: {stats.max_memory}",
            ]

            title = title_font.render("Game Stats", True, self.WHITE)
            self.screen.blit(title, (300, 100))

            for i, label in enumerate(labels):
                text = font.render(label, True, self.WHITE)
                self.screen.blit(text, (210, 170 + i * 50))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 38))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.MOUSEBUTTONUP:
                    if back_button.collidepoint(event.pos):
                        return

            pygame.display.update()

    def display_lose(self):
        """
        @brief Show the lose screen and ask whether to retry or go back.

        @return 0 to retry, 1 to return to menu, or -1 when quitting.
        """
        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            font = pygame.font.SysFont("arial", 40)
            lose_text = font.render("LOSS", True, self.WHITE)
            self.screen.blit(lose_text, (340, 180))

            retry_button = pygame.Rect(250, 280, 300, 50)
            menu_button = pygame.Rect(250, 360, 300, 50)

            pygame.draw.rect(
                self.screen,
                self.LIGHT if retry_button.collidepoint(mouse) else self.DARK,
                retry_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if menu_button.collidepoint(mouse) else self.DARK,
                menu_button,
            )
            retry_text = font.render("Retry", True, self.WHITE)
            menu_text = font.render("Back to menu", True, self.WHITE)

            self.screen.blit(retry_text, (345, 287))
            self.screen.blit(menu_text, (260, 367))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos
                    if retry_button.collidepoint(click_pos):
                        return 0
                    if menu_button.collidepoint(click_pos):
                        return 1

            pygame.display.update()

    def display_choose_file_menu(self, game: Game):
        """
        @brief Show file input UI and load an instance from the instances folder.

        @param game Game instance where the loaded state will be applied.
        @return -1 when quitting; otherwise returns after success/back.
        """
        font = pygame.font.SysFont("arial", 38)
        font_small = pygame.font.SysFont("arial", 20)

        text_box = pygame.Rect(100, 280, 600, 50)
        i_string = ""
        max_size = 26

        shift = False

        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        confirm_button = pygame.Rect(275, 420, 250, 50)
        confirm_text = font.render("Confirm", True, self.WHITE)

        explain_text = font.render("Input the file name:", True, self.WHITE)
        extra_text = font_small.render(
            "Exclude the file extension (.txt)", True, self.WHITE
        )
        error_text = None

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            self.screen.blit(explain_text, (220, 150))
            self.screen.blit(extra_text, (255, 200))

            pygame.draw.rect(self.screen, self.WHITE, text_box)
            rendered_text = i_string
            if len(i_string) > max_size:
                rendered_text = i_string[len(i_string) - max_size :]
            i_text = font.render(rendered_text, True, self.DARK)
            self.screen.blit(i_text, (110, 285))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 35))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if confirm_button.collidepoint(mouse) else self.DARK,
                confirm_button,
            )
            self.screen.blit(confirm_text, (325, 425))

            if error_text is not None:
                self.screen.blit(error_text, (165, 360))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = event.pos
                    if back_button.collidepoint(click_pos):
                        return
                    elif confirm_button.collidepoint(click_pos):
                        try:
                            state, _, _ = FileManager.load_instance(i_string)
                            game.set_board_state(state)
                            return
                        except Exception:
                            error_text = font_small.render(
                                "Could not load that file.", True, (255, 180, 180)
                            )

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        i_string = i_string[:-1]
                    elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        shift = True
                    elif event.key == pygame.K_RETURN:
                        try:
                            state, _, _ = FileManager.load_instance(i_string)
                            game.set_board_state(state)
                            return
                        except Exception:
                            error_text = font_small.render(
                                "Could not load that file.", True, (255, 180, 180)
                            )
                    elif len(i_string) < 64:
                        if shift:
                            if event.key == pygame.K_MINUS:
                                i_string += "_"
                            else:
                                i_string += pygame.key.name(event.key).upper()
                        else:
                            key_name = pygame.key.name(event.key)
                            if len(key_name) == 1 or key_name in ["_", "-"]:
                                i_string += key_name

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        shift = False

            pygame.display.update()
