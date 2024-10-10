"""
This is minigame Star Troopers. The game uses basic 2D graphics, loading images for the player, enemies
and bullets from external files. Sound effects (laser shooting) and background music add to the overall
gameplay experience, making the game more immersive.!
"""

import pygame
import random

"""
Initialization and Setup!
"""
pygame.init()

pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (50, 153, 213)
RED = (255, 0, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Troopers")

"""
Sound, Music and Images: Laser shooting sounds and background music are incorporated into the game for an immersive
experience. Volume levels are adjusted for balance between sound effects and background music.
Loading images who represent your work!
"""
shoot_sound = pygame.mixer.Sound('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/audio/laser.wav')
shoot_sound.set_volume(0.5)

pygame.mixer.music.load('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/audio/game_music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

player_img = pygame.image.load('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/images/player.png')
enemy_img = pygame.image.load('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/images/meteor.png')
bullet_img = pygame.image.load('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/images/laser.png')


class Player:
    """
    This player class: manages the player spaceship, its movement, health, and interaction with enemies.
    The player can move in four directions (left, right, up, and down) and is constrained by the game window.!
    """
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5
        self.health = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def lose_health(self):
        self.health -= 1


class Enemy:
    """
    Enemy class: Handles enemy behavior, including random spawning at the top of the screen and
    falling down toward the player.
    The enemies’ speed increases with the game level, introducing a difficulty progression.!
    """
    def __init__(self, speed_increase):
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(2, 5) + speed_increase

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullet:
    """
    Bullet class: represents the player's bullets, which are shot from the spaceship and move upward.
    Bullets can destroy enemies when they collide.!
    """
    def __init__(self, x, y):
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def show_end_game_screen(final_score):
    """
    Once the player’s health drops to zero, a game over screen appears with the final score,
    offering the option to restart the game (by pressing "R") or quit (by pressing "Q").!
    """
    screen.fill(BLUE)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER BOY", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Final Score: {final_score}", True, GREEN)
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))

    restart_text = font.render("Press R to Restart or Q to Quit", True, ORANGE)
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    waiting = False
                    main()


def main():
    """
    The game loop is responsible for:
        Handling Events: Captures user input, such as movement, shooting, and quitting.
    Object Movement: Moves the player, enemies, and bullets based on user input and game logic.
        Collision Detection: Detects collisions between bullets and enemies (destroying enemies), and between enemies
    and the player (damaging the player).
        Health and Game Over: The player has limited health (5 by default), and when it reaches zero,
    the game over screen is triggered.
        Scoring and Leveling: Points are awarded for destroying enemies, and as the score increases, the game level
        rises, introducing faster and more enemies.!
    """
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy(0) for _ in range(5)]
    bullets = []
    score = 0
    level = 1
    last_level_up_score = 0
    running = True

    def draw_health():
        font = pygame.font.Font(None, 36)
        health_text = font.render(f'Health: {player.health}', True, ORANGE)
        screen.blit(health_text, (WIDTH - 150, 10))

    def draw_score_and_level():
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, GREEN)
        level_text = font.render(f'Level: {level}', True, GREEN)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.rect.centerx, player.rect.top))
                    shoot_sound.play()

        player.move()

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                enemies.append(Enemy(level - 1))

            if enemy.rect.colliderect(player.rect):
                player.lose_health()
                enemies.remove(enemy)
                enemies.append(Enemy(level - 1))
                if player.health <= 0:
                    show_end_game_screen(score)
                    running = False

            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    enemies.append(Enemy(level - 1))

        """
        The game becomes progressively more difficult by increasing the speed of enemies and spawning more enemies
        as the player scores more points. Every 20 points, a new level starts, which raises the challenge by adding a
        new enemy and increasing their speed.!
        """
        if score >= last_level_up_score + 20:
            level += 1
            last_level_up_score = score
            enemies.append(Enemy(level - 1))

        """
        DRAW!
        """
        screen.fill(BLACK)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        draw_health()
        draw_score_and_level()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
