import pygame
import sys
import random
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Square Game with Enemies and Shooting")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

square_size = 50
square_x, square_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
square_speed = 10

bullet_radius  = 5
bullet_speed = 15
bullets = []

enemy_size = 40
enemy_speed = 5
enemies = []

last_direction = [0, -1]  # Default bullet direction is upwards
clock = pygame.time.Clock()

# Function to create a new enemy at a random position
def create_enemy():
    x = random.randint(0, SCREEN_WIDTH - enemy_size)
    y = random.randint(0, SCREEN_HEIGHT - enemy_size)
    return [x, y, random.choice([-1, 1]), random.choice([-1, 1])]  # Random direction

# Function to move enemies randomly
def move_enemy(enemy):
    enemy[0] += enemy[2] * enemy_speed
    enemy[1] += enemy[3] * enemy_speed

    # Bounce if it hits the screen edges
    if enemy[0] <= 0 or enemy[0] >= SCREEN_WIDTH - enemy_size:
        enemy[2] *= -1
    if enemy[1] <= 0 or enemy[1] >= SCREEN_HEIGHT - enemy_size:
        enemy[3] *= -1

# Function to detect collision
def check_collision(rect1, rect2):
    return (
        rect1[0] < rect2[0] + rect2[2] and
        rect1[0] + rect1[2] > rect2[0] and
        rect1[1] < rect2[1] + rect2[3] and
        rect1[1] + rect1[3] > rect2[1]
    )

# Create initial enemies
for _ in range(5):
    enemies.append(create_enemy())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot a bullet in the last direction of movement
                bullet_x = square_x + square_size // 2
                bullet_y = square_y + square_size // 2
                bullets.append([bullet_x, bullet_y, last_direction[0], last_direction[1]])

    # Movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= square_speed
        last_direction = [-1, 0]  # Update direction to left
    if keys[pygame.K_RIGHT]:
        square_x += square_speed
        last_direction = [1, 0]  # Update direction to right
    if keys[pygame.K_UP]:
        square_y -= square_speed
        last_direction = [0, -1]  # Update direction to up
    if keys[pygame.K_DOWN]:
        square_y += square_speed
        last_direction = [0, 1]  # Update direction to down

    # Keep the player within screen bounds
    square_x = max(0, min(square_x, SCREEN_WIDTH - square_size))
    square_y = max(0, min(square_y, SCREEN_HEIGHT - square_size))

    # Move bullets
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed
    bullets = [bullet for bullet in bullets if 0 < bullet[0] < SCREEN_WIDTH and 0 < bullet[1] < SCREEN_HEIGHT]

    # Move enemies
    for enemy in enemies:
        move_enemy(enemy)

    # Check for bullet-enemy collisions
    new_enemies = []
    for enemy in enemies:
        enemy_rect = (enemy[0], enemy[1], enemy_size, enemy_size)
        hit = False
        for bullet in bullets:
            bullet_rect = (bullet[0] - bullet_radius, bullet[1] - bullet_radius, bullet_radius * 2, bullet_radius * 2)
            if check_collision(enemy_rect, bullet_rect):
                hit = True
                break
        if not hit:
            new_enemies.append(enemy)
    enemies = new_enemies

    # Check for player-enemy collisions
    player_rect = (square_x, square_y, square_size, square_size)
    for enemy in enemies:
        enemy_rect = (enemy[0], enemy[1], enemy_size, enemy_size)
        if check_collision(player_rect, enemy_rect):
            print("Game Over!")
            running = False

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (square_x, square_y, square_size, square_size))  # Draw player
    for bullet in bullets:
        pygame.draw.circle(screen, RED, (bullet[0], bullet[1]), bullet_radius)  # Draw bullets
    for enemy in enemies:
        pygame.draw.rect(screen, GREEN, (enemy[0], enemy[1], enemy_size, enemy_size))  # Draw enemies

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
