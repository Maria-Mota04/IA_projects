import pygame
from src.algorithms.search_strategy import SearchStrategy


class HintSettings:
    def __init__(self, solver):
        """
        @brief Initialize hint settings UI.

        @param solver Solver instance whose hint configuration is edited.
        """
        self.solver = solver

    def run(self, screen):
        """
        @brief Render and handle the interactive hint settings screen.

        @param screen Pygame surface used for rendering.
        @return 0 on save, -2 on back, or -1 when quitting.
        """
        font = pygame.font.SysFont("arial", 22, bold=True)
        title_font = pygame.font.SysFont("arial", 32, bold=True)
        small_font = pygame.font.SysFont("arial", 16, bold=True)
        value_font = pygame.font.SysFont("arial", 18, bold=True)

        WHITE = (245, 245, 245)
        BG = (30, 15, 30)
        PANEL = (50, 25, 50)
        PANEL_2 = (40, 20, 40)
        SELECTED = (160, 80, 160)
        HOVER = (90, 50, 90)
        BORDER = (200, 160, 200)
        DARK_BTN = (60, 35, 60)

        screen_w, _ = 800, 600

        def draw_button(
            rect,
            text,
            selected=False,
            hovered=False,
            text_font=None,
            special=False,
        ):
            """
            @brief Draw a styled button with optional selected and hover states.
            """
            if text_font is None:
                text_font = small_font

            shadow = rect.copy()
            shadow.y += 2
            pygame.draw.rect(screen, (15, 5, 15), shadow, border_radius=10)

            color = (
                (40, 140, 80)
                if (special and hovered)
                else (
                    (30, 110, 60)
                    if special
                    else (SELECTED if selected else (HOVER if hovered else DARK_BTN))
                )
            )

            pygame.draw.rect(screen, color, rect, border_radius=10)

            border_color = (
                WHITE if selected else (BORDER if hovered else (100, 70, 100))
            )
            pygame.draw.rect(screen, border_color, rect, width=2, border_radius=10)

            txt = text_font.render(text, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))

        def draw_panel(rect, title):
            """
            @brief Draw a labeled panel container.
            """
            pygame.draw.rect(screen, PANEL, rect, border_radius=12)
            pygame.draw.rect(screen, BORDER, rect, width=1, border_radius=12)

            title_surf = font.render(title, True, BORDER)
            screen.blit(title_surf, (rect.x + 15, rect.y + 8))

        def draw_value_selector(y, label, value_text, mouse_pos):
            """
            @brief Draw a numeric selector with minus and plus controls.

            @return Tuple with minus and plus button rectangles.
            """
            label_surf = small_font.render(label, True, WHITE)
            screen.blit(label_surf, (160, y + 8))

            value_box = pygame.Rect(320, y, 160, 32)
            pygame.draw.rect(screen, PANEL_2, value_box, border_radius=8)
            pygame.draw.rect(screen, BORDER, value_box, width=1, border_radius=8)

            value_surf = value_font.render(value_text, True, WHITE)
            screen.blit(value_surf, value_surf.get_rect(center=value_box.center))

            minus_rect = pygame.Rect(275, y, 32, 32)
            plus_rect = pygame.Rect(495, y, 32, 32)

            for rect, symbol in [(minus_rect, "-"), (plus_rect, "+")]:
                is_hovered = rect.collidepoint(mouse_pos)
                pygame.draw.circle(
                    screen,
                    HOVER if is_hovered else DARK_BTN,
                    rect.center,
                    16,
                )
                pygame.draw.circle(screen, BORDER, rect.center, 16, width=1)

                txt = value_font.render(symbol, True, WHITE)
                screen.blit(txt, txt.get_rect(center=rect.center))

            return minus_rect, plus_rect

        back_button = pygame.Rect(20, 15, 70, 30)
        confirm_button = pygame.Rect(300, 545, 200, 40)

        algo_panel = pygame.Rect(40, 65, 720, 190)
        heur_panel = pygame.Rect(40, 265, 720, 90)
        config_panel = pygame.Rect(40, 365, 720, 165)

        algo_buttons = [
            (pygame.Rect(65, 105, 300, 32), "BFS", SearchStrategy.BFS),
            (pygame.Rect(435, 105, 300, 32), "DFS", SearchStrategy.DFS),
            (pygame.Rect(65, 142, 300, 32), "Limited DFS", SearchStrategy.DFS_LIMITED),
            (
                pygame.Rect(435, 142, 300, 32),
                "Iterative Deepening",
                SearchStrategy.ITERATIVE_DEEPENING,
            ),
            (
                pygame.Rect(65, 179, 300, 32),
                "Uniform Cost",
                SearchStrategy.UNIFORM_COST,
            ),
            (pygame.Rect(435, 179, 300, 32), "Greedy", SearchStrategy.GREEDY),
            (pygame.Rect(65, 216, 300, 32), "A*", SearchStrategy.A_STAR),
            (
                pygame.Rect(435, 216, 300, 32),
                "Weighted A*",
                SearchStrategy.WEIGHTED_A_STAR,
            ),
        ]

        heur_buttons = [
            (pygame.Rect(70, 305, 150, 32), "Misplaced", "misplaced"),
            (pygame.Rect(245, 305, 150, 32), "Breakpoints", "breakpoints"),
            (pygame.Rect(420, 305, 150, 32), "Distance", "distance"),
        ]

        if self.solver.has_pdb():
            heur_buttons.append((pygame.Rect(595, 305, 100, 32), "PDB", "pdb"))

        selected_strategy = self.solver._hint_strategy
        selected_heuristic_name = self.solver._hint_heuristic_name
        selected_depth_limit = self.solver._hint_config["depth_limit"]
        selected_max_cost = self.solver._hint_config["max_cost"]
        selected_weight = self.solver._hint_config["weight"]

        while True:
            screen.fill(BG)
            mouse_pos = pygame.mouse.get_pos()

            show_heuristics = self.solver.strategy_uses_heuristic(selected_strategy)
            show_depth = self.solver.strategy_uses_depth_limit(selected_strategy)
            show_weight = self.solver.strategy_uses_weight(selected_strategy)

            title = title_font.render("HINT SETTINGS", True, WHITE)
            screen.blit(title, title.get_rect(center=(screen_w // 2, 35)))

            draw_button(
                back_button, "BACK", hovered=back_button.collidepoint(mouse_pos)
            )

            draw_panel(algo_panel, "ALGORITHM")
            for button, label, strategy in algo_buttons:
                draw_button(
                    button,
                    label,
                    selected=(strategy == selected_strategy),
                    hovered=button.collidepoint(mouse_pos),
                )

            draw_panel(
                heur_panel,
                "HEURISTIC" if show_heuristics else "NO HEURISTIC NEEDED",
            )
            if show_heuristics:
                for button, label, heuristic_name in heur_buttons:
                    draw_button(
                        button,
                        label,
                        selected=(heuristic_name == selected_heuristic_name),
                        hovered=button.collidepoint(mouse_pos),
                    )

            draw_panel(config_panel, "PARAMETERS")

            current_y = 405
            d_minus = d_plus = None
            w_minus = w_plus = None
            c_minus = c_plus = None

            if show_depth:
                d_minus, d_plus = draw_value_selector(
                    current_y,
                    "Depth limit",
                    str(selected_depth_limit),
                    mouse_pos,
                )
                current_y += 40

            if show_weight:
                w_minus, w_plus = draw_value_selector(
                    current_y,
                    "Weight",
                    f"{selected_weight:.1f}",
                    mouse_pos,
                )
                current_y += 40

            c_minus, c_plus = draw_value_selector(
                current_y,
                "Max cost",
                "None" if selected_max_cost is None else str(selected_max_cost),
                mouse_pos,
            )

            draw_button(
                confirm_button,
                "SAVE CHANGES",
                hovered=confirm_button.collidepoint(mouse_pos),
                text_font=font,
                special=True,
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos

                    if back_button.collidepoint(click_pos):
                        return -2

                    for button, _, strategy in algo_buttons:
                        if button.collidepoint(click_pos):
                            selected_strategy = strategy

                    if show_heuristics:
                        for button, _, heuristic_name in heur_buttons:
                            if button.collidepoint(click_pos):
                                selected_heuristic_name = heuristic_name

                    if d_minus and d_minus.collidepoint(click_pos):
                        selected_depth_limit = max(1, selected_depth_limit - 1)

                    if d_plus and d_plus.collidepoint(click_pos):
                        selected_depth_limit += 1

                    if w_minus and w_minus.collidepoint(click_pos):
                        selected_weight = max(0.1, round(selected_weight - 0.1, 1))

                    if w_plus and w_plus.collidepoint(click_pos):
                        selected_weight = round(selected_weight + 0.1, 1)

                    if c_minus and c_minus.collidepoint(click_pos):
                        if selected_max_cost is None:
                            pass
                        elif selected_max_cost <= 1:
                            selected_max_cost = None
                        else:
                            selected_max_cost -= 1

                    if c_plus and c_plus.collidepoint(click_pos):
                        if selected_max_cost is None:
                            selected_max_cost = 1
                        else:
                            selected_max_cost += 1

                    if confirm_button.collidepoint(click_pos):
                        self.solver._hint_strategy = selected_strategy
                        self.solver._hint_heuristic_name = selected_heuristic_name
                        self.solver._hint_config.update(
                            {
                                "depth_limit": selected_depth_limit,
                                "max_cost": selected_max_cost,
                                "weight": selected_weight,
                            }
                        )
                        return 0

            pygame.display.update()
