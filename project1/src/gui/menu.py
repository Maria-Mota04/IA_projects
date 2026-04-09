import pygame
from src.game.solver import Solver
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState
import time


class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.WHITE = (255, 255, 255)
        self.LIGHT = (170, 170, 170)
        self.DARK = (100, 100, 100)
        self.BG = (60, 25, 60)

    def run(self):
        n = 20
        game_running = True
        font = pygame.font.SysFont("arial", 40)

        board = Board(
            [1, 2, 3, 7, 6, 5, 4, 8, 9, 10, 14, 13, 12, 11, 15, 16, 17, 18, 19, 20]
        )
        board.shuffle_board()
        state = GameState(board)
        game = Game(state)

        solver = Solver()
        try_again = False

        play_button = pygame.Rect(300, 300, 140, 50)
        ia_button = pygame.Rect(300, 380, 140, 50)
        quit_button = pygame.Rect(300, 460, 140, 50)

        play_text = font.render("Play", True, self.WHITE)
        ia_text = font.render("Algorithms", True, self.WHITE)
        quit_text = font.render("Quit", True, self.WHITE)

        loading_text = font.render("Loading...", True, self.WHITE)

        while game_running:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            pygame.draw.rect(
                self.screen,
                self.LIGHT if play_button.collidepoint(mouse) else self.DARK,
                play_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if ia_button.collidepoint(mouse) else self.DARK,
                ia_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if quit_button.collidepoint(mouse) else self.DARK,
                quit_button,
            )

            self.screen.blit(play_text, (335, 305))
            self.screen.blit(ia_text, (335, 385))
            self.screen.blit(quit_text, (335, 465))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_running = False

                if event.type == pygame.MOUSEBUTTONUP or try_again:

                    if play_button.collidepoint(mouse) or try_again:
                        try_again = False
                        self.screen.fill(self.BG)
                        ret = solver.solve(game=game, screen=self.screen, mode=2)

                        # won
                        if ret == 0:
                            # give it a time so the player can see his final play
                            time.sleep(0.5)
                            self.display_win(game)

                        # pressed x
                        elif ret == -1:
                            game_running = False

                        # pressed quit button
                        else:
                            ret1 = self.display_lose()

                            # they want to retry the level
                            if ret1 == 0:
                                board.reset_board()
                                game.set_board_state(GameState(board))
                                try_again = True
                                pygame.event.post(pygame.event.Event(1))
                                continue

                            # pressed x
                            if ret1 == -1:
                                game_running = False

                        # make a new board, for next try
                        board.shuffle_board()
                        state = GameState(board)
                        game = Game(state)

                    if ia_button.collidepoint(mouse):
                        ret = self.display_algorithm_choice()

                        # pressed x
                        if ret == -1:
                            game_running = False

                        # pressed go back
                        elif ret == -2:
                            continue

                        # chose an algorithm
                        else:
                            algo_board = Board(list(range(1, 21)))
                            algo_board.shuffle_few_moves(4)
                            algo_game = Game(GameState(algo_board))

                            self.screen.fill(self.BG)
                            self.screen.blit(loading_text, (335, 305))
                            pygame.display.update()

                            path, stats = solver.solve(
                                game=algo_game, screen=self.screen, mode=1, strategy=ret
                            )

                            self.display_algo_result(algo_game, path, stats, solver)

                            board.shuffle_board()
                            state = GameState(board)
                            game = Game(state)

                    if quit_button.collidepoint(mouse):
                        game_running = False

            pygame.display.update()

    def display_algorithm_choice(self):
        game_running = True

        font = pygame.font.SysFont("arial", 40)

        # back button
        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, (255, 255, 255))

        # title
        title_text = font.render("ALGORITHMS", True, self.WHITE)

        # button background
        bfs_button = pygame.Rect(76, 200, 285, 58)
        dfs_button = pygame.Rect(437, 200, 285, 58)
        dfs_limited_button = pygame.Rect(76, 287, 285, 58)
        id_button = pygame.Rect(437, 287, 285, 58)
        greedy_button = pygame.Rect(76, 374, 285, 58)
        a_star_button = pygame.Rect(437, 374, 285, 58)
        weighted_a_star_button = pygame.Rect(76, 461, 285, 58)
        uniform_button = pygame.Rect(437, 461, 285, 58)

        # button text
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
                (170, 170, 170) if back_button.collidepoint(mouse) else (100, 100, 100),
                back_button,
            )
            self.screen.blit(back_text, (35, 32))

            self.screen.blit(title_text, (335, 100))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if bfs_button.collidepoint(mouse) else self.DARK,
                bfs_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if dfs_button.collidepoint(mouse) else self.DARK,
                dfs_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if dfs_limited_button.collidepoint(mouse) else self.DARK,
                dfs_limited_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if id_button.collidepoint(mouse) else self.DARK,
                id_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if greedy_button.collidepoint(mouse) else self.DARK,
                greedy_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if a_star_button.collidepoint(mouse) else self.DARK,
                a_star_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if weighted_a_star_button.collidepoint(mouse) else self.DARK,
                weighted_a_star_button,
            )
            pygame.draw.rect(
                self.screen,
                self.LIGHT if uniform_button.collidepoint(mouse) else self.DARK,
                uniform_button,
            )

            self.screen.blit(bfs_text, (94, 204))
            self.screen.blit(dfs_text, (500, 204))
            self.screen.blit(dfs_limited_text, (80, 291))
            self.screen.blit(id_text, (440, 291))
            self.screen.blit(greedy_text, (84, 378))
            self.screen.blit(a_star_text, (500, 378))
            self.screen.blit(weighted_a_star_text, (84, 465))
            self.screen.blit(uniform_text, (500, 465))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:

                    if back_button.collidepoint(mouse):
                        return -2

                    if bfs_button.collidepoint(mouse):
                        return 0

                    if dfs_button.collidepoint(mouse):
                        return 1

                    if dfs_limited_button.collidepoint(mouse):
                        return 2

                    if id_button.collidepoint(mouse):
                        return 3

                    if greedy_button.collidepoint(mouse):
                        return 4

                    if a_star_button.collidepoint(mouse):
                        return 5

                    if weighted_a_star_button.collidepoint(mouse):
                        return 6

                    if uniform_button.collidepoint(mouse):
                        return 7

            pygame.display.update()

    def display_algo_result(self, game, path, stats, solver):
        font = pygame.font.SysFont("arial", 30)
        title_font = pygame.font.SysFont("arial", 40)

        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        step_button = pygame.Rect(270, 460, 250, 50)
        step_text = font.render("Show Step by Step", True, self.WHITE)

        if stats["found"]:
            labels = [
                f"Solution found!",
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
            self.screen.blit(title, (220, 100))

            for i, label in enumerate(labels):
                text = font.render(label, True, self.WHITE)
                self.screen.blit(text, (240, 180 + i * 50))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 38))

            if stats["found"] and path:
                pygame.draw.rect(
                    self.screen,
                    self.LIGHT if step_button.collidepoint(mouse) else self.DARK,
                    step_button,
                )
                self.screen.blit(step_text, (278, 467))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONUP:
                    if back_button.collidepoint(mouse):
                        return
                    if stats["found"] and path and step_button.collidepoint(mouse):
                        solver.animate_path(game, self.screen, path)

            pygame.display.update()

    def display_win(self, game=None):
        font = pygame.font.SysFont("arial", 40)
        win_text = font.render("YOU WIN!", True, (255, 255, 255))

        stats_button = pygame.Rect(270, 320, 200, 50)
        stats_text = font.render("Stats", True, self.WHITE)
        continue_button = pygame.Rect(270, 390, 200, 50)
        continue_text = font.render("Continue", True, self.WHITE)

        while True:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            self.screen.blit(win_text, (310, 220))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if stats_button.collidepoint(mouse) else self.DARK,
                stats_button,
            )
            self.screen.blit(stats_text, (340, 327))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if continue_button.collidepoint(mouse) else self.DARK,
                continue_button,
            )
            self.screen.blit(continue_text, (310, 397))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONUP:
                    if stats_button.collidepoint(mouse) and game is not None:
                        self.display_stats(game)
                    elif continue_button.collidepoint(mouse):
                        return

            pygame.display.update()

    def display_stats(self, game):
        font = pygame.font.SysFont("arial", 30)
        back_button = pygame.Rect(30, 30, 85, 50)
        back_text = font.render("Back", True, self.WHITE)

        stats = game._game_stats

        labels = [
            f"Moves: {stats.moves}",
            f"Score: {stats.score}",
            f"Time: {game.get_game_time():.2f}s",
            f"States explored: {stats.states_explored}",
            f"Solution depth: {stats.solution_depth}",
            f"Max memory: {stats.max_memory}",
        ]

        game_running = True
        while game_running:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            title = font.render("=== Game Stats ===", True, self.WHITE)
            self.screen.blit(title, (240, 100))

            for i, label in enumerate(labels):
                text = font.render(label, True, self.WHITE)
                self.screen.blit(text, (240, 160 + i * 45))

            pygame.draw.rect(
                self.screen,
                self.LIGHT if back_button.collidepoint(mouse) else self.DARK,
                back_button,
            )
            self.screen.blit(back_text, (35, 38))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONUP:
                    if back_button.collidepoint(mouse):
                        return

            pygame.display.update()

    def display_lose(self):
        game_running = True

        while game_running:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            font = pygame.font.SysFont("arial", 40)
            win_text = font.render("LOSS", True, self.WHITE)
            self.screen.blit(win_text, (335, 200))

            retry_button = pygame.Rect(300, 300, 140, 50)
            menu_button = pygame.Rect(300, 380, 140, 50)

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

            self.screen.blit(retry_text, (335, 305))
            self.screen.blit(menu_text, (335, 385))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:

                    if retry_button.collidepoint(mouse):
                        return 0

                    if menu_button.collidepoint(mouse):
                        return 1

            pygame.display.update()
