import pygame

class Bird:
    def __init__(self, x: int, y: int, image):
        """
        Initialize the Bird object.

        x int: Starting x position of the bird
        y int: Starting y position of the bird
        image pygame.Surface: Bird sprite/image surface
        """
        self.image = image
        self.image = pygame.transform.smoothscale(self.image, (100,130))
        self.rect = self.image.get_rect(center=(x, y))
        self.bar = None
        self.top = None

        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8
        self.update_hitbox()

    def flap(self):
        """Make the bird jump upward."""
        self.velocity = self.jump_strength

    def update(self):
        """Update bird position with gravity and velocity."""
        self.velocity += self.gravity
        self.rect.y += self.velocity
        self.update_hitbox()

    def draw(self, surface: pygame.Surface):
        """Draw the bird on the given surface."""
        surface.blit(self.image, self.rect)

    def update_hitbox(self):
        """Recalculate the T-shaped hitbox based on current position."""
        bar_width = self.rect.width // 3
        bar_height = self.rect.height
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top
        self.bar = pygame.Rect(bar_x, bar_y, bar_width, bar_height)

        top_width = self.rect.width
        top_height = self.rect.height // 4
        top_x = self.rect.left
        top_y = self.rect.top
        self.top = pygame.Rect(top_x, top_y, top_width, top_height)

    def get_hitboxes(self):
        """Return the two hitboxes for collision checks."""
        return [self.bar, self.top]
