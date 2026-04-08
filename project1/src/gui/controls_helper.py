import pygame


class ControlHelper:
    def __init__(self, screen):
        self.screen = screen

        self.WHITE = (255, 255, 255)
        self.LIGHT = (170, 170, 170)
        self.DARK = (100, 100, 100)
        self.BG = (60, 25, 60)

        self.controls = [
            "Left arrow: rotate left",
            "Right arrow: rotate right",
            "Click purple circle: reverse segment",
        ]

    def run(self):
        running = True
        font = pygame.font.SysFont("arial", 36)
        close_font = pygame.font.SysFont("arial", 28)
        clock = pygame.time.Clock()

        screen_w = self.screen.get_width()
        close_button = pygame.Rect(screen_w - 50, 10, 36, 36)

        while running:
            self.screen.fill(self.BG)

            title = font.render("Controls", True, self.WHITE)
            self.screen.blit(title, (50, 50))

            for i, line in enumerate(self.controls):
                text = font.render(line, True, self.LIGHT)
                self.screen.blit(text, (50, 120 + i * 40))

            mouse = pygame.mouse.get_pos()
            close_color = (
                (220, 60, 60) if close_button.collidepoint(mouse) else (160, 40, 40)
            )
            pygame.draw.rect(self.screen, close_color, close_button, border_radius=6)
            x_text = close_font.render("✕", True, self.WHITE)
            self.screen.blit(x_text, (close_button.x + 6, close_button.y + 4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_h]:
                        running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if close_button.collidepoint(event.pos):
                        running = False

            pygame.display.update()
            clock.tick(30)
