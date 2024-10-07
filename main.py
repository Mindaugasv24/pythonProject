import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (50, 153, 213)
RED = (255, 0, 0)
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender")

# Load images
player_img = pygame.image.load('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/images/player.png')
enemy_img = pygame.image.load('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/images/meteor.png')
bullet_img = pygame.image.load('C:/Users/k00zeris/Documents/pythonProject/5games-main/space shooter/images/laser.png')


# Classes
class Player:
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

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def lose_health(self):
        self.health -= 1


class Enemy:
    def __init__(self, speed_increase):
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(2, 5) + speed_increase

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullet:
    def __init__(self, x, y):
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Function to display the End Game screen
def show_end_game_screen(final_score):
    screen.fill(BLUE)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER", True, RED)
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
                    main()  # Restart the game by calling main()


# Game Loop
def main():
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy(0) for _ in range(5)]  # Initial set of enemies
    bullets = []
    score = 0
    level = 1
    last_level_up_score = 0  # Track when we last leveled up
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

        player.move()

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                enemies.append(Enemy(level - 1))  # Respawn enemy with level-based speed

            if enemy.rect.colliderect(player.rect):  # Enemy hits player
                player.lose_health()
                enemies.remove(enemy)
                enemies.append(Enemy(level - 1))  # Respawn new enemy
                if player.health <= 0:
                    show_end_game_screen(score)  # Trigger the end game screen
                    running = False

            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):  # Bullet hits enemy
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    enemies.append(Enemy(level - 1))  # Respawn new enemy

        # Level Progression
        if score >= last_level_up_score + 10:  # Every 10 points, increase level
            level += 1
            last_level_up_score = score  # Update last level-up score
            enemies.append(Enemy(level - 1))  # Add an extra enemy for each new level

        # Draw
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
