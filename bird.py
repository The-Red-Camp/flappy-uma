import pygame

class Bird:
    def __init__(self, x: int, y: int, image: pygame.Surface):
        """
        Initialize the Bird object.

        x int: Starting x position of the bird
        y int: Starting y position of the bird
        image pygame.Surface: Bird sprite/image surface
        """
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8

    def flap(self):
        """Make the bird jump upward."""
        self.velocity = self.jump_strength

    def update(self):
        """Update bird position with gravity and velocity."""
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def draw(self, surface: pygame.Surface):
        """Draw the bird on the given surface."""
        surface.blit(self.image, self.rect)
