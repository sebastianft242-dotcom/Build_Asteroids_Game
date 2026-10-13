import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, INVULNERABILITY_DURATION, SCREEN_HEIGHT, SCREEN_WIDTH, LINE_WIDTH, MAX_SPEED, PLAYER_TURN_ACCELERATION, ROTATIONAL_DRAG, PLAYER_ACCELERATION, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, BRAKE_DECELERATION
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.velocity = pygame.Vector2(0, 0)
        self.angular_velocity = 0.0
        self.invulnerable_timer = 0.0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        if self.invulnerable_timer > 0:
            if int(self.invulnerable_timer * 10) % 2 == 0:
                return
            
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self,dt):
        self.angular_velocity += dt * PLAYER_TURN_ACCELERATION

    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def brake(self, dt: float) -> None:
        self.velocity = self.velocity.move_towards(pygame.Vector2(0, 0), BRAKE_DECELERATION * dt)

    def shoot(self):
        if self.cooldown > 0:
            return

        self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def respawn(self) -> None:
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.angular_velocity = 0.0
        self.rotation = 0.0
        self.invulnerable_timer = INVULNERABILITY_DURATION

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.cooldown -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.accelerate(dt)

        if keys[pygame.K_s]:
            self.brake(dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)

        if self.invulnerable_timer > 0:
            self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)

        self.position += self.velocity * dt

        self.rotation += self.angular_velocity * dt
        self.angular_velocity *= max(0.0, 1.0 - ROTATIONAL_DRAG * dt)

        self.wrap_around()
  
