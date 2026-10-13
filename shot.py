import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH

class Shot(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        if self.position.x > SCREEN_WIDTH or self.position.x < 0 or self.position.y > SCREEN_HEIGHT or self.position.y < 0:
            self.kill()
