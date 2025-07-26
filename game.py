import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player
player_size = (50, 50)
player_img = pygame.Surface(player_size)
player_img.fill((0, 255, 0))
player_pos = [WIDTH // 2 - player_size[0] // 2, HEIGHT - player_size[1] - 10]
player_speed = 7

# Bullet
bullet_size = (5, 10)
bullet_img = pygame.Surface(bullet_size)
bullet_img.fill((255, 0, 0))
bullet_speed = 10
bullets = []

# Enemy
enemy_size = (50, 50)
enemy_img = pygame.Surface(enemy_size)
enemy_img.fill((0, 0, 255))
enemy_speed = 3
enemies = []
spawn_delay = 30  # frames
frame_count = 0

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)

# Clock
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)  # FPS = 60
    frame_count += 1
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size[0]:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE]:
        # Shoot bullet (limit firing rate)
        if len(bullets) == 0 or bullets[-1][1] < player_pos[1] - 50:
            bullet_pos = [player_pos[0] + player_size[0]//2 - bullet_size[0]//2, player_pos[1]]
            bullets.append(bullet_pos)

    # Update bullets
    for b in bullets[:]:
        b[1] -= bullet_speed
        if b[1] < 0:
            bullets.remove(b)

    # Spawn enemies
    if frame_count % spawn_delay == 0:
        x_pos = random.randint(0, WIDTH - enemy_size[0])
        enemies.append([x_pos, -enemy_size[1]])

    # Update enemies
    for e in enemies[:]:
        e[1] += enemy_speed
        # Check for collision with player
        player_rect = pygame.Rect(player_pos[0], player_pos[1], *player_size)
        enemy_rect = pygame.Rect(e[0], e[1], *enemy_size)
        if enemy_rect.colliderect(player_rect):
            running = False  # Game over

        # Remove enemies that go off screen
        if e[1] > HEIGHT:
            running = False  # Game over if enemy reaches bottom

    # Check bullet-enemy collisions
    for b in bullets[:]:
        bullet_rect = pygame.Rect(b[0], b[1], *bullet_size)
        for e in enemies[:]:
            enemy_rect = pygame.Rect(e[0], e[1], *enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(b)
                enemies.remove(e)
                score += 1
                break

    # Drawing everything
    screen.fill(BLACK)
    screen.blit(player_img, player_pos)
    for b in bullets:
        screen.blit(bullet_img, b)
    for e in enemies:
        screen.blit(enemy_img, e)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
print(f"Game Over! Your score was: {score}")
