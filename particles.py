import pygame
import random
from circleshape import CircleShape
from asteroid import Asteroid
from constants import PARTICLES_SPAWN_LIFE, LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS

class Particles(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.kill_timer = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, ASTEROID_MIN_RADIUS / 4, LINE_WIDTH)

    def update(self, dt):
        self.kill_timer += dt
        self.position += self.velocity * dt
        if self.kill_timer > PARTICLES_SPAWN_LIFE:
            self.kill()

    def asteroid_particles(self, asteroid_radius):
        split = 0
        if asteroid_radius == ASTEROID_MAX_RADIUS:
            split = 9  
        if ASTEROID_MIN_RADIUS < asteroid_radius < ASTEROID_MAX_RADIUS:
            split = 6
        if asteroid_radius == ASTEROID_MIN_RADIUS:
            split = 3

        for _ in range(0, split):
            random_angle = random.uniform(0, 360)
            vel = self.velocity.rotate(random_angle) * 1.2
            new_radius = ASTEROID_MIN_RADIUS / 4
            ast = Asteroid(self.position.x, self.position.y, new_radius)
            ast.velocity = vel
