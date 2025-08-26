import pygame
import random

class Pipe:
    def __init__(self, x: int, screen_height: int, image: pygame.Surface, gap_size: int = 150):
        """
        Initialize a pair of pipes (top and bottom).
        
        x int: Starting x position of the pipes.
        screen_height int: Height of the game window.
        image pygame.Surface: Pipe sprite/image.
        gap_size int: Vertical gap between top and bottom pipe.
        """
        self.image = image
        self.gap_size = gap_size
        self.speed = 3

        self.top_height = random.randint(50, screen_height - 50 - gap_size)
        self.bottom_y = self.top_height + gap_size

        self.top_rect = self.image.get_rect(midbottom=(x, self.top_height))
        self.bottom_rect = self.image.get_rect(midtop=(x, self.bottom_y))

        self.top_image = pygame.transform.flip(self.image, False, True)

    def update(self):
        """Move the pipes to the left."""
        self.top_rect.x -= self.speed
        self.bottom_rect.x -= self.speed

    def draw(self, surface: pygame.Surface):
        """Draw the pipes on the screen."""
        surface.blit(self.top_image, self.top_rect)
        surface.blit(self.image, self.bottom_rect)

    def off_screen(self) -> bool:
        """Check if the pipe has moved off the left side of the screen."""
        return self.top_rect.right < 0

    def collides_with(self, bird_rect: pygame.Rect) -> bool:
        """Check for collision with the bird."""
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
