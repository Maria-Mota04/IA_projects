import pygame
from src.algorithms.search_strategy import SearchStrategy

class HintSettings:
    def __init__(self, solver):
        self.solver = solver

    def run(self, screen):
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

        screen_w, screen_h = 800, 600

        def draw_button(rect, text, selected=False, hovered=False, text_font=None, special=False):
            if text_font is None: text_font = small_font
            shadow = rect.copy()
            shadow.y += 2
            pygame.draw.rect(screen, (15, 5, 15), shadow, border_radius=10)
            color = (40, 140, 80) if (special and hovered) else ((30, 110, 60) if special else (SELECTED if selected else (HOVER if hovered else DARK_BTN)))
            pygame.draw.rect(screen, color, rect, border_radius=10)
            b_color = WHITE if selected else (BORDER if hovered else (100, 70, 100))
            pygame.draw.rect(screen, b_color, rect, width=2, border_radius=10)
            txt = text_font.render(text, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))

        def draw_panel(rect, title):
            pygame.draw.rect(screen, PANEL, rect, border_radius=12)
            pygame.draw.rect(screen, BORDER, rect, width=1, border_radius=12)
            title_surf = font.render(title, True, BORDER)
            screen.blit(title_surf, (rect.x + 15, rect.y + 8))

        def draw_value_selector(y, label, value_text, mouse):
            label_surf = small_font.render(label, True, WHITE)
            screen.blit(label_surf, (160, y + 8))
            value_box = pygame.Rect(320, y, 160, 32)
            pygame.draw.rect(screen, PANEL_2, value_box, border_radius=8)
            pygame.draw.rect(screen, BORDER, value_box, width=1, border_radius=8)
            value_surf = value_font.render(value_text, True, WHITE)
            screen.blit(value_surf, value_surf.get_rect(center=value_box.center))
            
            m_rect = pygame.Rect(275, y, 32, 32)
            p_rect = pygame.Rect(495, y, 32, 32)
            
            for r, t in [(m_rect, "-"), (p_rect, "+")]:
                is_hov = r.collidepoint(mouse)
                pygame.draw.circle(screen, HOVER if is_hov else DARK_BTN, r.center, 16)
                pygame.draw.circle(screen, BORDER, r.center, 16, width=1)
                txt = value_font.render(t, True, WHITE)
                screen.blit(txt, txt.get_rect(center=r.center))
            return m_rect, p_rect

        back_button = pygame.Rect(20, 15, 70, 30)
        confirm_button = pygame.Rect(300, 545, 200, 40)
        algo_panel = pygame.Rect(40, 65, 720, 190)
        heur_panel = pygame.Rect(40, 265, 720, 90)
        config_panel = pygame.Rect(40, 365, 720, 165)

        algo_buttons = [
            (pygame.Rect(65, 105, 300, 32), "BFS", SearchStrategy.BFS),
            (pygame.Rect(435, 105, 300, 32), "DFS", SearchStrategy.DFS),
            (pygame.Rect(65, 142, 300, 32), "Limited DFS", SearchStrategy.DFS_LIMITED),
            (pygame.Rect(435, 142, 300, 32), "Iterative Deepening", SearchStrategy.ITERATIVE_DEEPENING),
            (pygame.Rect(65, 179, 300, 32), "Uniform Cost", SearchStrategy.UNIFORM_COST),
            (pygame.Rect(435, 179, 300, 32), "Greedy", SearchStrategy.GREEDY),
            (pygame.Rect(65, 216, 300, 32), "A*", SearchStrategy.A_STAR),
            (pygame.Rect(435, 216, 300, 32), "Weighted A*", SearchStrategy.WEIGHTED_A_STAR),
        ]

        heur_buttons = [
            (pygame.Rect(70, 305, 150, 32), "Misplaced", "misplaced"),
            (pygame.Rect(245, 305, 150, 32), "Breakpoints", "breakpoints"),
            (pygame.Rect(420, 305, 150, 32), "Distance", "distance"),
        ]
        if self.solver.has_pdb(): heur_buttons.append((pygame.Rect(595, 305, 100, 32), "PDB", "pdb"))

        selected_strategy = self.solver._hint_strategy
        selected_heuristic_name = self.solver._hint_heuristic_name
        selected_depth_limit = self.solver._hint_config["depth_limit"]
        selected_max_cost = self.solver._hint_config["max_cost"]
        selected_weight = self.solver._hint_config["weight"]
        max_cost_options = [None, 10, 20, 50, 100]

        while True:
            screen.fill(BG)
            mouse = pygame.mouse.get_pos()
            show_heuristics = self.solver.strategy_uses_heuristic(selected_strategy)
            show_depth = self.solver.strategy_uses_depth_limit(selected_strategy)
            show_weight = self.solver.strategy_uses_weight(selected_strategy)

            title = title_font.render("HINT SETTINGS", True, WHITE)
            screen.blit(title, title.get_rect(center=(screen_w // 2, 35)))
            draw_button(back_button, "BACK", hovered=back_button.collidepoint(mouse))

            draw_panel(algo_panel, "ALGORITHM")
            for btn, lbl, strat in algo_buttons:
                draw_button(btn, lbl, strat == selected_strategy, btn.collidepoint(mouse))

            draw_panel(heur_panel, "HEURISTIC" if show_heuristics else "NO HEURISTIC NEEDED")
            if show_heuristics:
                for btn, lbl, h_name in heur_buttons:
                    draw_button(btn, lbl, h_name == selected_heuristic_name, btn.collidepoint(mouse))

            draw_panel(config_panel, "PARAMETERS")
            curr_y = 405
            d_m, d_p, w_m, w_p, c_m, c_p = [None]*6
            
            if show_depth:
                d_m, d_p = draw_value_selector(curr_y, "Depth limit", str(selected_depth_limit), mouse)
                curr_y += 40
            if show_weight:
                w_m, w_p = draw_value_selector(curr_y, "Weight", f"{selected_weight:.1f}", mouse)
                curr_y += 40
            c_m, c_p = draw_value_selector(curr_y, "Max cost", str(selected_max_cost or "None"), mouse)

            draw_button(confirm_button, "SAVE CHANGES", hovered=confirm_button.collidepoint(mouse), text_font=font, special=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return -1
                if event.type == pygame.MOUSEBUTTONUP:
                    if back_button.collidepoint(mouse): return -2
                    for btn, _, strat in algo_buttons:
                        if btn.collidepoint(mouse): selected_strategy = strat
                    if show_heuristics:
                        for btn, _, h_name in heur_buttons:
                            if btn.collidepoint(mouse): selected_heuristic_name = h_name
                    
                    if d_m and d_m.collidepoint(mouse): selected_depth_limit = max(1, selected_depth_limit - 1)
                    if d_p and d_p.collidepoint(mouse): selected_depth_limit += 1
                    if w_m and w_m.collidepoint(mouse): selected_weight = max(0.1, round(selected_weight - 0.1, 1))
                    if w_p and w_p.collidepoint(mouse): selected_weight = round(selected_weight + 0.1, 1)
                    if c_m and c_m.collidepoint(mouse) or (c_p and c_p.collidepoint(mouse)):
                        idx = max_cost_options.index(selected_max_cost)
                        idx = (idx - 1 if c_m.collidepoint(mouse) else idx + 1) % len(max_cost_options)
                        selected_max_cost = max_cost_options[idx]

                    if confirm_button.collidepoint(mouse):
                        self.solver._hint_strategy = selected_strategy
                        self.solver._hint_heuristic_name = selected_heuristic_name
                        self.solver._hint_config.update({"depth_limit": selected_depth_limit, "max_cost": selected_max_cost, "weight": selected_weight})
                        return 0
            pygame.display.update()