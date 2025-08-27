import pygame
import sys
from bird import Bird
from pipe import Pipe


class Button:
    def __init__(self, rect, text, font, bg_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def run_game(screen, screen_width, screen_height, font, high_score_dict):
    bird_img = pygame.image.load('Assets/Goldship.PNG')

    pipe_img = pygame.Surface((52, 500), pygame.SRCALPHA)
    pipe_img.fill((255, 255, 255))  # White pipes

    background = pygame.transform.smoothscale(pygame.image.load('Assets/Background.png'),(500,700))
    bird = Bird(100, screen_height // 2, bird_img)
    pipes = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1500)

    score = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()
            if event.type == SPAWNPIPE:
                pipes.append(Pipe(screen_width, screen_height, pipe_img))

        # Update
        bird.update()
        for pipe in pipes:
            pipe.update()
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Collision
        for pipe in pipes:
            if pipe.collides_with(bird):
                running = False
        if bird.rect.top <= 0 or bird.rect.bottom >= screen_height:
            running = False

        # Score
        for pipe in pipes:
            if pipe.top_rect.right < bird.rect.left and not hasattr(pipe, "scored"):
                score += 1
                pipe.scored = True
                # Real-time high score update
                if score > high_score_dict["score"]:
                    high_score_dict["score"] = score

        # Draw
        screen.blit(background, (0, 0))
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Current score (top-left)
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        # High score (top-right)
        high_text = font.render(f"High: {high_score_dict['score']}", True, (255, 255, 0))
        screen.blit(high_text, (screen_width - high_text.get_width() - 20, 20))

        pygame.display.flip()

    return score


def main():
    pygame.init()
    screen_width, screen_height = 500, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flappy Goldship")
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    start_button = Button((screen_width // 2 - 80, screen_height // 2 - 30, 160, 60),
                          "START", font, (0, 150, 0))
    again_button = Button((screen_width // 2 - 100, screen_height // 2 + 60, 200, 60),
                          "PLAY AGAIN", font, (200, 0, 0))

    high_score_dict = {"score": 0}  # Store high score for real-time updates

    while True:
        # === Start Menu ===
        waiting = True
        while waiting:
            screen.fill((50, 50, 100))
            title = font.render("Flappy Goldship", True, (255, 255, 0))
            high_text = small_font.render(f"High Score: {high_score_dict['score']}", True, (255, 255, 255))
            screen.blit(title, (screen_width // 2 - title.get_width() // 2, 150))
            screen.blit(high_text, (screen_width // 2 - high_text.get_width() // 2, 230))
            start_button.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(event.pos):
                        waiting = False

        # === Run game ===
        score = run_game(screen, screen_width, screen_height, font, high_score_dict)

        # === Game Over Screen ===
        game_over = True
        while game_over:
            screen.fill((0, 0, 0))
            over_text = font.render("GAME OVER", True, (255, 0, 0))
            score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
            high_text = small_font.render(f"High Score: {high_score_dict['score']}", True, (255, 255, 0))

            screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, 200))
            screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 280))
            screen.blit(high_text, (screen_width // 2 - high_text.get_width() // 2, 320))
            again_button.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if again_button.is_clicked(event.pos):
                        game_over = False


if __name__ == "__main__":
    main()
