import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, PLAYER_LIVES
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particles import Particles

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)
    Particles.containers = (particles, updatable, drawable)

    asteroid_field = AsteroidField()

    dt = 0
    score = 0
    lives = PLAYER_LIVES

    game_over = False

    running = True

    while running:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                for asteroid in asteroids:
                    asteroid.kill()
                for shot in shots:
                    shot.kill()
                player.respawn()
                game_over = False
                lives = 1
                score = 0

        if game_over == False:

            updatable.update(dt)
            screen.fill("black")
            
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if player.invulnerable_timer > 0:
                        continue

                    lives -= 1
                    if lives > 0:
                        player.respawn()
                    else:
                        log_event("player_hit")
                        print("Game over!")
                        game_over = True

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        particles.asteroid_particles(asteroid.radius)
                        if asteroid.radius == ASTEROID_MAX_RADIUS:
                            score += 1
                            break
                        if ASTEROID_MIN_RADIUS < asteroid.radius < ASTEROID_MAX_RADIUS:
                            score += 2
                            break
                        if asteroid.radius == ASTEROID_MIN_RADIUS:
                            score += 3
                            break

            for entity in drawable:
                entity.draw(screen=screen)

            score_surface = font.render(f"Score: {score}", True, "white")
            screen.blit(score_surface, (10, 10))

            lives_surface = font.render(f"Lives: {lives}", True, "white")
            screen.blit(lives_surface, (10, 40))

        else:
            screen.fill("black")
            game_over_text = font.render(f"Game Over / To restart press R", True, "white")
            screen.blit(game_over_text, (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()