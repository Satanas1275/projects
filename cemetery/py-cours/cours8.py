import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
BLUE = (0, 55, 255)
screen.fill(BLUE)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)
    screen.fill(BLUE)
    pygame.draw.circle(screen, "red", player_pos, 40)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        player_pos.y -= 400 * dt
    if keys[pygame.K_s]:
        player_pos.y += 400 * dt
    if keys[pygame.K_q]:
        player_pos.x -= 400 * dt
    if keys[pygame.K_d]:
        player_pos.x += 400 * dt
    if keys[pygame.K_ESCAPE]:
        running = False
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000
pygame.quit()