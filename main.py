import pygame
import sys
from bird import Bird
from pipe import Pipe

def main():
    pygame.init()
    screen_width, screen_height = 400, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flappy Bird Clone")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    # Load placeholder assets
    bird_img = pygame.Surface((34, 24), pygame.SRCALPHA)
    bird_img.fill((255, 255, 0))  # Yellow bird

    pipe_img = pygame.Surface((52, 320), pygame.SRCALPHA)
    pipe_img.fill((0, 200, 0))  # Green pipes

    background = pygame.Surface((screen_width, screen_height))
    background.fill((135, 206, 235))  # Sky blue

    # Create Bird
    bird = Bird(100, screen_height // 2, bird_img)

    # Pipes list
    pipes = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1500)  # spawn every 1.5 sec

    score = 0
    running = True

    while running:
        clock.tick(60)  # 60 FPS
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

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Check collisions
        for pipe in pipes:
            if pipe.collides_with(bird.rect):
                running = False
        if bird.rect.top <= 0 or bird.rect.bottom >= screen_height:
            running = False

        # Scoring (increase when bird passes a pipe)
        for pipe in pipes:
            if pipe.top_rect.right < bird.rect.left and not hasattr(pipe, "scored"):
                score += 1
                pipe.scored = True

        # Draw
        screen.blit(background, (0, 0))
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Draw score
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()

    # Game Over Screen
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2,
                                 screen_height // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


if __name__ == "__main__":
    main()
